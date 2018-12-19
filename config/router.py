from api.videoHandler import VideoHandler
from api.proxyHandler import ProxyHandler
from api.novelHandler import NovelHandler

__all__ = ['routers']

routers = [
    (r"/proxy/(.*)", ProxyHandler),
    (r"/video/(.*)", VideoHandler),
    (r"/novel/(.*)", NovelHandler),
]