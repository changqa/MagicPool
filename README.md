# MagicPool
代理池
迅雷账号池。暂未完成。
视频池。 暂仅支持腾讯连续剧。

# 接口  (请善良对待它们)
## 代理ip
www.wenfengboy.com/proxy/gain    //获取代理ip
www.wenfengboy.com/proxy/count   //代理ip池的数量

## 视频
www.wenfengboy.com/video/get_video_interface     // 获取视频解析接口
www.wenfengboy.com/video/get_video_url_list?video_name=      // 获取视频url

# 开发环境
python3.6以上

## 使用的第三方库
**tornado**
本项目中使用tornado的异步网络框架，提高网络的访问效率。
使用tornado的web框架当api接口。

**aioredis**
使用异步的redis提高对redis读取的效率。

**aiohttp**
使用异步的方式访问网络资源。

#目录
- api
使用tornado web 完成请求接口s
- config
项目配置
- crwler
爬虫
- tester
测试
- utils
工具
- data
本地数据
