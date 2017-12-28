#coding:utf-8
import configparser
import pymysql
import requests
from bs4 import BeautifulSoup
import os
import re
import codecs
import textwrap
import time
import PIL
import pytesseract
import pytesser3


headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
}
url='http://data.cma.cn'
result=0
count=1
while result!='({\"status\":100,\"trueName\":\"\\u5218\\u6653\\u78ca\"})'#改为你自己的用户名:
	session=requests.session()
	print("666")
	print(u"\u5218\u6653\u78ca")
	HomePage_req=session.get(url)
	g_cookie=HomePage_req.headers['set-cookie']
	print(g_cookie)
	HomePage_html=HomePage_req.text
	HomePage_soup=BeautifulSoup(HomePage_html, 'html.parser')
	checkcodeurl = url+HomePage_soup.find('img', {'id':'yw0'})['src']
	checkcode = session.get(url=checkcodeurl, headers=headers).content
	with open('./check.png', 'wb') as f:
		f.write(checkcode)
		f.close()
	image=PIL.Image.open('./check.png')
	image.show()
	imgry = image.convert('L')
	code = pytesser3.image_to_string(imgry).strip()
	print(count)
	print(code)
	params={
	'userName':'**********',
	'password':'**********',
	'verifyCode':code
	}
	response = session.get('https://data.cma.cn/user/Login.html', params=params)
	result = response.text
	print(u"登录消息为："+result)
	print("*"*100)
	count=count+1
#print(response.headers)
cookies=response.headers['set-cookie']
#print(cookies)
headers={
'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.101 Safari/537.36',
'Content-Type':'application/x-www-form-urlencoded',
'Cookie':g_cookie+cookies
}

SelectPage_req=session.get('http://data.cma.cn/dataService/cdcindex/datacode/A.0012.0001/show_value/normal.html',headers=headers )
SelectPage_html=SelectPage_req.text
print(SelectPage_html)
SelectPage_soup=BeautifulSoup(SelectPage_html, 'html.parser')
SelectPage_soup=str(SelectPage_soup)#str
'''with codecs.open('./tmp.html' ,'wb','utf-8') as f:
	f.write(SelectPage_soup)
	f.close()'''
City=re.compile(r'<dd\s*alt\=\"[\u4e00-\u9fa5]+\"\s*data\="(\d+)">')
CityIds=City.findall(SelectPage_soup)
CityIds.pop()
CityIds.pop()
CityIds.pop()
CityIds.pop()
print(CityIds)#CityIds中没有北京的站点
#北京的站点
StationBJ=re.compile('<label>\[(\d+)\][\u4e00-\u9fa5]+<\/label>')
StationBJId=StationBJ.findall(SelectPage_soup)
StationList=StationBJId
#请求获取所有站点的代号
for CityId in CityIds:
	FormData1={
	'act':'getStationsByProvinceID',
	'provinceID':CityId,
	'dataCode':'A.0012.0001'
	}
	Ajax_req=session.post(url='http://data.cma.cn/dataService/ajax.html',data=FormData1,headers=headers)
	#print(type(Ajax_req.text))#str
	Station=re.compile('\"StationID\"\:\s*\"(\d+)\"')
	StationId=Station.findall(Ajax_req.text)
	#print(StationId)
	StationList=StationList+StationId
#print(StationList)
#请求某一站点最终数据的静态页面
dateE=time.strftime("%Y-%m-%d %H",time.localtime(time.time()))
dateS=time.strftime("%Y-%m-%d %H",time.localtime(time.time()-68400.0))
for station in StationList:
	print('station:'+station+' start')
	FormData2={
	'dateS':dateS,
	'dateE':dateE,
	'hidden_limit_timeRange':'7',
	'hidden_limit_timeRangeUnit':'Day',
	'isRequiredHidden[]':['dateS','dateE'],
	'chooseType':'Station',
	'isRequiredHidden[]':'station_ids[]',
	'station_ids[]':station,
	'station_maps':'',
	'select':'on',
	'elements[]':['PRS','PRS_Sea','PRS_Max','PRS_Min','WIN_S_Max','WIN_S_Inst_Max','WIN_D_INST_Max','WIN_D_Avg_10mi','WIN_S_Avg_10mi','WIN_D_S_Max','TEM','TEM_Max','TEM_Min','RHU','VAP','RHU_Min','PRE_1h','windpower','tigan'],
	'isRequiredHidden[]':'elements[]',
	'dataCode':'A.0012.0001',
	'dataCodeInit':'A.0012.0001',
	'show_value':'normal'
	}
	FinalPage_req=session.post(url='http://data.cma.cn/data/search.html?dataCode=A.0012.0001',data=FormData2,headers=headers)
	FinalPage_html=FinalPage_req.text
	FinalPage_soup=BeautifulSoup(FinalPage_html, 'html.parser')
	FinalPage_soup=str(FinalPage_soup)
	with codecs.open('./tmp.html' ,'wb','utf-8') as f:
		f.write(FinalPage_soup)
		f.close()
	station_weather_pattern=re.compile('<tr>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*<td>\s*([^\s*]+)\s*<\/td>\s*')
	station_weather_info=station_weather_pattern.findall(FinalPage_soup)
	#print(station_weather_info)
	if len(station_weather_info)==0:
		print('the weatherInfo of station:'+station+' from '+dateS+' to '+dateE+' is not released,please wait for its releasion')
		continue
	SqlList = []
	SqlList.append(textwrap.dedent('''replace into DaFu.WeatherInfo(SerialNumber,StationID,Year,Month,Day,Hour,PRS,PRS_Sea,PRS_Max,PRS_Min,WIN_S_Max,WIN_S_Inst_Max,WIN_D_INST_Max,WIN_D_Avg_10mi,WIN_S_Avg_10mi,WIN_D_S_Max,TEM,TEM_Max,TEM_Min,RHU,VAP,RHU_Min,PRE_1h,windpower,tigan) values\n'''))
	for num in range(0,len(station_weather_info)):
		SqlList.append(textwrap.dedent('''({0},{1},{2},{3},{4}
		,{5},{6},{7},{8},{9}
		,{10},{11},{12},{13},{14}
		,{15},{16},{17},{18},{19}
		,{20},{21},{22},{23},{24}
		)''').format(
		"'{0}'".format(station_weather_info[num][0])
		,"'{0}'".format(station_weather_info[num][1])
		,"'{0}'".format(station_weather_info[num][2])
		,"'{0}'".format(station_weather_info[num][3])
		,"'{0}'".format(station_weather_info[num][4])
		,"'{0}'".format(station_weather_info[num][5])
		,"'{0}'".format(station_weather_info[num][6])
		,"'{0}'".format(station_weather_info[num][7])
		,"'{0}'".format(station_weather_info[num][8])
		,"'{0}'".format(station_weather_info[num][9])
		,"'{0}'".format(station_weather_info[num][10])
		,"'{0}'".format(station_weather_info[num][11])
		,"'{0}'".format(station_weather_info[num][12])
		,"'{0}'".format(station_weather_info[num][13])
		,"'{0}'".format(station_weather_info[num][14])
		,"'{0}'".format(station_weather_info[num][15])
		,"'{0}'".format(station_weather_info[num][16])
		,"'{0}'".format(station_weather_info[num][17])
		,"'{0}'".format(station_weather_info[num][18])
		,"'{0}'".format(station_weather_info[num][19])
		,"'{0}'".format(station_weather_info[num][20])
		,"'{0}'".format(station_weather_info[num][21])
		,"'{0}'".format(station_weather_info[num][22])
		,"'{0}'".format(station_weather_info[num][23])
		,"'{0}'".format(station_weather_info[num][24])
		))
		SqlList.append(',')
	SqlList.pop(len(SqlList)-1)
	if len(SqlList) > 1 :
		with codecs.open('./out.sql' ,'a+','utf-8') as f:
			f.write(''.join(SqlList))
			f.close()
	Cur =Conn.cursor()
	Cur.execute(''.join(SqlList))
	Conn.commit()
	Cur.close()
	del SqlList
	print('the weatherInfo of station:'+station+' from '+dateS+' to '+dateE+' has been inserted into database')

