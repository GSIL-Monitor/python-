# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np



#计算累积概率，column_name为累计概率列名，n为计算的原始数据列索引
def Cumulative_Value(data, column_name, n):
    for i in np.arange(len(data)):
        if i == 0:
            data.loc[i, column_name] = data.iloc[i, n]
        else:
            data.loc[i, column_name] = data.iloc[:i+1, n].sum()

