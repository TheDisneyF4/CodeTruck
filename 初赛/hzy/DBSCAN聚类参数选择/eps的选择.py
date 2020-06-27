'''
@Desc: 利用k-临近距离来选择eps
@Author: huangzhiyuan
@Time: 2020/6/16 9:23 上午
@Modify Notes:
'''
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def foo(X,k):
    numRecords = X.shape[0]
    k_list = []
    for i in range(numRecords):
        x_before = X[:i]
        x_after = X[i+1:]
        X1 = np.vstack((x_before,x_after))
        res = [np.sqrt(pow((each[0]-X[i][0]),2)+pow((each[1]-X[i][1]),2)) for each in X1]
        # 默认升序
        res = np.sort(res)
        k_list.append(res[k])
    k_list = np.sort(k_list)
    return k_list


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
    k_list = foo(X,5-1)
    k_x = [i for i in range(len(k_list))]
    plt.figure()
    plt.xlabel('Distribution')
    plt.ylabel('k-neighbour distance')
    plt.scatter(k_x,k_list)
    plt.show()
