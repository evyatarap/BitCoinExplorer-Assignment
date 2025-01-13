import redis
import logging

class RedisDBConn:
    def __init__(self, host, port, access_key):
        self.host = host
        self.port = port
        self.access_key = access_key
        self.logger = logging.getLogger(__name__)  
        
    def connect(self):
        try:
            import redis

            self.conn = redis.Redis(
                host=self.host,
                port=self.port,
                password=self.access_key,
                decode_responses=True
            )

            # Test the connection
            if self.conn.ping():
                self.logger.info("Successfully connected to Redis")
                return True
            else:
                self.logger.error("Failed to connect to Redis")
                return False
        except redis.ConnectionError as e:
            self.logger.error(f"Failed to connect to Redis: {e}")
            self.conn = None
            return False

    def set(self, key, value, ttl=None):
        try:
            if ttl:
                self.conn.set(key, value, ex=ttl)
            else:
                self.conn.set(key, value)
        except redis.RedisError as e:
            self.logger.error(f"Failed to set key {key} in Redis: {e}")

    def get(self, key):
        try:
            return self.conn.get(key)
        except redis.RedisError as e:
            self.logger.error(f"Failed to get key {key} from Redis: {e}")
            return None

    def delete(self, key):
        try:
            self.conn.delete(key)
        except redis.RedisError as e:
            self.logger.error(f"Failed to delete key {key} from Redis: {e}")

    def exists(self, key):
        return self.conn.exists(key)

    def keys(self, pattern):
        return self.conn.keys(pattern)

    def flushdb(self):
        self.conn.flushdb()

    def close(self):
        self.conn.close()