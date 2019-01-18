import pandas as pd
import numpy as np
import datetime as dt
import xlwt as xw
import pyecharts as pch

#读取数据，设定时间为运行代码前一天
day = (dt.datetime.now() - dt.timedelta(days=1)).strftime("%m.%d")
data_apply = pd.read_csv(r'C:\Users\wuzhiqiang\Desktop\贷款进度.csv', engine='python')
data_success = pd.read_csv(r'C:\Users\wuzhiqiang\Desktop\贷款成功.csv', engine='python')

#剔除无效列
data_apply = data_apply.drop(data_apply.columns[1:4] | data_apply.columns[9:], axis=1)
data_success = data_success.drop(data_success.columns[1:5] | data_success.columns[9:11] | data_success.columns[12:], axis=1)

#剔除非颐尔信渠道进件的订单， 杭州美莱无法识别颐尔信三个字，所以使用颐一个字区别
data_apply_stra = data_apply[data_apply['门店名称'].str.contains('颐') == False]
data_success_stra = data_success[data_success['门店名称'].str.contains('颐') == False]
data_apply = data_apply.loc[data_apply[u'门店名称'].str.contains(u'颐'), :]
data_success = data_success.loc[data_success[u'门店名称'].str.contains(u'颐'), :]

#输入数据data, 设定re为检索关键词， store为期望修改的商户名， n为门店的列名
def data_store(data, re, store, n=u'门店名称'):
    data.loc[data[n].str.contains(re), n] = store

#遍历执行缩减商户名称，提高可视化程度
[data_store(data_apply, i, i) for i in [i[:6] for i in data_apply[u'门店名称'].unique()]]
[data_store(data_success, i, i) for i in [i[:6] for i in data_success[u'门店名称'].unique()]]
[data_store(data_apply_stra, i, i) for i in [i[:6] for i in data_apply_stra['门店名称'].unique()]]
[data_store(data_success_stra, i, i) for i in [i[:6] for i in data_success_stra['门店名称'].unique()]]

#贷款申请时间列转化为datetime格式与前一天0点做对比，筛选选择大于其的订单并依照商户、申请时间排序
data_mingxi = data_apply[pd.to_datetime(data_apply[u'贷款申请时间'], format='%Y%m%d %H:%M') > (dt.datetime.now() - dt.timedelta(days=1, hours=9))].sort_values([u'门店名称', u'贷款申请时间'], ascending=False)
today_store = data_mingxi.groupby('门店名称')['贷款本金金额'].sum() #选择前一天各商户的放款量，准备做玫瑰图
data_mingxi[u'贷款本金金额'] = data_mingxi[u'贷款本金金额'].map(lambda x : format(float("%.2f"%x), ',')) #贷款本金金额列做成千位分隔符的str格式

#输入数据data，n为时间数据列所在索引， format为其对应的时间格式， x_name为转化后的时间数据列列名， x为转化的时间数据格式
def date_processing(data, n, format, x_name, x='D'):
    data.index = pd.to_datetime(data[data.columns[n]], format=format)
    l = data.to_period(freq=x)
    l.index.rename(x_name, inplace=True)
    return l

#先添加日期格式时间数据列，再添加月份时间数据列
data_apply = date_processing(data_apply, n=5, format="%Y%m%d %H:%M", x_name='日期').reset_index()
data_success = date_processing(data_success, n=5, format="%Y%m%d %H:%M", x_name='日期').reset_index()
data_apply_stra = date_processing(data_apply_stra, n=5, format="%Y%m%d %H:%M", x_name='日期').reset_index()
data_success_stra = date_processing(data_success_stra, n=5, format="%Y%m%d %H:%M", x_name='日期').reset_index()
data_apply = date_processing(data_apply, n=6, format="%Y%m%d %H:%M", x_name='月份', x='M').reset_index()
data_success = date_processing(data_success, n=6, format="%Y%m%d %H:%M", x_name='月份', x='M').reset_index()
data_apply_stra = date_processing(data_apply_stra, n=6, format="%Y%m%d %H:%M", x_name='月份', x='M').reset_index()
data_success_stra = date_processing(data_success_stra, n=6, format="%Y%m%d %H:%M", x_name='月份', x='M').reset_index()

data_apply['贷款申请时间'] = pd.to_datetime(data_apply['贷款申请时间'], format="%Y%m%d %H:%M")
data_apply_stra['贷款申请时间'] = pd.to_datetime(data_apply_stra['贷款申请时间'], format="%Y%m%d %H:%M")

l = pd.DataFrame(columns=data_apply_stra.columns)
for i in data_apply['门店名称'].unique():
    x = data_apply.loc[data_apply['门店名称']==i, '贷款申请时间'].sort_values().reset_index()
    new_data = data_apply_stra.loc[(data_apply_stra['门店名称']==i) & (data_apply_stra['贷款申请时间'] >= x.iloc[0, 1]), :]
    l = pd.concat([l, new_data], axis=0)

#输入数据data_apply， data_success， n_index为需要分组视角列索引， is_huizong决定是否在输出数据最下方进行汇总， is_sorted决定是否在输出前进行排序， sort_index为排序列所在列索引
def data_huizong(data_apply, data_success, l, n_index, is_huizong=False, is_sorted=False, sort_index=0):
    all_columns = [u'申请量', u'授信失败', u'放款成功', u'累计放款额(元)']
    _index1 = data_apply.columns[n_index]
    _index2 = data_success.columns[n_index]
    x1 = data_apply.groupby(_index1)['客户姓名'].count()
    l1 = data_apply[data_apply['贷款进度'] == '授信失败']
    x2 = l1.groupby(_index1)['客户姓名'].count()
    x3 = data_success.groupby(_index2)['客户姓名'].count()
    x4 = data_success.groupby(_index2)['贷款本金金额'].sum()
    if list(x2) == []:
        x2 = pd.Series(index=x1.index).fillna(0)
    if list(x3) == []:
        x3 = pd.Series(index=x1.index).fillna(0)
    if list(x4) == []:
        x4 = pd.Series(index=x1.index).fillna(0)
    l2 = l.groupby(_index1)['客户姓名'].count()
    if list(l2) == []:
        x5 = 0.0 / x1
    else:
        x5 = l2 / pd.concat([x1, l2], axis=1).sum(1)
    x5.rename('直连进件占比', inplace=True)
    data = pd.concat([x1, x2, x3, x4], axis=1).fillna(0)
    data.columns = all_columns
    data.index = data.index.astype(str)
    x5.index = x5.index.astype(str)

    if is_huizong == True:
        data.loc['汇总'] = list(data.sum(0))
        data[u'通过率%'] = data[u'放款成功'] / data[u'申请量'].fillna(0)
        data[u'件均金额(元)'] = (data[u'累计放款额(元)'] / data[u'放款成功']).fillna(0)
        data_i = data[[data.columns[3], data.columns[-1]]]
        data = data.drop(data.columns[[3, -1]], axis=1)
        x5['汇总'] = x5.mean()
        data = pd.concat([data, data_i, x5], axis=1).fillna(0)
        data.reset_index(0, inplace=True)
        data[data.columns[4]] = data[data.columns[4]].map(lambda x: "%.2f%%" % (x * 100))
        data[data.columns[-3:-1]] = data[data.columns[-3:-1]].applymap(lambda x: format(float("%.2f" % x), ','))
        data[data.columns[-1]] = data[data.columns[-1]].map(lambda x: "%.2f%%" % (x * 100))
        return data
    else:
        data[u'通过率%'] = data[u'放款成功'] / data[u'申请量'].fillna(0)
        data[u'件均金额(元)'] = (data[u'累计放款额(元)'] / data[u'放款成功']).fillna(0)
        data_i = data[[data.columns[3], data.columns[-1]]]
        data = data.drop(data.columns[[3, -1]], axis=1)
        data = pd.concat([data, data_i, x5], axis=1).fillna(0)
        data.reset_index(0, inplace=True)
        if is_sorted == True:
            data.sort_values(data.columns[sort_index], inplace=True, ascending=False)
            data[data.columns[4]] = data[data.columns[4]].map(lambda x: "%.2f%%" % (x * 100))
            data[data.columns[-3:-1]] = data[data.columns[-3:-1]].applymap(lambda x: format(float("%.2f" % x), ','))
            data[data.columns[-1]] = data[data.columns[-1]].map(lambda x: "%.2f%%" % (x * 100))
            return data
        else:
            data[data.columns[4]] = data[data.columns[4]].map(lambda x: "%.2f%%" % (x * 100))
            data[data.columns[-3:-1]] = data[data.columns[-3:-1]].applymap(lambda x: format(float("%.2f" % x), ','))
            data[data.columns[-1]] = data[data.columns[-1]].map(lambda x: "%.2f%%" % (x * 100))
            return data

#获得月汇总数据，日汇总数据，为方便沿axis=0即向下拼接，统一列名，
data_month = data_huizong(data_apply, data_success, l, 0, is_huizong=True)
data_dayly = data_huizong(data_apply, data_success, l, 1)
data_month.columns = data_dayly.columns
data = pd.concat([data_dayly, data_month], axis=0, sort=False)

#获得商户维度按申请量排序汇总数据，按放款额排序汇总数据
store_data_apply = data_huizong(data_apply, data_success, l, 3, is_huizong=False, is_sorted=True, sort_index=1)
store_data_loan = data_huizong(data_apply, data_success, l, 3, is_huizong=False, is_sorted=True, sort_index=-2)

#转化为pyecharts可识别的list格式
x = list(data_dayly.iloc[:, 0])
y1 = list(data_dayly.iloc[:, 2])
y2 = list(data_dayly.iloc[:, 3])
y3 = []
for i in data_dayly.iloc[:, 4]:
    if len(i) == 5:
        y3.append(float(i[:4]))
    else:
        y3.append(float(i[:5]))

y4 = list(data_dayly.iloc[:, 5].map(lambda x: float(x.replace(',', ''))))
y5 = list(data_dayly.iloc[:, 6].map(lambda x: float(x.replace(',', ''))))

#新建page类，可向下放入图表，多张图表同一文件显示
page = pch.Page()
#新建overlap类，可将多个类型图表并入一张图表显示
overlap = pch.Overlap()
#新增bar条形图，line折线图
bar = pch.Bar('当前累计进件指标--日期维度')
line = pch.Line()
#全部显示x轴标签，x轴设置名称，位于末尾，x轴标签旋转45度，y轴设置名称，位于中间，离y轴标签距离35，数据堆叠成一条，开始区域缩放，显示图例，水平显示，最上方显示
bar.add('授信失败', x, y1, xaxis_interval=0, xaxis_name='日期', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='件数', yaxis_name_pos='middle', yaxis_name_gap=35,
        is_stack=True, is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left')
bar.add('放款成功', x, y2, xaxis_interval=0, xaxis_name='日期', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='件数', yaxis_name_pos='middle', yaxis_name_gap=35,
        is_stack=True, is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left')
line.add('通过率', x, y3, xaxis_interval=0, xaxis_name='日期', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='通过率%', yaxis_name_pos='middle',
         is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left',
         line_color="#00FA9A", line_width=3, line_opacity=0.8, mark_line=["average"])
#bar图为基础合并line图，并将line图y轴放置于右边
overlap.add(bar)
overlap.add(line, is_add_yaxis=True)

bar2 = pch.Bar('当前累计放款指标--日期维度')
bar2.add('累计放款额(元)', x, y4, xaxis_interval=0, xaxis_name='日期', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='金额(元)', yaxis_name_pos='middle', yaxis_name_gap=35,
         is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left')
bar2.add('件均金额(元)', x, y5, xaxis_interval=0, xaxis_name='日期', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='金额(元)', yaxis_name_pos='middle', yaxis_name_gap=35,
         is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left', mark_line=["average"])

page.add(overlap)
page.add(bar2)

x1 = list(store_data_apply.iloc[:, 0])
x2 = list(store_data_loan.iloc[:, 0])
y1 = list(store_data_apply.iloc[:, 1])
y2 = list(store_data_apply.iloc[:, 3])
y3 = []
for i in store_data_apply.iloc[:, 4]:
    if len(i) == 5:
        y3.append(float(i[:4]))
    else:
        y3.append(float(i[:5]))
y4 = list(store_data_loan.iloc[:, 5].map(lambda x: float(x.replace(',', ''))))
y5 = list(store_data_loan.iloc[:, 6].map(lambda x: float(x.replace(',', ''))))

overlap = pch.Overlap()
bar = pch.Bar('当前累计进件指标--商户维度')
line = pch.Line()
bar.add('申请订单量', x1, y1, xaxis_interval=0, xaxis_name='商户名称', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='件数', yaxis_name_pos='middle', yaxis_name_gap=35,
        is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left')
bar.add('放款成功', x1, y2, xaxis_interval=0, xaxis_name='商户名称', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='件数', yaxis_name_pos='middle', yaxis_name_gap=35,
        is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left')
line.add('通过率', x1, y3, xaxis_interval=0, xaxis_name='商户名称', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='通过率%', yaxis_name_pos='middle',
         is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left',
         line_color="#00FA9A", line_width=3, line_opacity=0.8, mark_line=["average"])
overlap.add(bar)
overlap.add(line, is_add_yaxis=True)

bar2 = pch.Bar('当前累计放款指标--商户维度')
bar2.add('累计放款额(元)', x2, y4, xaxis_interval=0, xaxis_name='商户名称', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='金额(元)', yaxis_name_pos='middle', yaxis_name_gap=35,
         is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left')
bar2.add('件均金额(元)', x2, y5, xaxis_interval=0, xaxis_name='商户名称', xaxis_name_pos='end', xaxis_rotate=45, yaxis_name='金额(元)', yaxis_name_pos='middle', yaxis_name_gap=35,
         is_datazoom_show=True, datazoom_type='both', is_legend_show=True, legend_orient='horizontal', legend_top='left', mark_line=["average"])

page.add(overlap)
page.add(bar2)

x = list(today_store.index)
y = list(today_store)
pie = pch.Pie('%s当日各商户放款占比'%day, title_pos='center')
pie.add('', x, y, is_label_show=True, rosetype='area', radius=[25, 75], is_legend_show=False)
page.add(pie)

page.render(r'C:\Users\wuzhiqiang\Desktop\报表数据\颐尔信-百度有钱花%s数据图.html'%day)


def excel_process(data, n, sheet):
    # 数据加工，转化为可以被xlwt模块读取的list class， 其中只能出现基础数据格式如str、int、float，不得使用如numpy.float64这种格式数据。
    x = np.array(data.iloc[:len(data) - n, :].T)
    list_data = []
    for i in range(len(x)):
        list1 = []
        for j in x[i]:
            if type(j) == str:
                list1.append(j)
            elif type(j) == np.str_:
                list1.append(str(j))
            else:
                list1.append(float(j))
        list_data.append(list1)

    y = np.array(data.iloc[(len(data)-n):, :])
    list_hz = []
    for i in range(len(y)):
        list1 = []
        for j in y[i]:
            if type(j) == str:
                list1.append(j)
            elif type(j) == np.str_:
                list1.append(str(j))
            else:
                list1.append(float(j))
        list_hz.append(list1)

    style1 = xw.XFStyle()  # 字段名称及汇总使用
    style2 = xw.XFStyle()  # 每天的常规内容
    # 字体设置
    font = xw.Font()
    font.name = u'黑体'
    font.colour_index = 0
    font.height = 16 * 20
    font.bold = True
    style1.font = font
    font = xw.Font()
    font.name = u'华文仿宋'
    font.colour_index = 0
    font.height = 14 * 20
    style2.font = font

    # 设置单元格靠齐方式
    ali = xw.Alignment()
    ali.horz = xw.Alignment.HORZ_RIGHT
    ali.vert = xw.Alignment.VERT_CENTER
    style2.alignment = ali
    ali = xw.Alignment()
    ali.horz = xw.Alignment.HORZ_RIGHT
    ali.vert = xw.Alignment.VERT_CENTER
    style2.alignment = ali

    # 设置单元格边框
    border = xw.Borders()
    border.left = xw.Borders.THIN
    border.right = xw.Borders.THIN
    border.top = xw.Borders.THIN
    border.bottom = xw.Borders.THIN
    border.left_colour = 0 * 40
    border.right_colour = 0 * 40
    border.top_colour = 0 * 40
    border.bottom_colour = 0 * 40
    style1.borders, style2.borders = border, border

    for i in range(len(data.columns)):
        column = sheet.col(i)
        column.width = 256 * (len(data.columns[i]) * 2 + 10)
        for j in range(len(data) + 1):
            if j == 0:
                sheet.write(j, i, data.columns[i], style1)
            elif j > (len(data)-n):
                l = (len(data) - (n))+1
                sheet.write(j, i, list_hz[j - l][i], style1)
            else:
                sheet.write(j, i, list_data[i][j - 1], style2)



def excel_process_color(data, sheet, _list):
    # 数据加工，转化为可以被xlwt模块读取的list class， 其中只能出现基础数据格式如str、int、float，不得使用如numpy.float64这种格式数据。
    x = np.array(data.iloc[:len(data), :].T)
    list_data = []
    for i in range(len(x)):
        list1 = []
        for j in x[i]:
            if type(j) == str:
                list1.append(j)
            else:
                list1.append(float(j))
        list_data.append(list1)


    style1 = xw.XFStyle()  # 字段名称及汇总使用
    style2 = xw.XFStyle()  # 每天的常规内容
    style3 = xw.XFStyle()  # 贷款进度非成功的需要标记单元格背景色

    # 字体设置
    font = xw.Font()
    font.name = u'黑体'
    font.colour_index = 0
    font.height = 16 * 20
    font.bold = True
    style1.font = font
    font = xw.Font()
    font.name = u'华文仿宋'
    font.colour_index = 0
    font.height = 14 * 20
    style2.font, style3.font = font, font

    # 设置单元格靠齐方式
    ali = xw.Alignment()
    ali.horz = xw.Alignment.HORZ_RIGHT
    ali.vert = xw.Alignment.VERT_CENTER
    style2.alignment = ali
    ali = xw.Alignment()
    ali.horz = xw.Alignment.HORZ_RIGHT
    ali.vert = xw.Alignment.VERT_CENTER
    style2.alignment, style3.alignment = ali, ali

    # 设置单元格边框
    border = xw.Borders()
    border.left = xw.Borders.THIN
    border.right = xw.Borders.THIN
    border.top = xw.Borders.THIN
    border.bottom = xw.Borders.THIN
    border.left_colour = 0 * 40
    border.right_colour = 0 * 40
    border.top_colour = 0 * 40
    border.bottom_colour = 0 * 40
    style1.borders, style2.borders, style3.borders = border, border, border

    #设置背景色
    pattern = xw.Pattern()
    pattern.pattern = xw.Pattern.SOLID_PATTERN
    pattern.pattern_fore_colour = 50
    style3.pattern = pattern



    for i in range(len(data.columns)):
        column = sheet.col(i)
        column.width = 256 * (len(data.columns[i]) * 2 + 10)
        for j in range(len(data) + 1):
            if j == 0:
                sheet.write(j, i, data.columns[i], style1)
            elif (j-1) in _list:
                sheet.write(j, i, list_data[i][j - 1], style3)
            else:
                sheet.write(j, i, list_data[i][j - 1], style2)


    column1 = sheet.col(7)
    column1.width = 256 * (len('贷款申请成功') * 2 + 10)
    column2 = sheet.col(8)
    column2.width = 256 * (len('存在两种情况：1.获得额度后撤销 ；2.授信过程中撤销') * 2 + 10)
    sheet.write(0, 7, '贷款进度', style1)
    sheet.write(0, 8, '释义', style1)
    sheet.write(1, 7, '授信处理中', style2)
    sheet.write(2, 7, '授信失败', style2)
    sheet.write(3, 7, '授信成功', style2)
    sheet.write(4, 7, '授信撤销', style2)
    sheet.write(5, 7, '贷款申请成功', style2)
    sheet.write(6, 7, '激活申请中', style2)
    sheet.write(7, 7, '激活失败', style2)
    sheet.write(8, 7, '激活成功', style2)
    sheet.write(9, 7, '贷款撤销', style2)
    sheet.write(10, 7, '交费失败', style2)
    sheet.write(11, 7, '贷款成功', style2)
    sheet.write(1, 8, '提交申请但未获得申请结果', style2)
    sheet.write(2, 8, '申请不通过，未获得额度', style2)
    sheet.write(3, 8, '申请通过，获得额度', style2)
    sheet.write(4, 8, '存在两种情况：1.获得额度后撤销 ；2.授信过程中撤销', style2)
    sheet.write(5, 8, '获得额度，但是并未使用', style2)
    sheet.write(6, 8, '使用额度，激活本次订单', style2)
    sheet.write(7, 8, '本次订单消费拒绝使用额度', style2)
    sheet.write(8, 8, '成功激活订单，但未打款', style2)
    sheet.write(9, 8, '放款阶段撤销订单', style2)
    sheet.write(10, 8, '客户取消消费/存在风险，财务撤销', style2)
    sheet.write(11, 8, '成功完成全程操作', style2)


#新增Workbook类，放入第一个工作簿，写入日期汇总数据
writer = xw.Workbook(encoding='utf-8')
sheet1 = writer.add_sheet(u'本月累计汇总表', True)
n = len(data_month)
excel_process(data, n, sheet1)

#遍历各商户，写入各商户日期汇总数据
for i in data_apply[u'门店名称'].unique():
    data_x = data_apply[data_apply[u'门店名称'] == i]
    data_y = data_success[data_success[u'门店名称'] == i]
    l_i = l[l['门店名称']==i]
    data_month_store = data_huizong(data_x, data_y, l_i, n_index=0, is_huizong=True)
    data_dayly_store = data_huizong(data_x, data_y, l_i, n_index=1)
    data_month_store.columns = data_dayly_store.columns
    data_tep = pd.concat([data_dayly_store, data_month_store], axis=0, sort=False)
    sheet = writer.add_sheet("%s"%i, True)
    n = len(data_month_store)
    excel_process(data_tep, n, sheet)

#写入前一天申请明细数据
sheet2 = writer.add_sheet(u'%s进件申请明细表' %day, True)
data_mingxi = data_mingxi.reset_index().drop('index', axis=1)
l = list(data_mingxi[data_mingxi[u'贷款进度'] != u'贷款成功'].index)
excel_process_color(data_mingxi, sheet2, l)

writer.save(r'C:\Users\wuzhiqiang\Desktop\报表数据\颐尔信-百度有钱花%s进件汇总.xls'%day)