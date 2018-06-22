# -*- coding=utf-8 -*-
# 
import sys
#获取数据用到的拓展
import requests 
from lxml import etree

from urllib.request import urlopen
from urllib.request import Request
import urllib.request
#写入文件用到的拓展
import csv
import codecs

class SetCsv:
    '''将百度爬取的数据写入csv'''

    def __init__(self, fileName):
        '''初始化文件'''
        self.filename = fileName + '.csv'
        self.csvfile = codecs.open(self.filename, 'w+', 'utf_8_sig')
        self.setfile = csv.writer(self.csvfile)

    def setParams(self,data):
        '''写入单行文件'''
        self.setfile.writerow(data)

    def closeFile(self):
        '''关闭文件流'''
        self.csvfile.close()

class GetBaidu:
    """docstring for GetBaidu"""
    def __init__(self, serUrl): 
        self.serUrl = serUrl

    def setResult(self):
        """开始请求并将结果写入入文件"""
        r = requests.get(self.serUrl,headers=httpHeaders,timeout=httpTimeout)
        if r.status_code != 200:
            file.setParams(("本次请求的状态是",r.status_code))           
        html = etree.HTML(r.text)
        retList = html.xpath('//body/div/div/div/div/div/h3/a')

        for a in retList:
        

            url = a.xpath('string(@href)').strip()
            # url = requests.get(url,headers=httpHeaders,timeout=httpTimeout).url
            # 
            req = Request(url)
            # 模拟一个浏览器访问百度, 不然不会重写到 https.
            req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64; rv:47.0) Gecko/20100101 Firefox/47.0')
            res = opener.open(req).getheaders()
            realUrl = res[4][1]
            isStatic = realUrl in '?'
            # 
            # 
            # 
            # 
            title = a.xpath('string(.)').strip()
            file.setParams((title,url,realUrl,isStatic))
  
class MyRedirectHandler(urllib.request.HTTPRedirectHandler):
    '''定义一个自己的头类, 继承HTTPRedirectHandler'''
    def http_error_302(self, req, fp, code, msg, hdrs):
        '''重写 http_error_302, 直接返回 fp(reponse)'''
        return fp

#程序运行配置
httpHeaders = { 'Accept': '*/*','Connection': 'keep-alive', 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36'}
httpTimeout = 5

#开始百度的搜索
reqQuestion = input("Search:") 
reqUrl =  'http://www.baidu.com/s?ie=utf-8&wd=' + reqQuestion
nowPage = 0 #百度页面规则页面搜索条件
resPage = 100;

file = SetCsv(reqQuestion)
file.setParams(("本次请求的url ",reqUrl))

myHandler = MyRedirectHandler()
opener = urllib.request.build_opener(myHandler)
while nowPage < resPage:
    GetBaidu(reqUrl).setResult()
    sys.stdout.write('正在获取数据中 {0}/{1} 如果想停止，请按键 Ctrl + C \r'.format(nowPage , resPage))
    sys.stdout.flush()
    nowPage += 10

file.closeFile()
sys.stdout.write('获取数据 {0}/{1} 完成 \r'.format(resPage , resPage))
sys.stdout.flush()

