from get_data import *
def cal_ema(arr,alpha):
    series = pd.Series(arr)
    return series.ewm(alpha=alpha,adjust=False).mean().iloc[-1]


# 选取5阶作为信号
ema_window = 90
alpha = ema_window + 1
# singal_series = temp_df['moment_5'].ewm(alpha=2/alpha,adjust=False).mean()
singal_series = temp_df['moment_5'].rolling(ema_window).apply(cal_ema, kwargs={'alpha': 2 / alpha}, raw=False)
# 获取昨日信号
per_singal = singal_series.shift(1)
# 当然信号大于上日信号
cond = singal_series > per_singal


# 获取持仓

def get_position(ret: pd.Series, cond: pd.Series) -> pd.DataFrame:
    df = pd.concat([ret, cond], axis=1)  # 收益率与信号合并
    df.columns = ['ret', 'cond']

    position = []  # 储存开仓信号，1为持仓，0为空仓
    for idx, row in df.iterrows():
        if position:
            # 当然出现开仓信号，上一日未持仓
            if row['cond'] and position[-1] == 0:
                position.append(1)
            # 当然有开仓信号，上日有持仓，大于止损线
            elif row['cond'] and position[-1] == 1 and row['ret'] >= -0.1:
                position.append(1)
            else:
                position.append(0)
        else:
            if row['cond']:
                position.append(1)
            else:
                position.append(0)
    df['position'] = position
    return df


# 获取
algorithm_return = get_position(ret, cond)

algorithm_return = algorithm_return['ret'].shift(-1) * algorithm_return['position']

cum = (1 + algorithm_return).cumprod()
benchmark = (1 + ret).cumprod()
plt.rcParams['font.family']='serif'
# 高阶矩净值
pd.DataFrame({'algorithm_return':cum,'benchmark':benchmark}).plot(title='高阶距择时',figsize=(18,8))