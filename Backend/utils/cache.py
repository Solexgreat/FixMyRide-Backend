from flask import Flask
import redis
import os
import json
from flask_caching import Cache
from dotenv import load_dotenv

load_dotenv()

# Configure Redis client
redis_host=os.getenv('REDIS_HOST')
redis_client = redis.StrictRedis.from_url(redis_host, decode_responses=True, ssl_cert_reqs=None)

def cache_set(key, value, ttl):
    """Set a key-value pair in Redis with a TTL"""
    redis_client.setex(key, ttl, json.dumps(value))

def cache_get(key):
    """Get a value from Redis by key"""
    cached_data = redis_client.get(key)
    return json.loads(cached_data) if cached_data else None

app = Flask(__name__)

# Configure Flask-Caching
app.config['CACHE_TYPE'] = 'RedisCache'  # Use Redis for caching
app.config['CACHE_REDIS_URL'] = redis_host
app.config['CACHE_DEFAULT_TIMEOUT'] = 400

cache = Cache(app)

    # functools.lru_cache
    #Cache on Flask Routes
# You can also cache responses at the API level using Flask extensions like Flask-Caching.