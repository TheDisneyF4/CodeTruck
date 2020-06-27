'''
@Desc:上车点与下车点的可视化
@Author: huangzhiyuan
@Time: 2020/6/19 2:20 下午
@Modify Notes:
'''

import folium
import pandas as pd
from coord_convert.transform import wgs2gcj

if __name__ == '__main__':
    data = pd.read_csv('data/od_temp.csv')
    x = list(data.DEST_LONGITUDE)
    y = list(data.DEST_LATITUDE)
    incidents = folium.map.FeatureGroup()
    for x_t, y_t in zip(x, y):
        x_t, y_t = wgs2gcj(x_t, y_t)
        incidents.add_child(
            folium.CircleMarker(
                [y_t, x_t],
                radius=7,
                color='green',
                fill=True,
                fill_color='yellow',
                fill_opacity=0.4
            )
        )
    xmmap = folium.Map(location=(24.45, 118.08), zoom_start=15,
                       tiles='http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
                       attr='Powered by Amap ©️2020 高德软件 GS(2019)6379号 - 甲测资字11002004'
                       )
    xmmap.add_child(incidents)
    xmmap.save('out/passenger-down-distribution.html')