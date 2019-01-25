import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#混淆矩阵的前提条件是y_classifi已经被分割点进行过分类了
def Confusion_Matrix(y, y_classifi):
    Y = pd.Series(np.array(y).reshape(len(y)))
    Y_classifi = pd.Series(np.array(y_classifi).reshape(len(y_classifi)))
    data = pd.concat([Y, Y_classifi], axis=1, join='inner')
    data.columns = ['Y', 'Y_classifi']
    grouped = data.groupby(['Y', 'Y_classifi'])['Y_classifi'].count().unstack(1).fillna(0.0)
    return grouped

def _index(data):
    #输入参数中应该默认结构为index[负，正], columns[负，正]，则（0,0）为TN， （0,1）为FP， （1,0）为FN， （1,1）为TP
    #TPR = TP/(TP+FN), FPR = FP/(FP+TN)
     _index = data.iloc[:, 1] / data.sum(axis=1).astype(float)
     FPR = _index[0]
     TPR = _index[1]
     return TPR, FPR


def ROC(y, y_predict):
    Y = pd.Series(np.array(y).reshape(len(y)))
    Y_predict = pd.Series(np.array(y_predict).reshape(len(y_predict)))
    unique = np.sort(Y_predict.unique())
    classification_points = []
    X_data = []
    Y_data = []
    for i in np.arange(len(unique)):
        if i != 0:
            classification_point = (unique[i] + unique[i - 1]) / 2.0
            classification_points.append(classification_point)
            Y_classifi = Y_predict.copy()
            Y_classifi[Y_classifi < classification_point] = 0.0
            Y_classifi[Y_classifi > classification_point] = 1.0
            grouped = Confusion_Matrix(Y, Y_classifi)
            TPR, FPR = _index(grouped)
            X_data.append(FPR)
            Y_data.append(TPR)

    plt.plot(X_data, Y_data)
    plt.xlabel("FPR")
    plt.ylabel("TPR")
    plt.show()
    return classification_points, X_data, Y_data

def AUC(y, y_predict):
    Y = pd.Series(np.array(y).reshape(len(y)))
    Y_predict = pd.Series(np.array(y_predict).reshape(len(y_predict)))
    data = pd.concat([Y, Y_predict], axis=1)
    data.columns = ['Y', 'Y_predict']
    data.sort_values('Y_predict', inplace=True)
    data['Rank'] = np.arange(1, len(Y_predict)+1, 1)
    M = len(data.loc[data['Y']==1.0, 'Rank'])
    N = len(Y) - M
    AUC = (data.loc[data['Y'] == 1.0, 'Rank'].sum() - M*(M+1)/2) / (M * N)
    return AUC

def InformationValues(data, n):
#parameters:  data: 输入m*n格式数据，m行是指样本数据量，n列是指存在（n-1）列特征变量， 剩余一列为因变量
#                n: 因变量值Y列所在列索引值，从0开始计数
    Y_columns = data.columns[n]
    unique_Y = data[Y_columns].unique()
    WOE_data = pd.Series()
    for i in data.columns.drop(Y_columns):
        group_data = data.groupby([i, Y_columns])[Y_columns].count().unstack(1).fillna(0.0)
        group_rate = group_data.div(group_data.sum(0), axis=1)
        woe = (group_rate[unique_Y[0]] - group_rate[unique_Y[1]]) * np.log10(group_rate[unique_Y[0]] / group_rate[unique_Y[1]])
        WOE_data = pd.concat([WOE_data, woe], axis=1)
    WOE_data = WOE_data.iloc[:, 1:].fillna(0.0)
    WOE_data.columns = data.columns.drop(Y_columns)
    WOE_data[WOE_data == np.inf] = 0.000
    InformationValues = WOE_data.sum(0)
    return WOE_data,  InformationValues

def KolmogorovSmirnov(y, y_predict):
    Y = pd.Series(np.array(y).reshape(len(y)))
    Y_predict = pd.Series(np.array(y_predict).reshape(len(y_predict)))
    unique = np.sort(Y_predict.unique())
    classification_points = []
    X_data = []
    Y_data = []
    KS_Values = {}
    for i in np.arange(len(unique)):
        if i != 0:
            classification_point = (unique[i] + unique[i - 1]) / 2.0
            classification_points.append(classification_point)
            Y_classifi = Y_predict.copy()
            Y_classifi[Y_classifi < classification_point] = 0.0
            Y_classifi[Y_classifi > classification_point] = 1.0
            grouped = Confusion_Matrix(Y, Y_classifi)
            TPR, FPR = _index(grouped)
            X_data.append(FPR)
            Y_data.append(TPR)
            KS_Values[classification_point] = (TPR - FPR)


    plt.plot(classification_points, X_data)
    plt.plot(classification_points, Y_data)
    plt.legend(["FPR", "TPR"])
    plt.show()

    return KS_Values










