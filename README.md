# [腾讯课堂、钉钉]在线网课视频直播回放下载离线播放 cloud-class-replay

有些精品好课真的是百看不厌、教师精心准备、学习氛围也好。不过有些已购买的课程却只能在线观看…现在讲究的是一个环保、节能。如果能将已购买的课程离线下载好，那么会为各大平台节省多少带宽费用当然还有数据包在这世间重复的传输所浪费的电力资源。

本着环保、节能、减排的目的，开始了尝试对腾讯课堂网页版中自己购买了课程的视频回放进行下载。

使用方法：

* 先安装依赖模块 `pip3 install pycrypto m3u8 aiofiles requests_async`
* 命令行执行 `python3 tencent_class_m3u8.py 这节课的名称 这节课的M3U文件请求地址(网址或者本地路径都可以)`

例如: `python3 tencent_class_m3u8.py 【Python进阶】Python-上午 https://1dada217.vod2.myqcloud.com/fdadadada3kmdkfsxxxxxxxxxxxxxxxxx`
