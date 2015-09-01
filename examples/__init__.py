import os
from urlparse import urlparse
from redis import StrictRedis


def get_redis():
    redis_url = urlparse(os.environ.get('REDIS_URL'))
    return StrictRedis(
        host=redis_url.hostname,
        port=redis_url.port,
        db=redis_url.path.strip('/'),
        password=redis_url.password)
