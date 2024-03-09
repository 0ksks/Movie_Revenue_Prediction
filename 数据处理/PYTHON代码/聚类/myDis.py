"""
自定义的距离函数
"""
from utils import compareStr
def affinity(lia,lib):
    aLen,bLen = len(lia),len(lib)
    if aLen==0 and bLen==0:return 1
    elif aLen==0 or bLen==0:return 0
    else:
        aPointer,bPointer = 0,0
        same = 0
        while aPointer<aLen and bPointer<bLen:
            strA,strB = lia[aPointer],lib[bPointer]
            if strA==strB:
                same+=2
                aPointer+=1
                bPointer+=1
            else:
                if compareStr(strA,strB)==0:bPointer+=1
                else:aPointer+=1
        while bPointer<bLen:
            strA,strB = lia[aPointer-1],lib[bPointer]
            if strA==strB:
                same+=2
                bPointer+=1
            elif compareStr(strA,strB)==0:bPointer+=1
            else:break
        while aPointer<aLen:
            strA,strB = lia[aPointer],lib[bPointer-1]
            if strA==strB:
                same+=2
                aPointer+=1
            elif compareStr(strA,strB)==1:aPointer+=1
            else:break
        return same/(aLen+bLen)
