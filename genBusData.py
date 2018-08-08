# -*- coding: utf-8 -*-
# author:ozzy
# 将抓取的公交线路解析，存储为geohson格式
import numpy as np
import json
from functools import reduce
from coordTransform import *
import re


def extendList(list1,list2):
	list1.extend(list2)
	return list1

def parseLine(line_data):
	'''
	解析传入的公交线路json文件
	生成描述公交线路走向的线geojson文件
	'''
	#统计公交线路走向
	line_xset=line_data['xs'].split(',')
	line_yset=line_data['ys'].split(',')
	line_coord_gd=np.array([line_xset,line_yset],dtype=np.float).T
	#转为84坐标
	line_coord_84=list(map(lambda x: list(gcj02_to_wgs84(x[0],x[1])),line_coord_gd))
	#解析线路属性
	properties={}
	property_keys=["id",
		"key_name",
		"name",
		"company",
		"length",
		"interval",
		"front_name",
		"front_spell",
		"terminal_name",
		"terminal_spell",
		"start_time",
		"end_time",
		"air",
		"areacode",
		"auto",
		"basic_price",
		"ic_card",
		"is_realtime",
		"status",
		"total_price"]
	for key in property_keys:
		if line_data[key]=='':
			properties[key]='null'
		else:
			properties[key]=line_data[key]
	
	line_feature={
		"type":"Feature",
		"geometry":{"type":"LineString","coordinates":line_coord_84},
		"properties":properties
			}
	return line_feature
	
def parseStation(line_data):
	'''
	解析传入的公交线路json文件
	描述公交站点的点geojson文件
	'''
	def genStationFeatureList(line_id,line_name,station_data):
		coord_gd=np.array(station_data['xy_coords'].split(';'),dtype=np.float)
		coord_84=list(gcj02_to_wgs84(coord_gd[0],coord_gd[1]))
		properties={}
		properties['line_id']=line_id
		properties['line_name']=line_name
		properties['station_id']=station_data['station_id']
		properties['name']=station_data['name']
		properties['sequence']=station_data['station_num']
		station_feature={
			"type":"Feature",
			"geometry":{"type":"Point","coordinates":coord_84},
			"properties":properties}
		return station_feature
		
	station_list=line_data['stations']
	line_id=line_data['id']
	line_name=line_data['name']
	station_features=list(map(lambda x:genStationFeatureList(line_id,line_name,x),station_list))
	return station_features


if __name__=='__main__':
	
	#for i in range(0,21):
	#filename='raw_json_'+str(i)+'.txt'
	data=[]
	filename='raw_json.txt'
	with open(filename,'r') as f:
		for line in f:
			data.append(json.loads(line))
			
	#加载公交线路数据 提取线路名			
	busline_lists=[]
	for i in range(len(data)):
		try:
			busline_lists.append(data[i]['data']['busline_list'])
		except:
			pass
	busline_data=reduce(lambda x,y:extendList(x,y),busline_lists)
	
	line_features=list(map(lambda x: parseLine(x),busline_data))
	station_feature_list=map(lambda x:parseStation(x),busline_data)
	station_features=reduce(lambda x,y:extendList(x,y),station_feature_list)
	
	line_json={"type": "FeatureCollection",
		"features": line_features}
	station_json={"type": "FeatureCollection",
		"features": station_features}
	
	#存储
	with open('line_json.json','w') as f:
		json.dump(line_json,f)
	with open('station_json.json','w') as f:
		json.dump(station_json,f)
	
	
	
	