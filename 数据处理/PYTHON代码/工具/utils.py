"""
一些优化代码，例如快速存取，展示进度条，二分查找等
"""
import pandas as pd
import sys

fpath = ""#路径头

def figLen(i):#数字位数
    s = 0
    while i!=0:
        s+=1
        i//=10
    return s

def getIdx(li,val):#返回元素索引
    ld = 0
    hd = len(li) - 2
    md = (ld+hd)//2
    lu = ld
    hu = hd
    mu = md
    while ld<hd:
        if ord(li[md][0])<ord(val[0]):ld = md+1
        else:hd = md
        md = ld+hd
        md//=2
    while lu<hu:
        if ord(li[mu][0])>ord(val[0]):hu = mu-1
        else:lu = mu
        mu = lu+hu+1
        mu//=2   
    for i in range(md,mu+1):
        if li[i]==val:return i
    return -1

def toExcel(li,fn,p=1):#存入excel
    if p==1:
        print()
        print(fn+"正在储存",end="")
        sys.stdout.flush()
    s = fpath+fn+".xlsx"
    if isinstance(li,list): pd.DataFrame(li).to_excel(s,index=False)
    else: li.to_excel(s,index=False)
    if p==1:
        sys.stdout.flush()
        print("\r"+fn+"储存完成")

def fromExcel(fn,setCol=False,p=1):#读取excel
    if p==1:
        print()
        print("\r",end="")
        print(fn+"正在读取",end="")
        sys.stdout.flush()
    s = fpath+fn+".xlsx"
    if setCol: res = pd.read_excel(s,index_col=0)
    else: res = pd.read_excel(s)
    if p==1:
        sys.stdout.flush()
        print("\r"+fn+"读取完成")
    return res

def toCsv(li,fn,p=1):#存入csv
    if p==1:
        print()
        print(fn+"正在储存",end="")
        sys.stdout.flush()
    s = fpath+fn+".csv"
    if not isinstance(li,pd.DataFrame): pd.DataFrame(li).to_csv(s,index=False)
    else: li.to_csv(s,index=False)
    if p==1:
        sys.stdout.flush()
        print("\r"+fn+"储存完成")

def fromCsv(fn,p=1):#读取csv
    if p==1:
        print()
        print("\r",end="")
        print(fn+"正在读取",end="")
        sys.stdout.flush()
    s = fpath+fn+".csv"
    res = pd.read_csv(s)
    if p==1:
        sys.stdout.flush()
        print("\r"+fn+"读取完成")
    return res

def procedure(i,lgth,st="",ed=""):#进度条
    tlg = figLen(lgth)
    ilg = figLen(i)
    print("\r",end="")
    procedure = round((i)/lgth*100)+1
    if procedure>100:procedure=100
    cnt = str(i+1)
    cnt += (tlg-ilg)*" "
    perc = str(procedure)
    tmp = " %s/%d"%(cnt,lgth)+" %s"%(perc)+"% "+(3-len(perc))*" "
    if i!=lgth-1:
        print(st+tmp,"-"*(procedure//2),"·"*(50-procedure//2),end="",sep="")
    else:
        print(ed," %d/%d"%(lgth,lgth)," %s"%(100)+"% ","-"*(51),end="\t",sep="")
    sys.stdout.flush()

def compareStr(s1,s2):#返回更大的
    s1Len = len(s1)
    s2Len = len(s2)
    i = 0
    while i<s1Len and i<s2Len:
        s1Ord = ord(s1[i])
        s2Ord = ord(s2[i])
        if s1Ord==s2Ord:i+=1
        elif s1Ord>s2Ord:return 0
        else:return 1
    return 0 if s1Len>s2Len else 1

def qs(arr,reverse=False):#默认从小到大排序
    if len(arr) >= 2:
        key = arr[len(arr)//2] #选取基准值
        right,left = [],[] #定义左右两侧数组
        arr.remove(key) #从原数组中移除基准值
        for i in arr:
            flag = compareStr(i,key)
            if reverse:
                if flag==0:
                    left.append(i)
                else:
                    right.append(i)
            else:
                if flag==1:
                    left.append(i)
                else:
                    right.append(i)
        return qs(left,reverse)+[key]+qs(right,reverse)
    else:
        return arr

