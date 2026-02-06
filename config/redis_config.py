import os

import redis
from dotenv import load_dotenv
load_dotenv()
config = redis.Redis.from_url(os.getenv('REDIS_URL'))
config.save()
