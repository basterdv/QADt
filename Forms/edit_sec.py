import tkinter as tk
from tkinter import simpledialog
from tkinter.messagebox import showerror, showwarning, showinfo, askyesno


class MyDialog(tk.simpledialog.Dialog):
    def __init__(self, parent, title, key2, key4):
        self.my_username = key2
        self.my_password = key4
        super().__init__(parent, title)

    def body(self, frame):
        # print(type(frame)) # tkinter.Frame
        self.my_username_label = tk.Label(frame, width=25, text="Тикер")

        self.my_username_label.pack()
        self.my_username_box = tk.Entry(frame, width=25)

        self.my_username_box.insert(0, f'{self.my_username}')
        self.my_username_box.pack()

        self.my_password_label = tk.Label(frame, width=25, text="Кол-во лотов")
        self.my_password_label.pack()

        self.my_password_box = tk.Entry(frame, width=25)
        self.my_password_box.insert(0, f'{self.my_password}')
        self.my_password_box.pack()
        # self.my_password_box['show'] = '*'

        return frame

    def ok_pressed(self):
        # print("ok")
        self.my_username = self.my_username_box.get()
        try:
            self.my_password = int(self.my_password_box.get())
        except:
            choice = showwarning(title="Предупреждение", message="Допустим ввод только целых чисел!")
            if choice:
                pass

        if self.my_username !="":
            self.destroy()
        else:
            choice = showwarning(title="Предупреждение", message="Данные не могут быть пустыми!")
            if choice:
                pass


    def cancel_pressed(self):
        # print("cancel")
        self.destroy()

    def buttonbox(self):
        self.ok_button = tk.Button(self, text='OK', width=5, command=self.ok_pressed)
        self.ok_button.pack(side="left")
        cancel_button = tk.Button(self, text='Cancel', width=5, command=self.cancel_pressed)
        cancel_button.pack(side="right")
        self.bind("<Return>", lambda event: self.ok_pressed())
        self.bind("<Escape>", lambda event: self.cancel_pressed())


def mydialog(root, key1, key2):
    dialog = MyDialog(title="Login", parent=root, key2=key1, key4=key2)
    return dialog.my_username, dialog.my_password



