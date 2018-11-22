from crawler import ProxyCrawler, XunleiCrawler
from utils import RedisClient
from tornado.ioloop import IOLoop
from tester import ProxyTester
from config import setting


async def main():
    # proxy = await ProxyCrawler.current()
    # await proxy.run()

    xunlei = await XunleiCrawler.current()
    await xunlei.run()

    # redis_client = await RedisClient.current()
    # rst = await redis_client.range("proxy", 0, 10)
    # print(rst)
    # count = await redis_client.count("proxy", 0, 100)
    # print(count)
    # score = await redis_client.score("proxy", "93.183.247.44:53281")
    # print(score)

    # proxy_test = await ProxyTester.current()
    # rst = await proxy_test.test_single_proxy("93.183.247.44:53281")
    # await proxy_test.run()

if __name__ == '__main__':

    IOLoop.current().run_sync(main)
