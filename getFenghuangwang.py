#coding:utf-8
'''
Created on 2016-9-5

@author: 刘帅
'''
import urllib2
from bs4 import BeautifulSoup
import socket
import httplib
import re

all_url = []
titles = []
contents = []
all_public_time = []
class FenHuangSpider(object):
    
    def __init__(self, url):
        self.url = url

    def getNextUrl(self):
        urls = []
        request = urllib2.Request(self.url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; \
            WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
        try:
            page = urllib2.urlopen(url)
            html = page.read()
        except socket.timeout, e:
            pass
        except urllib2.URLError,ee:
            pass
        except httplib.BadStatusLine:
            pass
        
        
        #print soup
        #print html
        datalist = re.findall(r"dataList.*?;",html)
        #titles = re.findall(r"title.*?,",datalist)
        
        datalist = datalist[0]
        
        u = re.findall(r"url.*?shtml",datalist)
        for i in u:
            i = re.findall("http:.*?shtml",i)
            urls.append(i[0])
        #print urls[0]
        
        return urls
    
    def getcommenturl(self):
        url = self.url
        t = re.findall(r"\d.*?.shtml",url)[0]
        s = t.split('/')
        #print s[0]
        #print s[1]
        curl = "http://comment.ifeng.com/get.php?callback=hotCommentListCallBack&orderby=uptimes&docUrl=http%3A%2F%2Fnews.ifeng.com%2Fa%2F" + s[0] + "%2F" + s[1] + "&format=js&job=1&p=1&pageSize=10&callback=hotCommentListCallBack"
        #print curl
        return curl
    
    def getDianZanUrl(self):
        url = self.url
        t = re.findall(r"\d.*?.shtml",url)[0]
        s = t.split('/')
        zurl = "http://survey.news.ifeng.com/getaccumulator_ext.php?callback=success_zan_0&format=js&key%5B%5D=http%3A%2F%2Fnews.ifeng.com%2Fa%2F" + s[0] + "%2F" + s[1] + "%3Fsmile&key%5B%5D=http%3A%2F%2Fnews.ifeng.com%2Fa%2F" + s[0] + "%2F" + s[1] + "%3Fcry&key%5B%5D=http%3A%2F%2Fnews.ifeng.com%2Fa%2F" + s[1]+ "%2F" + s[1]+ "%3Fshock&key%5B%5D=http%3A%2F%2Fnews.ifeng.com%2Fa%2F" + s[0] + "%2F" + s[1] + "%3Fboring&key%5B%5D=http%3A%2F%2Fnews.ifeng.com%2Fa%2F" + s[0] + "%2F"+ s[1] + "%3Fangry"
        return zurl
    
    def getDianZan(self):
        request = urllib2.Request(self.url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; \
            WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
        try:
            page = urllib2.urlopen(request)
            html = page.read()
        except socket.timeout, e:
            pass
        except urllib2.URLError,ee:
            pass
        except httplib.BadStatusLine:
            pass
        pattern = re.findall(r"smile.*?,",html)
        smile = pattern[0].split(':')
        smile = smile[1]
        pattern2 = re.findall(r"cry.*?,",html)
        cry = pattern2[0].split(':')
        cry = cry[1]
        pattern3 = re.findall(r"shock.*?,",html)
        shock = pattern3[0].split(':')
        shock = shock[1]
        pattern4 = re.findall(r"boring.*?,",html)
        boring = pattern4[0].split(':')
        boring =  boring[1]
        pattern5 = re.findall(r"angry.*?}",html)
        angry = pattern5[0].split(':')
        angry = angry[1].replace("}","")
        return smile,cry,shock,boring,angry 
    
    def getComment(self):
        request = urllib2.Request(self.url)
        request.add_header('User-Agent','Mozilla/5.0 (Windows NT 6.1; \
            WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36')
        try:
            page = urllib2.urlopen(request)
            html = page.read()
        except socket.timeout, e:
            pass
        except urllib2.URLError,ee:
            pass
        except httplib.BadStatusLine:
            pass
        
        pattern = re.findall(r"\"count.*?,",html)
        count = pattern[0].split(':')
        count = count[1]
        pattern2 = re.findall(r"\"join_count.*?,",html)
        join_count = pattern2[0].split(':')
        join_count = join_count[1]
        comment = re.findall(r"comment_contents\":\".*?\"",html)
        return comment,count,join_count
   
    

url = 'http://news.ifeng.com'
    #print url
s = FenHuangSpider(url)
    #print s.getNextUrls()
all_url.extend(s.getNextUrl())
#urls = set(all_url)


for ur in all_url:
    s.url = ur
    print "---------------------------"
    print ur
    curl = s.getcommenturl()
    s.url = curl
    #print curl
    comment,count,join_count = s.getComment()
    print "评论数:" + count + "参与数:" + join_count 
    if len(comment) != 0:
        for c in comment:
            c = c.replace("'","")
            print eval(r"u'%s'" %(c))
    s.url = ur
    zurl = s.getDianZanUrl()
    s.url = zurl
    #print zurl
    smile,cry,shock,boring,angry  = s.getDianZan()
    #if len(smile) | len(cry) | len(shock) | len(boring) | len(angry) != 0:
    print "笑抽数:"  + smile + "泪崩数:" + cry + "惊呆数:" + shock + "无聊数:" + boring +"气炸数:" + angry 
