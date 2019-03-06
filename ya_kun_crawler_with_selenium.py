#-*- coding: UTF-8 -*-
from selenium import webdriver
import xlrd
import time
import xlwt
import urllib
from urllib import request
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

class Crawler():
    def __init__(self):
        self.url = 'https://baike.baidu.com/'
        self.txt = 'import_工作分析.txt'
        self.crawler()
        pass

    def crawler(self):
        with open(self.txt, 'r', encoding='utf-8') as f:
            for line in f:
                temp = line.strip().split(' ')
                name = temp[0]
                tag = temp[2]
                if (tag == 'zhong'):
                    ###在搜索框中搜索
                    self.browser = webdriver.Chrome()
                    self.browser.get(self.url)
                    self.browser.implicitly_wait(10)

                    ##向搜索框里输入问句
                    search_input_kuang = self.browser.find_element_by_id('query')
                    search_input_kuang.send_keys(name)

                    ##点击搜索
                    self.browser.find_element_by_id('search').click()
                    time.sleep(3)

                    text = self.browser.page_source
                    print(text)
                    self.browser.close()
                    self.handle_page(page=text, name=name)
                    break

    def handle_page(self, page, name):
        # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
        soup = BeautifulSoup(page, 'html.parser')
        # print(soup)

        title = soup.find(class_='lemmaWgt-lemmaTitle-title').text.strip()
        tit = title.split('\n')
        print('原始名:', name)
        print('页面名:', tit[:-2])

        all_div_my_tag = []
        er_ji_title_count = 0
        body = soup.find(class_='main-content')
        all_div = body.find_all('div')

        for pos, div in enumerate(all_div):
            t = div.get('class')
            # print(t)
            if (t is not None):
                if (t[0] == 'para-title' and t[1] == 'level-2'):
                    try:
                        er_ji_title_name = div.text.strip().split('\n')[0]
                        # print(er_ji_title_name)
                        er_ji_title_count = er_ji_title_count + 1
                        my_tag = [pos, er_ji_title_name, er_ji_title_count]
                        # print('ni ni ni ni :', er_ji_title_name)
                    except:
                        my_tag = [pos, div, -1]
                else:
                    my_tag = [pos, div, -1]
            else:
                my_tag = [pos, div, -1]

            all_div_my_tag.append(my_tag)

        try:
            er_ji_titles = soup.find_all(class_='para-title level-2')

            for er_ji in er_ji_titles:
                ###找到二级目录名称
                er_ji_title_name = er_ji.find(class_='title-text').text
                ###找到二级目录内容 开始位置 和 结束位置
                content_beg = -1
                content_end = -1
                er_ji_flag = False
                er_ji_count = -2
                for pos, my_tag in enumerate(all_div_my_tag):
                    if (my_tag[1] == er_ji_title_name):
                        ##找到当前二级标题
                        content_beg = my_tag[0] + 1
                        er_ji_count = my_tag[2]
                        er_ji_flag = True

                    if (er_ji_flag and my_tag[2] == er_ji_count + 1):
                        ##找到下一个二级标题
                        content_end = my_tag[0]

                    if (er_ji_flag and content_end != -1):
                        break

                if (content_end == -1):
                    content_end = len(all_div_my_tag)

                my_content = ''
                for i in range(content_beg, content_end):
                    my_div = all_div_my_tag[i][1]
                    my_content = my_content + my_div.text

                print('关键词:\n' + name + '\n')
                print('标题:\n' + er_ji_title_name + '\n')
                print('内容:\n' + my_content.strip() + '\n')

        except:
            print('该页面没有找到二级标签')


if __name__ == '__main__':
    Crawler()