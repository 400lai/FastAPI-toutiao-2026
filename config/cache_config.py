import redis

REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0

# 创建redis连接对象
redis_client = redis.Redis(
    host=REDIS_HOST,  # Redis 服务器的主机地址
    port=REDIS_PORT,  # Redis 端口号
    db=REDIS_DB,  # Redis 数据库编号，0~15
    decode_responses=True  # Redis 默认返回的响应是字节对象，设置decode_responses=True，将字节对象转换为字符串对象
)