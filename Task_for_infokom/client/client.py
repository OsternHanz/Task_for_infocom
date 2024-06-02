import requests
import tkinter as tk
from tkinter import ttk
import datetime
from tkinter import messagebox


def statistic():
    global new_window, variable, from_text, to_text
    new_window=tk.Toplevel(root)
    options = ["date_of_insert", "date_of_delete"]
    variable = tk.StringVar(root)
    variable.set(options[0])
    dropdown = tk.OptionMenu(new_window, variable, *options)
    dropdown.grid(row=0, column=0)
    from_label=ttk.Label(new_window, text="От:")
    from_label.grid(row=0, column=1)
    from_text=ttk.Entry(new_window)
    from_text.grid(row=0, column=2)
    to_label=ttk.Label(new_window, text="До:")
    to_label.grid(row=0, column=3)
    to_text=ttk.Entry(new_window)
    to_text.grid(row=0, column=4)
    send_btn=ttk.Button(new_window, text="Отправить", command=send_statistic)
    send_btn.grid(row=1, column=0)

def send_statistic():
    try:
        column=variable.get()
        if column=="Id" or column=="length" or column=="weight":
            from_filter=int(from_text.get())
            to_filter=int(to_text.get())
        else:
            from_filter=datetime.datetime.strptime(from_text.get(), "%Y-%m-%d %H:%M:%S")
            to_filter=datetime.datetime.strptime(to_text.get(), "%Y-%m-%d %H:%M:%S")
    except:
        messagebox.showerror("Ошибка", "Не верные данные")
        return False
    print(from_filter, to_filter)
    url=f"http://localhost:7000/filter?column={column}&from_filter={from_filter}&to_filter={to_filter}&stat=True"
    response = requests.get(url)
    #try:
    response.raise_for_status()
    metrics=response.json()
    new_window.destroy()
    another_new_window=tk.Toplevel()
    c_ins=ttk.Label(another_new_window, text=f"Количестов созданных: {metrics["count_insert"]}")
    c_ins.grid(row=0, column=0)
    c_del=ttk.Label(another_new_window, text=f"Количестов удаленных: {metrics["count_delete"]}")
    c_del.grid(row=1, column=0)
    avg_len=ttk.Label(another_new_window, text=f"Средняя длина рулона: {metrics["avg_length"]}")
    avg_len.grid(row=2, column=0)
    avg_weig=ttk.Label(another_new_window, text=f"Средний вес рулона: {metrics["avg_weight"]}")
    avg_weig.grid(row=3, column=0)
    min_len=ttk.Label(another_new_window, text=f"Минимальная длина: {metrics["min_length"]}")
    min_len.grid(row=4, column=0)
    min_weig=ttk.Label(another_new_window, text=f"Минимальный вес: {metrics["min_weight"]}")
    min_weig.grid(row=5, column=0)
    max_len=ttk.Label(another_new_window, text=f"Максимальная длина: {metrics["max_length"]}")
    max_len.grid(row=6, column=0)
    max_weig=ttk.Label(another_new_window, text=f"Максимальный вес: {metrics["max_weight"]}")
    max_weig.grid(row=7, column=0)
    sum_weig=ttk.Label(another_new_window, text=f"Общая сумма масс всех рулонов: {metrics["sum_weight"]}")
    sum_weig.grid(row=8, column=0)
    date_max=ttk.Label(another_new_window, text=f"Максимальная продолжительность(в часах): {metrics["date_max"]/3600:.2f}")
    date_max.grid(row=9, column=0)
    date_min=ttk.Label(another_new_window, text=f"Минимальная продолжительность(в часах): {metrics["date_min"]/3600:.2f}")
    date_min.grid(row=10, column=0)
    #except:
        #messagebox.showerror("Ошибка", "Ошибка на сервере")


def send_filter():
    try:
        column=variable.get()
        if column=="Id" or column=="length" or column=="weight":
            from_filter=int(from_text.get())
            to_filter=int(to_text.get())
        else:
            from_filter=datetime.datetime.strptime(from_text.get(), "%Y-%m-%d %H:%M:%S")
            to_filter=datetime.datetime.strptime(to_text.get(), "%Y-%m-%d %H:%M:%S")
    except:
        messagebox.showerror("Ошибка", "Не верные данные")
        return False
    print(from_filter, to_filter)
    url=f"http://localhost:7000/filter?column={column}&from_filter={from_filter}&to_filter={to_filter}&stat=False"
    response = requests.get(url)
    try:
        response.raise_for_status()
        new_window.destroy()
        default("filter", response)
    except:
        messagebox.showerror("Ошибка", "Ошибка на сервере")

def filter_table():
    global new_window, variable, from_text, to_text
    new_window=tk.Toplevel(root)
    options = ["Id", "length", "weight", "date_of_insert", "date_of_delete"]
    variable = tk.StringVar(root)
    variable.set(options[0])
    dropdown = tk.OptionMenu(new_window, variable, *options)
    dropdown.grid(row=0, column=0)
    from_label=ttk.Label(new_window, text="От:")
    from_label.grid(row=0, column=1)
    from_text=ttk.Entry(new_window)
    from_text.grid(row=0, column=2)
    to_label=ttk.Label(new_window, text="До:")
    to_label.grid(row=0, column=3)
    to_text=ttk.Entry(new_window)
    to_text.grid(row=0, column=4)
    send_btn=ttk.Button(new_window, text="Отправить", command=send_filter)
    send_btn.grid(row=1, column=0)

def send_delete():
    try:
        id=int(id_text.get())
        print(id)
    except:
        messagebox.showerror("Ошибка", "Не верные данные")
        return False
    url=f"http://localhost:7000/delete?id={id}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        answer=response.text
        if answer!="Уже удалено со склада":
            messagebox.showinfo("Внимание", f"Данная строка была удалена из склада\n{answer}")
            new_window.destroy()
            default("all", "")
        else:
            messagebox.showerror("Ошибка", "Уже удалено со склада")
    except:
        messagebox.showerror("Ошибка", "Не верные данные")


def delete():
    global id_text, new_window
    new_window=tk.Toplevel(root)
    label_id=ttk.Label(new_window, text="Id")
    label_id.grid(row=0, column=0)
    id_text=ttk.Entry(new_window)
    id_text.grid(row=0, column=1)
    send_btn=ttk.Button(new_window, text="Отправить", command=send_delete)
    send_btn.grid(row=1, column=0)

def send_insert():
    try:
        length=int(length_text.get())
        weight=int(weight_text.get())
    except:
        messagebox.showerror("Ошибка", "Не верные данные")
        return False
    print(length, weight)
    url=f"http://localhost:7000/insert?length={length}&weight={weight}"
    response = requests.get(url)
    try:
        response.raise_for_status()
        answer=response.text
        new_window.destroy()
        default("all", "")
    except:
        messagebox.showerror("Ошибка", "Не верные данные")


def insert():
    global length_text, weight_text, new_window
    new_window=tk.Toplevel(root)
    label_length=ttk.Label(new_window, text="Длина")
    label_length.grid(row=0, column=0)
    label_length=ttk.Label(new_window, text="Вес")
    label_length.grid(row=1, column=0)
    length_text=ttk.Entry(new_window)
    length_text.grid(row=0, column=1)
    weight_text=ttk.Entry(new_window)
    weight_text.grid(row=1, column=1)
    send_btn=ttk.Button(new_window, text="Отправить", command=send_insert)
    send_btn.grid(row=2, column=0)


def default(mode, answer):
    print(mode)
    for child in root.winfo_children():
        child.pack_forget()
    button_frame = tk.Frame(root)
    table_frame = tk.Frame(root)
    button_frame.pack(side="left", fill="y", padx=10, pady=10)
    table_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)
    if mode=="all":
        response=requests.get("http://localhost:7000/all/")
    elif mode=="filter":
        response=answer
    else:
        response=requests.get("http://localhost:7000/warehouse/")
    print(response.text)
    #try:
    response.raise_for_status()
    insert_btn=ttk.Button(button_frame, text="Добавить", command=insert)
    insert_btn.pack(side="top", padx=5, pady=5)
    del_btn=ttk.Button(button_frame, text="Удалить строку", command=delete)
    del_btn.pack(side="top", padx=5, pady=5)
    all_btn=ttk.Button(button_frame, text="Все записи", command=lambda: default("all", ""))
    all_btn.pack(side="top", padx=5, pady=5)
    ware_btn=ttk.Button(button_frame, text="Склад", command=lambda: default("warehouse", ""))
    ware_btn.pack(side="top", padx=5, pady=5)
    filter_btn=ttk.Button(button_frame, text="Фильтрация", command=filter_table)
    filter_btn.pack(side="top", padx=5, pady=5)
    statistic_btn=ttk.Button(button_frame, text="Статистика", command=statistic)
    statistic_btn.pack(side="top", padx=5, pady=5)
    table = ttk.Treeview(table_frame)
    table['columns'] = ('length', 'weight', 'date_of_insert', 'date_of_delete')

    table.column("0", width=100)
    table.column("1", width=100)
    table.column("2", width=100)
    table.column("3", width=100)

    table.heading("#0", text="rulon_id")
    table.heading("0", text="length")
    table.heading("1", text="weight")
    table.heading("2", text="date_of_insert")
    table.heading("3", text="date_of_delete")
    i=0
    for rulon in response.json()["list_output"]:
        table.insert('', f"{i}", text=f"{rulon["id"]}", values=(rulon['length'],
                                        rulon['weight'],
                                        rulon['date_of_insert'],
                                        rulon['date_of_delete'] if datetime.datetime.strptime(rulon['date_of_delete'], "%Y-%m-%dT%H:%M:%S.%f").year!=1000 else "NULL")
                        )
        i+=1

    table.pack(fill="both", expand=True)
    #except:
        #messagebox.showerror("Ошибка", "Произошла ошибка!")

root = tk.Tk()
default("all", "")
root.mainloop()
