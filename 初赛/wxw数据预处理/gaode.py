import requests,json,time
import pandas as pd
fpath = "texi_data.csv"
data = pd.read_csv(fpath)
key ='45da1050dbccb31d69adee29eeb37f41'

def get_area(lng,lat):
    paramaters={
        'key':key,
        'location':str(lng)+','+str(lat)
    }
    r = requests.get("https://restapi.amap.com/v3/geocode/regeo?parameters",params=paramaters)
    area = r.json()['regeocode']['formatted_address']
    return area


tmp=data[pd.isnull(data['DEP_AREA'])]
tmp['DEP_AREA']=tmp.apply(lambda x: get_area(x['DEP_LONGITUDE'],x['DEP_LATITUDE']), axis=1)
tmp.to_csv('tmp1.csv',encoding="utf_8_sig",index=None)#处理中文，并且将INDEX取出
tmp['DEST_AREA']=tmp.apply(lambda x: get_area(x['DEST_LONGITUDE'],x['DEST_LATITUDE']), axis=1)
tmp.to_csv('tmp2.csv',encoding="utf_8_sig",index=None)#处理中文，并且将INDEX取出

data = pd.concat([data,tmp],join='outer')
data = data.reset_index(drop = True)
data.to_csv('texi_data.csv',encoding="utf_8_sig",index=None)#处理中文，并且将INDEX取出




