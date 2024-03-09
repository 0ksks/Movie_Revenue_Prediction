import torch
# 构造lstm网络
class LSTM_for_movie_access(torch.nn.Module):
    def __init__(self, word_vec_len_list, hidden_size, num_layers, output_size_lstm, criteria_size, output_size_total):
        # word_vec_len_list:int 词向量维度列表 # hidden_size 隐藏层维度 # num_layers 层数 # output_size_lstm 每层lstm输出维度 # criteria_size 不包括词向量在内的其他指标个数 # output_size_total 最终输出维度
        super(LSTM_for_movie_access, self).__init__()
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.lstm_list = []
        self.fc_list = []
        for word_vec_len in word_vec_len_list:
            self.lstm_list.append(torch.nn.LSTM(word_vec_len,hidden_size,num_layers,batch_first=True))
            self.fc_list.append(torch.nn.Linear(hidden_size,output_size_lstm))
        self.total_fc = torch.nn.Linear(len(word_vec_len_list)+criteria_size, output_size_total)
    
    def forward(self, input_x_list, input_criteria):
        # input_x_list:输入词向量数据的列表 # input_criteria:输入的其他指标数据
        out_list = []
        for x,lstm,fc in zip(input_x_list, self.lstm_list, self.fc_list):
            h0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            c0 = torch.zeros(self.num_layers, x.size(0), self.hidden_size)
            h0 = h0.to(torch.float32)
            c0 = c0.to(torch.float32)
            x = x.to(torch.float32)
            out, _ = lstm(x, (h0, c0))
            out = fc(out[:, -1, :])
            out_list.append(out)
        input_criteria = input_criteria.to(torch.float32)
        out_list.append(input_criteria)
        out = torch.cat(out_list,dim=1)
        out = self.total_fc(out)
        return out
        

