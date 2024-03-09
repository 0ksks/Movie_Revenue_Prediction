"""
为glove生成所需的数据
"""
from readSet import getMovieSet
from utils import toExcel
from glove import coMatrix
from warnings import filterwarnings
filterwarnings('ignore')

ms = getMovieSet()
dic = []
for i in range(len(ms["id"])):
    dic+=ms["genres"][i]
    dic = list(set(dic))
toExcel(dic,"dict")
coMatrix(ms["genres"])