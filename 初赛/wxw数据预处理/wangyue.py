import pandas as pd
import numpy as np
fpath ="wangyue51.xlsx"
data=pd.read_excel(fpath)

#去重复（车牌号，上车时间均一致的删除）
data.drop_duplicates(subset =['VEHICLE_NO','DEP_TIME'],keep='first',inplace=True)
#去除里程超过40km的
data = data.drop(data[data.DRIVE_MILE>40].index)
#去除载客时间超过80min的
data = data.drop(data[data.DRIVE_TIME/60>80].index)
#去除平均速度超过80km/h的
data["average_v"] = data["DRIVE_MILE"]/data["DRIVE_TIME"]*3600
data= data.drop(data[data.average_v>80.0].index)
#去除两点间距离小于50m的,直线距离大于行驶距离的去除
long1 = data["DEP_LONGITUDE"]
lat1 = data["DEP_LATITUDE"]
long2 = data["DEST_LONGITUDE"]
lat2 = data["DEST_LATITUDE"]
delta_long = np.radians(long2 - long1)
delta_lat = np.radians(lat2 - lat1)
data["line_len"] = 2 * np.arcsin(np.sqrt(np.square(np.sin(delta_lat / 2)) + np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * np.square(np.sin(delta_long / 2))))
data["line_len"] = data["line_len"] * 6378137.0
data = data.drop(data[data.line_len<50.0].index)
data = data.drop(data[data.line_len/1000>data.DRIVE_MILE].index)
#缺失值补充
data.loc[:,"WAIT_TIME"]=data["WAIT_TIME"].fillna(-1)
data.loc[:,"WAIT_MILE"]=data["WAIT_MILE"].fillna(-1)

#上下车不合理的
data["DEP_TIME"] = pd.to_datetime(data["DEP_TIME"],format='%Y%m%d%H%M%S')
data["DEST_TIME"] = pd.to_datetime(data["DEST_TIME"],format='%Y%m%d%H%M%S')
data["delta_time"] = data["DEST_TIME"]-data["DEP_TIME"]
data["delta_time"]=data["delta_time"].astype('timedelta64[s]')
data = data.drop(data[data.delta_time<0].index)

print(data["delta_time"].min())

data.to_excel(fpath,index=False,header=True,columns=None)


print("success")

















