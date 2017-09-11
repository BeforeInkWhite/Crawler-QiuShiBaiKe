# -*- coding: utf-8 -*-

import re
import urllib2
import time
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



UPDATE_NUM = 0
DIRS = ''

def makeDir():
    global DIRS
    nowtime = time.strftime('%Y%m%d%H%M%S',time.localtime(time.time()))
    path = 'F:/MachineLearning/pachong/demo_qiushibaike/'
    DIRS = path + nowtime + '/'
    os.makedirs(DIRS) 
        
def getHtml(pageIndex):
    try:
        url = 'https://www.qiushibaike.com/hot/page/' + str(pageIndex)
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        header = {'User-Agent': user_agent}
        request = urllib2.Request(url, headers = header)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        return content
    except urllib2.URLError, e:
        if hasattr(e, "reason"):
            print u'连接网页失败，错误原因：',e.reason
            return None
                
def write2txt(txtNum, ID, story, num_good, num_comment):  
    global DIRS              
    f = open(DIRS + str(txtNum) + '.txt', 'a')
    f.write('用户ID:' + ID + '\n')
    f.write('正文：' + story + '\n')
    f.write('点赞数：' + num_good + '\n')
    f.write('评论数：' + num_comment)    
    f.close()

        
def getDocument(pageIndex, num):
    global UPDATE_NUM    
    content = getHtml(pageIndex)
    if not content:
        print '爬出网页出现异常'
    
    pattern =  re.compile('<div.*?author clearfix">.*?<h2>(.*?)</h2>.*?<div.*?content">.*?<span>' + \
                       '(.*?)</span>(.*?)<i.*?number">(.*?)</i>.*?<i.*?number">(.*?)</i>',re.S)
    # (.*?)中即为需要抓取的内容，其中第三个是为了判断是否包含图片而提取的
    preText = re.findall(pattern, content)
            
    txtNum = num
    for item in preText:
        haveImg = re.search('thumb',item[2])
        if haveImg:
            continue
        else:
            ID = item[0].strip()       
            story = item[1].strip()
            num_good = item[3]
            num_comment = item[4]
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
     
        









