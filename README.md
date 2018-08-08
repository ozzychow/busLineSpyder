# busLineSpyder
高德公交API爬虫

从高德公交API获取公交数据，包括线路走向和站点信息，生成geojson文件或shp文件。

环境：
python3.6，requests，pandas

使用方法：
1.将需要获取的公交线路名放在Linename.xlsx中，并在getBusLineStation.py中填写目标城市编码，运行getBusLineStation.py，得到返回的原始数据,被存储在raw_json.txt 
2.运行genBusData.py，生成记录公交线路的line_json.json和记录公交站点的station_json.json，这两个geojson文件可以直接在qgis中打开 
3.运行genShp，可以将两个json文件生成对应的shp文件

存在问题：
使用同一个ip连续抓取比较多的线路（差不多50条的样子），会被封，暂时的解决方法是换一个ip或者等24小时。

