"""
生成热力图
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import griddata
from pandas import read_csv
x = np.array([[i+1 for i in range(19)]])
y = np.array([[i+1 for i in range(19)]]).T
labels = ["Adventure",
"Foreign",
"Drama",
"Action",
"Romance",
"Mystery",
"Fantasy",
"Comedy",
"Animation",
'Documentary',
"Family",
"Thriller",
"Western",
"Science Fiction",
"Crime",
"Music",
"War",
"Horror",
"History",]
xr = np.repeat(x,19,axis=0)
yr = np.repeat(y,19,axis=1)
print(xr)
print(yr)
comat = read_csv("coMat.csv")
z = np.array(comat)
print(z)
c = plt.pcolormesh(xr, yr, z, cmap='Blues')
plt.colorbar(c, label='Frequency')
plt.xticks(ticks=x[0],labels=labels,rotation=90)
plt.yticks(ticks=x[0],labels=labels)
plt.tight_layout()
plt.show()