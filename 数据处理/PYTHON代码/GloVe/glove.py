"""
glove相关计算，详情参照论文
"""
import random as r
import math
from utils import *
from vec import *
from matplotlib.pyplot import plot,show,savefig,title
from UUID import getData
from readSet import readKeywordSet

fpath = ""

def getDict(dictName=""):
    if dictName!="":dic = list(fromExcel(dictName+"Dict")[0])
    else:dic = list(fromExcel("dict")[0])
    dic = dict(list(zip(dic,[i for i in range(len(dic))])))
    return dic

def getWord2Vec(dictName=""):
    dic = getDict(dictName)
    vec = getWordVec(dictName)
    for k in dic.keys():
        dic[k] = vec[dic[k]]
    return dic

def avgVect(li):
    dic = getWord2Vec()
    summ = zeroV(len(dic.values()[0]))
    for word in li:
        summ = addE(summ,dic[word])
    summ/=len(li)
    return summ

def coMatrix(msCol,keyword=False):#计算共现矩阵
    dic = getDict()
    n = len(dic)
    coMat=[]
    row = [0 for j in range(n)]
    for i in range(n):
        procedure(i,n,"coMat正在初始化","coMat初始化完成")
        coMat.append(row.copy())
    print()
    if keyword:hfmDICT,hfmT=readKeywordSet()
    for row in msCol:
        if keyword:row = getData(row,hfmT)
        for i in range(len(row)):
            for j in range(i+1,len(row)):
                coMat[dic[row[i]]][dic[row[j]]]+=1
                coMat[dic[row[j]]][dic[row[i]]]+=1
    toCsv(coMat,'coMat')

def iniWordVec(dim):#初始化词向量
    dic = fromExcel('dict')
    print(dic)
    n = len(dic[0])
    res = []
    for i in range(n):
        res.append([[r.randint(0,9) for i in range(dim)],[r.randint(0,9) for i in range(dim)]])
    return res

def f(x,alpha=0.75,xmax=3):#损失函数中的fx
    if x>=xmax:
        return 1
    return (x/xmax)**alpha

def wwbbl(wordVec,bi,bj,comat,i,j):#损失函数平方项的底
    if comat[i][j]==0:
        return 0
    summ = 0
    summ += dot(wordVec[i][0],wordVec[j][1])
    summ += bi[i]+bj[j]
    summ += -math.log(comat[i][j])
    return summ

def J(comat,wordVec,bi,bj):#损失函数
    summ = 0
    for i in range(len(comat)):
        for j in range(len(comat)):
            summ += f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j)*wwbbl(wordVec,bi,bj,comat,i,j)
    return summ

def plotLoss():#显示损失函数图像
    with open(fpath+"lossLog.txt") as fp:
        y = fp.read()
    y = "[%s]"%("".join(y.split("\n"))[:-2])
    y = eval(y)
    x = [i+1 for i in range(len(y))]
    plot(x,y)

def getWordVec(wordVecName=""):#读取词向量
    if wordVecName!="": wordVec = fromExcel(wordVecName+"WordVec")
    else: wordVec = fromExcel("wordVec")
    res = []
    for i in range(len(wordVec[0])):
        res.append(addE(eval(wordVec[0][i]),eval(wordVec[1][i])))
    return res

def getSentencesAndLabels():#获取训练集
    finalTrainSet = fromExcel("finalTrainSet",0)
    wordVec = getWordVec()
    sentences = list(map(eval,list(finalTrainSet[2])))
    for i in range(len(sentences)):
        for j in range(len(sentences[i])):
            sentences[i][j]=wordVec[sentences[i][j]]
    labels = list(finalTrainSet[1])
    return (sentences, labels)


def trainWordVec(restart,dim,maxEpoch,eta0,eta1,turning,autoSaving=20,savingConfig=60,percent=0.1,beta1=0.9,beta2=0.999):#训练词向量（restart：是否重新训练；dim：词向量维度；maxEpoch：最大轮数；eta0：初始学习率；eta1：降低后的学习率；turning：降低学习率的轮数
    comat = fromCsv('coMat')
    comat = comat.values.tolist()
    wordVec = []
    if restart == 1:
        wordVec = iniWordVec(dim)
        lossLog = ""
    else:
        wv = fromExcel("wordVec",0)
        for i in range(len(wv[0])):
            wordVec.append([eval(wv[0][i]),eval(wv[1][i])])
        with open(fpath+"lossLog.txt") as fp:
            lossLog = fp.read()
    wordAcnt = len(wordVec)#词数量
    epsilon = 1e-6
    epsilonList = [epsilon for i in range(dim)]
    

    bi = [r.randint(0,9) for i in range(wordAcnt)]
    bj = [r.randint(0,9) for i in range(wordAcnt)]

    v = 0
    s = 0

    beta1t = 1
    beta2t = 1

    batchSize = round(wordAcnt*percent)

    eta = eta0
    for times in range(maxEpoch):#adam
        if times==turning:
            eta = eta1
        beta1t *= beta1
        beta2t *= beta2
        wordGradList = []
        bGradList = []
        centreWordVLast = [zeroV(dim) for i in range(wordAcnt)]
        centreWordSLast = [zeroV(dim) for i in range(wordAcnt)]
        contextWordVLast = [zeroV(dim) for i in range(wordAcnt)]
        contextWordSLast = [zeroV(dim) for i in range(wordAcnt)]
        vLast = [0 for i in range(wordAcnt)]
        sLast = [0 for i in range(wordAcnt)]
        stdFig = str(times+1)+(figLen(maxEpoch)-len(str(times+1)))*" "
        sstr = "epoch "+stdFig+" | word"
        for para in range(wordAcnt):#遍历所有参数
            procedure(para,wordAcnt,sstr,sstr)
            centreWordV = zeroV(dim)
            centreWordS = zeroV(dim)
            contextWordV = zeroV(dim)
            contextWordS = zeroV(dim)
            batchRange = r.sample(range(wordAcnt),batchSize)
            centreWordGrad = zeroV(dim)
            contextWordGrad = zeroV(dim)
            bGrad = 0
            for i in batchRange:#小批量随机梯度
                cewgrad = zeroV(dim)
                cowgrad = zeroV(dim)
                for j in batchRange:
                    cewgrad = addE(cewgrad,SxV(2*f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j),wordVec[j][1]))
                    cowgrad = addE(cowgrad,SxV(2*f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j),wordVec[i][0]))
                    bGrad += 2*f(comat[i][j])*wwbbl(wordVec,bi,bj,comat,i,j)
                centreWordGrad = addE(centreWordGrad,cewgrad)
                contextWordGrad = addE(contextWordGrad,cowgrad)
            centreWordGrad = SxV(1/batchSize, centreWordGrad)
            centreWordV = addE(SxV(beta1, centreWordVLast[para]), SxV(1-beta1, centreWordGrad))
            centreWordS = addE(SxV(beta2, centreWordSLast[para]), SxV(1-beta2, mulE(centreWordGrad, centreWordGrad)))
            centreWordV = SxV(1/(1-beta1t), centreWordV)
            centreWordS = SxV(1/(1-beta2t), centreWordS)
            centreWordVLast[para] = centreWordV
            centreWordSLast[para] = centreWordS
            centreWordGrad = SxV(eta, divE(centreWordV, addE(sqtE(centreWordS), epsilonList)))

            contextWordGrad = SxV(1/batchSize, contextWordGrad)
            contextWordV = addE(SxV(beta1, contextWordVLast[para]), SxV(1-beta1, contextWordGrad))
            contextWordS = addE(SxV(beta2, contextWordSLast[para]), SxV(1-beta2, mulE(contextWordGrad, contextWordGrad)))
            contextWordV = SxV(1/(1-beta1t), contextWordV)
            contextWordS = SxV(1/(1-beta2t), contextWordS)
            contextWordVLast[para] = contextWordV
            contextWordSLast[para] = contextWordS
            contextWordGrad = SxV(eta, divE(contextWordV, addE(sqtE(contextWordS), epsilonList)))

            bGrad = bGrad/batchSize
            v = beta1*vLast[para] + (1-beta1)*bGrad
            s = beta2*sLast[para] + (1-beta2)*bGrad*bGrad
            v = v/(1-beta1t)
            s = s/(1-beta2t)
            bGrad = eta*v/(math.sqrt(s)+epsilon)
            vLast[para] = v
            sLast[para] = s
            wordGradList.append([centreWordGrad,contextWordGrad])

            bGradList.append(bGrad)

        for i in range(wordAcnt):
            wordVec[i][0] = minusE(wordVec[i][0],wordGradList[i][0])
            wordVec[i][1] = minusE(wordVec[i][1],wordGradList[i][1])
            bi[i] -= bGradList[i]
            bj[i] -= bGradList[i]
            # wordVec[i][0] = addE(wordGradList[i][0],wordVec[i][0])
            # wordVec[i][1] = addE(wordGradList[i][1],wordVec[i][1])
            # bi[i] += bGradList[i]
            # bj[i] += bGradList[i]
        loss = J(comat,wordVec,bi,bj)
        print(" loss=%d"%(loss))
        lossLog+="%d,"%(loss)
        if times%10==9:
            lossLog+="\n"
        if times%autoSaving==autoSaving-1:
            print("save")
            toExcel(wordVec,'wordVec',0)
            with open(fpath+"lossLog.txt","w") as fp:
                fp.write(lossLog)
        if times%savingConfig==savingConfig-1:
            a = input("continue?(n to end)")
            if a=="n":break
    toExcel(wordVec,'wordVec')
    with open(fpath+"lossLog.txt","w") as fp:
        fp.write(lossLog)



if __name__=="__main__":
    trainWordVec(0,36,20,0.05,0.05,150,savingConfig=-1,percent=1)#训练词向量
                                                # restart：是否重新训练；
                                                # dim：词向量维度；
                                                # maxEpoch：最大轮数；
                                                # eta0：初始学习率；
                                                # eta1：降低后的学习率；
                                                # turning：降低学习率的轮数；
                                                # autoSaving(20)：自动保存轮数；
                                                # savingconfig(60)：问询保存轮数；
                                                # precent(0.1)：adam批量大小；
    plotLoss()
    figname = "spokenLanguageLoss"
    title(figname)
    show()