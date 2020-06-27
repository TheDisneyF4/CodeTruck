import pandas as pd
import numpy as np
fpath = "xunyou51.csv"
data = pd.read_csv(fpath)

#
# #去重复（车牌号，上车时间均一致的删除）
# data.drop_duplicates(subset =['VEHICLE_PLATE_NUMBER','GETON_DATE'],keep='first',inplace=True)
#
# #去除里程超过40km的
# data = data.drop(data[data.PASS_MILE>40].index)
#
# #去除上下车时间不明确的数据行
# data = data.drop(data[(data.GETON_DATE.str.len()<13)&(data.GETOFF_DATE.str.len()<13)].index)
#
# #去除载客时间超过80min的
# data["all_time"]=pd.to_datetime(data["GETOFF_DATE"])-pd.to_datetime(data["GETON_DATE"])
# data["all_time"]=data["all_time"].astype('timedelta64[s]')
# data = data.drop(data[(data.all_time/60)>80.0].index)
# print(data["all_time"].min())
# #去除平均速度超过80km/h的
# data["average_v"] = data["PASS_MILE"]/data["all_time"]*3600
# data= data.drop(data[data.average_v>80.0].index)
#
# #去除两点间距离小于50m的
# long1 = data["GETON_LONGITUDE"]
# lat1 = data["GETON_LATITUDE"]
# long2 = data["GETOFF_LONGITUDE"]
# lat2 = data["GETOFF_LATITUDE"]
# delta_long = np.radians(long2 - long1)
# delta_lat = np.radians(lat2 - lat1)
# data["line_len"] = 2 * np.arcsin(np.sqrt(np.square(np.sin(delta_lat / 2)) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.square(np.sin(delta_long / 2))))
# data["line_len"] = data["line_len"] * 6378137.0
# data = data.drop(data[data.line_len<50.0].index)
# data = data.drop(data[data.line_len/1000>data.PASS_MILE].index)
#
# #修正，下车时间在上车时间之前的删除
# data = data.drop(data[data.all_time<0].index)
#
# print(data.dtypes)
# data.to_csv(fpath,index=False,header=True,columns=None)
# print("success")