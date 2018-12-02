import asyncio
import json
import re

from aiohttp import ClientSession

from .baseCrawler import BaseCrawler


class VideoCrawler(BaseCrawler):
    """ 爬取视频链接。

    """

    def __init__(self):
        pass

    async def get_video_url_tencent(self, video_name):
        """ 从腾讯网. 根据剧名爬取所有集数的url

            Params:
                video_name: 剧名

            Returns:
                该电视剧所有的集数的title及其url
        """
        query_url = f'https://v.qq.com/x/search/?q={video_name}'
        detail_url = 'https://s.video.qq.com/get_playsource'

        ret_video_url = []

        async with ClientSession() as client:
            # 获取 video_id, video_range集数
            resp = await client.get(query_url)
            text = await resp.text()
            video_id = re.search(r"id: '(.*?)';", text).group(1)
            video_range = re.search(r"initRange: '(.*?)';", text).group(1)

            # 获取视频级数信息
            data = {
                "id": video_id,
                "range": video_range,
                "otype": "json",
                "type": "4",
            }
            resp = await client.get(detail_url, params=data)
            text = await resp.text()
            text_json = re.search(r"QZOutputJson=(.*?);", text).group(1)
            video_info = json.loads(text_json)
            for video_play in video_info['PlaylistItem']['videoPlayList']:
                play_id = video_play['id']
                title = video_play['title']
                video_play_url = video_play['playUrl']
                real_play_url = "{}/{}.html".format(
                    video_play_url[:video_play_url.find('.html')],
                    play_id
                )
                ret_video_url.append(
                    {"real_play_url": real_play_url, "title": title})

        return ret_video_url


async def main():
    crawler = VideoCrawler()
    await crawler.get_video_url_tencent("夜天子")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
