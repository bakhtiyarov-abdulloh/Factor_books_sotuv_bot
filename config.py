import os
from dotenv import load_dotenv
from redis_dict import RedisDict

load_dotenv('.env')

TOKEN = os.getenv('TOKEN')
ADMIN = list(map(int, os.getenv('ADMIN', []).split(',')))
db = RedisDict('books')
