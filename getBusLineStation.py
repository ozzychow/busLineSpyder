# -*- coding: utf-8 -*-
# author:ozzy
# 利用高德API,获取公交线路走向,站点坐标数据


import pandas as pd
import numpy as np
import requests
import time
import json
from coordTransform import *
import random


def getWebJson(url,print_json=False,save_json=True):
	head_user_agent=[
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Maxthon/4.0.6.2000 Chrome/26.0.1410.43 Safari/537.1 ',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.92 Safari/537.1 LBBROWSER',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36',
		'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.11 TaoBrowser/3.0 Safari/536.11',
		'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko',
		'Mozilla/5.0 (Macintosh; PPC Mac OS X; U; en) Opera 8.0',
		'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063']
	headers={'User-Agent': head_user_agent[random.randrange(0, len(head_user_agent))]}
	s=requests.session()
	json_obj=s.get(url,headers=headers)
	json_data=json_obj.json()
	if print_json==True:
		print(json_data)
	if json_data['status']!='1':
		return json_data
	#以txt形式存储json原始数据
	if save_json==True:
		with open('raw_json.txt','a') as f:
			json.dump(json_data,f)
			f.write('\n')
			print('json file saved')
		'''读取
		data=[]
		with open('raw_json.txt') as f:
			for line in f:
				data.append(json.loads(line))
			
		'''
	return json_data


def main(linefile,city_code):
	bus_line=pd.read_excel(linefile,sheet_name='Sheet1')
	basic_url='https://ditu.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=1000&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=12&city='+city_code+'&'+'keywords='
	missing_line_list=[]

	for bus in bus_line['Line']:
		url=basic_url+str(bus)
		json_data=getWebJson(url)
		#随机休眠
		time.sleep(3*np.random.rand(1))
		#解析数据
		if json_data['status']!='1':
			print(json_data)
			print(bus)
			break
		
	
if __name__=='__main__':
	linefile='Linename.xlsx'
	city_code='029'
	main(linefile,city_code,parse_data=False)