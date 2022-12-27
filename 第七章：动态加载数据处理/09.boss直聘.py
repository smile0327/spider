from lxml import etree

from selenium import webdriver
import time
#实现规避检测
from selenium.webdriver import ChromeOptions

#实现规避检测 （浏览器认为是selenium登录，在验证阶段无法通过）
from selenium.webdriver.chrome.options import Options

option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])

# 实现无可视化界面的操作
chrome_options = Options()
# 浏览器不提供界面
chrome_options.add_argument('--headless')
# 禁用GPU加速
chrome_options.add_argument('--disable-gpu')
# 设置UA检测
chrome_options.add_argument('--user-agent="Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.81 Safari/537.36"')

#如何实现让selenium规避被检测到的风险  , chrome_options=chrome_options
bro = webdriver.Chrome(executable_path='./chromedriver', options=option)

bro.get('https://www.zhipin.com/job_detail/?query=python&city=101200100&industry=&position=')
time.sleep(2)
# 获取页面源码数据
page_text = bro.page_source

tree = etree.HTML(page_text)
li_list = tree.xpath('//*[@id="main"]/div/div[3]/ul/li')
for li in li_list:
    job_company = li.xpath('.//div/div[1]/div[2]/div/h3/a/@title')
    job_salary = li.xpath('.//div/div[1]/div[1]/div/div[2]/span/text()')
    print(job_company,job_salary)

time.sleep(2)
print('close')
bro.quit()
