from api.proxyHandler import ProxyHandler

__all__ = ['routers']

routers = [
    (r"/proxy", ProxyHandler)
]