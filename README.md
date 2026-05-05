# GitHub Codespaces ♥️ Jupyter Notebooks

Welcome to your shiny new codespace! We've got everything fired up and running for you to explore Python and Jupyter notebooks.

You've got a blank canvas to work on from a git perspective as well. There's a single initial commit with what you're seeing right now - where you go from here is up to you!

Everything you do here is contained within this one codespace. There is no repository on GitHub yet. If and when you’re ready you can click "Publish Branch" and we’ll create your repository and push up your project. If you were just exploring then and have no further need for this code then you can simply delete your codespace and it's gone forever.

## 数字工具应用

这是一个基于 Streamlit 的数字工具 Web 应用，包含以下功能：
- 数字配对：输入两组数字，自动配对（如 18=21, 19=17）
- 字符串解析数字：提取字符串中的数字并格式化
- 生肖包数计算：根据生肖计算份数，支持别称映射

### 本地运行

1. 安装依赖：
   ```
   pip install -r requirements.txt
   ```

2. 运行应用：
   - 双击 `数字工具应用.desktop` 文件启动
   - 或使用脚本：`./run_app.sh`
   - 或命令：`streamlit run app.py`

3. 在浏览器打开显示的 URL（如 http://localhost:8501）

### 修改和添加功能

- 编辑 `app.py` 文件添加新功能
- 更新 `requirements.txt` 添加新依赖
- 重新运行应用查看更改

所有代码保存在此目录中，便于后续修改。
