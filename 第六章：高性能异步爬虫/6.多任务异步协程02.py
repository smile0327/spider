import requests
import asyncio
import time

start = time.time()
urls = [
    'http://127.0.0.1:5000/bobo','http://127.0.0.1:5000/jay','http://127.0.0.1:5000/tom'
]

async def get_page(url):
    print('正在下载',url)
    #requests.get是基于同步，必须使用基于异步的网络请求模块进行指定url的请求发送
    #aiohttp:基于异步网络请求的模块
    response = requests.get(url=url)
    print('下载完毕：',response.text)

# 多任务列表
tasks = []

for url in urls:
    c = get_page(url)
    task = asyncio.ensure_future(c)
    tasks.append(task)

# 将多任务注册到循环对象中
loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.wait(tasks))

end = time.time()

print('总耗时:',end-start)