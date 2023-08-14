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
    filter_sec = ['SBER']
    df_row = df.to_numpy().tolist()

    for row in df_row:
        # фильтруем поток по выбранным инстментам
        for i in filter_sec:
            if row[2] == i:
                tree.insert("", END, values=row)

def analise():
    btn.configure(state=DISABLED)
    root.after(3000, lambda: analise())
    listbox1.insert(0, "Проверяем ленту-")
    new_list = []
    for k in tree.get_children(""):
        row = tree.item(k)
        new_list.append(row['values'])
    df_a = pd.DataFrame(new_list, columns=['key1', 'key2', 'key3', 'key4', 'key5', 'key6', 'key7'])
    subset2 = ['key2']
    que = df_a.duplicated(subset=subset2, keep=False)
    df1 = df_a[que].groupby(subset2)['key5'].sum().reset_index()
    #df1 = df_a[~que].groupby(subset2)['key5'].sum().reset_index()
    #df1 = df_a.groupby(subset2)['key5'].sum().reset_index()
    print(df_a)
    print(df1)



# создаем блок для загруки данных из файла
frame1 = ttk.LabelFrame(text='Таблица обезличенных сделок', width=1000, height=800)
frame1.grid(column=0, row=0, padx=5, ipady=200, ipadx=220)

# создаем блок для управления
frame2 = ttk.LabelFrame(text='2', width=300, height=200)
frame2.grid(column=1, row=0, sticky=N, padx=10, ipady=50, ipadx=45)
# таблица для анализа
frame4 = ttk.LabelFrame(text='Расчёт', width=450, height=250)
frame4.grid(column=1, row=0, padx=0, pady=0, ipady=100, ipadx=190, sticky=S)

frame3 = ttk.LabelFrame(text='log frame', width=300, height=200)
frame3.grid(column=0, row=1, padx=5, sticky=W, ipadx=3, columnspan=3)

listbox1 = Listbox(frame3, width=180)
listbox1.pack(side='left')

label1 = ttk.Label(frame2, text='Выборка по инструменту:')
label1.grid(column=0, row=1)

label2 = ttk.Label(frame2, text='Выыбран инструмент - ')
label2.grid(column=0, row=2)

labe3 = ttk.Label(frame2, text='')
labe3.grid(column=1, row=2)

open_button = ttk.Button(frame2, text="Подключиться", command=get_data)
open_button.grid(column=0, row=0)

btn = ttk.Button(frame2, text='Анализ', command=analise)
btn.grid(column=1, row=0)

text_label = ttk.Label(text="")
text_label.grid(column=1, row=0, sticky=W, padx=10, columnspan=50)

# определяем столбцы
columns = ('key1', 'key2', 'key3', 'key4', 'key5', 'key6', 'key7')

tree = ttk.Treeview(frame1, columns=columns, show="headings")
tree.place(relheight=1, relwidth=1)
tree.bind()

treescrolly = ttk.Scrollbar(frame1, orient="vertical", command=tree.yview)
treescrollx = ttk.Scrollbar(frame1, orient='horizontal', command=tree.xview)
tree.configure(xscrollcommand=treescrollx.set, yscrollcommand=treescrolly.set)
treescrolly.pack(side='right', fill='y')
treescrollx.pack(side='bottom', fill='x')

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
tree.column("#3", stretch=NO, width=100)
tree.column("#4", stretch=NO, width=60)
tree.column("#6", stretch=NO, width=60)
tree.column("#7", stretch=NO, width=60)

# определяем столбцы для таблицы 2
columns2 = ('key1', 'key2', 'key3', 'key4', 'key5',)

tree2 = ttk.Treeview(frame4, columns=columns2, show="headings")
tree2.place(relheight=1, relwidth=1)

treescrolly2 = ttk.Scrollbar(frame4, orient="vertical", command=tree2.yview)
treescrollx2 = ttk.Scrollbar(frame4, orient='horizontal', command=tree2.xview)
tree2.configure(xscrollcommand=treescrollx2.set, yscrollcommand=treescrolly2.set)
treescrolly2.pack(side='right', fill='y')
treescrollx2.pack(side='bottom', fill='x')

# определяем заголовки
tree2.heading("key1", text="Время", anchor=W)
tree2.heading("key2", text="Инструмент ", anchor=W)
tree2.heading("key3", text="Тикер", anchor=W)
tree2.heading("key4", text="Направление")
tree2.heading("key5", text="Кол-во")

# настраиваем столбцы
tree2.column("#1", stretch=NO, width=110)
tree2.column("#2", stretch=NO, width=60)
tree2.column("#3", stretch=NO, width=100)
tree2.column("#4", stretch=NO, width=60)
tree2.column("#5", stretch=NO, width=60)

if __name__ == "__main__":

    root.protocol("WM_DELETE_WINDOW", exit)
    root.mainloop()
