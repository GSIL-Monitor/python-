# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd

data = pd.DataFrame([[1,0,0,-1],[1,0,1,1],[1,1,0,1],[1,1,1,1],[0,0,1,-1],[0,1,0,-1],[0,1,1,1],[0,0,0,-1]],columns=['X1', 'X2', 'X3', 'Y'])

# def Perceptron(data, n):
#     #改成浮点数，方便后续计算
#     data = data.astype(float)
#     #选出特征变量数据集
#     X = data.drop(data.columns[n], axis=1)
#     #选出因变量数据集
#     Y = data.iloc[:, n]
#     #添加“截距”项数据
#     X['Xb'] = -np.ones(len(X))
#     #假设初始W系数及b系数
#     W = np.ones((len(X.columns), 1)) * 0.001
#     while
#         #计算感知器划分结果
#         Y_predict = pd.Series(np.where(X.dot(W) > 0.0, 1, -1).T[0])
#         #
#         W = W + p * (Y - Y_predict).dot(X)




