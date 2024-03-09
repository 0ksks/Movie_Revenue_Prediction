"""
线性回归，并处理多重共线性
"""
import pandas as pd
import statsmodels.formula.api as smf
import toad
df = pd.read_csv("pureLR.csv").iloc[:,:-2]
# df = df.drop(["release_date",],axis=1)
runtimeMean = 190
for i in range(df.shape[0]):
    df["runtime"][i] = df["runtime"][i] - runtimeMean if df["runtime"][i]>runtimeMean else runtimeMean - df["runtime"][i]
y = df["revenue"]
final = toad.selection.stepwise(df,
                                target = 'revenue',
                                estimator='ols', 
                                direction = 'both', 
                                criterion = 'aic'
                                )
X = final.iloc[:,1:]
model = smf.ols('y~X', data=final).fit()
columns = ["c",]+list(X.columns)
corrs = list(zip(columns,model.params))
print(corrs)
maxLen0 = 0
maxLen1 = 0
for corr in corrs:
    if len(corr[0])>maxLen0:maxLen0=len(corr[0])
    if len(str(corr[1]))>maxLen1:maxLen1=len(str(corr[1]))
for corr in corrs:
    print(("{:<%d}\t{:<%d}"%(maxLen0,maxLen1)).format(*corr))
print(model.summary())
# corr = list(round(X.corr(),3).values)
# for i in range(len(corr)):
#     corr[i] = list(corr[i])
# imax = 0
# jmax = 0
# mmax = 0
# for i in range(len(corr)):
#     for j in range(len(corr)):
#         if corr[i][j]!=1:
#             if corr[i][j]>mmax:
#                 imax = i
#                 jmax = j
#                 mmax = corr[i][j]
# print(imax,jmax,mmax)