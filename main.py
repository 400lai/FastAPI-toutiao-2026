from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from routers import news, users
from utils.exception_handlers import register_exception_handlers

app = FastAPI()

# 注册异常处理器
register_exception_handlers(app)

# 允许的来源（可以是域名列表）
origins = [
    "http://localhost",
    "http://localhost:8080",
    "https://your-frontend-domain.com"
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # 允许的源，开发阶段允许所有源，生产环境需要指定源
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],     # 允许的请求方法
    allow_headers=["*"],     # 允许的请求头
)
@app.get("/")
async def root():
    return {"message": "Hello World"}

# 注册路由
app.include_router(news.router)
app.include_router(users.router)

