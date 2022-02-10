from Crypto.Cipher import AES
import requests
import aiofiles
import m3u8
import os, sys

class_video_name = sys.argv[1]
m3u8_file_uri = sys.argv[2]

prefix_request_url = f'{m3u8_file_uri.rsplit("/", 1)[0]}/'
headers={'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_16_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36 DingTalk(5.1.40-macOS-macOS-MAS-14354546) nw Channel/201200'}

def download_m3u8_video(index: int, suffix_url: str):
    if not os.path.exists(f'{class_video_name}/downloads/{index}.ts'):
        i = 0
        while i < 3:
            try:
                download_video_ts = requests.get(url=prefix_request_url + suffix_url, timeout=60)
                if download_video_ts.content:
                    with open(f'{class_video_name}/downloads/{index}.ts', "wb") as ts:
                        ts.write(download_video_ts.content)
                    print(f'[{class_video_name}]——已下载第 {index} 个片段/ 共 {len(playlist.files)} 个片段')
                    return
                raise requests.exceptions.RequestException
            except requests.exceptions.RequestException:
                print(f'[{class_video_name}]——下载超时，正在重新下载第 {index} 个片段/ 共 {len(playlist.files)} 个片段')
                i += 1


def download_m3u8_all():
    print(f'[{class_video_name}]——已开始下载，请稍后……')
    if not os.path.exists(class_video_name + '/downloads'):
        os.makedirs(class_video_name + '/downloads')
    [download_m3u8_video(i, video_suffix_url) for i, video_suffix_url in enumerate(playlist.files, 1)]
    download_encrypt_list = [uri for uri in os.listdir(f'{class_video_name}/downloads') if uri[0] != '.']
    if len(download_encrypt_list) == len(playlist.files):  # 判断是否有漏下的分段视频没有下载
        print(f'[{class_video_name}]——视频全部下载完成')
        return download_encrypt_list
    else:  # 有部分视频在多次重试后依旧没有下载成功
        print(f'[{class_video_name}]——下载过程中出现问题，正在重试...')
        return download_m3u8_all()


def merge_m3u8_all():
    with open(f'{class_video_name}/{class_video_name}.mp4', 'ab') as final_file:
        print(f'[{class_video_name}]——开始拼接下载的分段视频')
        temp_file_uri_list = [uri for uri in os.listdir(f'{class_video_name}/downloads') if uri[0] != '.']
        temp_file_uri_list.sort(key=lambda x: int(x[:-3]))
        for uri in temp_file_uri_list:
            # if uri[0] == '.': continue  # 忽略隐藏文件
            with open(f'{class_video_name}/downloads/{uri}', 'rb') as temp_file:
                final_file.write(temp_file.read())  # 将ts格式分段视频追加到完整视频文件中
        print(f'[{class_video_name}]——合成视频成功')

def merge_m3u8_ffmpeg():
    with open(f'{class_video_name}/list.txt', 'w+') as list_file:
        print(f'[{class_video_name}]——开始生成合并列表清单',end="...")
        temp_file_uri_list = [uri for uri in os.listdir(f'{class_video_name}/downloads') if uri[0] != '.']
        temp_file_uri_list.sort(key=lambda x: int(x[:-3]))
        for uri in temp_file_uri_list:
            list_file.writelines(f"file downloads/{uri}\n")
        print('已生成')
        print('使用ffmpeg合成视频文件')
        os.chdir(f'{class_video_name}')
        os.popen('ffmpeg -y -loglevel info -f concat -i list.txt -acodec copy -vcodec copy output.mp4')
        print(f'[{class_video_name}]——视频文件:{os.getcwd()}/output.mp4')




if __name__ == '__main__':
    playlist = m3u8.load(m3u8_file_uri, verify_ssl=False)
    download_m3u8_all()
    merge_m3u8_all()
    # merge_m3u8_ffmpeg()

