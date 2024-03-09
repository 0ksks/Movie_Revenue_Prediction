from sklearn.preprocessing import StandardScaler
from pandas import read_csv
from torch import from_numpy
from numpy import array
# 读取并标准化数据
scaler = StandardScaler()
def getTensor(name):
    print("reading",name)
    name = read_csv(name+".csv")
    name = array(name)
    nameList = []
    for i in range(name.shape[0]):
        dim0 = []
        for j in range(name.shape[1]):
            dim1 = []
            # print(eval(name[i][j]))
            for v in eval(name[i][j]):
                dim1.append(v)
            dim0.append(array(dim1))
        nameList.append(array(dim0))
    return from_numpy(array(nameList))
    
def getCriAndY():
    df = read_csv("numeric.csv")
    y = df["revenue"]
    y = from_numpy(array(y))
    df = df.drop("revenue",axis=1)
    Cri = []
    for col in df.columns:
        Cri.append(array(df[col]))
    Cri = from_numpy(array(Cri)).T
    return from_numpy(scaler.fit(Cri).transform(Cri)), from_numpy(scaler.fit(y.reshape(-1,1)).transform(y.reshape(-1,1)))

def getX():
    nameList = ["genre","productionCountry","spokenLanguage"]
    X_list = []
    for name in nameList:
        X_list.append(getTensor(name))
    return X_list