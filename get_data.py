from jqdata import *
import pandas as pd
import numpy as np
import pickle
from tqdm import *
import itertools
import matplotlib.pyplot as plt
import matplotlib.dates as mdate
from prettytable import *
from config_operate import *

my_config = MyConfig()
account,pw = my_config.get_jq_account()
auth(account,pw)
# 设置字体 用来正常显示中文标签
plt.rcParams['font.sans-serif'] = ['SimHei']
#mpl.rcParams['font.family']='serif'
# 用来正常显示负号
plt.rcParams['axes.unicode_minus'] = False

# 图表主题
plt.style.use('seaborn')

# 获取数据
price_df = pd.read_csv('HS300.csv')

# 计算每日收益
ret = price_df['close'] / price_df['close'].shift(1) - 1
ret = ret.dropna()
# N阶原点矩计算
def cal_moment(arr: np.array, Order: int):
    return np.mean(arr**Order)
# 计算N阶矩
temp = {}
for n in range(2, 8):
    temp['moment_' + str(n)] = ret.rolling(20).apply(
        cal_moment, kwargs={'Order': n}, raw=False)

# 加入收盘价
temp['close'] = price_df['close']
temp_df = pd.DataFrame(temp)

# 可视化
def plot_twin(df: pd.DataFrame, numRows: int, numCols: int):

    s = numRows * 100 + numCols * 10 + 1
    fig = plt.figure(figsize=(18, 10))
    for i, col_name in enumerate(
        [x for x in df.columns.tolist() if x != "close"]):

        ax1 = fig.add_subplot(s + i)
        df[col_name].plot(ax=ax1, alpha=0.5, label=col_name, color='red')

        plt.xlabel('year')
        ax1.set_ylabel('moment')  # 设置左边纵坐标标签
        plt.legend(loc=2)  # 设置图例在左上方

        ax2 = ax1.twinx()
        df['close'].plot(ax=ax2, grid=True, label='close', alpha=0.4)
        ax1.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m'))
        ax2.set_ylabel('price')  # 设置右边纵坐标标签
        plt.legend(loc=1)  # 设置图例在右上方
        plt.show()
plot_twin(temp_df,3,2)
