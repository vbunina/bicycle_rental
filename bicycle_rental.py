import pandas as pd
import seaborn as sns
import numpy as np

sns.set(rc={'figure.figsize': (12,6)}, style="whitegrid")

#загрузим данные об аренде велосипедов в Лондоне с 4 января 2015 по 3 января 2017, проверим число наблюдений и столбцов, наличие пропусков (их нет). убедимся, что типы данных были прочитаны правильно. приведём переменную времени к типу datetime64[ns]
df_bicycles_rent = pd.read_csv('https://stepik.org/media/attachments/lesson/384464/london.csv', parse_dates=['timestamp'])
df_bicycles_rent.shape
df_bicycles_rent.dtypes
df_bicycles_rent.isna().sum()

#для начала постоим график, чтобы посмотреть на число поездок по датам и времени
sns.lineplot(x='timestamp', y='cnt', data=df_bicycles_rent)

#так как наблюдений слишком много и трудно выделить тренды, преобразуем данные (агрегируем число поездок по дням) с помощью метода .resample и снова построим график
df_bicycles_rent = df_bicycles_rent.set_index('timestamp')
sum_of_cnt = df_bicycles_rent.resample(rule='D').agg({'cnt':'sum'})
sns.lineplot(x='timestamp', y='cnt', data=sum_of_cnt)

#чтобы сгладить ряд, посчитаем скользящее среднее с окном 3
sum_of_cnt_window = sum_of_cnt.rolling(3).mean()

#посчитаем стандартное отклонение
std_cnt = np.std(sum_of_cnt['cnt'] - sum_of_cnt_window['cnt'])

#соберём все полученные данные в один датафрейм
sum_of_cnt_window = sum_of_cnt_window.rename(columns={'cnt': 'cnt_window'})
cnt_comparison = pd.merge(sum_of_cnt, sum_of_cnt_window, on='timestamp')

#определим границы интервалов, запишем их в новые столбцы
cnt_comparison['upper_bound'] = cnt_comparison.cnt_window + 2.576 * std_cnt
cnt_comparison['lower_bound'] = cnt_comparison.cnt_window - 2.576 * std_cnt

#посмотрим, чему равно значение верхней границы для последнего наблюдения
cnt_comparison.groupby('timestamp').max()

#выведем наблюдения, для которых наблюдаемые значения оказались больше верхней границы 99% доверительного интервала, а также когда число аренд оказалось ниже ожидаемого
cnt_comparison.query('cnt > upper_bound')
cnt_comparison.query('cnt < lower_bound')