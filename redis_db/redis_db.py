import redis

client_db = redis.StrictRedis(host='localhost', port=6379, db=0)


def save_to_db(key, value):
    return client_db.set(key, value)
