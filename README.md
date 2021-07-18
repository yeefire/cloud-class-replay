# [腾讯课堂、钉钉]在线网课视频直播回放下载离线播放 cloud-class-replay

有些精品好课真的是百看不厌、教师精心准备、学习氛围也好。不过有些已购买的课程却只能在线观看…现在讲究的是一个环保、节能。如果能将已购买的课程离线下载好，那么会为各大平台节省多少带宽费用当然还有数据包在这世间重复的传输所浪费的电力资源。

本着环保、节能、减排的目的，开始了尝试对腾讯课堂网页版中自己购买了课程的视频回放进行下载。

# 更新记录

## 2021.7.18

- 更新后钉钉回放可以通过本脚本下载了
- 请重新pull拉取本项目，进入虚拟环境。重新执行`pip3 install -r requirements.txt`来完成本次更新。

1. 更新user-agent
2. 使用`requests[security]`，解决SSL错误。请重新执行`pip3 install -r requirements.txt`来进行更新。

使用方法：

1. 克隆本项目到某当前 `git clone https://github.com/yeefire/cloud-class-replay.git`
2. 进入项目目录 `cd cloud-class-replay`
3. 创建虚拟环境 `pyhton3 -m venv ./venv`
4. 激活虚拟环境 `source venv/bin/activate`
5. 先安装依赖模块 `pip3 install -r requirements.txt`
6. 命令行执行 
   - 下载腾讯课堂回放：`python3 tencent_class_m3u8.py 这节课的名称 这节课的M3U文件请求地址(网址或者本地路径都可以)`
   - 下载钉钉回放：`python3 dingtalk_class_m3u8_standard.py 这节课的名称 这节课的M3U文件请求地址(网址或者本地路径都可以)`
    
7. 脚本会在运行的目录创建一个这节课名的文件夹，最终下载合成后的视频就在这个目录里。
  
* 钉钉有两个下载脚本，顺序下载和异步方式下载。建议使用`dingtalk_class_m3u8_standard.py`，如果你希望并发下载请尝试使用`dingtalk_class_m3u8_async.py`

例如: `python3 tencent_class_m3u8.py 【Python进阶】Python-上午 https://1dada217.vod2.myqcloud.com/fdadadada3kmdkfsxxxxxxxxxxxxxxxxx`

获取详细使用及脚本思路可以访问博客寻找更多信息或与我联系。[Yee's Blog](https://blog.yeefire.com/2020_12/cloud_class_replay.html)
