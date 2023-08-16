from tkinter import *
from tkinter import ttk

root = Tk()
root.title("Программа по анализу ленты сделок")
root.geometry("1500x675")

# # создаем блок для загруки данных из файла
# frame1 = ttk.LabelFrame(text='Таблица обезличенных сделок', width=500, height=400)
# frame1.grid(column=0, row=0, padx=5, ipady=200, ipadx=170,sticky=W,rowspan=2)
#
# # создаем блок для управления
# frame2 = ttk.LabelFrame(text='2', width=300, height=200)
# frame2.grid(column=1, row=0,  padx=5, ipady=50, ipadx=45)
# # таблица для анализа
# frame4 = ttk.LabelFrame(text='Расчёт', width=450, height=250)
# frame4.grid(column=1, row=1, padx=0, pady=0, ipady=100, ipadx=150)
# # Логер
# frame3 = ttk.LabelFrame(text='log frame', width=300, height=200)
# frame3.grid(column=0, row=2, padx=5 )

# создаем блок для загруки данных из файла
frame1 = ttk.LabelFrame(text='Таблица обезличенных сделок', width=400, height=400)
frame1.grid(column=0, row=0, rowspan=2)
#frame1.grid(column=0, row=0, padx=5, ipady=200, ipadx=170,sticky=W,rowspan=2)
# создаем блок для управления
frame2 = ttk.LabelFrame(text='2', width=100, height=100)
frame2.grid(column=1, row=0, )
# таблица для анализа
frame4 = ttk.LabelFrame(text='Расчёт', width=450, height=250)
frame4.grid(column=1, row=1,)
# Логер
frame3 = ttk.LabelFrame(text='log frame', width=800, height=200)
frame3.grid(column=0, row=2, columnspan = 2)


root.mainloop()