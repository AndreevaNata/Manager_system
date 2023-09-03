from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import engine as en

DB_NAME = 'chatoyer_sms'
USER_NAME = 'kris'
USER_PASSWORD = 'kris'

from pathlib import Path

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH1 = OUTPUT_PATH / 'assets' / 'frame0'
ASSETS_PATH2 = OUTPUT_PATH / 'assets' / 'frame1'
ASSETS_PATH3 = OUTPUT_PATH / 'assets' / 'frame2'
ASSETS_PATH4 = OUTPUT_PATH / 'assets' / 'frame3'
ASSETS_PATH5 = OUTPUT_PATH / 'assets' / 'frame4'
ASSETS_PATH6 = OUTPUT_PATH / 'assets' / 'frame5'
ASSETS_PATH7 = OUTPUT_PATH / 'assets' / 'frame6'
def relative_to_assets1(path: str) -> Path:
    return ASSETS_PATH1 / Path(path)
def relative_to_assets3(path: str) -> Path:
    return ASSETS_PATH2 / Path(path)
def relative_to_assets2(path: str) -> Path:
    return ASSETS_PATH3 / Path(path)
def relative_to_assets4(path: str) -> Path:
    return ASSETS_PATH4 / Path(path)
def relative_to_assets5(path: str) -> Path:
    return ASSETS_PATH5 / Path(path)
def relative_to_assets6(path: str) -> Path:
    return ASSETS_PATH6 / Path(path)
def relative_to_assets7(path: str) -> Path:
    return ASSETS_PATH7 / Path(path)
cursor = None

try:
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)

except:
    print('database not exists')


# Button's commands
def btnCommand_createDB():
    global cursor
    en.create_database(DB_NAME, USER_NAME)
    cursor = en.connect_as_user(USER_NAME, USER_PASSWORD, DB_NAME)


def btnCommand_deleteDB():
    global cursor
    if cursor is not None:
        en.disconnect_user(cursor)
        en.drop_database(DB_NAME)
        cursor = None


def btnCommand_clearTablesDB():
    if cursor is None:
        return

    def btnCommand_clearTables():
        en.clear_all_tables(cursor)
        root1.destroy()

    root1 = Toplevel()
    root1.title('Подтведите действие')
    root1.configure(bg="#FAF9F4")
    root1.geometry("600x200")
    Label(root1, text="Вы же в курсе, что мы сейчас все удалим?",bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14)).pack(side=TOP)
    button_image_1 = PhotoImage(
        file=relative_to_assets7("button_1.png"))
    button_1 = Button(
        root1,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTables,
        relief="flat"
    )
    button_1.place(
        x=20.0,
        y=100.0,
        width=263.0,
        height=55.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets7("button_2.png"))
    button_2 = Button(
        root1,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=root1.destroy,
        relief="flat"
    )
    button_2.place(
        x=290.0,
        y=100.0,
        width=263.0,
        height=55.0
    )
    root1.resizable(False, False)
    root1.mainloop()



def btnCommand_printTableWorkers():
    root2 = Toplevel()
    root2.title('Таблица "Сотрудники"')
    root2.geometry("800x200")

    root2.configure(bg="#FAF9F4")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three")
    tree.column("#0", width=90, minwidth=90, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')



    tree.heading("#0", text="Должность")
    tree.heading("one", text="Зарплата")
    tree.heading("two", text="Номер телефона")
    tree.heading("three", text="Имя")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_worker(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
    tree.pack()

def btnCommand_printTableContact():
    root2 = Toplevel()
    root2.title('Таблица "Контактная Информация"')
    root2.geometry("800x200")

    root2.configure(bg="#FAF9F4")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one","two")
    tree.column("#0", width=90, minwidth=90, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')

    tree.heading("#0", text="order")
    tree.heading("one", text="name")
    tree.heading("two", text="number")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_ContactInformation(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[2] = values[2][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1],values[2]))
    tree.pack()


def btnCommand_printTableClient():
    root2 = Toplevel()
    root2.title('Таблица "Клиенты"')
    root2.geometry("800x200")

    root2.configure(bg="#FAF9F4")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two")
    tree.column("#0", width=90, minwidth=90, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')



    tree.heading("#0", text="Имя")
    tree.heading("one", text="Номер телефона")
    tree.heading("two", text="Почта")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_clients(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[2] = values[2][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2]))
    tree.pack()

def btnCommand_printTableContactC():
    root2 = Toplevel()
    root2.title('Таблица "Контактная Информация о покупателях"')
    root2.geometry("800x200")
    root2.configure(bg="#FAF9F4")

    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two","three")
    tree.column("#0", width=90, minwidth=90, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')



    tree.heading("#0", text="должность")
    tree.heading("one", text="имя")
    tree.heading("two", text="номер телефона")
    tree.heading("three", text="почта")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_ClientInformation(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[3] = values[3][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2],values[3]))
    tree.pack()

#
def btnCommand_printTableBuy():
    root2 = Toplevel()
    root2.title('Таблица "Выведена таблица покупок"')
    root2.geometry("1100x200")
    root2.configure(bg="#FAF9F4")


    tree = ttk.Treeview(root2, selectmode='browse')

    tree["columns"] = ("one", "two", "three", "four", "five", "six")
    tree.column("#0", width=110, minwidth=110, anchor='center')
    tree.column("one", anchor='center')
    tree.column("two", anchor='center')
    tree.column("three", anchor='center')
    tree.column("four", anchor='center')
    tree.column("five", anchor='center')
    tree.column("six", anchor='center')

    tree.heading("#0", text="Имя покупателя")
    tree.heading("one", text="товар")
    tree.heading("two", text="размер")
    tree.heading("three", text="цена")
    tree.heading("four", text="скидка")
    tree.heading("five", text="дата покупки")
    tree.heading("six", text="место покупки")
    scrollbar = Scrollbar(root2, orient="vertical", command=tree.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    tree.configure(yscrollcommand=scrollbar.set)

    result = en.print_table_buying(cursor)

    for line in result:
        values = line[0].split(',')
        values[0] = values[0][1:]
        values[6] = values[6][:-1]
        tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3], values[4], values[5], values[6]))
    tree.pack()



def btnCommand_printTablesDB():
    if cursor is None:
        return
    btnCommand_printTableWorkers()
    btnCommand_printTableContact()
    btnCommand_printTableClient()
    btnCommand_printTableContactC()
    btnCommand_printTableBuy()



def btnCommand_workWithTableWorkers():
    if cursor is None:
        return

    def btnCommand_clearTable():
        en.clear_worker(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_worker(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get())
            root2.destroy()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("600x200")

        label = Label(root2, text='Должность', bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=2, column=0)
        label = Label(root2, text='Зарплата',bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=2, column=1)
        label = Label(root2, text='Номер телефона',bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=2, column=2)
        label = Label(root2, text='Имя',bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=2, column=3)
        entry1 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 12))
        entry1.insert(0, 'post')
        entry1.grid(row=4, column=0)
        result = en.print_table_worker(cursor)
        entry2 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 12))
        entry2.grid(row=4, column=1)
        entry2.insert(0, '1')
        entry3 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 12))
        entry3.grid(row=4, column=2)
        entry3.insert(0, '+7')
        entry4 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 12))
        entry4.grid(row=4, column=3)
        entry4.insert(0, 'name')

        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=20.0,
            y=100.0,
            width=263.0,
            height=55.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets7("button_2.png"))
        button_2 = Button(
            root2,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=root2.destroy,
            relief="flat"
        )
        button_2.place(
            x=290.0,
            y=100.0,
            width=263.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()

    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_worker_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("600x200")

        label = Label(root2, text='Введите номер по порядку, пожалуйста не перепутайте!',bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.pack()
        entry1 = Entry(root2, width=8, fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry1.insert(0, '0')
        entry1.pack()
        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=20.0,
            y=100.0,
            width=263.0,
            height=55.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets7("button_2.png"))
        button_2 = Button(
            root2,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=root2.destroy,
            relief="flat"
        )
        button_2.place(
            x=290.0,
            y=100.0,
            width=263.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()


    root1 = Toplevel()
    root1.title('Таблица "Работники"')

    root1.geometry("967x596")
    root1.configure(bg="#FAF9F4")

    canvas = Canvas(
        root1,
        bg="#FAF9F4",
        height=596,
        width=967,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        270.0,
        23.0,
        anchor="nw",
        text="CHATOYER ",
        fill="#000000",
        font=("LeagueGothicRegular Regular", 75 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets2("image_1.png"))
    image_1 = canvas.create_image(
        810.0,
        250.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets2("image_2.png"))
    image_2 = canvas.create_image(
        168.0,
        351.0,
        image=image_image_2
    )
    button_image_1 = PhotoImage(
        file=relative_to_assets2("button_1.png"))
    button_1 = Button(
        root1,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_deleteLine,
        relief="flat"
    )
    button_1.place(
        x=350.0,
        y=387.0,
        width=269.0,
        height=54.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets2("button_2.png"))
    button_2 = Button(
        root1,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_addNewLine,
        relief="flat"
    )
    button_2.place(
        x=351.0,
        y=327.0,
        width=267.0,
        height=55.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets2("button_3.png"))
    button_3 = Button(
        root1,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_printTableWorkers,
        relief="flat"
    )
    button_3.place(
        x=347.0,
        y=208.0,
        width=263.0,
        height=55.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets2("button_4.png"))
    button_4 = Button(
        root1,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTable,
        relief="flat"
    )
    button_4.place(
        x=354.0,
        y=268.0,
        width=256.0,
        height=54.0
    )
    root1.resizable(False, False)
    root1.mainloop()


def btnCommand_workWithTableClients():
    if cursor is None:
        return

    def btnCommand_clearTable():
        en.clear_clients(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_clients(cursor, entry1.get(), entry2.get(), entry3.get())
            root2.destroy()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("600x200")
        label = Label(root2, text='Имя', bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=0, column=0)
        label = Label(root2, text='Номер телефона', bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=0, column=1)
        label = Label(root2, text='Почта', bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        label.grid(row=0, column=2)
        entry1 = Entry(root2, width=14,  bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        entry1.insert(0, 'имя')
        entry1.grid(row=1, column=0)
        result = en.print_table_clients(cursor)
        entry2 = Entry(root2, width=14,  bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '+7')
        entry3 = Entry(root2, width=14, bg ="#FAF9F4",font=("LeagueGothicRegular Regular", 12))
        entry3.grid(row=1, column=2)
        entry3.insert(0, 'mail')

        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=20.0,
            y=100.0,
            width=263.0,
            height=55.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets7("button_2.png"))
        button_2 = Button(
            root2,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=root2.destroy,
            relief="flat"
        )
        button_2.place(
            x=290.0,
            y=100.0,
            width=263.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()



    def btnCommand_deleteLine():
        def btnAccept():
            en.delete_client_by_id(cursor, entry1.get())
            root2.destroy()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("600x200")
        label = Label(root2, text='Введите номер по порядку, пожалуйста не перепутайте!', bg="#FAF9F4",
                      font=("LeagueGothicRegular Regular", 12))
        label.pack()
        entry1 = Entry(root2, width=8, fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry1.insert(0, '0')
        entry1.pack()
        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=20.0,
            y=100.0,
            width=263.0,
            height=55.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets7("button_2.png"))
        button_2 = Button(
            root2,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=root2.destroy,
            relief="flat"
        )
        button_2.place(
            x=290.0,
            y=100.0,
            width=263.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()

    root1 = Toplevel()
    root1.title('Таблица "Клиенты"')

    root1.geometry("967x596")
    root1.configure(bg="#FAF9F4")

    canvas = Canvas(
        root1,
        bg="#FAF9F4",
        height=596,
        width=967,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        270.0,
        23.0,
        anchor="nw",
        text="CHATOYER ",
        fill="#000000",
        font=("LeagueGothicRegular Regular", 75 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets3("image_1.png"))
    image_1 = canvas.create_image(
        810.0,
        250.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets3("image_2.png"))
    image_2 = canvas.create_image(
        168.0,
        351.0,
        image=image_image_2
    )
    button_image_1 = PhotoImage(
        file=relative_to_assets3("button_1.png"))
    button_1 = Button(
        root1,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_deleteLine,
        relief="flat"
    )
    button_1.place(
        x=350.0,
        y=387.0,
        width=269.0,
        height=54.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets3("button_2.png"))
    button_2 = Button(
        root1,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_addNewLine,
        relief="flat"
    )
    button_2.place(
        x=351.0,
        y=327.0,
        width=267.0,
        height=55.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets3("button_3.png"))
    button_3 = Button(
        root1,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_printTableClient,
        relief="flat"
    )
    button_3.place(
        x=347.0,
        y=208.0,
        width=263.0,
        height=55.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets3("button_4.png"))
    button_4 = Button(
        root1,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTable,
        relief="flat"
    )
    button_4.place(
        x=354.0,
        y=268.0,
        width=256.0,
        height=54.0
    )
    window.resizable(False, False)
    window.mainloop()






def btnCommand_workWithTableContact():
    if cursor is None:
        return

    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_worker(cursor)


    def btnCommand_findLine():
        def btnAccept():
            result = en.search_contact_by_name(cursor, entry1.get())

            root3 = Toplevel()
            tree = ttk.Treeview(root3, selectmode='browse')

            tree["columns"] = ("one", "two")
            tree.column("#0", width=40, minwidth=40)
            tree.column("one")
            tree.column("two")

            tree.heading("#0", text="id")
            tree.heading("one", text="Имя")
            tree.heading("two", text="Номер")

            values = result[0][0].split(',')
            values[0] = values[0][1:]
            values[2] = values[2][:-1]
            tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2]))
            tree.pack()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("700x200")
        label = Label(root2, text='Введите имя', bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.pack()
        entry1 = Entry(root2, width=20,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry1.insert(0, '')
        entry1.pack()

        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
        x=220.0,
        y=100.0,
        width=267.0,
        height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()




    root1 = Toplevel()
    root1.title('Таблица "Информация о сотрудниках"')
    root1.geometry("967x596")
    root1.configure(bg="#FAF9F4")

    canvas = Canvas(
        root1,
        bg="#FAF9F4",
        height=596,
        width=967,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        270.0,
        23.0,
        anchor="nw",
        text="CHATOYER ",
        fill="#000000",
        font=("LeagueGothicRegular Regular", 75 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets4("image_1.png"))
    image_1 = canvas.create_image(
        810.0,
        250.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets4("image_2.png"))
    image_2 = canvas.create_image(
        168.0,
        351.0,
        image=image_image_2
    )
    button_image_1 = PhotoImage(
        file=relative_to_assets4("button_1.png"))
    button_1 = Button(
        root1,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_findLine,
        relief="flat"
    )
    button_1.place(
        x=352.0,
        y=365.0,
        width=267.0,
        height=55.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets4("button_2.png"))
    button_2 = Button(
        root1,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_printTableContact,
        relief="flat"
    )
    button_2.place(
        x=348.0,
        y=246.0,
        width=263.0,
        height=55.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets4("button_3.png"))
    button_3 = Button(
        root1,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTable,
        relief="flat"
    )
    button_3.place(
        x=355.0,
        y=306.0,
        width=256.0,
        height=54.0
    )
    window.resizable(False, False)
    window.mainloop()


def btnCommand_workWithTableContactC():
    if cursor is None:
        return

    def btnCommand_clearTable():
        if cursor is not None:
            en.clear_clients(cursor)



    def btnCommand_findLine():
        def btnAccept():
            result = en.search_client_by_name(cursor, entry1.get())

            root4 = Toplevel()
            tree = ttk.Treeview(root4, selectmode='browse')

            tree["columns"] = ("one", "two", "three")
            tree.column("#0", width=40, minwidth=40)
            tree.column("one")
            tree.column("two")
            tree.column("three")

            tree.heading("#0", text="id")
            tree.heading("one", text="Имя")
            tree.heading("two", text="Номер")
            tree.heading("three", text="Почта")

            values = result[0][0].split(',')
            values[0] = values[0][1:]
            values[3] = values[3][:-1]
            tree.insert(parent="", index="end", text=values[0], values=(values[1], values[2], values[3]))
            tree.pack()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("600x200")
        label = Label(root2, text='Введите имя', bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.pack()
        entry1 = Entry(root2, width=20, fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry1.insert(0, '')
        entry1.pack()

        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=170.0,
            y=100.0,
            width=267.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()



    root1 = Toplevel()
    root1.title('Таблица "Информация о покупателях"')
    root1.geometry("967x596")
    root1.configure(bg="#FAF9F4")

    canvas = Canvas(
        root1,
        bg="#FAF9F4",
        height=596,
        width=967,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        270.0,
        23.0,
        anchor="nw",
        text="CHATOYER ",
        fill="#000000",
        font=("LeagueGothicRegular Regular", 75 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets5("image_1.png"))
    image_1 = canvas.create_image(
        810.0,
        250.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets5("image_2.png"))
    image_2 = canvas.create_image(
        168.0,
        351.0,
        image=image_image_2
    )
    button_image_1 = PhotoImage(
        file=relative_to_assets5("button_1.png"))
    button_1 = Button(
        root1,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_findLine,
        relief="flat"
    )
    button_1.place(
        x=352.0,
        y=365.0,
        width=267.0,
        height=55.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets5("button_2.png"))
    button_2 = Button(
        root1,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_printTableContactC,
        relief="flat"
    )
    button_2.place(
        x=348.0,
        y=246.0,
        width=263.0,
        height=55.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets5("button_3.png"))
    button_3 = Button(
        root1,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTable,
        relief="flat"
    )
    button_3.place(
        x=355.0,
        y=306.0,
        width=256.0,
        height=54.0
    )
    window.resizable(False, False)
    window.mainloop()




def btnCommand_workWithTableBuy():
    if cursor is None:
        return

    def btnCommand_clearTable():
        en.clear_buying(cursor)

    def btnCommand_addNewLine():
        def btnAccept():
            en.add_to_buying(cursor, entry1.get(), entry2.get(), entry3.get(), entry4.get(), entry5.get(), entry6.get(), entry7.get())
            root2.destroy()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("1100x200")
        result = en.print_table_buying(cursor)
        label = Label(root2, text='Имя покупателя',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=0)
        label = Label(root2, text='Товар',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=1)
        label = Label(root2, text='Размер',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=2)
        label = Label(root2, text='Цена',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=3)
        label = Label(root2, text='Скидка',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=4)
        label = Label(root2, text='Дата покупки',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=5)
        label = Label(root2, text='Где купили?',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=6)
        entry1 = Entry(root2, width=13, fg="#000000", font=("LeagueGothicRegular Regular", 14))
        entry1.insert(0, 'name')
        entry1.grid(row=1, column=0)

        entry2 = Entry(root2, width=14, fg="#000000", font=("LeagueGothicRegular Regular", 14))
        entry2.grid(row=1, column=1)
        entry2.insert(0, 'product')
        entry3 = Entry(root2, width=14, fg="#000000", font=("LeagueGothicRegular Regular", 14))
        entry3.grid(row=1, column=2)
        entry3.insert(0, 'S')
        entry4 = Entry(root2, width=14, fg="#000000", font=("LeagueGothicRegular Regular", 14))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '0000')
        entry5 = Entry(root2, width=14, fg="#000000", font=("LeagueGothicRegular Regular", 14))
        entry5.grid(row=1, column=4)
        entry5.insert(0, '0')
        entry6 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry6.grid(row=1, column=5)
        entry6.insert(0, '11/11/2021')
        entry7 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry7.grid(row=1, column=6)
        entry7.insert(0, 'where')

        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=320.0,
            y=100.0,
            width=263.0,
            height=55.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets7("button_2.png"))
        button_2 = Button(
            root2,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=root2.destroy,
            relief="flat"
        )
        button_2.place(
            x=600.0,
            y=100.0,
            width=263.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()

    def btnCommand_updateLine():
        def btnAccept():
            en.update_buying(cursor, entry1.get(), entry2.get(), entry3.get(),
                             entry4.get(), entry5.get(), entry6.get(), entry7.get())
            root2.destroy()

        root2 = Toplevel()
        root2.configure(bg="#FAF9F4")
        root2.geometry("1100x200")
        label = Label(root2, text='id',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=0)
        label = Label(root2, text='Товар',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=1)
        label = Label(root2, text='Размер',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=2)
        label = Label(root2, text='Цена',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=3)
        label = Label(root2, text='Скидка',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=4)
        label = Label(root2, text='Дата покупки',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=5)
        label = Label(root2, text='Где купили?',bg="#FAF9F4", font=("LeagueGothicRegular Regular", 14))
        label.grid(row=0, column=6)
        entry1 = Entry(root2, width=14,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry1.grid(row=1, column=0)
        entry1.insert(0, '-1')
        entry2 = Entry(root2, width=14,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry2.grid(row=1, column=1)
        entry2.insert(0, '')
        entry3 = Entry(root2, width=14,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry3.grid(row=1, column=2)
        entry3.insert(0, '')
        entry4 = Entry(root2, width=14, fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry4.grid(row=1, column=3)
        entry4.insert(0, '-1')
        entry5 = Entry(root2, width=14,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry5.grid(row=1, column=4)
        entry5.insert(0, '-1')
        entry6 = Entry(root2, width=14,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry6.grid(row=1, column=5)
        entry6.insert(0, '')
        entry7 = Entry(root2, width=14,  fg='#000000', font=("LeagueGothicRegular Regular", 14))
        entry7.grid(row=1, column=6)
        entry7.insert(0, '')

        button_image_1 = PhotoImage(
            file=relative_to_assets7("button_1.png"))
        button_1 = Button(
            root2,
            image=button_image_1,
            borderwidth=0,
            highlightthickness=0,
            command=btnAccept,
            relief="flat"
        )
        button_1.place(
            x=320.0,
            y=100.0,
            width=263.0,
            height=55.0
        )

        button_image_2 = PhotoImage(
            file=relative_to_assets7("button_2.png"))
        button_2 = Button(
            root2,
            image=button_image_2,
            borderwidth=0,
            highlightthickness=0,
            command=root2.destroy,
            relief="flat"
        )
        button_2.place(
            x=600.0,
            y=100.0,
            width=263.0,
            height=55.0
        )
        root2.resizable(False, False)
        root2.mainloop()

    root1 = Toplevel()
    root1.title('Таблица "Товары"')
    root1.geometry("967x596")
    root1.configure(bg="#FAF9F4")

    canvas = Canvas(
        root1,
        bg="#FAF9F4",
        height=596,
        width=967,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        270.0,
        23.0,
        anchor="nw",
        text="CHATOYER ",
        fill="#000000",
        font=("LeagueGothicRegular Regular", 75 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets6("image_1.png"))
    image_1 = canvas.create_image(
        810.0,
        250.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets6("image_2.png"))
    image_2 = canvas.create_image(
        168.0,
        351.0,
        image=image_image_2
    )
    button_image_1 = PhotoImage(
        file=relative_to_assets6("button_1.png"))
    button_1 = Button(
        root1,
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_addNewLine,
        relief="flat"
    )
    button_1.place(
        x=350.0,
        y=354.0,
        width=267.0,
        height=55.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets6("button_2.png"))
    button_2 = Button(
        root1,
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_updateLine,
        relief="flat"
    )
    button_2.place(
        x=354.0,
        y=414.0,
        width=267.0,
        height=55.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets6("button_3.png"))
    button_3 = Button(
        root1,
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_printTableBuy,
        relief="flat"
    )
    button_3.place(
        x=346.0,
        y=235.0,
        width=263.0,
        height=55.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets6("button_4.png"))
    button_4 = Button(
        root1,
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTable,
        relief="flat"
    )
    button_4.place(
        x=353.0,
        y=295.0,
        width=256.0,
        height=54.0
    )
    window.resizable(False, False)
    window.mainloop()



if __name__ == '__main__':
    # Creating GUI



    window = Tk()
    window.title('Магазин одежды - склад')
    window.geometry("967x596")
    window.configure(bg="#FAF9F4")

    canvas = Canvas(
        window,
        bg="#FAF9F4",
        height=596,
        width=967,
        bd=0,
        highlightthickness=0,
        relief="ridge"
    )

    canvas.place(x=0, y=0)
    canvas.create_text(
        270.0,
        23.0,
        anchor="nw",
        text="CHATOYER ",
        fill="#000000",
        font=("LeagueGothicRegular Regular", 75 * -1)
    )

    image_image_1 = PhotoImage(
        file=relative_to_assets1("image_1.png"))
    image_1 = canvas.create_image(
        810.0,
        190.0,
        image=image_image_1
    )

    image_image_2 = PhotoImage(
        file=relative_to_assets1("image_2.png"))
    image_2 = canvas.create_image(
        168.0,
        351.0,
        image=image_image_2
    )

    button_image_1 = PhotoImage(
        file=relative_to_assets1("button_1.png"))
    button_1 = Button(
        image=button_image_1,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_workWithTableContact,
        relief="flat"
    )
    button_1.place(
        x=720.0,
        y=419.0,
        width=214.0,
        height=42.0
    )

    button_image_2 = PhotoImage(
        file=relative_to_assets1("button_2.png"))
    button_2 = Button(
        image=button_image_2,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_workWithTableContactC,
        relief="flat"
    )
    button_2.place(
        x=720.0,
        y=473.0,
        width=214.0,
        height=42.0
    )

    button_image_3 = PhotoImage(
        file=relative_to_assets1("button_3.png"))
    button_3 = Button(
        image=button_image_3,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_workWithTableBuy,
        relief="flat"
    )
    button_3.place(
        x=720.0,
        y=524.0,
        width=214.0,
        height=42.0
    )

    button_image_4 = PhotoImage(
        file=relative_to_assets1("button_4.png"))
    button_4 = Button(
        image=button_image_4,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_workWithTableClients,
        relief="flat"
    )
    button_4.place(
        x=720.0,
        y=383.0,
        width=214.0,
        height=24.0
    )

    button_image_5 = PhotoImage(
        file=relative_to_assets1("button_5.png"))
    button_5 = Button(
        image=button_image_5,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_workWithTableWorkers,
        relief="flat"
    )
    button_5.place(
        x=720.0,
        y=350.0,
        width=214.0,
        height=24.0
    )

    button_image_6 = PhotoImage(
        file=relative_to_assets1("button_6.png"))
    button_6 = Button(
        image=button_image_6,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_deleteDB,
        relief="flat"
    )
    button_6.place(
        x=352.0,
        y=272.0,
        width=256.0,
        height=54.0
    )

    button_image_7 = PhotoImage(
        file=relative_to_assets1("button_7.png"))
    button_7 = Button(
        image=button_image_7,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_printTablesDB,
        relief="flat"
    )
    button_7.place(
        x=345.0,
        y=331.0,
        width=263.0,
        height=55.0
    )

    button_image_8 = PhotoImage(
        file=relative_to_assets1("button_8.png"))
    button_8 = Button(
        image=button_image_8,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_clearTablesDB,
        relief="flat"
    )
    button_8.place(
        x=354.0,
        y=391.0,
        width=267.0,
        height=55.0
    )

    button_image_9 = PhotoImage(
        file=relative_to_assets1("button_9.png"))
    button_9 = Button(
        image=button_image_9,
        borderwidth=0,
        highlightthickness=0,
        command=btnCommand_createDB,
        relief="flat"
    )
    button_9.place(
        x=352.0,
        y=213.0,
        width=256.0,
        height=54.0
    )
    window.resizable(False, False)
    window.mainloop()


