# -*- coding: utf-8 -*-
import numpy as np
import pandas as pd
import scipy.stats as st
import matplotlib.pyplot as plt
import math as mt
import statsmodels as sm


#以下内容都是一元线性回归内容
data = pd.read_excel(unicode(r'C:\Users\mime\Desktop\某商业银行的主要业务数据.xlsx','utf-8'))
data.set_index(u'分行编号',inplace=True)
fig = plt.figure()    
ax1 = fig.add_subplot(2,2,1)
ax2 = fig.add_subplot(2,2,2)
ax3 = fig.add_subplot(2,2,3)
ax4 = fig.add_subplot(2,2,4)
from matplotlib.font_manager import FontProperties
#通过调用函数确认matplotlib在画图中的中文显示的字体类型为 simkai格式
font_set = FontProperties(fname=r'C:\Windows\Fonts\simkai.ttf',size=12) 
ax1.scatter(data[u'各项贷款余额'],data[u'不良贷款'],color = 'limegreen')
ax1.set_xlabel(u'各项贷款余额',fontproperties=font_set)
ax1.set_ylabel(u'不良贷款',fontproperties=font_set)

ax2.scatter(data[u'本年累计应收贷款'],data[u'不良贷款'],color='tomato')
ax2.set_xlabel(u'累计应收贷款',fontproperties=font_set)
ax2.set_ylabel(u'不良贷款',fontproperties=font_set)

ax3.scatter(data[u'贷款项目个数'],data[u'不良贷款'],color = 'cyan')
ax3.set_xlabel(u'贷款项目个数',fontproperties=font_set)
ax3.set_ylabel(u'不良贷款',fontproperties=font_set)

ax4.scatter(data[u'本年固定资产投资额'],data[u'不良贷款'],color = 'violet')
ax4.set_xlabel(u'固定资产投资额',fontproperties=font_set)
ax4.set_ylabel(u'不良贷款',fontproperties=font_set)
#计算相关系数（correlation coefficient）矩阵
data.corr()
r = data[u'各项贷款余额'].corr(data[u'不良贷款'])
#编译t统计量匿名函数
x = lambda x : abs(x) * mt.sqrt(23 / (1-x**2))
st.t.ppf(1-a/2,len(data.index)-2)

import statsmodels.api as sm
data1 = data.rename(index=str,columns={u'不良贷款':'no_performing loan',u'各项贷款余额':'loan balance',u'本年累计应收贷款':'accumulative receivable loan',u'贷款项目个数':'loan project amount',u'本年固定资产投资额':'fixed investments'})
X = data1['loan balance']
Y = data1['no_performing loan']
X = sm.add_constant(X)  # 添加常数项系数 
model = sm.OLS(Y,X) #Y是因变量 X是自变量
result = model.fit()
result.params #查看回归方程系数
result.summary() #查看线性回归关联概要

#计算估计标准误差测定观测值在直线上的散布情况
from statsmodels.stats.outliers_influence import summary_table
name, data_Y, columns = summary_table(result,alpha=0.05)
Y_e = pd.DataFrame(data_Y,columns = columns)
SSR = (Y_e ** 2).sum(0)
SSR = SSR['Std Error\nResidual']
Se = mt.sqrt(SSR / (len(data1.index)-2))

def gre_values(x,a,b):
    return a*x + b
Y_value = gre_values(data1['loan balance'],a=result.params[1],b=result.params[0])
SSE = ((Y-Y_value)**2).sum()
SST = ((Y-Y.mean())**2).sum()
SSR = ((Y_value-Y.mean())**2).sum()

#计算y的平均值的区间估计范围
def Ey0(x,x0,n,a=0.5):
    t = st.t.ppf(1-a/2,n-2)
    Sy0 = Se * mt.sqrt(1/n + ((x0-x.mean())**2) / (((x-x.mean())**2).sum()))
    return   (gre_values(x0,a=result.params[1],b=result.params[0]) - t*Sy0,  gre_values(x0,a=result.params[1],b=result.params[0]) + t*Sy0)
#计算回归估计值y0的区间估计范围    
def Ey0_1(x,x0,n,a=0.5):
    t = st.t.ppf(1-a/2,n-2)
    Sy0 = Se * mt.sqrt(1+1/n + ((x0-x.mean())**2) / (((x-x.mean())**2).sum()))
    return   (gre_values(x0,a=result.params[1],b=result.params[0]) - t*Sy0,  gre_values(x0,a=result.params[1],b=result.params[0]) + t*Sy0)
    
data_all = pd.concat([X,Y],axis=1,join='inner')
data_all = pd.concat([data_all,Y_value],axis=1,join='inner')
data.columns =[u'贷款余额',u'不良贷款','预测值Y']
data_all['residual'] = data_all[u'不良贷款'] - data_all['预测值Y']
data_all[u'标准化残差'] = data_all['residual'] / Se
