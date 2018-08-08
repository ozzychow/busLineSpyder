# -*- coding: utf-8 -*-
# author:ozzy
# 读取geojson格式数据，生成shp文件

import json
import gdal
import osr
import ogr


def createPoint(point_json,shp_name,field):
	'''
	生成点shp文件
	输入：
	point_json:描述点的geojson文件
	name:要生成的shp文件名
	field:shp文件中的字段名及数据类型 {字段1:类型1，字段2:类型2,字段3:类型3}

	常见数据类型：ogr.OFTString ogr.OFTReal ogr.OFTInteger
	'''
	# 设置shapefile驱动
	gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
	gdal.SetConfigOption("SHAPE_ENCODING", "gbk")
	driver = ogr.GetDriverByName("ESRI Shapefile")

	# 创建数据源
	data_source = driver.CreateDataSource(shp_name)

	# 创建空间参考，WGS84
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)

	# 创建图层
	layer = data_source.CreateLayer("point", srs,ogr.wkbPoint) # 带坐标系文件
	# 设置字段
	for field_name,field_type in field.items():
		if len(field_name)>10:
			fn=ogr.FieldDefn(field_name[0:10],field_type)
		else:
			fn=ogr.FieldDefn(field_name,field_type)
		#数据类型为str时，设置字段长度
		if field_type==ogr.OFTString:
			fn.SetWidth(128)
		layer.CreateField(fn)

	for point in point_json['features']:
		# 创建特征
		feature = ogr.Feature(layer.GetLayerDefn())
		# 和设置字段内容进行关联  ,从数据源中写入数据
		for field_name,_ in field.items():
			if len(field_name)>10:
				feature.SetField(field_name[0:10],point['properties'][field_name])
			else:
				feature.SetField(field_name,point['properties'][field_name])
			
		# 生成点坐标
		point_geo = ogr.CreateGeometryFromJson(str(point['geometry']))
		feature.SetGeometry(point_geo)
		# 添加点
		layer.CreateFeature(feature)
		# 关闭 特征
		feature = None
	# 关闭数据
	data_source = None

def createLine(line_json,shp_name,field):
	'''
	生成线shp文件
	输入：
	line_json:描述线的geojson文件
	name:要生成的shp文件名
	field:shp文件中的字段名及数据类型 {字段1:类型1，字段2:类型2,字段3:类型3}

	常见数据类型：ogr.OFTString ogr.OFTReal ogr.OFTInteger
	'''
	# 设置shapefile驱动
	gdal.SetConfigOption("GDAL_FILENAME_IS_UTF8", "YES")
	gdal.SetConfigOption("SHAPE_ENCODING", "gbk")
	driver = ogr.GetDriverByName("ESRI Shapefile")

	# 创建数据源
	data_source = driver.CreateDataSource(shp_name)

	# 创建空间参考，WGS84
	srs = osr.SpatialReference()
	srs.ImportFromEPSG(4326)

	# 创建图层
	layer = data_source.CreateLayer("line", srs,ogr.wkbLineString) # 带坐标系文件
	# 设置字段
	for field_name,field_type in field.items():
		if len(field_name)>10:
			fn=ogr.FieldDefn(field_name[0:10],field_type)
		else:
			fn=ogr.FieldDefn(field_name,field_type)
		#数据类型为str时，设置字段长度
		if field_type==ogr.OFTString:
			fn.SetWidth(128)
		layer.CreateField(fn)

	for line in line_json['features']:
		# 创建特征
		feature = ogr.Feature(layer.GetLayerDefn())
		# 和设置字段内容进行关联  ,从数据源中写入数据
		for field_name,_ in field.items():
			if len(field_name)>10:
				feature.SetField(field_name[0:10],line['properties'][field_name])
			else:
				feature.SetField(field_name,line['properties'][field_name])
		# 生成线坐标
		line_geo = ogr.CreateGeometryFromJson(str(line['geometry']))
		feature.SetGeometry(line_geo)
		# 添加点
		layer.CreateFeature(feature)
		# 关闭 特征
		feature = None
	# 关闭数据
	data_source = None
	
	

if __name__=='__main__':
	
	with open('line_json.json',encoding='utf-8') as f:
		line_json=json.load(f)
	with open('station_json.json',encoding='utf-8') as f:
		station_json=json.load(f)
	
	station_field={'line_id':ogr.OFTString, 'line_name': ogr.OFTString, 'station_id': ogr.OFTString, 'name': ogr.OFTString, 'sequence': ogr.OFTString}
	line_field={'id':ogr.OFTString,
		'key_name':ogr.OFTString,
		'name':ogr.OFTString,
		'company':ogr.OFTString,
		'length':ogr.OFTString,
		'interval':ogr.OFTString,
		'front_name':ogr.OFTString,
		'front_spell':ogr.OFTString,
		'terminal_name':ogr.OFTString,
		'terminal_spell':ogr.OFTString,
		'start_time':ogr.OFTString,
		'end_time':ogr.OFTString,
		'air':ogr.OFTString,
		'areacode':ogr.OFTString,
		'auto':ogr.OFTString,
		'basic_price':ogr.OFTString,
		'ic_card':ogr.OFTString,
		'is_realtime':ogr.OFTString,
		'status':ogr.OFTString,
		'total_price':ogr.OFTString}
	createLine(line_json,'line.shp',line_field)
	createPoint(station_json,'station.shp',station_field)
	
	
	