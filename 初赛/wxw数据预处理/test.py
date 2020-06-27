import pandas as pd
fpath1 = "wangyue51.xlsx"
fpath2 = "xunyou51.csv"
data1 = pd.read_excel(fpath1)
data1.loc[:,"NOPASS_MILE"]=data1["NOPASS_MILE"].fillna(-1)
data2 = pd.read_csv(fpath2)
all_data = pd.concat([data1,data2])
all_data.to_csv("texi_data.csv",index=False,header=True,columns=None)
print(all_data.shape)











