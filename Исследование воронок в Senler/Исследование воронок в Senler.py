#!/usr/bin/env python
# coding: utf-8

# # Исследование воронок в Senler

# ## Введение
# 
# Я аналитик онлайн-школы Топскул. Отдел маркетинга внедрил две новые автоматизированные воронки, однако их использование не принесло планового количества заявок. Я получил задачу исследовать воронки.
# 
# **Цель исследования**
# - Исследовать воронки.
# 
# **Задачи исследования** 
# - Узнать сколько пользователей доходит до заявки и покупки, а сколько — «застревает» на предыдущих шагах и на каких именно;
# - Изучить открываемость, конверсии в заявку и продажу, долю отписок.
# 
# **Описание данных**
# - EventName — название "шага" в воронке;
# - Users - количество активных пользователей, которые продолжают получать рассылки;
# - Received - количество пользователей, получивших сообщение в шаге;
# - Readed - количество пользователей, прочитавших сообщение в шаге.
# 
# **Ход исследования**
# - Ознакомление с данными;
# - Исследование воронки `100 аргументов для сочинения` и `Вся геометрия на ЕГЭ`:
#      - Рассмотрение следующих показателей: доля отписок, конверсия в заявку, конверсия в продажу;
#      - Визуализация openrate каждого сообщения в шаге;
#      - Визуализация воронок;
# - Ответ на вопросы исследования.

# ## Ознакомление с данными

# Импортируем библиотеки

# In[34]:


import pandas as pd
import matplotlib.pyplot as plt
from plotly import graph_objects as go
import seaborn as sns
import re
import warnings
warnings.filterwarnings("ignore") 
from plotly.subplots import make_subplots
import plotly.io as pio


# Импортируем датасеты

# In[35]:


events_by_users_rus = pd.read_csv('funnel_arguments.csv', sep=";")
events_by_users_geometry = pd.read_csv('funnel_geometry.csv', sep=";")


# Изучим информацию о файлах

# In[36]:


events_by_users_rus.info()


# In[37]:


events_by_users_rus


# In[38]:


events_by_users_geometry.info()


# In[39]:


events_by_users_geometry


# ### Вывод
# 
# - С данными все в порядке, можно приступать к анализу.

# ## Воронка `100 аргументов для сочинения`

# Добавим показатель `openrate`

# In[40]:


events_by_users_rus.loc[events_by_users_rus['event_name'] == 'Подготовка к сочинению', 'event_name'] = 'Сочинение'
events_by_users_rus['openrate'] = round(events_by_users_rus['readed'] / events_by_users_rus['received'],2)
events_by_users_rus.head(8)


# Рассмотрим показатели оттока клиентов, конверсии в заявку и продажу

# In[41]:


print(f"Доля отписок: {100 - ((3364/6881) * 100):.2f}%")
print(f"Конверсия в заявку: {(152/6881) * 100:.2f}%")
print(f"Конверсия в продажу: {(1/152) * 100:.2f}%")


# Рассмотрим openrate по шагам с помощью графика

# In[42]:


event_pivot = events_by_users_rus.query('event_name !="Заявка" and event_name !="Автоменеджер" and event_name !="Продаж"').sort_values(by = 'received', ascending = False)

plt.figure(figsize=(12,6))
sns.barplot(x='openrate', y='event_name', data=event_pivot, palette='gnuplot_r');
plt.xlabel('Openrate')
# plt.grid()
plt.ylabel('Шаги')
plt.title('Openrate по шагам')
plt.show();


# Визуализируем воронки и наглядно рассмотрим на каких шагах мы теряем пользователей

# In[44]:


fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Funnel(name = 'От первого шага',
y = (events_by_users_rus.sort_values('received', ascending=False)['event_name']),
x = (events_by_users_rus.sort_values('received', ascending=False)['received']),
textposition = "inside",
textinfo = "value+percent initial",  #value+percent previous+
connector = {"fillcolor": '#bde0eb'},
insidetextfont = {'color': 'white', 'size': 14}), row=1, col=1)

fig.add_trace(go.Funnel(name = 'От предыдущего шага',
y = (events_by_users_rus.sort_values('received', ascending=False)['event_name']),
x = (events_by_users_rus.sort_values('received', ascending=False)['received']),
textposition = "inside",
textinfo = "value+percent previous",
connector = {"fillcolor": '#bde0eb'},
insidetextfont = {'color': 'white', 'size': 14}), row=1, col=2)

fig.update_layout(title_text='Воронка "100 аргументов"')
fig.show(renderer="svg", width=1000, height=500)


# ### Выводы и рекомендации
# 
# - **Доля отписок:** 51.11%. 
# 
# 
# - **Конверсии.** Конверсия в заявку: 2.21%. Конверсия в продажу: 0.66%. Учитывая конверсии в заявку и продажу, их количество -  необходима переработка оффера и УТП.
# 
# 
# - **Чтобы повысить openrate полезных видео и контента необходимы более "яркие" названия.**
# `Когда лучше всего начать подготовку к ЕГЭ по русскому языку, чтобы получить 90+ ⁉️` - слишком длинное и как показывают цифры не привлекает внимания. Возможно более короткий заголовок позволит удерживать внимание аудитории. 
# 
# 
# - **Высокий openrate** оффера вызван тем, что пользователи не оставившие заявку, получают его снова и снова. Это может выжечь аудиторию и повлечь большое количество отписок. 

# ## Воронка `Вся геометрия на ЕГЭ`

# Добавим показатель `openrate`

# In[45]:


events_by_users_geometry['openrate'] = round(events_by_users_geometry['readed'] / events_by_users_geometry['received'],2)
events_by_users_geometry.head(15)


# Рассмотрим показатели конверсии и оттока клиентов

# In[46]:


print(f"Доля отписок: {100 - ((1128/1646) * 100):.2f}%")
print(f"Конверсия в заявку: {(29/996) * 100:.2f}%")


# Рассмотрим `openrate` на графике

# In[47]:


event_pivot_geometry = events_by_users_geometry.query('event_name !="Заявка" and event_name !="Автоменеджер" and event_name !="Продаж"').sort_values(by = 'received', ascending = False)

plt.figure(figsize=(12,6))
sns.barplot(x='openrate', y='event_name', data=event_pivot_geometry, palette='gnuplot_r');
plt.xlabel('Openrate')
#plt.grid()
plt.ylabel('Шаги')
plt.title('Openrate по шагам')
plt.show();


# Визуализируем воронки и наглядно рассмотрим на каких шагах мы теряем пользователей

# In[48]:


fig = make_subplots(rows=1, cols=2)

fig.add_trace(go.Funnel(name = 'От первого шага',
y = (events_by_users_geometry.sort_values('received', ascending=False)['event_name']),
x = (events_by_users_geometry.sort_values('received', ascending=False)['received']),
textposition = "inside",
textinfo = "value+percent initial",  #value+percent previous+
connector = {"fillcolor": '#bde0eb'},
insidetextfont = {'color': 'white', 'size': 14}), row=1, col=1)

fig.add_trace(go.Funnel(name = 'От предыдущего шага',
y = (events_by_users_geometry.sort_values('received', ascending=False)['event_name']),
x = (events_by_users_geometry.sort_values('received', ascending=False)['received']),
textposition = "inside",
textinfo = "value+percent previous",
connector = {"fillcolor": '#bde0eb'},
insidetextfont = {'color': 'white', 'size': 14}), row=1, col=2)

fig.update_layout(title_text='Воронка "Вся геометрия на ЕГЭ"')
fig.show()


# ### Выводы и рекомендации
# 
# - **Доля отписок:** 31.47%;
# 
# 
# - **Конверсии.** Конверсия в заявку: 2.91%. Продаж с воронки не было. Показатель конверсии в заявку говорит о том, что необходимо проработать УТП и оффер.
# 
# 
# - **Падает openrate** для "шагов-кнопок", где пользователю необходимо совершить действие - нажать на кнопку "Продолжить". На мой взгляд большое количество таких шагов выглядит навязчиво. Рекомендую объединить сообщения такие как приветствие и сегментацию, прогревающие видео и предложение "продолжить воронку". Для шагов с прогревающим контентом - необходима работа с заголовками, для повышения опенрейта.

# ## Общий вывод
# 
# - Исследование воронок выявило высокий процент отписок, низкие конверсии и снижение опенрейта для шагов, в которых пользователь получает полезный контент. Необходима полная переработка и проведение A/B тестов.
