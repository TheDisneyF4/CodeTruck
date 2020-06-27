'''
@Desc:核密度分析
@Author: huangzhiyuan
@Time: 2020/6/17 8:10 上午
@Modify Notes:
白话空间统计二十一：密度分析（七）
https://blog.csdn.net/allenlu2008/article/details/103028967?ops_request_misc=%257B%2522request%255Fid%2522%253A%2522159288080519726869020244%2522%252C%2522scm%2522%253A%252220140713.130102334..%2522%257D&request_id=159288080519726869020244&biz_id=0&utm_medium=distribute.pc_search_result.none-task-blog-2~all~top_click~default-2-103028967.first_rank_ecpm_v3_pc_rank_v3&utm_term=%E7%99%BD%E8%AF%9D%E7%A9%BA%E9%97%B4%E7%BB%9F%E8%AE%A1%E4%BA%8C%E5%8D%81%E4%B8%80
'''
import pandas as pd
import numpy as np
import folium
from folium.plugins import HeatMap
import webbrowser
from sklearn.neighbors import KernelDensity
import matplotlib.pyplot as plt
from coord_convert.transform import wgs2gcj

# 计算核密度估计带宽（参考arcgis中默认带宽生成算法）
def getBandWidth(X):
    # 计算均数中心
    x_bar = sum(X[:,0])/len(X[:,0])
    y_bar = sum(X[:,1])/len(X[:,1])
    # 计算每个点到均数中心的距离
    dist = []
    for x_t, y_t in X:
        dist_t = np.sqrt((x_t-x_bar) ** 2 + (y_t-y_bar) ** 2)
        dist.append(dist_t)
    dist = np.asarray(dist)
    dist.sort()
    mid_index = round(len(dist)/2)
    dm = dist[mid_index]
    # 计算标准距离
    x_sum = 0
    y_sum = 0
    for x_t,y_t in X:
        x_sum += (x_t - x_bar) ** 2
        y_sum += (y_t - y_bar) ** 2
    sd = np.sqrt(x_sum / len(X[:,0]) + y_sum / len(X[:,0]))
    # 计算带宽
    band = 0.9 * min(sd,np.sqrt(1/np.log(2)) * dm) * pow(len(X[:,0]),-0.2)
    return band



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
    x = np.asarray(x).reshape((len(x), 1))
    y = np.asarray(y).reshape((len(y), 1))
    X = np.hstack((x, y))
    for i in range(len(X)):
        X[i][0],X[i][1] = wgs2gcj(X[i][0],X[i][1])
    X1 = np.hstack((y,x))
    for i in range(len(X1)):
        X1[i][1], X1[i][0] = wgs2gcj(X1[i][1], X1[i][0])
    band = getBandWidth(X)
    print('Band Width:'+str(band))
    kde = KernelDensity(bandwidth=band,kernel='epanechnikov').fit(X)
    res = kde.score_samples(X)
    res = np.asarray(res).reshape((len(res),1))
    kde_y = np.hstack((X1,res))
    xmmap = folium.Map(location=(24.45, 118.08), zoom_start=13,max_zoom=14,
                       tiles='http://wprd02.is.autonavi.com/appmaptile?x={x}&y={y}&z={z}&lang=zh_cn&size=1&scl=1&style=7',
                       attr='Powered by Amap ©️2020 高德软件 GS(2019)6379号 - 甲测资字11002004'
                       )
    HeatMap(kde_y).add_to(xmmap)
    xmmap.save('out/passengerkde.html')