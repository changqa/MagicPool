import asyncio

import aiohttp
from .baseCrawler import BaseCrawler
from bs4 import BeautifulSoup
from feng_libs.data.proxyPool import ProxyPool


class NorvalCrawler(BaseCrawler):

    def __init__(self):
        pass

    async def crawl_biquge(self, name):
        """ 爬取笔趣读小说存入数据库中

        Args:
            name: 小说名

        """

        # proxy = await ProxyPool.get_proxy()

        base_url = "https://www.biqudu.com"

        query_url = f"{base_url}/searchbook.php"
        params = {
            "keyword": name
        }

        async with aiohttp.ClientSession() as client:
            resp = await client.get(query_url, params=params,
                                    headers=self.headers, ssl=False)
            resp_text = await resp.text()
            book_url = BeautifulSoup(resp_text, 'lxml').select(
                "#hotcontent > div > div > div.image > a")[0]['href']

            resp = await client.get(base_url+book_url,
                                    headers=self.headers, ssl=False)
            resp_text = await resp.text()
            book_section_a = BeautifulSoup(resp_text, "lxml").select("#list > dl > dd > a")
            for _ in book_section_a:
                print(_['href'])


async def main():
    norvalCrawler = NorvalCrawler()
    await norvalCrawler.crawl_biquge("一念永恒")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
