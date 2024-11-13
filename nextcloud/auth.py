import random
import string

def generate_password(length: int = 20) -> str:
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))
