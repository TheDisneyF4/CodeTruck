'''
@Desc:载客点匹配
@Author: huangzhiyuan
@Time: 2020/6/16 6:27 下午
@Modify Notes:
各大知名地图所使用的坐标系：
https://www.jianshu.com/p/c39a2c72dc65?from=singlemessage
赛题方提供的数据的坐标系为：cgcs2000
CGCS2000与WGS84是相容的，在坐标系实现精度范围内二者坐标是一致的。所以可以直接利用wgs84的转换方法
'''
import folium
import webbrowser
import pandas as pd
import numpy as np
from coord_convert.transform import wgs2gcj

if __name__ == '__main__':
    # data = pd.read_csv('data/普通工作日及双休日厦门巡游车订单数据.csv', skiprows=1)
    # data['GETON_DATE'] = pd.to_datetime(data.GETON_DATE)
    # begin = pd.to_datetime('2020-01-07')
    # end = pd.to_datetime('2020-01-08')
    # subset = data[(data.GETON_DATE >= begin) & (data.GETON_DATE <= end)]
    # subset = subset[(subset.GETON_LONGITUDE >= 118.05) & (subset.GETON_LATITUDE >= 24.44)]
    # subset = subset.sample(frac=0.25, random_state=99)
    # x = list(subset.GETON_LONGITUDE)
    # y = list(subset.GETON_LATITUDE)
    od = pd.read_csv('data/od_temp.csv')
    x = list(od.DEP_LONGITUDE)
    y = list(od.DEP_LATITUDE)
    incidents = folium.map.FeatureGroup()
    for x_t , y_t in zip(x,y):
        x_t, y_t = wgs2gcj(x_t, y_t)
        incidents.add_child(
            folium.CircleMarker(
                [y_t,x_t],
                radius=7,
                color='yellow',
                fill=True,
                fill_color='red',
                fill_opacity=0.4
            )
        )
    xmmap = folium.Map(location=(24.45, 118.08), zoom_start=13,
                       tiles='http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
                       attr='Powered by Amap ©️2020 高德软件 GS(2019)6379号 - 甲测资字11002004')
    xmmap.add_child(incidents)
    xmmap.save('out/passenger-up-distribution.html')