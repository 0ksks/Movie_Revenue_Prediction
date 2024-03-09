# 记录训练次数
def addEpoch(epoch):
    with open("globalEpoch.txt","r") as f:
        oldEpoch = f.read()
    with open("globalEpoch.txt","w") as f:
        newEpoch = str(int(oldEpoch)+epoch)
        f.write(newEpoch)
def getEpoch():
    with open("globalEpoch.txt","r") as f:
        oldEpoch = int(f.read())
    return oldEpoch
def setEpoch(epoch):
    with open("globalEpoch.txt","w") as f:
        f.write(str(epoch))