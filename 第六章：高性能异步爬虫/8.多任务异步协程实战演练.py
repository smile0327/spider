import threading

import requests
from lxml import etree
import time
import os

# 引入协程相关依赖
import asyncio
import aiohttp


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'
}

def createDir():
    if not os.path.exists('./libs'):
        os.mkdir('./libs')

def getImageUrls():
    """
    获取所有图片url
    :return:
    """
    template_url = 'http://pic.netbian.com/4kmeinv/index_%d.html'
    img_urls = []
    for page in range(2, 5):
        new_url = format(template_url % page)
        page_text = requests.get(url=new_url, headers=headers).text
        tree = etree.HTML(page_text)
        li_list = tree.xpath('//div[@class="slist"]/ul/li')
        for li in li_list:
            img_src = 'http://pic.netbian.com' + li.xpath('./a/img/@src')[0]

            # 以下为串行下载
            # name = img_src.split('/')[-1]
            # data = requests.get(url=img_src).content
            # path = './libs/'+name
            # with open(path,'wb') as fp:
            #     fp.write(data)
            #     print(name,'下载成功')
            # tasks.append(name)

            # 将图片url放入列表中
            img_urls.append(img_src)


async def download_img(url):
    """
    异步协程下载图片
    :param url:
    :return:
    """
    async with aiohttp.ClientSession() as session:
        async with await session.get(url=url) as response:
            name = url.split('/')[-1]
            path = './libs/' + name
            # 注意：获取响应数据操作之前一定要使用await进行手动挂起
            # read()返回二进制数据
            data = await response.read()
            with open(path, 'wb') as fp:
                fp.write(data)
            print(url, '下载成功')


def createTasks(img_urls):
    tasks = []
    for url in img_urls:
        # 返回协程对象
        c = download_img(url)
        # 将协程对象封装为future
        task = asyncio.ensure_future(c)
        tasks.append(task)
    return task


if __name__ == '__main__':
    start = time.time()
    createDir()

    img_urls = getImageUrls()
    tasks = createTasks(img_urls)

    # 将多任务注册到循环对象中
    loop = asyncio.get_event_loop()
    # 多任务执行
    loop.run_until_complete(asyncio.wait(tasks))

    print(len(img_urls))
    print('总耗时：', time.time() - start)