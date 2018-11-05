import re

from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop
from tornado.gen import sleep

from config import REDIS_PROXY_KEY, CRAWEL_INTERVAL_TIME
from utils import RedisClient


class ProxyCrawler:

    _self = None

    def __init__(self, db):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            "AppleWebKit/537.36 (KHTML, like Gecko)"
            "Chrome/54.0.2840.71 Safari/537.36",
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7'
        }

        self._db = db

    @classmethod
    async def current(cls):
        if not cls._self:
            db = await RedisClient.current()
            cls._self = cls(db)

        return cls._self

    async def crawler_89ip(self, count=100, port=''):
        """
        异步生成器, 获取ip
        """
        url = "http://www.89ip.cn/tqdl.html?" \
              f"api=1&num={count}&port={port}&address=&isp="

        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url, headers=self.headers)
        if response.code == 200:
            for record in re.finditer(
                "(\d+.\d+.\d+.\d+:\d+)",
                str(response.body)
            ):
                yield record.group(0)
        else:
            print("crawler_89ip 匹配代理失败")

    async def run(self):

        while True:
            print("开始爬取代理ip")

            if await self._db.count(REDIS_PROXY_KEY) < 100:
                async for record in self.crawler_89ip():
                    await self._db.add(REDIS_PROXY_KEY, record)
                
            print("爬取代理ip结束")
            await sleep(CRAWEL_INTERVAL_TIME)

if __name__ == '__main__':
    crawler = ProxyCrawler.current()
    IOLoop.current().run_sync(crawler.run)
