from readData import getX,getCriAndY#2500 0.39049646258354187
from lstm import LSTM_for_movie_access
from torch.optim import Adam,SGD
from torch.nn import MSELoss
from torch import save,load,no_grad
from globalEpoch import *
# from torchviz import make_dot
from torch.utils.tensorboard import SummaryWriter
# 拟合数据后进行预测
### define parameters here
epochs = 600 # 训练轮数
trainSetSizeProportion = 0.7 # 训练集占比
learningRate = 0.01 # Adam学习率 (0.1 0.05 0.02 0.01 0.01 0.01)
train = True # 训练还是预测
retrain = False # 是否重新训练

'''
tensorboard --logdir=runs/
'''
###

PATH = "modelSave/model{}.pth"#

X = getX()
Cri,y = getCriAndY()
word_vec_len_list = []
for x in X:
    word_vec_len_list.append(x.shape[2])

train_X = []
test_X = []
for x in X:
    train_X.append(x[:int(x.shape[0]*trainSetSizeProportion),:,:])
    test_X.append(x[int(x.shape[0]*trainSetSizeProportion):,:,:])
train_Cri = Cri[:int(Cri.shape[0]*trainSetSizeProportion)]
test_Cri = Cri[int(Cri.shape[0]*trainSetSizeProportion):]
train_y = y[:int(y.shape[0]*trainSetSizeProportion)]
test_y = y[int(y.shape[0]*trainSetSizeProportion):]

model = LSTM_for_movie_access(word_vec_len_list, 64, 2, 1, Cri.shape[1], 1)
globalEpoch = getEpoch()
# output = model(train_X,train_Cri)
# graph=make_dot(output,params=dict(list(model.named_parameters()))) #第一个参数是模型的输出，第二个是模型的参数先列表化再字典化
# graph.render("modelPic")
# graph.view('model_structure','/Users/pc/Desktop/桌面/大三上.nosync/103 商务智能/versionDEC14/lstm/')  #第一个参数是文件名 第二个是保存路径

if train:
    # optimizer = Adam(model.parameters(),lr=learningRate)
    optimizer = SGD(model.parameters(),lr=learningRate)
    writer = SummaryWriter()
    if not retrain:
        # globalEpoch = 900
        print("load",PATH.format(globalEpoch))
        model.load_state_dict(load(PATH.format(globalEpoch)))#
        # model.load_state_dict(load(PATH.format(900)))
    else:
        globalEpoch = 0
    for i in range(epochs):
        output = model(train_X,train_Cri)
        loss = MSELoss()(output.reshape([1,-1]), train_y.reshape([1,-1]).float())
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        print(globalEpoch+i+1,loss.tolist())
        writer.add_scalar('Loss', loss.item(), globalEpoch+i)
    if not retrain:
        addEpoch(epochs)
    else:
        setEpoch(epochs)
    writer.close()
    save(model.state_dict(),PATH.format(globalEpoch+epochs))#
else:
    with no_grad():
        model.load_state_dict(load(PATH.format(globalEpoch)))
        model.eval()
        pred = model(test_X,test_Cri)
        loss = MSELoss()(pred.reshape([1,-1]), test_y.reshape([1,-1]).float())
        print(loss.tolist())