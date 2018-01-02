#coding:gbk
'''
Created on 2016-9-8

@author: 刘丁屹
'''
import urllib2
from bs4 import BeautifulSoup
import socket
import httplib
import re
import urllib
import urllib2
import cookielib
import os
urls = []
def mkdir(path):
 
    path=path.strip()
   
    path=path.rstrip("\\")

    if not os.path.exists(path):
        os.makedirs(path)
        
    return path
def save_file(path, file_name, data):
    if data == None:
        return
    
    mkdir(path)
    if(not path.endswith("/")):
        path=path+"/"
    file=open(path+file_name, "wb")
    file.write(data)
    file.flush()
    file.close()
class PersonSpider(object):
    
    def __init__(self, url):
        self.url = url

    
    def getUrls(self):
        
      # postdata = urllib.urlencode({
           # 'IPT_LOGINUSERNAME':'1101030088',
            #'IPT_LOGINPASSWORD':'1234411231'
       # })
        #filename = 'cookie.txt'
        #cookie = cookielib.MozillaCookieJar(filename)
        #opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookie))
        request = urllib2.Request(self.url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; \
            WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
        try:
             page = urllib2.urlopen(request)
             html = page.read()
            
             #loginUrl = 'http://es.bnuz.edu.cn'
             #result = opener.open(loginUrl,postdata)
        except socket.timeout, e:
            pass
        except urllib2.URLError,ee:
            pass
        except httplib.BadStatusLine:
            pass
        
#print html
        pattern = re.findall(r"thumbURL\":\".*?\"",html)
        #print pattern
#s = "\u80af\u5b9a\u662f\u7f8e\u554a.\u4e00\u8d2f\u7684\u4f5c"
        for i in range(len(pattern)):
            url = pattern[i]
            url = url.replace("thumbURL\":","")
            url = url.replace("\"","")
            urls.append(url)
        #print titles[0]
        #print html
       
        return urls

    def getPic(self,urls,name):
        hdr = {
               'Referer':'http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word=%E8%94%A1%E4%BE%9D%E6%9E%97&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word=%E8%94%A1%E4%BE%9D%E6%9E%97&pn=30&rn=30&gsm=1e&1473341493765=',
               'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
               'Host':'img5.imgtn.bdimg.com',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip', 'deflate'
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Request-Line':'GET /it/u=1667366492,1668761829&fm=11&gp=0.jpg HTTP/1.1'
        }
        x = 0
        for site in urls:
            
            #site = "http://img5.imgtn.bdimg.com/it/u=1667366492,1668761829&fm=11&gp=0.jpg"
            #print x
            #print site
            #urllib.urlretrieve(request,'%s.jpg' % x)
            req = urllib2.Request(site,headers=hdr)
       
            page = urllib2.urlopen(req)
            data = page.read()
        #print data
            save_file("D:/tomcat/GetNews/bs/pic", name + str(x) + ".jpg", data)
            x = x + 1
            print('Pic Saved!')   
name = raw_input("请输入要查找的人: ")

#print name
url = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word=" + name.encode("utf-8") + "&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word=" + name.encode("utf-8") + "&pn=30&rn=30&gsm=1e&"
#url = "http://image.baidu.com/search/acjson?tn=resultjson_com&ipn=rj&ct=201326592&is=&fp=result&queryWord+=&cl=2&lm=-1&ie=utf-8&oe=utf-8&adpicid=&st=-1&word=%E8%94%A1%E4%BE%9D%E6%9E%97&z=&ic=0&s=&se=&tab=&width=&height=&face=0&istype=2&qc=&nc=1&fr=&step_word=%E8%94%A1%E4%BE%9D%E6%9E%97&pn=60&rn=30&gsm=1e&1473325483995="
    #print url
#print url
s = PersonSpider(url)
    #print s.getNextUrls()
#urls = set(all_url)
urls = s.getUrls()
s.getPic(urls,name)
print "---------------------------"

