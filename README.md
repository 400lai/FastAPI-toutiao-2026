# Toutiao Backend

基于 FastAPI 构建的头条应用后端 API 服务。

## 项目概述

本项目为头条应用提供 RESTful API 后端服务，利用 FastAPI 的高性能和异步特性。

## 技术栈

- **框架**: FastAPI
- **语言**: Python 3.x
- **服务器**: Uvicorn (ASGI)

## 项目结构

```
toutiao_backend/
├── main.py              # 主应用入口文件
├── test_main.http       # HTTP 测试请求文件
└── README.md            # 项目文档
```

## 安装

1. 克隆项目：
```bash
git clone <https://github.com/400lai/FastAPI-toutiao-2026.git>
cd toutiao_backend
```

2. 安装依赖：
```bash
pip install fastapi uvicorn
```

## 使用方法

### 启动服务器

运行开发服务器：

```bash
uvicorn main:app --reload
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
