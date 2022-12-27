import requests
from lxml import etree
from datetime import datetime

if __name__ == '__main__':
    url = 'https://www.zdaye.com/dayProxy.html'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4515.159 Safari/537.36'
    }
    # verify=False  禁用证书验证
    content = requests.get(url, headers=headers, verify=False).content
    tree = etree.HTML(content)
    latest_page_time = tree.xpath("//span[@class='thread_time_info']/text()")[0].strip()
    interval = datetime.now() - datetime.strptime(latest_page_time, "%Y/%m/%d %H:%M:%S")
    print(interval.seconds)
    if interval.seconds < 300:
        target_url = "https://www.zdaye.com/" + tree.xpath("//h3[@class='thread_title']/a/@href")[0].strip()
        while target_url:
            _tree = etree.HTML(requests.get(url, headers=headers).content)
            for tr in _tree.xpath("//table//tr"):
                ip = "".join(tr.xpath("./td[1]/text()")).strip()
                port = "".join(tr.xpath("./td[2]/text()")).strip()
                print(ip, port)
            next_page = _tree.xpath("//div[@class='page']/a[@title='下一页']/@href")
            target_url = "https://www.zdaye.com/" + next_page[0].strip() if next_page else False