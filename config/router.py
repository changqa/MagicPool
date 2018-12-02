from api import ProxyHandler, VideoHandler

__all__ = ['routers']

routers = [
    (r"/proxy/(.*)", ProxyHandler),
    (r"/video/(.*)", VideoHandler)
]