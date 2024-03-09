"""
预处理，把原数据的json转为python可以处理的格式
"""

from utils import fromCsv,toCsv,fromExcel,toExcel,procedure,figLen,qs
from hfmCodeGen import T,dict_tree_hfm,dictFlat,treeFlat,decode_hfm,encode_hfm
from UUID import getBI,getUUID,getData
from readSet import readKeywordSet,getMovieSet,getID
from glove import getWord2Vec,getWordVec,coMatrix
import sys
import matplotlib.pyplot as plt
sys.setrecursionlimit(10000)
import warnings
warnings.filterwarnings("ignore")

import inspect
import pandas as pd

#const params
moviesSet = fromCsv("tmdb_5000_movies_after1")
cols = ["budget",               "genres",         "homepage", "id",           "keywords",\
       "original_language",    "original_title", "overview", "popularity",   "production_companies",\
       "production_countries", "release_date",   "revenue",  "runtime",      "spoken_languages",\
       "status",               "tagline",        "title",    "vote_average", "vote_count"]
lanTrans = fromExcel("languageBook",True)
############

def getVariableName(var):
    frame = inspect.currentframe().f_back
    locals_dict = frame.f_locals
    for name in locals_dict:
        if locals_dict[name] is var:
            return name

def getName(seriesStr):
    series = eval(seriesStr)
    nameSet = []
    for content in series:
        nameSet.append(content["name"])
    nameSet = qs(nameSet)
    return nameSet

def getNameByISO(iso,lan):
    return lanTrans.loc[iso,lan]

def getLan(seriesStr,lan):
    series = eval(seriesStr)
    lanSet = []
    for content in series:
        lanSet.append(getNameByISO(content["iso_639_1"],lan))
    lanSet = qs(lanSet)
    return lanSet

def showEXP(set):
    print()
    for i in range(len(cols)):
        print(" "*(figLen(len(cols))-figLen(i)),end="")
        print("%d: %s"%(i,cols[i]))
        print("-"*( len(cols[i]) + figLen(len(cols)) + 2))
        print(set[cols[i]][0])
        print()

def depthTree(node):
    if isinstance(node,str):return -1
    else:
        return depthTree(node.left_node)+1 if depthTree(node.left_node)>depthTree(node.right_node) else depthTree(node.right_node)+1
            
def longestStr(node):
    if isinstance(node,str):return len(node)
    else:
        return longestStr(node.left_node) if longestStr(node.left_node)>longestStr(node.right_node) else longestStr(node.right_node)

def DFSTree(node,codeLen,strLen,tab=0,code=""):
    if tab==0:print("root")
    if isinstance(node.left_node,T):
        DFSTree(node.left_node,codeLen,strLen,1,code+"0")
    if isinstance(node,str):
        return
    if isinstance(node.left_node,str):
        codeT = code+"0"
        print(" "*len(codeT)+codeT+"-"*(codeLen-len(codeT))+"-"+"-"*(strLen-len(node.left_node))+node.left_node)
    if isinstance(node.right_node,str):
        codeT = code+"1"
        print(" "*len(codeT)+codeT+"-"*(codeLen-len(codeT))+"-"+"-"*(strLen-len(node.right_node))+node.right_node)
    if isinstance(node.right_node,T):
        DFSTree(node.right_node,codeLen,strLen,1,code+"1")

def DFSTreeUse(node):
    codeLen = depthTree(node)
    strLen = longestStr(node)
    DFSTree(node,codeLen,strLen)

moviesSetLen = len(moviesSet[cols[0]])
unprocessedCols = [1,4,9,10]
def pro(len):
    keywordSet = []
    cnt = 0
    for i in range(moviesSetLen):
        cnt+=1
        procedure(i,moviesSetLen)
        for unprocessedCol in unprocessedCols:
            try:moviesSet[cols[unprocessedCol]][i] = getName(moviesSet[cols[unprocessedCol]][i])
            except:
                moviesSet[cols[unprocessedCol]][i] = []
        moviesSet[cols[14]][i] = getLan(moviesSet[cols[14]][i],"English")
        moviesSet[cols[5]][i] = getNameByISO(moviesSet[cols[5]][i],"English")
        keywordSet = moviesSet[cols[4]][i] + keywordSet
        # if cnt==len:
        #     print()
        #     print()
        #     return (moviesSet.loc[:len-1],keywordSet)
    return (moviesSet,keywordSet)

# proTmp,keywordSet = pro(1)
# hfmDict,hfmT=dict_tree_hfm(keywordSet)
# with open(getVariableName(keywordSet)[:-3]+"Dict&Tree.txt","+w") as fp:
#     fp.write(dictFlat(hfmDict))
#     fp.write(treeFlat(hfmT))

# hfmDict,hfmT=readKeywordSet()
# DFSTreeUse(hfmT)
# for i in range(len(proTmp["keywords"])):
#     hfmCode=encode_hfm(proTmp["keywords"][i],hfmDict)
#     proTmp["keywords"][i]=getUUID(hfmCode)

# toCsv(proTmp,"polishedDATA")
# ms = getMovieSet()
# dic = []
# for i in range(len(ms["id"])):
#     dic+=ms["genres"][i]
#     dic = list(set(dic))
# toExcel(dic,"dict")
# coMatrix(ms["genres"])


proCol = getMovieSet()['spoken_languages']
dic = []
for row in proCol:
    dic += row
    dic = list(set(dic))
toExcel(dic,"dict")
# coMatrix(proCol)





from vec import SxV, addE, zeroV
processClass = 'spoken_languages'
ms = getMovieSet(0,0)
dic = getWord2Vec()
vecLen = len(list(dic.values())[0])
data = []
ids = []
for (li,id) in zip(ms[processClass],ms["id"]):
    ids.append(id)
    summ = zeroV(vecLen)
    if len(li)==0:
        data.append([0 for i in range(vecLen)])
    else:
        for word in li:
            summ = addE(summ,dic[word])
        summ = SxV(1/len(li),summ)
        data.append(summ)
data = list(zip(ids,data))
toCsv(data,'spokenLanguageVec')





# from vec import zeroV,addE,SxV
# dic = getWord2Vec()
# vecLen = 3
# ms = getMovieSet(100)
# res = []
# for li in ms["genres"]:
#     if len(li)==0:continue
#     summ = zeroV(vecLen)
#     for word in li:
#         summ = addE(summ,dic[word])
#     summ = SxV(1/len(li),summ)
#     res.append(summ)

# import numpy as np
# import matplotlib.pyplot as plt
# from mpl_toolkits.mplot3d import Axes3D

# fig = plt.figure()
# ax = fig.add_axes(Axes3D(fig))

# dic = getWord2Vec()
# x = []
# y = []
# z = []
# for v in res:
#     x.append(v[0])
#     y.append(v[1])
#     z.append(v[2])
# ax.scatter(x,y,z,c='b',alpha=0.6,s=10)
# # plt.scatter(x, y, s=20, c='b', marker='o', alpha=0.5)
# # for i in range(len(x)):
# #     plt.plot([0,x[i]],[0,y[i]],c='b',alpha=0.1)
#     # ax.plot([0,x[i]],[0,y[i]],[0,z[i]],c='b',alpha=0.1)



# res = getWordVec()
# x = []
# y = []
# z = []
# for v in res:
#     x.append(v[0])
#     y.append(v[1])
#     z.append(v[2])
# # plt.scatter(x, y, s=20, c='r', marker='o')
# for i in range(len(x)):
#     plt.plot([0,x[i]],[0,y[i]],c='r',alpha=0.9)
#     ax.plot([0,x[i]],[0,y[i]],[0,z[i]],c='r')

# ax.set_xlim(-10,10)
# ax.set_ylim(-10,10)
# ax.set_zlim(-10,10)
# plt.show()