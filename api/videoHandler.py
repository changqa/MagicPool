import json
import os

from tornado.web import RequestHandler

from crawler.videoCrawler import VideoCrawler


class VideoHandler(RequestHandler):

    async def get_video_url_list(self):
        """ 根据剧名查找所有的集数的url

        """
        video_name = self.get_argument("video_name")
        crawler = VideoCrawler()
        return await crawler.get_video_url_tencent(video_name)

    async def get_video_interface(self):
        file_path = os.getcwd() + "/data/videoPool.json"
        with open(file_path, "r") as f:
            video_interface = json.load(fp=f)

        return str(video_interface)

    async def get(self, method):
        result = await eval("self."+method)()
        return self.write(str(result))
