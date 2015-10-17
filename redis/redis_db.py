import redis


class RedisDataBase(object):
    r = redis.StrictRedis(host='localhost', port=6379, db=0)

    @staticmethod
    def save_to_db(key, value):
        return RedisDataBase.r.set(key, value)

