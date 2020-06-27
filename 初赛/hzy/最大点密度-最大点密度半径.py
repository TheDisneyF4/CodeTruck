'''
@Desc:最大点密度/最大密度半径计算demo
@Author: huangzhiyuan
@Time: 2020/6/24 4:30 下午
@Modify Notes:
    密度的计算参考了人口密度的计算方法，放到这里也就变成了：载客点数/圆面积。
    但是按照我的理解，圆半径在增大->圆面积在增大->加入的载客点数变多->密度持续增大。
    然后我就想根据每次半径增大时所纳入的载客点数，如果跟上一次比，纳入的载客点下降了，并且少于10个，
    说明现在圆的边界载客比较稀疏了，可以停止计算了。
    我感觉可能有问题，这应该算得的是一个局部解。
    但是如果少于10个后又再次增大，少于10个影响不大，还是稀疏的；如果大于10个，说明可能触及另外一个载客热点了
'''

import pandas as pd
import numpy as np

if __name__ == '__main__':
    od = pd.read_csv('厦门出租车运行特性分析研究/od_temp.csv')
    # 经度
    target_lon = 118.125383
    # 纬度
    target_lat = 24.49561
    # 100米
    step = 0.001
    x = list(od.DEP_LONGITUDE)
    y = list(od.DEP_LATITUDE)
    x = np.asarray(x).reshape((len(x), 1))
    y = np.asarray(y).reshape((len(y), 1))
    X = np.hstack((x, y))
    print('Total: '+str(len(X)))
    time = 1
    # 与上一次循环增加的载客点数
    preCount = -1
    # 与上一次循环载客点数的差值
    loss = 0
    while 1:
        # 半径每次增加100米
        r = time * step
        # print('半径:'+str(time))
        # 计算圆面积 单位：平方米
        s = np.pi * (r ** 2)
        count = 0
        for index in range(len(X)):
            dist = np.sqrt((X[index][0]-target_lon)**2+(X[index][1]-target_lat)**2)
            if(dist <= r):
                count += 1
        # 计算载客点密度 单位：个/平方千米
        p = count / s
        p = p * 0.000001
        if preCount == -1:
            preCount = count
        else:
            print('增加了:'+str(count-preCount))
            if count - preCount < loss and count - preCount < 10:
                print('最大点密度半径 km: ' + str(time*100/1000)+' 最大点密度 个/km^2：'+ str(p)+' 圆中共有载客点: '+str(count))
                break
            loss = count - preCount
            preCount = count
            time += 1

