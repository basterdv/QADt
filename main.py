import itertools
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno
import pandas as pd
from datetime import datetime
import time  # Подписка на события по времени
from QuikPy import QuikPy  # Работа с QUIK из Python через LUA скрипты QuikSharp

root = Tk()
root.title("Программа по анализу ленты сделок")
root.geometry("1500x675")
qp_provider = QuikPy()  # Подключение к локальному запущенному терминалу QUIK по портам по умолчанию
# root.minsize(width=300, height=400)
# # root.resizable(width=0, height=0)
filter_sec = [('VTBR', '100'),('SBER', '200')]


def close_connect():
    qp_provider.CloseConnectionAndThread()


def exit():
    choice = askyesno(title="Выход", message="Хотите закрыть приложение?")
    if choice:
        close_connect()
        # root.destroy()
        time.sleep(1)  # Ждем кол-во секунд
        root.quit()


def changed_connection(data):
    """Пользовательский обработчик событий:
    - Соединение установлено
    - Соединение разорвано
    """
    # dpg.add_text(f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}', parent='data_w')
    log_index = f'{datetime.now().strftime("%d.%m.%Y %H:%M:%S")} - {data}'
    print(log_index)  # Печатаем полученные данные
    listbox1.insert(0, log_index)


def get_data():
    class_code = 'TQBR'  # Класс тикера
    sec_code = 'SBER'  # Тикер
    # Обезличенные сделки. Чтобы получать, в QUIK открыть Таблицу обезличенных сделок, указать тикер
    qp_provider.OnAllTrade = print_callback  # Обработчик получения обезличенной сделки
    sleep_sec = 0, 5  # Кол-во секунд получения обезличенных сделок
    # print('Секунд обезличенных сделок:', sleep_sec)
    # time.sleep(sleep_sec)  # Ждем кол-во секунд получения обезличенных сделок

    # qp_provider.OnAllTrade = qp_provider.DefaultHandler  # Возвращаем обработчик по умолчанию
    qp_provider.OnConnected = changed_connection  # Нажимаем кнопку "Установить соединение" в QUIK
    qp_provider.OnDisconnected = changed_connection  # Нажимаем кнопку "Разорвать соединение" в QUIK


def print_callback(data):
    """Пользовательский обработчик событий:
    - Изменение стакана котировок
    - Получение обезличенной сделки
    - Получение новой свечки
    """
    lst = data

    hour = str(lst['data']['datetime']['hour'])
    min = str(lst['data']['datetime']['min'])
    sec = str(lst['data']['datetime']['sec'])
    str_d = str(f'{hour}:{min}:{sec}')
    datetime_new = datetime.strptime(str_d, '%H:%M:%S').strftime('%X')

    lst['data']['datetime'] = datetime_new  # меняем значение в поле даты
    # Проверям напряление по номеру флага
    if lst['data']['flags'] == 1025:
        lst['data']['flags'] = 'продажа'
    elif lst['data']['flags'] == 1026:
        lst['data']['flags'] = 'купля'
    else:
        lst['data']['flags'] = '------'

    df = pd.DataFrame([lst['data']])  # тоже самое df = pd.DataFrame(lst2,index=[ 0 ])
    df = df.drop(columns=['exec_market', 'repoterm', 'reporate', 'exchange_code', 'yield', 'open_interest',
                          'repovalue', 'sec_code', 'tradenum', 'settlecode', 'repo2value', 'class_code', 'benchmark',

                          'accruedint', 'period'])
    df = df[['trade_num', 'datetime', 'seccode', 'price', 'qty', 'value', 'flags']]

    # filter_sec = ['SBER','VTBR', 'LKOH']
    #filter_sec = ['SBER']

    df_row = df.to_numpy().tolist()
    new_filter = []
    for i in filter_sec:
        new_filter.append(i[0])

    for row in df_row:
        # фильтруем поток по выбранным инстментам
        for i in new_filter:
            if row[2] == i:
                tree.insert("", END, values=row)


def analise():
    btn.configure(state=DISABLED)
    time_tape = int(input1.get()) * 300
    root.after(time_tape, lambda: analise())

    listbox1.insert(0, f'Проверяем ленту каждые {time_tape / 300} секунд')

    list_sec = []
    for i in tree3.get_children(""):
        row = tree3.item(i)
        list_sec.append(row['values'])

    new_list = []
    for k in tree.get_children(""):
        row = tree.item(k)
        new_list.append(row['values'])

    df_a = pd.DataFrame(new_list, columns=['key1', 'key2', 'key3', 'key4', 'key5', 'key6', 'key7'])
    df_a['key5'] = df_a['key5'].astype('float')
    print(df_a)

    subset2 = ['key2', 'key3', 'key7']
    que = df_a.duplicated(subset=subset2, keep=False)

    # df_a = df_a.astype({'a': df_a.object, 'b': df_a.int8})
    df1 = df_a[que].groupby(subset2)['key5'].sum().reset_index()

    # df1 = df_a[~que].groupby(subset2)['key5'].sum()
    # df1 = df_a.groupby(subset2)['key5'].sum().reset_index()
    # print(df1)

    df1 = df1[['key2', 'key3', 'key5', 'key7']]
    print(df1)
    df_row = df1.to_numpy().tolist()
    tree2.delete(*tree2.get_children())
    for row in df_row:
        for j in range(2):
            if row[1] == list_sec[j][0] and row[2] >= list_sec[j][1]:
                tree2.insert("", END, values=row)


# # создаем блок для загруки данных из файла
# frame1 = ttk.LabelFrame(text='Таблица обезличенных сделок', width=400, height=400)
# frame1.grid(column=0, row=0, padx=5,sticky=W,rowspan=2)
# #frame1.grid(column=0, row=0, padx=5, ipady=200, ipadx=170,sticky=W,rowspan=2)
# # создаем блок для управления
# frame2 = ttk.LabelFrame(text='2', width=100, height=100)
# frame2.grid(column=1, row=0,  padx=5, ipady=50, ipadx=45)
# # таблица для анализа
# frame4 = ttk.LabelFrame(text='Расчёт', width=450, height=250)
# frame4.grid(column=1, row=1, padx=0, pady=0, ipady=100, ipadx=150)
# # Логер
# frame3 = ttk.LabelFrame(text='log frame', width=400, height=200)
# frame3.grid(column=0, row=2, padx=5 , columnspan = 2)

# создаем блок для загруки данных из файла
frame1 = ttk.LabelFrame(text='Таблица обезличенных сделок', width=528, height=500)
frame1.grid(column=0, row=0, padx=5, sticky=W, rowspan=2, )

# frame1.grid(column=0, row=0, padx=5, ipady=200, ipadx=170,sticky=W,rowspan=2)
# создаем блок для управления
frame2 = ttk.LabelFrame(text='2', width=100, height=100)
frame2.grid(column=2, row=0, padx=5, )
# Логер
frame3 = ttk.LabelFrame(text='log frame', width=850, height=250)
frame3.grid(column=0, row=2, columnspan=3, sticky=W, padx=5)
# таблица для анализа
frame4 = ttk.LabelFrame(text='Расчёт', width=400, height=250)
frame4.grid(column=2, row=1, padx=5, sticky=SW)
# Таблица фиксированных значений инструментов
frame5 = ttk.LabelFrame(text='5', width=150, height=500)
frame5.grid(column=1, row=0, rowspan=2)

listbox1 = Listbox(frame3, width=160)
listbox1.pack(side='left')

label1 = ttk.Label(frame2, text='Выборка по инструменту:')
label1.grid(column=0, row=1)

label2 = ttk.Label(frame2, text='Анализ ленты секунд - ')
label2.grid(column=0, row=2)

input1 = ttk.Entry(frame2, width=2, )
input1.grid(column=1, row=2, sticky=W)
input1.insert(0, '25')

labe3 = ttk.Label(frame2, text='')
labe3.grid(column=1, row=2)

open_button = ttk.Button(frame2, text="Подключиться", command=get_data)
open_button.grid(column=0, row=0)

btn = ttk.Button(frame2, text='Анализ', command=analise)
btn.grid(column=1, row=0)

# text_label = ttk.Label(text="")
# text_label.grid(column=1, row=0, sticky=W, padx=10, columnspan=50)

# определяем столбцы
columns = ('key1', 'key2', 'key3', 'key4', 'key5', 'key6', 'key7')

tree = ttk.Treeview(frame1, columns=columns, show="headings", )
vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
vsb.place(x=30 + 481 + 2, y=19, height=458 + 20)
tree.configure(yscrollcommand=vsb.set)
tree.place(relheight=1, relwidth=1)

# tree.bind()
# treescrolly = ttk.Scrollbar(frame1, orient="vertical", command=tree.yview)
# treescrollx = ttk.Scrollbar(frame1, orient='horizontal', command=tree.xview)
# tree.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
# treescrolly.pack(side='right', fill='y')
# treescrollx.pack(side='bottom', fill='x')

# определяем заголовки
tree.heading("key1", text="Номер операции", anchor=W)
tree.heading("key2", text="Время ", anchor=W)
tree.heading("key3", text="Тикер")
tree.heading("key4", text="Цена")
tree.heading("key5", text="Кол-во")
tree.heading("key6", text="Объём")
tree.heading("key7", text="Направление")
# настраиваем столбцы
tree.column("#1", stretch=NO, width=110)
tree.column("#2", stretch=NO, width=60)
tree.column("#5", stretch=NO, width=60)
tree.column("#3", stretch=NO, width=60)
tree.column("#4", stretch=NO, width=60)
tree.column("#6", stretch=NO, width=60)
tree.column("#7", stretch=NO, width=100)

# определяем столбцы для таблицы 2
columns2 = ('key1', 'key2', 'key3', 'key4', 'key5')

tree2 = ttk.Treeview(frame4, columns=columns2, show="headings")
vsb = ttk.Scrollbar(root, orient="vertical", command=tree2.yview)
vsb.place(x=30 + 1042 + 2, y=265, height=230 + 2)
tree2.configure(yscrollcommand=vsb.set)

tree2.place(relheight=1, relwidth=1)

# определяем заголовки
tree2.heading("key1", text="Время", anchor=W)
tree2.heading("key2", text="Тикер", anchor=W)
tree2.heading("key3", text="Кол-во лотов")
tree2.heading("key4", text="Кол-во сделок")
tree2.heading("key5", text="Направление")

# настраиваем столбцы
tree2.column("#1", stretch=NO, width=60)
tree2.column("#2", stretch=NO, width=50)
tree2.column("#3", stretch=NO, width=90)
tree2.column("#4", stretch=NO, width=90)
tree2.column("#5", stretch=NO, width=90)

# Список настроек для инструментов
columns3 = ('key1', 'key2',)

tree3 = ttk.Treeview(frame5, columns=columns3, show="headings")
# vsb = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
# vsb.place(x=30 + 481 + 2, y=19, height=458 + 20)
# tree3.configure(yscrollcommand=vsb.set)

tree3.place(relheight=1, relwidth=1)

# treescrolly3 = ttk.Scrollbar(tree3, orient="vertical", command=tree3.yview)
# treescrollx3 = ttk.Scrollbar(tree3, orient='horizontal', command=tree3.xview)
# tree3.configure(xscrollcommand=treescrollx3.set, yscrollcommand=treescrolly3.set)
# treescrolly3.pack(side='right', fill='y')
# treescrollx3.pack(side='bottom', fill='x')

# определяем заголовки
tree3.heading("key1", text="Тикер", anchor=W)
tree3.heading("key2", text="От лотов", anchor=W)

# настраиваем столбцы
tree3.column("#1", stretch=NO, width=60)
tree3.column("#2", stretch=NO, width=60)

for row in filter_sec:
    tree3.insert("", END, values=row)

if __name__ == "__main__":
    root.protocol("WM_DELETE_WINDOW", exit)
    root.mainloop()
