from passlib.context import CryptContext

# 创建密码上下文
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_hash_password(password: str):
    """
    对密码进行哈希加密

    :param password: 待加密的原始密码字符串
    :return: 加密后的密码哈希值
    """
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    """
    验证密码是否正确

    :param plain_password: 待验证的原始密码
    :param hashed_password: 已存储的密码哈希值
    :return: 密码匹配返回 True，否则返回 False
    """
    return pwd_context.verify(plain_password, hashed_password)
