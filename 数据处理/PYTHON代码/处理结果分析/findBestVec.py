"""
根据回归系数寻找到最佳向量组合
"""
from glove import getWordVec
from math import sqrt
import numpy as np
from utils import procedure,toExcel
corrs = [('c', -2240400.1745455433), ('budget', 1.8032530413779306), ('release_date', -1919.5823973157978), ('runtime', -327494.0130759779), \
         ('vote_average', 13463449.549968567), ('vote_count', 69320.16252776768), ('genre_vec2', 1427760.1698934475), \
        ('genre_vec7', 3246688.906545842), ('genre_vec9', -6811954.053377822), ('genre_vec10', -6045326.232212262), \
        ('genre_vec16', -6314507.877471608), ('genre_vec18', 1594114.1698398173), ('genre_vec22', -3256457.789737307), \
        ('genre_vec23', 4430021.416681433), ('production_country_vec9', 2174605.900083012), ('production_country_vec15', -3057347.0115399957), \
        ('spoken_language_vec0', -4191217.545154311), ('spoken_language_vec9', -3576028.7435377627), ('spoken_language_vec21', 3415666.2926096255), \
        ('spoken_language_vec28', -5043586.985539696), ('spoken_language_vec29', -8662249.408736693)]
names = ["genre","productionCountry","spokenLanguage"]
def camel2underline(camel):
    capitalIdx = 0
    for i in range(len(camel)):
        if "A"<=camel[i]<="Z":
            capitalIdx=i
            break
    if capitalIdx!=0:underline = camel.replace(camel[capitalIdx],"_"+camel[capitalIdx].lower())
    else:underline = camel
    return underline
def get_subset2(mylist):
    n = len(mylist)
    for i in range(2**n):
        combi = []
        for j in range(n):
            if (i>>j)%2:
                combi.append(mylist[j])
        print(combi)
def cosVec(v1,v2):
    v1v2 = 0
    absV1 = 0
    absV2 = 0
    for (i1,i2) in zip(v1,v2):
        v1v2+=i1*i2
        absV1+=i1*i1
        absV2+=i2*i2
    return v1v2/(sqrt(absV1)*sqrt(absV2))
def genGrad(classname):
    vec = np.array(getWordVec(classname))
    grad = [0 for i in range(vec.shape[1])]
    for items in corrs:
        if camel2underline(classname) in items[0]:
            grad[int(items[0][len(camel2underline(classname))+4:])]=items[1]
    return vec,grad
def sumV(vLi):
    sumVini = [0 for i in range(len(vLi[0]))]
    for v in vLi:
        for i in range(len(v)):
            sumVini[i]+=v[i]
    return sumVini
def findBestVecs(classname):
    vec,grad = genGrad(classname)
    bestCos = -1
    n = len(vec)
    rangeLen = 2**n
    for i in range(rangeLen):
        procedure(i,rangeLen,"处理子集","处理完成")
        combi = []
        combiIdx = []
        for j in range(n):
            if (i>>j)%2:
                combi.append(vec[j])
                combiIdx.append(j)
        if len(combi)==0:
            cosNow = 0
        else:
            cosNow = cosVec(sumV(combi),grad)
        print("best={:<20} cos={:<20}      ".format(bestCos,cosNow),end="")
        if cosNow>bestCos:
            bestCos=cosNow
            bestIdx=combiIdx
    print()
    return bestIdx,bestCos


toExcel(findBestVecs(names[0])[0],names[0]+"BestVec")

