from pandas import read_csv,DataFrame
data = read_csv("/Users/pc/Desktop/桌面/大三上.nosync/103 商务智能/versionDEC14/archive/polishedDATA.csv")
nameList = ["genres","original_language","production_companies","production_countries","spoken_languages"]
nameDict = {}
for name in nameList:
    nameDict[name] = {}
for name in nameList:
    col = data[name]
    revenue = data["revenue"]
    for i in range(len(col)):
        li = col[i]
        if col[i][0]!="[":
            li = "['"+col[i]+"',]"
        try:
            for v in eval(li):
                if v in nameDict[name].keys():
                    nameDict[name][v][0]+=revenue[i]
                    nameDict[name][v][1]+=1
                else:
                    nameDict[name][v] = [revenue[i],1]
        except:
            li = "['"+col[i]+"',]"
            for v in eval(li):
                if v in nameDict[name].keys():
                    nameDict[name][v][0]+=revenue[i]
                    nameDict[name][v][1]+=1
                else:
                    nameDict[name][v] = [revenue[i],1]
for name in nameList:
    for k,v in nameDict[name].items():
        if v[1]!=0:
            nameDict[name][k] = v[0]/v[1]
    nameDict[name] = DataFrame(list(nameDict[name].items()),columns=[name,"revenue_avg"])

for k,v in nameDict.items():
    v.to_csv("avgs/"+k+"AvgRevenue.csv",index=False)