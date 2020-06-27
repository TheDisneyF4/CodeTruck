'''
@Desc:载客点DBSCAN聚类
@Author: huangzhiyuan
@Time: 2020/6/17 10:04 上午
@Modify Notes:
sklearn-DBSCAN:
https://sklearn.apachecn.org/docs/master/22.html#dbscan

'''
import pandas as pd
import numpy as np
import random
import folium
from sklearn.cluster import DBSCAN
from coord_convert.transform import wgs2gcj
import colorsys


def randomcolor():
    colorArr = ['1','2','3','4','5','6','7','8','9','A','B','C','D','E','F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0,14)]
    return "#"+color

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
    x = np.asarray(x).reshape((len(x),1))
    y = np.asarray(y).reshape((len(y),1))
    X = np.hstack((x, y))
    db = DBSCAN(eps=0.003, min_samples=5).fit(X)
    labels = db.labels_
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    noise = list(labels).count(-1)
    print('clusters: '+str(n_clusters))
    print('noises: '+str(noise))
    incidents = folium.map.FeatureGroup()
    for i in range(n_clusters):
        colorA = randomcolor()
        colorB = randomcolor()
        one_cluster = X[labels == i]
        for j in one_cluster:
            j[0],j[1] = wgs2gcj(j[0],j[1])
            incidents.add_child(
                folium.CircleMarker(
                    [j[1], j[0]],
                    radius=7,
                    color=colorA,
                    fill=True,
                    fill_color=colorB,
                    fill_opacity=0.4
                )
            )
    xmmap = folium.Map(location=(24.45, 118.08), zoom_start=12,
                       tiles='http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
                       attr='Powered by Amap ©️2020 高德软件 GS(2019)6379号 - 甲测资字11002004'
                       )
    xmmap.add_child(incidents)
    xmmap.save('out/passenger-clustering.html')