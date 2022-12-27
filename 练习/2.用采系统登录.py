import json
import re
import time

from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

USERNAME = 'cy'
PASSWORD = 'Aa123456'

class Login(object):

    def __init__(self):
        self.url = 'http://yongcai-test.bobandata.com/collect/#/login'
        opt = webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(r"../chromedriver.exe", chrome_options=opt)
        self.browser.maximize_window()  # 第一处修复，设置浏览器全屏
        self.username = USERNAME
        self.password = PASSWORD
        self.wait = WebDriverWait(self.browser, 20)

    def open(self):
        """
        打开网页，并点击登录
        :return:
        """
        self.browser.get(self.url)

        username = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/form/div[1]/div/div[1]/input')
        username.send_keys(self.username)
        time.sleep(1)
        password = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/form/div[2]/div/div/input')
        password.send_keys(self.password)
        time.sleep(1)
        login_button = self.browser.find_element(By.XPATH, '//*[@id="app"]/div/div[2]/form/div[4]/div/button')
        login_button.click()
        time.sleep(2)

    def get_gap(self):
        """
        获取滑块验证缺口位置
        :return:
        """
        # 获取缺口位置
        gap_element = self.wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[7]/div[2]/div/div/div[2]/div/div/div[1]')))
        # 获取元素的属性
        style = gap_element.get_attribute('style')
        # eg:  position: absolute; width: 40px; height: 40px; background: rgb(255, 255, 255); left: 72.829px; top: 202.083px;
        param_dict = {p.split(':')[0].strip(): p.split(':')[1].strip() for p in style.split(';') if len(p) > 0}
        # print(param_dict)
        # 使用正则去掉px  也可以直接使用 replace('px','')进行替换
        regex = re.compile('[a-zA-Z]')
        left = regex.sub('', param_dict['left'])
        gap = round(float(left))
        return gap

    def get_track(self, distance):
        """
        根据偏移量获取移动轨迹
        :param distance: 偏移量
        :return: 移动轨迹
        """
        # 初速度
        v = 0
        # 单位时间为0.2s来统计轨迹，轨迹即0.2内的位移
        t = 0.3
        # 位移/轨迹列表，列表内的一个元素代表0.2s的位移
        tracks = []
        # 当前的位移
        current = 5
        # 到达mid值开始减速  滑块行程的3/5处开始减速
        mid = distance * 3 / 5
        while current < distance:
            if current < mid:
                # 加速度越小，单位时间的位移越小,模拟的轨迹就越多越详细
                a = 5
            else:
                a = -4
            # 初速度
            v0 = v
            # 0.2秒时间内的位移  s = V0 * t + 1/2a*t² (v0:初速度  a:加速度)
            s = v0 * t + 0.5 * a * (t ** 2)
            # 当前的位置
            current += s
            # 添加到轨迹列表
            tracks.append(round(s))
            # 速度已经达到v,该速度作为下次的初速度
            v = v0 + a * t
        return tracks

    def operate_slider(self, track):
        '''
        拖动滑块
        '''
        # 获取拖动按钮
        slider_bt = self.browser.find_element(By.CLASS_NAME, 'silde')

        # 点击拖动验证码的按钮不放
        ActionChains(self.browser).click_and_hold(slider_bt).perform()

        # 按正向轨迹移动
        for i in track:
            ActionChains(self.browser).move_by_offset(xoffset=i, yoffset=0).perform()

        time.sleep(1)
        ActionChains(self.browser).release().perform()
        time.sleep(3)

    def get_token(self):
        try:
            # 获取token，登录成功后token存储在Local Storage中（F12 Application中可以查看）
            token = self.browser.execute_script('return localStorage.getItem("token-t1");')
            userData = self.browser.execute_script('return localStorage.getItem("userData");')

            # 获取cookies方法，用采系统没有cookies
            # cookies = self.browser.get_cookies()

            # loads将 json字符串转换为dict对象
            user_dict = json.loads(userData)
            user_dict['token'] = token
            # TODO 获取token后保存下来，请求其他接口时使用
            return user_dict
        except:
            print("cookie 获取失败")
            return None

    def run(self):
        # 打开网页并登录
        self.open()
        gap = self.get_gap()
        print('缺口偏移量:', gap)
        track = self.get_track(gap)
        print('滑动轨迹:', track)
        self.operate_slider(track)
        print('登录成功')

        try:
            # 判断是否存在 用电信息采集扩展平台 文本
            elem = self.wait.until(EC.text_to_be_present_in_element((By.CLASS_NAME, 'header-title'), '用电信息采集扩展平台'))
            if elem:
                # 登录成功后获取token,接口请求需要用到
                user_token = self.get_token()
                print(user_token)
                time.sleep(10)
            else:
                print("get user_token errors")
        except Exception as e:
            print(e, 'fail! ')
        finally:
            self.browser.quit()


if __name__ == '__main__':
    login = Login()
    login.run()