'''
@Desc:
@Author: huangzhiyuan
@Time: 2020/6/25 10:32 下午
@Modify Notes:
'''
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMapWithTime
from coord_convert.transform import wgs2gcj

if __name__ == '__main__':
    od = pd.read_csv('data/od_temp.csv')
    od['DEP_TIME'] = pd.to_datetime(od.DEP_TIME)
    tm1 = pd.to_datetime('2020-01-07 23:00:00')
    tm2= pd.to_datetime('2020-01-07 23:30:00')
    testList = []
    testList.append(
        od.loc[od.DEP_TIME < tm1, ['DEP_LATITUDE', 'DEP_LONGITUDE']].groupby(
            ['DEP_LATITUDE', 'DEP_LONGITUDE']).sum().reset_index().values.tolist()
    )

    testList.append(
        od.loc[(od.DEP_TIME >= tm1) & (od.DEP_TIME < tm2), ['DEP_LATITUDE', 'DEP_LONGITUDE']].groupby(
            ['DEP_LATITUDE', 'DEP_LONGITUDE']).sum().reset_index().values.tolist()
    )

    testList.append(
        od.loc[od.DEP_TIME >= tm2, ['DEP_LATITUDE', 'DEP_LONGITUDE']].groupby(
            ['DEP_LATITUDE', 'DEP_LONGITUDE']).sum().reset_index().values.tolist()
    )

    xmmap = folium.Map(location=(24.45, 118.08), zoom_start=13, max_zoom=14,
                       tiles='http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
                       attr='Powered by Amap ©️2020 高德软件 GS(2019)6379号 - 甲测资字11002004')

    HeatMapWithTime(testList,radius=25).add_to(xmmap)
    xmmap.save('out/heatMapWithTime.html')
