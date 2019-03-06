#!/usr/bin/python
# -*- coding:utf8 -*-

import  urllib.request
from bs4 import BeautifulSoup
import re
from urllib import parse
nameList=[]
Names=[]

def namePaChong():

    with open('import_工作分析.txt','r',encoding='utf-8') as f:
        for line in f:
            temp = line.strip().split(' ')
            name = temp[0]
            tag = temp[2]
            if(tag=='zhong'):
                ###首先只能先判断这个词是不是多义词，进去多义词判别url
                multi_name_url = findLink(name)

                ###去爬取每个多义词的页面，并形成三元组形式
                for url in multi_name_url:
                    findMuLv(url, name)

                break

def findLink(name):

    hanzi = urllib.parse.quote(name)
    url = r'https://baike.baidu.com/item/' + hanzi+'?force=1'
    print('多义词'+name+'页面url:',url)

    res = urllib.request.urlopen(url)
    html = res.read().decode('utf-8')

    # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    text=soup.find_all(href=re.compile("/item/%"))
    mutil_name_urls = []
    count = 0
    for t in text:
        count = count + 1
        string=str(t)
        beg=string.find('href="')
        end=string.find('" target=')
        print(str(count)+' '+name+' '+string[beg+6:end])
        new_url = 'https://baike.baidu.com'+string[beg+6:end]
        mutil_name_urls.append(new_url)

    return mutil_name_urls



def findMuLv(url,name):

    print('爬取该url页面信息:',url)
    res = urllib.request.urlopen(url)
    html = res.read().decode('utf-8')
    # 将获取到的内容转换成BeautifulSoup格式，并将html.parser作为解析器
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)

    title = soup.find(class_='lemmaWgt-lemmaTitle-title').text.strip()
    tit = title.split('\n')
    print('原始名:',name)
    print('页面名:',tit[:-2])

    all_div_my_tag = []
    er_ji_title_count = 0
    body = soup.find(class_='main-content')
    all_div = body.find_all('div')

    for pos, div in enumerate(all_div):
        t = div.get('class')
        # print(t)
        if(t is not None):
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
                if(my_tag[1] == er_ji_title_name):
                    ##找到当前二级标题
                    content_beg = my_tag[0]+1
                    er_ji_count = my_tag[2]
                    er_ji_flag = True

                if(er_ji_flag and my_tag[2]==er_ji_count+1):
                    ##找到下一个二级标题
                    content_end = my_tag[0]

                if(er_ji_flag and content_end!=-1):
                    break

            if(content_end==-1):
                content_end = len(all_div_my_tag)

            my_content = ''
            for i in range(content_beg,content_end):
                my_div = all_div_my_tag[i][1]
                my_content = my_content + my_div.text

            print('关键词:\n'+name+'\n')
            print('标题:\n'+er_ji_title_name+'\n')
            print('内容:\n'+my_content.strip()+'\n')

    except:
        print('该页面没有找到二级标签')





if __name__=='__main__':
    namePaChong()



