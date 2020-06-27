'''
@Desc:经纬度曼哈顿距离计算测试
@Author: huangzhiyuan
@Time: 2020/6/27 11:35 上午
@Modify Notes:
lng,lat
1770上车：118.13459,24.691331
1770下车：118.135816,24.69129
1770 GPS：118.13556,24.68833
下车坐标与GPS轨迹差大约256m
上车坐标与GPS轨迹差大约97m
经纬度之间的曼哈顿距离计算：https://stackoverrun.com/cn/q/9071019
haversine公式用于计算两个经纬度点间跨越地球表面的最短距离
This uses the ‘haversine’ formula to calculate the great-circle distance between two points –
that is, the shortest distance over the earth’s surface –
 giving an ‘as-the-crow-flies’ distance between the points
 http://www.movable-type.co.uk/scripts/latlong.html
'''

import pandas as pd
import numpy as np
from coord_convert.transform import wgs2gcj

if __name__ == '__main__':
    ##########经纬度距离计算测试--单位：米################
    R = 6371000
    x1 = 118.13459
    y1 = 24.691331
    x2 = 118.135816
    y2 = 24.69129
    delta_lat = np.abs(y2-y1) * np.pi / 180
    delta_lng = np.abs(x2-x1) * np.pi / 180
    a_lat = np.sin(delta_lat) ** 2
    c_lat = 2 * np.arctan2(np.sqrt(a_lat),np.sqrt(1-a_lat))
    lat_dist = R * c_lat
    a_lng = np.sin(delta_lng) ** 2
    c_lng = 2 * np.arctan2(np.sqrt(a_lng),np.sqrt(1-a_lng))
    lng_dist = R * c_lng
    d = np.abs(lat_dist) + np.abs(lng_dist)
    print(d)
    ###########以下代码验证经纬度间距离是否与坐标系有关#--单位：米#########
    x1,y1 = wgs2gcj(118.13459,24.691331)
    x2,y2 = wgs2gcj(118.135816,24.69129)
    delta_lat = np.abs(y2 - y1) * np.pi / 180
    delta_lng = np.abs(x2 - x1) * np.pi / 180
    a_lat = np.sin(delta_lat) ** 2
    c_lat = 2 * np.arctan2(np.sqrt(a_lat), np.sqrt(1 - a_lat))
    lat_dist = R * c_lat
    a_lng = np.sin(delta_lng) ** 2
    c_lng = 2 * np.arctan2(np.sqrt(a_lng), np.sqrt(1 - a_lng))
    lng_dist = R * c_lng
    d = np.abs(lat_dist) + np.abs(lng_dist)
    print(d)

