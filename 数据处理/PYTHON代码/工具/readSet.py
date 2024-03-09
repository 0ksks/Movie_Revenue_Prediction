"""
读取并转换电影数据
"""
from hfmCodeGen import T
from utils import fromCsv,procedure
from datetime import datetime
from warnings import filterwarnings
filterwarnings('ignore')
def readKeywordSet():
    with open("keywordDict&Tree.txt") as fp:
        txts = fp.readlines()
        return (eval(txts[0]),eval(txts[1]))
def getMovieSet(st=0,ed=0):
    movieSet = fromCsv("polishedDATA")
    evalCols = ["genres","production_companies","production_countries","spoken_languages"]
    if ed==0:ed=len(movieSet.iloc[:,0])
    for i in range(st,ed):
        procedure(i,len(movieSet.iloc[:,0]),"正在拉取","拉取完成")
        for evalCol in evalCols:
            movieSet[evalCol][i] = eval(movieSet[evalCol][i])
        try:
            movieSet["release_date"][i] = datetime.strptime(movieSet["release_date"][i],"%Y/%m/%d")
        except TypeError:
            pass
        movieSet["vote_average"][i] = float(movieSet["vote_average"][i])
        if ed!=0 and i==ed-1:
            print()
            return movieSet.iloc[:i+1]
    print()
    return movieSet
def getID(ms,query,attribute):
    res = []
    for i in range(len(ms[attribute])):
        if set(query).issubset(set(ms[attribute][i])):
            res.append(ms["id"][i])
    return res

if __name__=='__main__':
    ms = getMovieSet()
    mms = fromCsv('polishedDATA')
    print(ms.shape[0],mms.shape[0])
