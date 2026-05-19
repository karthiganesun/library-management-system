# import hashlib


# def hashed_password(Password):
#     return hashlib.sha256(Password.encode()).hexdigest()


# pip install passlib[bcrypt]


from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hashed_password(Password : str):
    return pwd_context.hash(Password)

def verify_password(plain_password:str, hashed_password:str):
    return pwd_context.verify(plain_password,hashed_password)
