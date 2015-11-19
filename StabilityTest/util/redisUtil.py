import redis
from StabilityTest import app


def connect_db():
    r = redis.Redis(host=app.config['DB_IP'], port=app.config['DB_PORT'])
    return r
