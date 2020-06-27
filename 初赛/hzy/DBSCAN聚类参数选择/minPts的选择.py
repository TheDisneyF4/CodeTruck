'''
@Desc:DBScan Demo2 根据噪声点变化和聚类数确定minPts的值
@Author: huangzhiyuan
@Time: 2020/6/16 7:35 上午
@Modify Notes:
经纬度与距离的关系：
https://blog.csdn.net/qq_23392639/article/details/89446703
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import DBSCAN

def foo(X,epsList,minptsList):
    res = []
    flag = 1
    for eps in epsList:
        for minpts in minptsList:
            db = DBSCAN(eps=eps, min_samples=minpts).fit(X)
            labels = db.labels_
            n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
            noise = list(labels).count(-1)
            tmpres = [eps, minpts,noise,n_clusters,flag]
            res.append(tmpres)
        flag += 1
    return res

if __name__ == '__main__':
    # data = pd.read_csv('厦门出租车运行特性分析研究/普通工作日及双休日厦门巡游车订单数据.csv', skiprows=1)
    # data['GETON_DATE'] = pd.to_datetime(data.GETON_DATE)
    # begin = pd.to_datetime('2020-01-07')
    # end = pd.to_datetime('2020-01-08')
    # subset = data[(data.GETON_DATE >= begin) & (data.GETON_DATE <= end)]
    # subset = subset[(subset.GETON_LONGITUDE >= 118.05) & (subset.GETON_LATITUDE >= 24.44)]
    # subset = subset.sample(frac=0.25, random_state=99)
    # x = list(subset.GETON_LONGITUDE)
    # y = list(subset.GETON_LATITUDE)
    od = pd.read_csv('厦门出租车运行特性分析研究/od_temp.csv')
    x = list(od.DEP_LONGITUDE)
    y = list(od.DEP_LATITUDE)
    x = np.asarray(x).reshape((len(x), 1))
    y = np.asarray(y).reshape((len(y), 1))
    X = np.hstack((x, y))
    # 20m 30m 40m 50m 60m 70米
    epsList = [0.0002,0.0003,0.0004,0.0005,0.0006,0.0007]
    minptsList = [1,2,3,4,5,6,7,8,9,10]
    res = foo(X,epsList,minptsList)
    flag = 1
    y = []
    y1 = []
    t = []
    t1 = []
    label = [0.0002]
    plt.figure()
    plt.xlim((1, 10))
    plt.xlabel('minPts')
    plt.ylabel('noise')
    for i in range(len(res)):
        if res[i][4] == flag:
            t.append(res[i][2])
            t1.append(res[i][3])
        else:
            flag += 1
            y.append(t)
            y1.append(t1)
            t = []
            t1 = []
            t.append(res[i][2])
            t1.append(res[i][3])
            label.append(res[i][0])
    y.append(t)
    y1.append(t1)
    for i in range(len(y)):
        plt.plot(minptsList,y[i],'--',label='eps:'+str(label[i]))
    plt.legend(loc='best')
    plt.figure()
    plt.xlim((1, 10))
    plt.xlabel('minPts')
    plt.ylabel('clusters')
    for i in range(len(y1)):
        print(y1[i])
        plt.plot(minptsList,y1[i],'--',label='eps:'+str(label[i]))
    plt.legend(loc='best')
    plt.show()