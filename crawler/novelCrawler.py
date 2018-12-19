import asyncio

import aiohttp
from .baseCrawler import BaseCrawler
from bs4 import BeautifulSoup
from feng_libs.data.proxyPool import ProxyPool


class NovelCrawler(BaseCrawler):

    def __init__(self):
        self.base_url_biquge = "https://www.biqudu.com"
        self.timeout = 30

    async def crawl_biquge_brower(self, name):
        """ 在笔趣阁中搜索小说得到目录url

        Args:
            name: 小说名

        Returns:
            novel_brower: 小说的章节目录列表，list 

        Exceptions:
            超时
        """

        proxy = await ProxyPool.get_proxy()
        proxy = None

        query_url = f"{self.base_url_biquge}/searchbook.php"
        params = {
            "keyword": name
        }

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as client:
            resp = await client.get(query_url, params=params,
                                    headers=self.headers, ssl=False,
                                    proxy=proxy)
            resp_text = await resp.text()

            try:
                book_url = BeautifulSoup(resp_text, 'lxml').select(
                    "#hotcontent > div > div > div.image > a")[0]['href']
            except Exception as e:
                raise Exception("未搜索到该小说")

            resp = await client.get(self.base_url_biquge+book_url,
                                    headers=self.headers, ssl=False)
            resp_text = await resp.text()
            book_section_a = BeautifulSoup(
                resp_text, "lxml").select("#list > dl > dd > a")
            return [_['href'] for _ in book_section_a]

    async def crawl_biquge_content(self, url):
        """ 根据url爬去笔趣阁的章节内容

            Args:
                url: 章节url
        """

        timeout = aiohttp.ClientTimeout(total=self.timeout)
        async with aiohttp.ClientSession(timeout=timeout) as client:
            resp = await client.get(self.base_url_biquge+url,
                                    headers=self.headers, ssl=False)

            resp_text = await resp.text()
            soup = BeautifulSoup(resp_text, 'lxml').select("#content")[0]

            # 清除script标签
            [script.extract() for script in soup('script')]

            return soup.text.lstrip().rstrip()

    async def crawl_brower(self, name):
        """ 对外提供获取小说目录url的接口

            Args:
                name: 小说名称

            Returns:
                novel_brower: 小说的章节目录列表，list 
        """

        retry_number = 0
        while retry_number < self.retry_max_num:

            try:
                novel_browler = await self._crawl_biquge_brower(name)
                break
            except Exception as e:
                print(f"retry {retry_number}")
                retry_number += 1
        else:
            raise Exception("获取目录失败")

        return novel_browler

    async def crawl_content(self, url):
        """ 通过url

        """
        pass


async def main():
    novelCrawler = NovelCrawler()
    novel_brower = await novelCrawler.crawl_biquge_brower("人皇纪")
    print(novel_brower)

    # novel_content = await novelCrawler.crawl_biquge_content("/16_16431/9883799.html")
    # print(novel_content)

    # novel_brower = await novelCrawler.crawl_brower("人皇纪")
    # print(novel_brower)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
