from Crypto.Cipher import AES
import requests_async as requests
import aiofiles
import m3u8
import os, sys
import asyncio

class_video_name = sys.argv[1]
m3u8_file_uri = sys.argv[2]
prefix_request_url = f'{m3u8_file_uri.rsplit("/", 1)[0]}/'


async def download_m3u8_video(index: int, suffix_url: str):
    if not os.path.exists(f'{class_video_name}/downloads/{index}.ts'):
        i = 0
        while i < 3:
            try:
                download_video_ts = await requests.get(url=prefix_request_url + suffix_url, timeout=60)
                with open(f'{class_video_name}/downloads/{index}.ts', "wb") as ts:
                    ts.write(download_video_ts.content)
                print(f'[{class_video_name}]——已下载第 {index} 个片段/ 共 {len(playlist.files)} 个片段')
                return
            except requests.exceptions.RequestException:
                print(f'[{class_video_name}]——下载超时，正在重新下载第 {index} 个片段/ 共 {len(playlist.files)} 个片段')
                await asyncio.sleep(i)
                i += 1


async def download_m3u8_all():
    print(f'[{class_video_name}]——已开始下载，请稍后……')
    if not os.path.exists(class_video_name + '/downloads'):
        os.makedirs(class_video_name + '/downloads')
    download_async_list = [asyncio.create_task(download_m3u8_video(i, video_suffix_url))
                           for i, video_suffix_url in enumerate(playlist.files, 1)]
    await asyncio.wait(download_async_list)

    download_encrypt_list = [uri for uri in os.listdir(f'{class_video_name}/downloads') if uri[0] != '.']
    if len(download_encrypt_list) == len(playlist.files):  # 判断是否有漏下的分段视频没有下载
        print(f'[{class_video_name}]——视频全部下载完成')
        return download_encrypt_list
    else:  # 有部分视频在三次重试后依旧没有下载成功
        print(f'[{class_video_name}]——下载过程中出现问题，正在重试...')
        return await download_m3u8_all()


async def decrypt_m3u8_video(m3u8_encrypt_file_uri: str, key: bytes, iv: bytes):
    decrypt_name = f'{m3u8_encrypt_file_uri.split("/")[-1].split(".")[0]}'
    dest_decrypt_uri = f'{class_video_name}/decryption/{decrypt_name}.de.ts'
    if not os.path.exists(dest_decrypt_uri):
        async with aiofiles.open(m3u8_encrypt_file_uri, mode='rb') as f:
            f = await f.read()
            content_video_part = AES.new(key, AES.MODE_CBC, iv).decrypt(f)
        async with aiofiles.open(dest_decrypt_uri, mode='wb') as f:
            await f.write(content_video_part)
    print(f'[{class_video_name}]——已解密第 {decrypt_name} 个片段/ 共 {len(playlist.files)} 个片段')


async def decrypt_m3u8_all():
    if not os.path.exists(class_video_name + '/decryption'):
        os.makedirs(class_video_name + '/decryption')
    key = await requests.get(playlist.keys[0].uri)
    key = key.content
    iv = bytes(playlist.keys[0].iv, 'UTF-8')[:16]
    decrypt_m3u8_list = [asyncio.create_task(decrypt_m3u8_video(f'{class_video_name}/downloads/{uri}', key, iv))
                         for uri in os.listdir(f'{class_video_name}/downloads') if uri[0] != '.']  # 忽略隐藏文件
    await asyncio.wait(decrypt_m3u8_list)
    print(f'[{class_video_name}]——视频全部解密完成')


def merge_m3u8_all():
    download_decrypt_list = [uri for uri in os.listdir(f'{class_video_name}/decryption') if uri[0] != '.']
    download_encrypt_list = [uri for uri in os.listdir(f'{class_video_name}/downloads') if uri[0] != '.']
    if len(download_decrypt_list) != len(download_encrypt_list):  # 判断是否有漏下的分段视频没有下载
        print('解密分段视频出现问题，可能是受限于类Unix系统文件句柄数量限制导致脚本不能获取足够的文件句柄。\n '
              '如果你是 Linux 或 Macos 请尝试在运行本脚本的终端内执行 "ulimit -n 5120" 命令，以解除255(Macos)/1024(Linux)数量限制')
        return
    with open(f'{class_video_name}/{class_video_name}.mp4', 'ab') as final_file:
        print(f'[{class_video_name}]——开始拼接解密后的分段视频')
        # temp_file_uri_list = os.listdir(f'{class_video_name}/decryption')
        temp_file_uri_list = [uri for uri in os.listdir(f'{class_video_name}/decryption') if uri[0] != '.']
        temp_file_uri_list.sort(key=lambda x: int(x[:-6]))
        for uri in temp_file_uri_list:
            # if uri[0] == '.': continue  # 忽略隐藏文件
            with open(f'{class_video_name}/decryption/{uri}', 'rb') as temp_file:
                final_file.write(temp_file.read())  # 将ts格式分段视频追加到完整视频文件中
        print(f'[{class_video_name}]——合成视频成功')


if __name__ == '__main__':
    playlist = m3u8.load(m3u8_file_uri, verify_ssl=False)
    del playlist.files[0]  # 第一个文件为视频密钥，忽略这个文件。
    asyncio.run(download_m3u8_all())
    asyncio.run(decrypt_m3u8_all())
    merge_m3u8_all()
    print(f'[{class_video_name}]——视频文件:{os.getcwd()}/{class_video_name}/{class_video_name}.mp4')
