"""
和clustering同理，但是处理keyword需要哈夫曼编码和解码，所以有所不同
"""
from readSet import getMovieSet,readKeywordSet
from UUID import getData
from warnings import filterwarnings
from sklearn.cluster import AgglomerativeClustering
filterwarnings('ignore')
import numpy as np
import myDis
import scipy.spatial.distance as dist
from scipy.cluster.hierarchy import dendrogram, linkage
from utils import toCsv,fromCsv
from clustering import findLongest
from matplotlib.pyplot import show,subplots,tight_layout,savefig
from copy import deepcopy
from utils import procedure
ms = getMovieSet(0,0)
hfmT = readKeywordSet()[1]
keywords = []
labels = []
ids = []
i = 0
n = ms.shape[0]
for (label,row,id) in zip(ms['original_title'],ms['keywords'],ms['id']):
    procedure(i,n,"keyword decoding","keyword decoded")
    i+=1
    keywords.append(getData(row,hfmT))
    labels.append(label)
    ids.append(id)
print()
num = ms.shape[0]
distMat = np.mat(np.zeros((num,num)))
for i in range(num):
    procedure(i,num,"distMat preparing","distMat prepared")
    for j in range(i,num):
        distance = 1-myDis.affinity(keywords[i],keywords[j])
        distMat[i:i+1,j:j+1] = distance
        distMat[j:j+1,i:i+1] = distance
print()
distMatForAC = np.array(distMat)
print("first agc")
ac = AgglomerativeClustering(affinity='precomputed',linkage='average')
clustering = ac.fit(distMatForAC)
distMatSave = np.array(deepcopy(distMat))
distMat = dist.squareform(distMat)
Z = linkage(distMat,'average')
toCsv(Z,"Ztmp")
Z = fromCsv("Ztmp")
longestIDX = findLongest(Z)
buttom = 2
height = 0.05
scaler = Z.shape[0]/20
fig,ax = subplots(figsize=(scaler*buttom,scaler*height+3.375))
ddg = dendrogram(Z,ax=ax,labels=labels,color_threshold=Z['2'][longestIDX],leaf_rotation=270,leaf_font_size=5)
print("next agc")
cluster = AgglomerativeClustering(n_clusters=Z.shape[0]-longestIDX,affinity='precomputed',linkage='average')
classification = cluster.fit_predict(distMatSave)
toCsv(list(zip(ids,classification)),"keywordClass")
ax.get_yaxis().set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
tight_layout()
savefig("keywordClass.svg",format='svg',dpi=100)
print("finish")
# show()