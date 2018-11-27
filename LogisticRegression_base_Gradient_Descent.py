import numpy as np
import pandas as pd


# data格式为m*(i+1)，其中m是指样本个数，i为特征变量维度（包括一列为标签结果Y）。params格式应为（i+1）*1，（i+1）为特征变量权重系数

def Logic_func(X, params): #逻辑回归的分类模型
    return 1 / (1 + np.exp(X.dot(params)))

def Logic_cost(X, Y, params): #逻辑回归的代价函数
    Y_predict = Logic_func(X, Y, params)
    return -(Y * np.log(Y_predict) + (1 - Y) * np.log(1 - Y_predict)).sum()

def LRGD(data, n, times=10000, threshold_change=0.0001, alpha=0.001, error_threshold=0.05):
    #数据处理
    data = data.astype(float)
    data['x0'] = 1.0
    X = data.drop(data.columns[n], axis=1)
    Y = data.iloc[:, n]

    count = 0
    params = np.zeros((len(data.columns), 1))
    errors_dict = {}
    params_dict = {}

    while count <= times: #执行times次梯度下降
        if count == 0: #第一次执行时，为了实现下降幅度阈值，做了区分
            error = Logic_cost(X, Y, params)
            errors_dict[count] = error
            params_dict[count] = params
            Y_predict = Logic_func(X, params)
            params = params - np.array(alpha * (((Y_predict - Y).dot(X)) / float(len(Y)))).reshape(params.shape[0], 1) #更新params
            count = count + 1
            error = Logic_cost(X, Y, params)
            if error <= error_threshold: #本次params实现的误差小于阈值，提前终止梯度下降
                break
        else:
            if abs(error-errors_dict[count-1]) > threshold_change:
                error = Logic_cost(X, Y, params)
                errors_dict[count] = error
                params_dict[count] = params
                Y_predict = Logic_func(X, params)
                params = params - np.array(alpha * (((Y_predict - Y).dot(X)) / float(len(Y)))).reshape(params.shape[0], 1)
                count = count + 1
                error = Logic_cost(X, Y, params)
                if error <= error_threshold:
                    break
            else: #本次梯度下降带来的误差削减幅度小于阈值，提前终止梯度下降
                break
    return params, errors_dict, params_dict






