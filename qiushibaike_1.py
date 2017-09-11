# -*- coding: utf-8 -*-


import re
import requests
import time
import os
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



UPDATE_NUM = 0  # 全局变量，保存当前已爬取的文档数
DIRS = ''       # 全局变量，存储文件写入的路径


# 创建文件夹，用以存放爬取的文档
def makeDir():
    global DIRS
    nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))  #获取时间，作为此次爬取的文件夹的名字
    path = 'F:/MachineLearning/pachong/demo_qiushibaike/'    #程序的地址
    DIRS = path + nowtime + '/'                              #合成文件的完整路径
    os.makedirs(DIRS) 

# 爬取整个网页内容        
def getHtml(pageIndex):
    try:
        url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex) 
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent': user_agent}
        rs = requests.get(url, headers = header)
        
        rs.raise_for_status()
        rs.encoding = rs.apparent_encoding
        r = rs.text
        return r
    except:
        return '爬出代码出现异常'

# 将爬取的内容写入TXT中
def write2txt(txtNum, ID, story, num_good, num_comment):  
    global DIRS              
    f = open(DIRS + str(txtNum) + '.txt', 'a') 
    f.write('用户ID:' + ID.get_text().strip() + '\n')
    f.write('正文：' + story.get_text().strip() + '\n')
    f.write('点赞数：' + num_good.get_text() + '\n')
    f.write('评论数：' + num_comment.get_text())    
    f.close()

# 获取所需要的内容        
def getDocument(pageIndex, num):
    global UPDATE_NUM    
    html = getHtml(pageIndex)
    if not html:
        print '爬出代码出现异常'
        
    soup = BeautifulSoup(html, "html.parser")
    preText = soup.find_all('div', class_ = re.compile('article block untagged'))
    # 解析获取包含所需文档那部分
    
    txtNum = num
    for item in preText:
        haveImg = item.find_all('div', class_ = re.compile('thumb')) #判断是否是图片形式
        if haveImg:  #如果有图片就跳过去
            continue
        else:
            ID = item.find('h2')       #获取用户ID      
            story = item.find('span')  #获取正文
            stats = item.find_all('i', class_ = re.compile("number"))
            num_good = stats[0]        #获取点赞数
            num_comment = stats[1]     #获取评论数
            txtNum = txtNum + 1
            write2txt(txtNum, ID, story, num_good, num_comment)
    UPDATE_NUM = txtNum

def getResult(pageIndex):
    makeDir()
    for i in range(pageIndex):
        global UPDATE_NUM
        getDocument(pageIndex, UPDATE_NUM) 


if __name__ == "__main__":
    page = input("how many pages you want: ")
    getResult(page)
     
        









