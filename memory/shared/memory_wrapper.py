"""
轻量记忆层 — 用于 OpenClaw 和 Hermes 双智能体共享记忆
基于 sentence-transformers + SQLite，无额外依赖
"""

import sqlite3
import json
import os
import re
from typing import List, Dict, Optional
from pathlib import Path

MEMORY_DIR = Path(__file__).parent.resolve()
DB_PATH = MEMORY_DIR / "shared_memory.db"

class LocalMemory:
    """极简向量记忆系统，不需要 Qdrant/ChromaDB"""

    def __init__(self, db_path=None):
        self.db_path = db_path or str(DB_PATH)
        self._embedder = None
        self._init_db()

    def _get_embedder(self):
        """延迟加载 sentence-transformers"""
        if self._embedder is None:
            from sentence_transformers import SentenceTransformer
            self._embedder = SentenceTransformer(
                'sentence-transformers/all-MiniLM-L6-v2'
            )
        return self._embedder

    def _init_db(self):
        conn = sqlite3.connect(self.db_path)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS memories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT NOT NULL DEFAULT 'system',
                content TEXT NOT NULL,
                embedding BLOB,
                category TEXT DEFAULT 'general',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE INDEX IF NOT EXISTS idx_user ON memories(user_id)
        """)
        conn.commit()
        conn.close()

    def add(self, content: str, user_id: str = "system", category: str = "general"):
        """写入记忆"""
        import numpy as np
        emb = self._get_embedder().encode(content)
        emb_bytes = emb.astype(np.float32).tobytes()

        conn = sqlite3.connect(self.db_path)
        conn.execute(
            "INSERT INTO memories (user_id, content, embedding, category) VALUES (?, ?, ?, ?)",
            (user_id, content, emb_bytes, category)
        )
        conn.commit()
        conn.close()
        return True

    def search(self, query: str, user_id: str = "system", top_k: int = 5) -> List[Dict]:
        """语义搜索记忆"""
        import numpy as np

        conn = sqlite3.connect(self.db_path)

        if user_id:
            rows = conn.execute(
                "SELECT id, content, category, created_at FROM memories WHERE user_id = ? ORDER BY id",
                (user_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, content, category, created_at FROM memories ORDER BY id"
            ).fetchall()
        conn.close()

        if not rows:
            return []

        query_emb = self._get_embedder().encode(query)

        # 加载所有 embedding
        conn = sqlite3.connect(self.db_path)
        cursor = conn.execute("SELECT embedding FROM memories")
        all_embs = []
        batch = cursor.fetchmany(100)
        while batch:
            for row in batch:
                if row[0]:
                    emb = np.frombuffer(row[0], dtype=np.float32)
                    all_embs.append(emb)
            batch = cursor.fetchmany(100)
        conn.close()

        if not all_embs:
            return []

        # 余弦相似度
        all_embs = np.array(all_embs)
        query_emb = query_emb / np.linalg.norm(query_emb)
        all_embs = all_embs / np.linalg.norm(all_embs, axis=1, keepdims=True)
        scores = np.dot(all_embs, query_emb)

        # 取 top_k
        top_idx = np.argsort(scores)[-top_k:][::-1]

        results = []
        for i, idx in enumerate(top_idx):
            r = rows[idx]
            results.append({
                "id": r[0],
                "content": r[1],
                "category": r[2],
                "created_at": r[3],
                "score": float(scores[idx]),
            })
        return results

    def get_all(self, user_id: str = "system") -> List[Dict]:
        """列出所有记忆"""
        conn = sqlite3.connect(self.db_path)
        if user_id:
            rows = conn.execute(
                "SELECT id, content, category, created_at FROM memories WHERE user_id = ? ORDER BY id",
                (user_id,)
            ).fetchall()
        else:
            rows = conn.execute(
                "SELECT id, content, category, created_at FROM memories ORDER BY id"
            ).fetchall()
        conn.close()
        return [
            {"id": r[0], "content": r[1], "category": r[2], "created_at": r[3]}
            for r in rows
        ]

    def delete(self, mem_id: int):
        conn = sqlite3.connect(self.db_path)
        conn.execute("DELETE FROM memories WHERE id = ?", (mem_id,))
        conn.commit()
        conn.close()


# 单例
_memory_instance = None

def get_memory() -> LocalMemory:
    global _memory_instance
    if _memory_instance is None:
        _memory_instance = LocalMemory()
    return _memory_instance


if __name__ == "__main__":
    mem = get_memory()
    mem.add("OpenClaw 和 Hermes 是双智能体协作系统，共享记忆层", category="system")
    mem.add("村长（Min-1987）是唯一用户，GitHub 已配置", category="user")
    mem.add("工作区已 git init，推送到 origin/master", category="config")

    print("✅ 写入 3 条记忆")

    results = mem.search("双智能体")
    print(f"✅ 检索到 {len(results)} 条")
    for r in results:
        print(f"  [{r['score']:.3f}] {r['content']}")

    print(f"\n✅ 全部记忆 ({len(mem.get_all())} 条)")
