#!/usr/bin/python3
# -*- coding: UTF-8 -*-
from urllib import request
from bs4 import BeautifulSoup
import re
import time
import gevent
from gevent import monkey

monkey.patch_all()


# 分析图片地址
def parser(html):
    try:
        soup = BeautifulSoup(html, 'html.parser', from_encoding='gbk')
        imgs = soup.find_all('img', src=re.compile(r'/d/file/\d+/\w+\.jpg'))
        print(imgs)
        return imgs
    except Exception as e:
        print('in parser error=%s' % e)
        return None


# 保存爬取得图片
def save_imgs(path, data):
    print(path)
    try:
        with open(path, 'wb') as f:
            f.write(data)
    except Exception as e:
        print('in save_imgs error=%s' % e)


# 下载器
def download(url):
    # 封装请求头
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) '
                      'AppleWebKit/604.1.38 (KHTML, like Gecko) '
                      'Version/11.0 Safari/604.1.38'
    }
    try:
        # 拼装请求体
        req = request.Request(url=url, headers=header)
        # 发送请求
        response = request.urlopen(req, timeout=10)
        return response.read()
    except Exception as e:
        print('in download error=%s' % e)
        return None



# 爬取图片主函数
def spider():
    imgs = []
    temp = []
    first_url = "http://www.xiaohuar.com/list-1-%s.html"
    for i in range(10):
        html = download(first_url % i)
        if html:
            temp = parser(html)
        if temp != []:
            imgs += temp
    s_time = time.time()
    glist = []
    if imgs:
        print(imgs.__len__())
        for img in imgs:
            data = download("http://www.xiaohuar.com%s" % img['src'])
            g = gevent.spawn(save_imgs, '%s.jpg' % img['alt'], data)
            glist.append(g)
            # save_imgs('%s.jpg' % img['alt'], data)
        gevent.joinall(glist)
        e_time = time.time()
        print('耗费%s 秒' % (e_time - s_time))
    else:
        print("网络错误")


if __name__ == '__main__':
    spider()