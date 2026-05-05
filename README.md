# 数字工具应用

这是一个基于 Streamlit 的数字工具 Web 应用，包含以下功能：
- 数字配对：输入两组数字，自动配对（如 18=21, 19=17）
- 字符串解析数字：提取字符串中的数字并格式化
- 生肖包数计算：根据生肖计算份数，支持别称映射

## 部署到本地

### 前提条件
- Python 3.7 或更高版本
- pip 包管理器

### 步骤 1: 下载项目
```bash
git clone <repository-url>
cd codespaces-jupyter
```

### 步骤 2: 创建虚拟环境（推荐）
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 步骤 3: 安装依赖
```bash
pip install -r requirements.txt
```

### 步骤 4: 运行应用
```bash
# 方法1: 使用启动脚本
./run_app.sh

# 方法2: 直接运行
streamlit run app.py

# 方法3: 双击桌面启动器（Linux）
# 双击 数字工具应用.desktop 文件
```

### 步骤 5: 访问应用
在浏览器中打开显示的 URL，通常是：
- http://localhost:8501

## 项目结构
```
codespaces-jupyter/
├── app.py                 # 主应用文件
├── requirements.txt       # 依赖列表
├── run_app.sh            # 启动脚本
├── 数字工具应用.desktop   # Linux 桌面启动器
├── README.md             # 项目文档
├── LICENSE               # 许可证
├── data/                 # 数据文件
│   └── atlantis.csv
└── notebooks/            # Jupyter 笔记本
    ├── image-classifier.ipynb
    ├── matplotlib.ipynb
    └── population.ipynb
```

## 依赖说明
- streamlit: Web 应用框架
- pandas: 数据处理
- matplotlib: 数据可视化
- torch/torchvision: 机器学习（用于笔记本）
- 其他工具库

## 修改和添加功能
- 编辑 `app.py` 文件添加新功能
- 更新 `requirements.txt` 添加新依赖
- 重新运行应用查看更改

## 故障排除
- 如果端口被占用：`streamlit run app.py --server.port 8502`
- 如果权限问题：`chmod +x run_app.sh`
