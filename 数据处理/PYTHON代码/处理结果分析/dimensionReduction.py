"""
降维可视化
"""
from sklearn.manifold import TSNE
from utils import fromCsv
import matplotlib.pyplot as plt
import numpy as np
model = TSNE(n_components=2,random_state=0)
genreClass = fromCsv("genresClass")
genresVec = fromCsv("genresVec")
X = []
y = []
for vec in genresVec["1"]:
    X.append(eval(vec))
for c in genreClass["1"]:
    y.append(c)
X = np.array(X)
y = np.array(y)
X_dr = model.fit_transform(X)
plt.scatter(X_dr[:,0],X_dr[:,1],c=y,cmap="turbo",alpha=0.5)
plt.xticks([])
plt.yticks([])
plt.show()