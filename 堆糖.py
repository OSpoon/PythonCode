# 准备
# 请求地址
# https://www.duitang.com/napi/blog/list/by_search/?kw=%E6%A0%A1%E8%8A%B1&type=fee&start=0
# 数据结构
# {
#     "status": 1,
#     "data": {
#         "total": 3600,
#         "next_start": 48,
#         "object_list": [
#             {
#                 "photo": {
#                     "width": 533,
#                     "height": 800,
#                     "path": "https://b-ssl.duitang.com/uploads/item/201511/06/20151106134813_vd2SC.jpeg"
#                 },
#                 "msg": "校花",
#                 "id": 477444978,
#                 "buyable": 0,
#                 "add_datetime": "2015年11月6日 13:48",
#                 "add_datetime_pretty": "2年前",
#                 "add_datetime_ts": 1446788894,
#                 "sender_id": 10556290,
#                 "favorite_count": 4,
#                 "extra_type": "PICTURE",
#                 "is_certify_user": false
#             }
#         ],
#         "more": 1,
#         "limit": 24
#     }
# }

import requests
import json
import os
import threading

url = 'https://www.duitang.com/napi/blog/list/by_search/?kw=%s&type=fee&start=%s'
thread_lock = threading.BoundedSemaphore(value=5)


# 获取数据
def get_page(keyword, start):
    return requests.get(url % (keyword, start)).text


# 数据解析
def findall(page_data):
    photo_path_list = []
    data = json.loads(page_data)
    photo_list = data['data']['object_list']
    for photo in photo_list:
        photo_path_list.append(photo['photo']['path'])
    return photo_path_list


# 下载文件
def down_photo(photo_path):
    save_image(requests.get(photo_path).content, photo_path)


# 保存文件
def save_image(byte, photo_path):
    filename = os.path.basename(photo_path)
    print('成功提取文件名 :', filename)
    is_have = os.path.exists('pics')
    if not is_have:
        os.mkdir('pics')
    file_path = 'pics/' + filename
    with open(file_path, 'wb') as f:
        f.write(byte)
    thread_lock.release()


# main方法
if __name__ == '__main__':
    kw = '校花'
    for index in range(0, 3600, 24):
        # 获取数据
        page = get_page(kw, index)
        # 数据解析
        path_list = findall(page)
        for path in path_list:
            # 循环图片路劲进行下载操作
            thread_lock.acquire()
            t = threading.Thread(target=down_photo, args=(path,))
            t.start()
