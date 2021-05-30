# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mb
from tkinter.filedialog import askopenfilename
from tkinter.filedialog import asksaveasfilename
import sqlite3
from DataBase import GroupDataBase
from DataBase import SubjectDataBase


def open_group_frame():
    close_subject_frame()
    close_export_frame()
    groupFrame.pack()


def close_group_frame():
    groupFrame.pack_forget()


def open_group_file():
    group_db.groupFile = askopenfilename(filetypes=[("DB Files", "*.db"), ("All Files", "*.*")])
    group_db.reopen()
    groupNameLabel.config(text=group_db.groupFile)
    groupFrame.view_records()


def save_group_file():
    save_file = asksaveasfilename(filetypes=[("DB Files", "*.db"), ("All Files", "*.*")])
    group_db.save(save_file)
    group_db.groupFile = save_file
    group_db.reopen()
    groupNameLabel.config(text=group_db.groupFile)
    groupFrame.view_records()


def open_subject_frame():
    close_group_frame()
    close_export_frame()
    subjectFrame.pack()


def close_subject_frame():
    subjectFrame.pack_forget()


def open_subject_file():
    subject_db.subjectFile = askopenfilename(filetypes=[("DB Files", "*.db"), ("All Files", "*.*")])
    subject_db.reopen()
    subjectNameLabel.config(text=subject_db.subjectFile)
    subjectFrame.db.c.execute('''SELECT * FROM info''')
    subjectFrame.group_name = subjectFrame.db.c.fetchall()
    subjectFrame.groupNameLabel.configure(text=subjectFrame.group_name)
    subjectFrame.update_date_list()
    subjectFrame.view_records()


def save_subject_file():
    save_file = asksaveasfilename(filetypes=[("DB Files", "*.db"), ("All Files", "*.*")])
    subject_db.save(save_file)
    subject_db.subjectFile = save_file
    subject_db.reopen()
    subjectNameLabel.config(text=subject_db.subjectFile)
    groupFrame.view_records()


def open_export_frame():
    close_subject_frame()
    close_group_frame()
    exportFrame.pack()


def close_export_frame():
    exportFrame.pack_forget()


class SubjectFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        self.view = workSpace
        self.init_subject_frame()
        #self.view_records()

    def init_subject_frame(self):
        self.db = subject_db

        toolbar = tk.Frame(self, bg='#98817C', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background="#98817C", fieldbackground="#98817C")
        style.map("Treeview", background=[('selected', '#76878F')], foreground=[('selected', "black")])

        file_open_button = tk.Button(toolbar, text='Открыть файл', command=open_subject_file, bg='#98817C', bd=1)
        file_open_button.pack(side=tk.LEFT)

        file_save_button = tk.Button(toolbar, text='Сохранить файл', command=save_subject_file, bg='#98817C', bd=1)
        file_save_button.pack(side=tk.LEFT)

        infobar = tk.Frame(self, bg='#98817C', bd=2)
        infobar.pack(side=tk.TOP, fill=tk.X)

        infoNameLabel = tk.Label(infobar, bg='#98817C', text='Активная группа:')
        infoNameLabel.grid(column=0, row=0)

        self.db.c.execute('''SELECT * FROM info''')
        self.group_name = self.db.c.fetchall()
        self.groupNameLabel = tk.Label(infobar, bg='#6C858F', text=self.group_name)
        self.groupNameLabel.grid(column=1, row=0)

        gap_1 = tk.Frame(infobar, bg='#98817C', width=80)
        gap_1.grid(column=2, row=0)

        self.groupName = tk.Entry(infobar, width=20, bg='white', bd=1)
        self.groupName.grid(column=3, row=0)

        groupChange = tk.Button(infobar, command=self.change_group_name, text='Поменять название группы', bg='#98817C', bd=1)
        groupChange.grid(column=4, row=0)

        infoDateLabel = tk.Label(infobar, bg='#98817C', text='Активная дата:')
        infoDateLabel.grid(column=0, row=1)

        self.subjectDates = ttk.Combobox(infobar)
        self.subjectDates.grid(column=1, row=1)

        gap_2 = tk.Frame(infobar, bg='#98817C', width=80)
        gap_2.grid(column=2, row=1)

        self.activeDate = tk.Entry(infobar, width=20, bg='white', bd=1)
        self.activeDate.grid(column=3, row=1)

        dateChange = tk.Button(infobar, command=self.add_date, text='Добавить дату', bg='#98817C', bd=1)
        dateChange.grid(column=4, row=1)

        self.studentsFIO = ttk.Combobox(infobar)
        self.studentsFIO.grid(column=0, row=2)

        self.studentsDates = tk.Listbox(infobar)
        self.studentsDates.grid(column=1, row=2)


    def change_group_name(self):
        try:
            self.db.c.execute('''DELETE FROM info WHERE GROUP_NAME=?''', (self.group_name,))
            self.db.conn.commit()
        finally:
            self.group_name = self.groupName.get()
            self.db.set_group_name(self.group_name)
            self.groupNameLabel.configure(text=self.group_name)

        #self.view_records()

    def view_records(self):
        groupFrame.db.c.execute('''SELECT FIO FROM students''')
        students = []
        for row in groupFrame.db.c.fetchall():
            students.append(row)
            print(row)

        self.studentsFIO.config(values=students)
        self.studentsFIO.current(0)

        groupFrame.db.c.execute('''SELECT ID FROM students''')
        students_id = []
        for row in self.db.c.fetchall():
            students_id.append(row)

        for id in students_id:
            self.db.c.execute('''SELECT DATES FROM subject WHERE ID LIKE ?''', id)
            self.studentsDates.delete(0,'end')
            [self.studentsDates.insert('', 'end', values=row) for row in self.db.c.fetchall()]



    def add_date(self):
        self.db.add_lesson(self.activeDate.get())
        self.update_date_list()
        #self.view_records()

    def update_date_list(self):
        self.db.c.execute('''SELECT * FROM lessons''')
        dates = []
        for row in self.db.c.fetchall():
            dates.append(row)
        self.subjectDates.config(values=dates)
        self.subjectDates.current(0)
        # self.view_records()

class GroupFrame(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_group_frame()
        self.view = workSpace
        self.db = group_db
        self.view_records()

    def init_group_frame(self):
        toolbar = tk.Frame(self, bg='#98817C', bd=2)
        toolbar.pack(side=tk.TOP, fill=tk.X)

        style = ttk.Style(self)
        style.theme_use("default")
        style.configure("Treeview", background="#98817C", fieldbackground="#98817C")
        style.map("Treeview", background=[('selected', '#76878F')], foreground=[('selected', "black")])

        file_open_button = tk.Button(toolbar, text='Открыть файл', command=open_group_file, bg='#98817C', bd=1, compound=tk.TOP)
        file_open_button.pack(side=tk.LEFT)

        file_save_button = tk.Button(toolbar, text='Сохранить файл', command=save_group_file, bg='#98817C', bd=1, compound=tk.TOP)
        file_save_button.pack(side=tk.LEFT)

        btn_open_dialog = tk.Button(toolbar, text='Добавить студента', command=self.open_dialog, bg='#98817C', bd=1, compound=tk.TOP)
        btn_open_dialog.pack(side=tk.LEFT)

        btn_edit_dialog = tk.Button(toolbar, text='Редактировать запись', bg='#98817C', bd=1, compound=tk.TOP, command=self.open_update_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        btn_delete = tk.Button(toolbar, text='Удалить запись', bg='#98817C', bd=1, compound=tk.TOP, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)

        btn_search = tk.Button(toolbar, text='Поиск студента', bg='#98817C', bd=1, compound=tk.TOP, command=self.open_search_dialog)
        btn_search.pack(side=tk.LEFT)

        btn_refresh = tk.Button(toolbar, text='Обновить таблицу', bg='#98817C', bd=1, compound=tk.TOP, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        self.tree = ttk.Treeview(self, columns=('FIO', 'Group_Name', 'ID'), height=15, show='headings')

        self.tree.column('FIO', width=300, anchor=tk.CENTER)
        self.tree.column('Group_Name', width=180, anchor=tk.CENTER)
        self.tree.column('ID', width=230, anchor=tk.CENTER)

        self.tree.heading('Group_Name', text='Group_Name')
        self.tree.heading('FIO', text='FIO')
        self.tree.heading('ID', text='ID')

        self.tree.pack(side=tk.LEFT, fill=tk.BOTH)

        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    def records(self, FIO, GROUP, ID):
        try:
            self.db.insert_data(FIO, GROUP, ID)
        except sqlite3.DatabaseError as err:
            mb.showerror('Ошибка','Проверьте вводимую информацию')
        else:
            mb.showinfo('Выполнено', 'Запись добавлена!')
        self.view_records()

    def update_record(self, FIO, Group_Name, ID):
        try:
            self.db.c.execute('''UPDATE students SET FIO=?, Group_Name=?, ID=? WHERE ID=?''', (FIO, Group_Name, ID, ID))
            self.db.conn.commit()
        except sqlite3.DatabaseError as err:
            mb.showerror('Ошибка', 'Проверьте вводимую информацию')
        else:
            mb.showinfo('Выполнено', 'Запись изменена!')
        self.view_records()

    def view_records(self):
        self.db.c.execute('''SELECT * FROM students''')
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def delete_records(self):
        for selection_item in self.tree.selection():
            self.db.c.execute('''DELETE FROM students WHERE FIO=?''', (self.tree.set(selection_item, '#1'),))
        self.db.conn.commit()
        self.view_records()

    def search_records(self, description):
        description = ('%' + description + '%',)
        self.db.c.execute('''SELECT * FROM students WHERE FIO LIKE ?''', description)
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    def open_dialog(self):
        Child()

    def open_update_dialog(self):
        Update()

    def open_search_dialog(self):
        Search()


class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(window, bg='#98817C')
        self.init_child()
        self.view = groupFrame

    def init_child(self):
        self.title('Добавить информацию о студенте')
        self.geometry('400x220+600+400')
        self.resizable(False, False)

        label_fio = tk.Label(self, text='ФИО:')
        label_fio.place(x=50, y=50)
        label_group = tk.Label(self, text='Группа студента')
        label_group.place(x=50, y=80)
        label_id = tk.Label(self, text='ID')
        label_id.place(x=50, y=110)

        self.entry_fio = ttk.Entry(self, width=30)
        self.entry_fio.place(x=200, y=50)

        self.entry_group = ttk.Entry(self, width=30)
        self.entry_group.place(x=200, y=80)

        self.id = ttk.Entry(self, width=30)
        self.id.place(x=200, y=110)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=300, y=170)

        self.btn_ok = ttk.Button(self, text='Добавить', command=self.add_data)
        self.btn_ok.place(x=220, y=170)

        self.grab_set()
        self.focus_set()

    def add_data(self):
        try:
            self.view.records(self.entry_fio.get(), self.entry_group.get(), self.id.get())
        finally:
            self.destroy()


class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = groupFrame
        self.db = group_db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        btn_edit = ttk.Button(self, text='Редактировать')
        btn_edit.place(x=205, y=170)
        btn_edit.bind('<Button-1>', lambda event: self.view.update_record(self.entry_fio.get(), self.entry_group.get(), self.id.get()))

        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM students WHERE FIO=?''',
                          (self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_fio.insert(0, row[0])
        self.entry_group.insert(0, row[1])
        self.id.insert(0, row[2])


class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = groupFrame

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100+400+300')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text='Поиск')
        btn_search.place(x=105, y=50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', lambda event: self.destroy(), add='+')


group_db = GroupDataBase('')
subject_db = SubjectDataBase('')

window = tk.Tk()
window.title("Программа учета посещаемости")
window.geometry("1000x500")

mainFrame = tk.Frame(window, bg='#98817C', bd=5)
mainFrame.pack(fill=tk.BOTH)

chooserFrame = tk.Frame(mainFrame, bg='#98817C', height=800, width=200)
chooserFrame.pack(side= 'left', fill="y")

attendanceButtonBackground = tk.PhotoImage(file="attendance.png")
attendanceButton = tk.Button(chooserFrame, command=open_subject_frame, bd=0, height=100, width=100)
attendanceButton.config(image=attendanceButtonBackground)
attendanceButton.grid(column=0, row=0)

chooser_gap_1 = tk.Frame(chooserFrame, bg='#98817C', height=10)
chooser_gap_1.grid(column=0, row=1)

groupButtonBackground = tk.PhotoImage(file="group.png")
groupButton = tk.Button(chooserFrame, command=open_group_frame, bd=0, height=100, width=100)
groupButton.config(image=groupButtonBackground)
groupButton.grid(column=0, row=2)

chooser_gap_2 = tk.Frame(chooserFrame, bg='#98817C', height=10)
chooser_gap_2.grid(column=0, row=3)

exportButtonBackground = tk.PhotoImage(file="export.png")
exportButton = tk.Button(chooserFrame, command=open_export_frame, bd=0, height=100, width=100)
exportButton.config(image=exportButtonBackground)
exportButton.grid(column=0, row=4)

chooser_gap_2 = tk.Frame(chooserFrame, bg='#98817C', height=200)
chooser_gap_2.grid(column=0, row=6)

infoFrame = tk.Frame(mainFrame, bg='#988D72', bd=5, height=30)
infoFrame.pack(side= 'top', fill="x")

groupLabel = tk.Label(infoFrame, bg='#988D72', text='Открытый файл группы:')
groupLabel.grid(column=0, row=0)

groupNameLabel = tk.Label(infoFrame, bg='#988D72', text='НЕТ ОТКРЫТОГО ФАЙЛА ГРУППЫ')
groupNameLabel.grid(column=1, row=0)

subjectLabel = tk.Label(infoFrame, bg='#988D72', text='Открытый файл предмета:')
subjectLabel.grid(column=0, row=1)

subjectNameLabel = tk.Label(infoFrame, bg='#988D72', text='НЕТ ОТКРЫТОГО ФАЙЛА ПРЕДМЕТА')
subjectNameLabel.grid(column=1, row=1)

workSpace = tk.Frame(mainFrame, bg='#98817C', bd=5)
workSpace.pack(side= 'right', expand=True, fill=tk.BOTH)

groupFrame = GroupFrame(workSpace)
subjectFrame = SubjectFrame(workSpace)

exportFrame = tk.Frame(workSpace)

window.resizable(False, False)

window.mainloop()

