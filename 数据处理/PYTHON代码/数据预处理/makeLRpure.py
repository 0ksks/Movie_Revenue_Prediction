"""
处理用于回归分析的数据　
"""
import pandas as pd
from utils import procedure
from warnings import filterwarnings
filterwarnings('ignore')
def getMovieSet(st=0,ed=0):
    dicNewCol = {}
    movieSet = pd.read_csv("numericLR.csv")
    if ed==0:ed=len(movieSet.iloc[:,0])
    for i in range(st,ed):
        procedure(i,len(movieSet.iloc[:,0]),"正在拉取","拉取完成")
        for col in movieSet.columns:
            if isinstance(movieSet[col].get(i),str):
                movieSet[col][i] = eval(movieSet[col].get(i))
                for x in range(len(movieSet[col][i])):
                    if i==0:
                        dicNewCol[(col+"{}").format(x)] = [movieSet[col][i][x],]
                    else:
                        dicNewCol[(col+"{}").format(x)].append(movieSet[col][i][x])
            else:
                if i==0:
                    dicNewCol[col] = [movieSet[col][i],]
                else:
                    dicNewCol[col].append(movieSet[col][i])
    print()
    return pd.DataFrame(dicNewCol)
getMovieSet().to_csv("pureLR.csv",index=False)