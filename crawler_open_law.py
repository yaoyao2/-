#-*- coding: UTF-8 -*-
from selenium import webdriver
import xlrd
import time
import xlwt
import urllib
from urllib import request
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
import json
import requests
import pymysql

class OpenLawCrawler():

    def __init__(self):
        self.url = 'http://openlaw.cn/login.jsp'
        self.get_picture()
        # self.get_cookie()
        # self.crawler()

    def get_picture(self):
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.browser.implicitly_wait(5)
        while True:
            try:
                new = self.browser.find_element_by_link_text('看不清？刷新')
                new.click()
                self.browser.implicitly_wait(5)
                img = self.browser.find_element_by_id('kaptcha')
                img_url = img.get_attribute('src')
                print(img_url)
                pos = str(img_url).find('.jpg?v=')
                img_id = str(img_url)[pos+7:]
                img_name = 'img_' + img_id + '.png'
                self.save_img(img_url, img_name)
            except:
                min_img = ''



    def save_img(self, img_url, img_name):
        # self.conn = pymysql.connect(host='193.112.56.204', user='renrendata',
        #                             passwd='data@2018',
        #                             db='renren_data', port=3306, charset='utf8')
        # self.cur = self.conn.cursor()
        #
        # self.cur.execute(
        #     "insert into hualv_Img (%s,%s,%s) values ('%s','%s','%s')" % (
        #         'id', 'url', 'img_name', img_id, img_url, img_name))
        # self.conn.commit()
        # 下载图片，并保存到文件夹中
        response = urllib.request.urlopen(img_url)
        f = open('openlaw_data/' + img_name, 'wb')
        f.write(response.read())
        f.close()
        print('img save ok')

    def crawler(self):

        str = ''
        with open('crawler_open_law.json', 'r', encoding='utf-8') as f:
            listCookies = json.loads(f.read())
        cookie = [item["name"] + "=" + item["value"] for item in listCookies]
        cookiestr = '; '.join(item for item in cookie)
        print(cookiestr)

        ###检查cookie能否使用

        url = 'http://openlaw.cn/user/profile.jsp'

        headers = {
            'cookie': cookiestr,
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'
        }

        # html = requests.get(url=url, headers=headers)

        new_url = 'http://openlaw.cn/judgement/'
        # new_url = 'http://openlaw.cn/search/judgement/type?causeId=08df5355fffa4053b9f4478a46cd51d2'
        new_html = requests.get(url=new_url, headers=headers)

        print(new_html.text)



    def get_cookie(self):
        # chrome_options = Options()
        # chrome_options.add_argument('--headless')
        # self.browser = webdriver.Chrome(chrome_options=chrome_options)
        self.browser = webdriver.Chrome()
        self.browser.get(self.url)
        self.browser.implicitly_wait(10)

        ##向搜索框里输入问句
        username = '1216117959@qq.com'
        password = 'openlaw4288'
        search_input_kuang = self.browser.find_element_by_id('username')
        search_input_kuang.send_keys(username)
        pwd_input = self.browser.find_element_by_id('password')
        pwd_input.send_keys(password)

        code = input()
        code_input = self.browser.find_element_by_id('code')
        code_input.send_keys(code)

        ##点击搜索
        self.browser.find_element_by_id('submit').click()
        time.sleep(5)

        # ###获取保存cookie
        # print(self.browser.current_url)
        # cookie = self.browser.get_cookies()
        # print(cookie)
        # jsonCookies = json.dumps(cookie)
        # with open('crawler_open_law.json', 'w') as f:
        #     f.write(jsonCookies)

        wenshu = self.browser.find_element_by_link_text('裁判文书')
        wenshu.click()
        time.sleep(3)

        qinquan = self.browser.find_element_by_link_text('侵权责任纠纷')
        qinquan.click()
        time.sleep(4)

        anlis = self.browser.find_elements_by_class_name('entry-title')
        ##获取当前句柄
        now_handle = self.browser.current_window_handle

        text_num = 0
        for an in anlis:
            text_num = text_num + 1
            an.click()
            title = an.text
            time.sleep(3)
            # 获取当前浏览器所有的窗口
            handles = self.browser.window_handles
            # 窗口切换，切换为新打开的窗口
            self.browser.switch_to.window(handles[-1])
            # html = self.browser.find_element_by_class_name('ht_kb type-ht_kb status-publish format-standard hentry').text  # 获取网页的html数据
            # soup = BeautifulSoup(html, 'lxml')  # 对html进行解析，如果提示lxml未安装，直接pip install lxml即可
            html = self.browser.page_source
            soup = BeautifulSoup(html, 'lxml')
            print(text_num)
            # print(soup.text)
            # nef = open(str(text_num)+'.txt', 'w', encoding='utf8')
            # nef.write(soup.text)
            # nef.close()

            self.conn = pymysql.connect(host='193.112.56.204', user='renrendata', passwd='data@2018',
                                        db='renren_data', port=3306, charset='utf8')
            self.cur = self.conn.cursor()

            self.cur.execute("insert into open_law (%s, %s, %s) values ('%s','%s','%s');" % (
                'id', 'text', 'title', str(text_num), pymysql.escape_string(soup.text), pymysql.escape_string(title)))
            self.conn.commit()
            self.browser.close()
            self.browser.switch_to_window(now_handle)


        while True:
            try:
                next_page = self.browser.find_elements_by_class_name('next page-numbers')
                next_page.click()
                anlis = self.browser.find_element_by_class_name('entry-title')
                ##获取当前句柄
                now_handle = self.browser.current_window_handle

                for an in anlis:
                    text_num = text_num + 1
                    an.click()
                    title = an.text
                    time.sleep(3)
                    # 获取当前浏览器所有的窗口
                    handles = self.browser.window_handles
                    # 窗口切换，切换为新打开的窗口
                    self.browser.switch_to.window(handles[-1])
                    # html = self.browser.find_element_by_class_name('ht_kb type-ht_kb status-publish format-standard hentry').text # 获取网页的html数据
                    # soup = BeautifulSoup(html, 'lxml')  # 对html进行解析，如果提示lxml未安装，直接pip install lxml即可
                    html = self.browser.page_source
                    soup = BeautifulSoup(html, 'lxml')
                    print(text_num)
                    # nef = open(str(text_num) + '.txt', 'w', encoding='utf8')
                    # nef.write(soup.text)
                    # nef.close()

                    self.conn = pymysql.connect(host='193.112.56.204', user='renrendata', passwd='data@2018',
                                                db='renren_data', port=3306, charset='utf8')
                    self.cur = self.conn.cursor()

                    self.cur.execute("insert into open_law (%s, %s, %s) values ('%s','%s','%s');" % (
                        'id', 'text', 'title', str(text_num), pymysql.escape_string(soup.text),pymysql.escape_string(title)))
                    self.conn.commit()
                    self.browser.close()
                    self.browser.switch_to_window(now_handle)
            except:
                print('没有下一页')










myCrawler = OpenLawCrawler()