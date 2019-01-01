from tornado.gen import sleep
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from tornado.web import Application

from config import routers, settings, APP_PORT
from crawler.proxyCrawler import ProxyCrawler
from tester.proxyTester import ProxyTester


async def run():
    # crawel proxy ip run
    proxy_crawler = await ProxyCrawler.current()
    IOLoop.current().spawn_callback(proxy_crawler.run)

    # proxt tester run
    proxy_tester = await ProxyTester.current()
    IOLoop.current().spawn_callback(proxy_tester.run)

    pass


def main():
    IOLoop.current().spawn_callback(run)

    # api start
    app = Application(routers, **settings)

    http_server = HTTPServer(app)
    http_server.listen(APP_PORT)

    IOLoop.current().start()


if __name__ == '__main__':
    main()
