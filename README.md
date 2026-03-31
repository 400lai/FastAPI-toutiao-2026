# Toutiao Backend

基于 FastAPI 构建的头条应用后端 API 服务。

## 项目概述

本项目是一个基于 FastAPI 开发的头条应用后端服务，提供新闻管理、用户认证等核心功能的 RESTful API。采用异步编程模型，结合 SQLAlchemy 异步 ORM 和 MySQL 数据库，实现了高性能的 API 服务。

## 技术栈

- **框架**: FastAPI
- **语言**: Python 3.11+
- **服务器**: Uvicorn (ASGI)
- **数据库**: MySQL
- **ORM**: SQLAlchemy (异步)
- **认证**: JWT (JSON Web Token)
- **密码加密**: bcrypt

## 项目结构

```
toutiao_backend/
├── main.py                      # 应用入口文件
├── config/                      # 配置文件目录
│   └── db_config.py            # 数据库配置
├── models/                      # 数据库模型层
│   ├── users.py                # 用户模型
│   └── news.py                 # 新闻模型
├── schemas/                     # Pydantic 模型层（数据验证）
│   └── users.py                # 用户数据验证模型
├── routers/                     # 路由控制器层
│   ├── users.py                # 用户相关路由
│   └── news.py                 # 新闻相关路由
├── crud/                        # 数据库操作层
│   ├── users.py                # 用户数据库操作
│   └── news.py                 # 新闻数据库操作
├── utils/                       # 工具函数层
│   ├── auth.py                 # 认证工具
│   ├── security.py             # 安全工具（密码加密）
│   ├── response.py             # 响应格式化工具
│   ├── exception.py            # 自定义异常
│   └── exception_handlers.py   # 异常处理器
├── test_main.http              # HTTP 测试请求文件
└── README.md                   # 项目文档
```

## 安装

### 1. 克隆项目

```bash
git clone https://github.com/400lai/FastAPI-toutiao-2026.git
cd toutiao_backend
```

### 2. 创建虚拟环境（推荐）

```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. 安装依赖

```bash
pip install fastapi uvicorn sqlalchemy pymysql bcrypt python-jose[crypto] passlib python-dotenv
```

### 4. 配置数据库

在 `config/db_config.py` 中配置 MySQL 数据库连接信息：

```python
DATABASE_URL = "mysql+aiomysql://username:password@localhost:3306/toutiao_db"
```

## 使用方法

### 启动服务器

```bash
# 开发环境（自动重载）
uvicorn main:app --reload

# 生产环境
uvicorn main:app --host 0.0.0.0 --port 8000
```

API 服务将在 `http://127.0.0.1:8000` 启动

### API 文档

服务器运行后，您可以访问：

- **交互式 API 文档 (Swagger UI)**: http://127.0.0.1:8000/docs
- **备用 API 文档 (ReDoc)**: http://127.0.0.1:8000/redoc
- **OpenAPI JSON 模式**: http://127.0.0.1:8000/openapi.json

## API 端点

### 根端点

```http
GET /
```

**响应：**
```json
{
  "message": "Hello World"
}
```

### 问候端点

```http
GET /hello/{name}
```

**参数：**
- `name` (路径参数): 要问候的名称

**响应：**
```json
{
  "message": "Hello {name}"
}
```

## 测试

您可以使用以下方式测试 API 端点：

1. **内置 HTTP 客户端**: 在 JetBrains IDEs (PyCharm, IntelliJ IDEA) 中使用 `test_main.http` 文件

2. **curl 命令**:
```bash
# 测试根端点
curl http://127.0.0.1:8000/

# 测试问候端点
curl http://127.0.0.1:8000/hello/User
```

3. **交互式文档**: 在浏览器中访问 http://127.0.0.1:8000/docs



## 开发

### 生产环境部署

生产环境部署时，请移除 `--reload` 参数：

```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

### 环境变量

根据需要使用环境变量配置应用程序。

## 许可证

本项目采用 MIT 许可证。
