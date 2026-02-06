from redis import Redis

config = Redis(host='localhost', port=6379, db=0)
config.save()
