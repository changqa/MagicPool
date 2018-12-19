from .baseHandler import BaseHandler
from crawler.novelCrawler import NovelCrawler


class NovelHandler(BaseHandler):

    async def get_browser(self):

        name = self.get_argument("name", None)
        if not name:
            return self.fail("请输入书名")
        norvelCrawler = NovelCrawler()
        brower = await norvelCrawler.crawl_biquge_brower(name)
        return self.success(brower)

    async def get_content(self):

        url = self.get_argument("url", None)
        if not url:
            return self.fail("请输入url")

        norvelCrawler = NovelCrawler()
        content = await norvelCrawler.crawl_biquge_content(url)
        return self.success(content)

    async def get(self, method):
        return await eval("self."+method)()
