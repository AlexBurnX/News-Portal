import os
import redis
from dotenv import load_dotenv
load_dotenv()


red = redis.Redis(
    host=os.getenv('REDIS_HOST'),  # Укажите свой хост
    port=int(os.getenv('REDIS_PORT')),  # Укажите свой порт
    password=os.getenv('REDIS_PASS')  # Укажите свой пароль
)
