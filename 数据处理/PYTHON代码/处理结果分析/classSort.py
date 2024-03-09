"""
将分类标签从小到大排序，从而进行回归
"""
from pandas import read_excel
import matplotlib.pyplot as plt
from numpy import reshape
from warnings import filterwarnings
filterwarnings('ignore')

LRdata = read_excel("/Users/pc/Desktop/桌面/大三上.nosync/103 商务智能/versionDEC14/archive/LR.xlsx")
revenue = LRdata["revenue"]
colName = ["genre_class","keyword_class"]
dicdic = {}
for col in colName:
    xNow = LRdata[col]
    ymean = {}
    for i in range(len(xNow)):
        if xNow[i] in ymean.keys():
            ymean[xNow[i]].append(revenue[i])
        else:
            ymean[xNow[i]] = [revenue[i],]
    xydata = list(ymean.items())
    for i in range(len(xydata)):
        xydata[i] = list(xydata[i])
        xydata[i][1] = sum(xydata[i][1])/len(xydata[i][1])
    xydata.sort(key = lambda x:x[1])
    old2new = []
    for i in range(len(xydata)):
        old2new.append([xydata[i][0],i])
    dicdic[col] = dict(old2new)

for col in colName:
    colTmp = []
    for i in range(LRdata.shape[0]):
        colTmp.append(dicdic[col][LRdata[col][i]])
    LRdata[col+"_new"] = colTmp

LRdata.to_excel("newLR.xlsx",index=False)
