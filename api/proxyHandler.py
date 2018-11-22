from tornado.web import RequestHandler

from config.config import REDIS_PROXY_KEY
from utils.redisClient import RedisClient


class ProxyHandler(RequestHandler):

    async def gain(self):
        redis_client = await RedisClient.current()
        return await redis_client.get(REDIS_PROXY_KEY)

    async def count(self):
        redis_client = await RedisClient.current()
        return await redis_client.count(REDIS_PROXY_KEY)

    async def get(self):
        method = self.get_argument("method", None)
        result = await eval("self."+method)()
        return self.write(str(result))
