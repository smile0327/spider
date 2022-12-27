import time

from selenium import webdriver
from time import sleep
#实现规避检测
from selenium.webdriver import ChromeOptions

# 指定google浏览器驱动（使用个规避监测时指定了驱动，此处不再需要）
from selenium.webdriver import ActionChains
# bro = webdriver.Chrome(executable_path='./chromedriver')

#实现规避检测 （浏览器认为是selenium登录，在验证阶段无法通过）
option = ChromeOptions()
option.add_experimental_option('excludeSwitches', ['enable-automation'])
#如何实现让selenium规避被检测到的风险
bro = webdriver.Chrome(executable_path='./chromedriver', options=option)

# 规避js监测，否则无法验证通过
script = '''
           Object.defineProperty(navigator, 'webdriver', {
               get: () => undefined
           })
           '''
bro.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
     "source": script})

#打开12306首页
bro.get('https://kyfw.12306.cn/otn/resources/login.html')
time.sleep(1)

# 找到账号登录按钮并点击  切换到账号登录界面
hd_btn = bro.find_element_by_class_name('login-hd-account')
hd_btn.click()
time.sleep(1)

# 找到用户名/密码输入框
userName_input = bro.find_element_by_id('J-userName')
password_input = bro.find_element_by_id('J-password')
userName_input.send_keys('cy840878453')
password_input.send_keys('caoyong0327')
time.sleep(1)

# 找到登录按钮 并点击
login_btn = bro.find_element_by_id('J-login')
login_btn.click()
# 延时1秒，否则无法捕捉到span模块
time.sleep(1)

#动作链  引入动作连
action = ActionChains(bro)
# 滑动验证 先找到需要滑动的div,然后向右滑动
# n1z_div = bro.find_element_by_xpath('//*[@id="nc_1_n1z"]')
n1z_div = bro.find_element_by_id('nc_1_n1z')
print(n1z_div)
# 长按需要滑动的span元素
action.click_and_hold(n1z_div)
# 开始向右滑动 每次异动30个offset
action.move_by_offset(300, 0).perform()


time.sleep(10)
# 关闭浏览器
bro.quit()
