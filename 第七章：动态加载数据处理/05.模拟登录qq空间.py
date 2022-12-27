from selenium import webdriver
from time import sleep

bro = webdriver.Chrome(executable_path='./chromedriver')

bro.get('https://qzone.qq.com/')

# 切换到iframe标签也页面
bro.switch_to.frame('login_frame')

# 定位到账号密码登录标签 并点击
a_tag = bro.find_element_by_id("switcher_plogin")
a_tag.click()

# 定位账号/密码输入框
userName_tag = bro.find_element_by_id('u')
password_tag = bro.find_element_by_id('p')
sleep(1)
# 输入账号
userName_tag.send_keys('840878453')
sleep(1)
# 输入密码
password_tag.send_keys('password')
sleep(1)
# 定位登录标签 定点击
btn = bro.find_element_by_id('login_button')
btn.click()

sleep(3)

bro.quit()