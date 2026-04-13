# 导入异步 Redis 客户端库，用于缓存操作（适配 FastAPI 异步框架）
import json
from typing import Any

import redis.asyncio as redis

REDIS_HOST = "192.168.100.128"
REDIS_PORT = 6379
REDIS_DB = 0
REDIS_PASSWORD = "123456"

# 创建redis连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # Redis 服务器的主机地址
    port=REDIS_PORT,  # Redis 端口号
    db=REDIS_DB,  # Redis 数据库编号，0~15
    password=REDIS_PASSWORD,
    decode_responses=True  # Redis 默认返回的响应是字节对象，设置decode_responses=True，将字节对象转换为字符串对象
)

# 设置 和 读取（字符串 和 列表或字典）"[{}]"
# 读取：字符串
async def get_cache(key: str):
    try:
        return await redis_client.get(key)
    except Exception as e:
        print(f"获取缓存失败: {e}")
        return None

# 读取：列表或字典
async def get_json_cache(key: str):
    try:
        data = await redis_client.get(key)
        if data:
            return json.loads(data) # 将redis取出的json字符串反序列化为python对象
        return None
    except Exception as e:
        print(f"获取 JSON 缓存失败: {e}")

# 设置缓存 setex key (key, expire, value)
async def set_cache(key: str, value: Any, expire: int = 3600):
    try:
        if isinstance(value, (dict, list)): # 判断 value 是否为字典或列表
            # 将字典或列表序列化为 JSON 字符串
            value = json.dumps(value, ensure_ascii=False) # 中文默认编码为 ASCII，设置 ensure_ascii=False，将中文编码为 UTF-8
        await redis_client.setex(key, expire, value)
        return True
    except Exception as e:
        print(f"设置缓存失败: {e}")
        return False
