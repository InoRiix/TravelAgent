# TravelAgent
AI Travel Agent Web Application

## 项目描述
一个基于AI的旅行助手Web应用，旨在简化旅行规划过程。通过AI了解用户需求，自动生成详细的旅行路线和建议，并提供实时旅行辅助。

## 核心功能
1. 智能行程规划: 用户可以通过语音或文字输入旅行信息，AI自动生成个性化旅行路线
2. 费用预算与管理: AI进行预算分析，记录旅行开销
3. 用户管理与数据存储: 用户注册登录系统，保存和管理多份旅行计划
4. 云端行程同步: 旅行计划、费用记录等数据云端同步

## 技术栈
### 后端
- Flask: Python Web框架
- Flask-RESTful: REST API构建
- Firebase Authentication: 用户认证
- Firestore: 数据存储
- Celery + Redis: 异步任务处理
- 阿里云百炼平台API: 语音识别
- 高德地图API: 地理位置服务和导航

### 前端
- HTML5/CSS3/JavaScript: 基础前端技术
- Vue.js: 前端框架
- Bootstrap: UI框架

## 环境配置和运行说明

### 创建虚拟环境
```bash
# 创建虚拟环境
python -m venv venv

# 激活虚拟环境 (Windows)
venv\Scripts\activate

# 激活虚拟环境 (Mac/Linux)
source venv/bin/activate
```

### 安装依赖
```bash
# 安装项目依赖
pip install -r requirements.txt
```

### 配置环境变量
复制 `.env.example` 文件为 `.env` 并填写相应配置：
```bash
cp .env.example .env
```

在 `.env` 文件中配置以下环境变量：
- `DASHSCOPE_API_KEY`: 阿里云百炼平台API Key

### 运行应用
```bash
# 启动Flask应用
python app.py
```

### 在IDE中运行
有两种方式可以在IDE中运行应用：

1. 直接运行项目中的 `start_app.py` Python脚本（推荐）
2. 运行 `run.bat` 批处理文件

两种方式都会自动使用虚拟环境中的Python解释器启动Flask服务器。

应用启动后，访问 http://127.0.0.1:5000 查看登录页面。

## 安全说明

本项目使用环境变量存储敏感信息，`.env` 文件已被添加到 `.gitignore` 中，不会被上传到代码仓库。

## 项目结构
```
TravelAgent/
├── app.py              # Flask应用主文件
├── requirements.txt    # 项目依赖
├── run.bat             # Windows启动脚本
├── README.md           # 项目说明文档
├── templates/          # HTML模板文件
│   └── login.html      # 登录页面
└── venv/               # Python虚拟环境 (需要自己创建)
```
