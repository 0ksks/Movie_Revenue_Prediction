"""
绘制散点图和平均值折线图
"""
from pandas import read_excel
import matplotlib.pyplot as plt
from numpy import reshape
from warnings import filterwarnings
filterwarnings('ignore')
def F(x):
    return eval(x)

LRdata = read_excel("versionDEC14/archive/LR.xlsx")
# budget = LRdata["budget"]
revenue = LRdata["revenue"]
# runtime = LRdata["runtime"]
# genreVec = LRdata["genre_vec"]
# genreClass = LRdata["genre_class"]
# keywordClass = LRdata["keyword_class"]
# voteAvg = LRdata["vote_average"]
# voteCnt = LRdata["vote_count"]
# productionCountryVec = LRdata["production_country_vec"]
# spokenLanguageVec = LRdata["spoken_language_vec"]
# releaseDate = LRdata["release_date"]
colName = ["genre_class","keyword_class"]
fig,axs = plt.subplots(2,2)
print(axs)
for (ax,col) in zip(axs,colName):
    xNow = LRdata[col]
    ymean = {}
    Plo = []
    for i in range(len(xNow)):
        if xNow[i] in ymean.keys():
            ymean[xNow[i]].append(revenue[i])
        else:
            ymean[xNow[i]] = [revenue[i],]
    Plox = []
    for k,v in ymean.items():
        Plo.append([k,sum(v)/len(v)])
    Plo.sort(key = lambda x:x[1])
    for row in Plo:
        Plox.append(row[0])
    sx = []
    sy = []
    for (xn,rev) in zip(xNow,revenue):
        sx.append(Plox.index(xn))
        sy.append(rev)
    px = []
    py = []
    i = 0
    for row in Plo:
        px.append(i)
        i+=1
        py.append(row[1])
        ax[1].plot([0,px[-1]],[py[-1],py[-1]],"r",alpha = 0.5)
    ax[0].scatter(sx,sy,marker='x',s=10,alpha=0.3)
    ax[0].set_title(col)
    ax[1].plot(px,py,'g.-')
    ax[1].set_title(col+"_mean")
fig.tight_layout(pad=1.0,w_pad=1.0,h_pad=1.0)

plt.show()

# PCVflag = 0
# SLVflag = 0
# for i in range(LRdata.shape[0]):
#     try:
#         productionCountryVec[i] = eval(productionCountryVec[i])
#         spokenLanguageVec[i] = eval(spokenLanguageVec[i])
#         if PCVflag==0:
#             lenPCV = len(productionCountryVec[i])
#             PCVflag=1
#         if SLVflag==0:
#             lenSLV = len(spokenLanguageVec[i])
#             SLVflag=1
#     except:
#         productionCountryVec[i] = [0 for i in range(lenPCV)]
#         spokenLanguageVec[i] = [0 for i in range(lenSLV)]



