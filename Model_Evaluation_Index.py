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
     _index = data.iloc[:, 1] / data.sum(axis=1).astype(float)
     FPR = _index[0]
     TPR = _index[1]
     return TPR, FPR


def ROC(y, y_predict):
    Y = pd.Series(np.array(y).reshape(len(y)))
    Y_predict = pd.Series(np.array(y_predict).reshape(len(y_predict)))
    unique = np.sort(Y_predict.unique())
    classification_points = []
    for i in np.arange(len(unique)):
        if i != 0:
            classification_point = (unique[i] + unique[i - 1]) / 2.0
            classification_points.append(classification_point)
    X_data = []
    Y_data = []
    for i in classification_points:
        Y_classifi = Y_predict.copy()
        Y_classifi[Y_classifi < i] = 0.0
        Y_classifi[Y_classifi > i] = 1.0
        grouped = Confusion_Matrix(Y, Y_classifi)
        TPR, FPR = _index(grouped)
        X_data.append(FPR)
        Y_data.append(TPR)

    plt.plot(X_data, Y_data)
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










