from flask import Flask
import redis
import json
from flask_caching import Cache

# Configure Redis client
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

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
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_DEFAULT_TIMEOUT'] = 300  # Default TTL: 5 minutes

cache = Cache(app)

    # functools.lru_cache
    #Cache on Flask Routes
# You can also cache responses at the API level using Flask extensions like Flask-Caching.