import re
import json

from pyquery import PyQuery as pq
from tornado.httpclient import AsyncHTTPClient
from tornado.ioloop import IOLoop

from utils.redisClient import RedisClient
from config.config import REDIS_XUNLEI_KEY

from .baseCrawler import BaseCrawler


class XunleiCrawler(BaseCrawler):

    _self = None

    def __init__(self, db):
        super().__init__()
        self._db = db

    @classmethod
    async def current(cls):
        if not cls._self:
            db = await RedisClient.current()
            cls._self = cls(db)

        return cls._self

    async def crawl_fenxiangdashi_index(self):
        """
        获取分享大师网迅雷列表链接
        """
        url = "http://www.fenxiangdashi.com"
        xunlei_url = url + "/xunlei"
        http_client = AsyncHTTPClient()
        response = await http_client.fetch(xunlei_url, headers=self.headers)
        if response.code == 200:
            doc = pq(str(response.body, 'utf-8'))
            rst = doc(".clearfix .more")
            for record in rst.items():
                yield url+record.attr("href")

    async def crawl_fenxiangdashi(self):

        http_client = AsyncHTTPClient()

        async for url in self.crawl_fenxiangdashi_index():
            response = await http_client.fetch(url, headers=self.headers)
            if response.code == 200:

                for record in re.finditer(r'账号：(.*?) 密码：(.*?)<br/>',
                                          str(response.body, 'utf-8')):
                    yield (record.group(1), record.group(2))
            else:
                print("crawler_89ip 匹配代理失败")

    async def crawl_xunl8_index(self):
        """ 爬取 迅雷吧(http://www.xunl8.com/) 的首页获取链接

            Returns:
                返回链接
        """
        url = 'http://www.xunl8.com/'

        http_client = AsyncHTTPClient()
        response = await http_client.fetch(url, headers=self.headers)
        if response.code == 200:
            doc = pq(str(response.body, 'utf-8'))
            rst = doc("#divMain .post-title a")
            for record in rst.items():
                yield record.attr("href")

    async def crawl_xunl8(self):
        """爬取 迅雷吧 的vip账号

        """
        http_client = AsyncHTTPClient()

        async for url in self.crawl_xunl8_index():
            response = await http_client.fetch(url, headers=self.headers)
            if response.code == 200:

                doc = pq(str(response.body), 'utf-8')
                rst = doc("#divMain .post-body")

                for record in re.finditer(r'账号：(.*?) 密码：(.*?)<br/>',
                                          str(response.body, 'utf-8')):
                    yield (record.group(1), record.group(2))
            else:
                print("crawler_89ip 匹配代理失败")


    async def run(self):
        async for account in self.crawl_fenxiangdashi():
            print(account)
            value = json.dumps(
                {"username": account[0], "password": account[1]}
            )
            await self._db.add(REDIS_XUNLEI_KEY, value)


async def main():
    crawler = await XunleiCrawler.current()
    await crawler.crawl_xunl8_index()

    # crawler = await XunleiCrawler.current()
    # await crawler.run()

if __name__ == '__main__':
    IOLoop.current().run_sync(main)
