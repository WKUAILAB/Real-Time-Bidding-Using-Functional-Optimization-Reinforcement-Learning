import math
import numpy as np
import pandas as pd

batch_size = 20
gamma = 0.95

epsilon_start = 1.0
epsilon_final = 0.01
epsilon_decay = 20000


def epsilon_by_frame(request):
    return epsilon_final + (epsilon_start - epsilon_final) * math.exp(
        -1. * request / epsilon_decay)

def win_prob_second(data):
    #print(data)
    bk = sorted(data["bi"].unique())
    dj = list()
    nj = list()
    wo = list()
    for i in bk:
        # loss = len(data[(data["zi"] < i-1) & (data["wi"]==1)]) + len(data[(data["bi"] <= i-1) & (data["wi"]==0)])
        nj.append(len(data[(data['zi'] >= i-1) & (data['wi']==1)]) + len(data[(data['bi'] >= i) & (data['wi']==0)]))
        dj.append(len(data[(data["zi"] == i-1) & (data["zi"]>0)]))
        # nj.append(8 - loss)
    wo =[1]
    for c,i,j,k in zip(range(len(bk)),bk,nj,dj):
        if c>0:
             wo.append(((j-k)/(j+0.0000001)) * wo[c-1])
    wo = list(map(lambda x:1-x,wo))
    return pd.DataFrame({"bj":bk,"nj":nj,"dj":dj,"w(bj)":wo})

if __name__ == '__main__':
    print(epsilon_by_frame(150000))
