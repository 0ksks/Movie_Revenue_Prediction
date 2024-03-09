from pandas import read_csv,DataFrame
from quickSort import quickSort
revenue = read_csv("numeric.csv")["revenue"]
colName = "spokenLanguage"
COL = read_csv(colName+".csv")
vecsRevenue = {}
vecsCount = {}
for col in COL.columns:
    for val in COL[col]:
        if val not in vecsRevenue.keys():
            vecsRevenue[val] = 0
        if val not in vecsCount.keys():
            vecsCount[val] = 0
        else:
            vecsCount[val]+=1
COL["revenue"] = revenue
for col in COL.columns:
    for i in range(len(COL[col])):
        if col!="revenue":
            vecsRevenue[COL[col][i]]+=COL["revenue"][i]
for k,v in vecsRevenue.items():
    if vecsCount[k]!=0: vecsRevenue[k] = v/vecsCount[k]
    else: vecsRevenue[k] = 0
COL = COL.drop("revenue",axis=1)
COL = list(COL.values)
for i in range(len(COL)):
    quickSort(vecsRevenue, COL[i])
COL = DataFrame(COL)
COL.to_csv(colName+".csv",index=False)