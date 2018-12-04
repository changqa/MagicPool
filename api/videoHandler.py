import json
import os

from tornado.web import RequestHandler

from crawler.videoCrawler import VideoCrawler
from .baseHandler import BaseHandler


class VideoHandler(BaseHandler):

    async def get_video_url_list(self):
        """ 根据剧名查找所有的集数的url

        """
        video_name = self.get_argument("video_name", None)
        if not video_name:
            ret = self.fail("请输入视频名称!")
        else:
            crawler = VideoCrawler()
            try:
                url_list = await crawler.get_video_url_tencent(video_name)
            except Exception as e:
                ret = self.fail(str(e))
            else:
                ret = self.success(url_list)

        return ret

    async def get_video_interface(self):
        """ 获取视频解析接口

            从本地文件中读取视频解析接口数据。
        """
        file_path = os.getcwd() + "/data/videoPool.json"
        with open(file_path, "r") as f:
            video_interface = json.load(fp=f)

        return self.success(video_interface)

    async def get(self, method):
        return await eval("self."+method)()
