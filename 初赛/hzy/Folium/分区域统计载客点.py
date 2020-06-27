'''
@Desc:载客点统计
@Author: huangzhiyuan
@Time: 2020/6/18 5:55 下午
@Modify Notes:
'''

import pandas as pd
import folium
from folium import plugins
from coord_convert.transform import wgs2gcj

if __name__ == '__main__':
    od = pd.read_csv('data/od_temp.csv')
    x = list(od.DEP_LONGITUDE)
    y = list(od.DEP_LATITUDE)
    xmmap = folium.Map(location=(24.45, 118.08), zoom_start=10,
                       tiles='http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
                       attr='Powered by Amap ©️2020 高德软件 GS(2019)6379号 - 甲测资字11002004'
                       )
    folium.GeoJson(
        data='data/福建省厦门市.geojson',
        style_function=lambda feature: {
            'fillColor': "#ffff00",
            'color': 'black',
            'weight': 2,
            'dashArray': '5,5'
        }
    ).add_to(xmmap)
    incidents = plugins.MarkerCluster().add_to(xmmap)
    for lng,lat in zip(x,y):
        lng, lat = wgs2gcj(lng, lat)
        folium.Marker(
            location=[lat,lng]
        ).add_to(incidents)
    xmmap.add_child(incidents)
    xmmap.save('out/passengercount.html')