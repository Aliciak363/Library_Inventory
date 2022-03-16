from tkinter import *
from database import Database

database = Database("books.db")


class Window(object):
    def __init__(self, window):
        self.window = window
        self.window.title("Library management system")

        # LABEL title
        l_text = Label(window, text='Title')
        l_text.grid(row=0, column=0)

        l_author = Label(window, text='Author')
        l_author.grid(row=0, column=2)

        l_year = Label(window, text='Year')
        l_year.grid(row=1, column=0)

        l_isbn = Label(window, text='ISBN')
        l_isbn.grid(row=1, column=2)

        #ENTRY box
        self.title_text = StringVar()
        self.e_title = Entry(window, textvariable=self.title_text)
        self.e_title.grid(row=0, column=1)

        self.author_text = StringVar()
        self.e_author = Entry(window, textvariable=self.author_text)
        self.e_author.grid(row=0, column=3)

        self.year_text = StringVar()
        self.e_year = Entry(window, textvariable=self.year_text)
        self.e_year.grid(row=1, column=1)

        self.isbn_text = StringVar()
        self.e_isbn = Entry(window, textvariable=self.isbn_text)
        self.e_isbn.grid(row=1, column=3)

        #LIST box
        self.list_box = Listbox(height=6, width=25, font="Helvetica")
        self.list_box.grid(column=0, row=2, columnspan=2, rowspan=6)

        #scrollbar
        scrollbar = Scrollbar(window)
        scrollbar.grid(row=2, column=2, rowspan=6)

        #configure listbox with scrollbar
        self.list_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=self.list_box.yview())

        self.list_box.bind("<<ListboxSelect>>", self.get_selected_row)

        #Buttons
        button_1 = Button(window, text='View all', width=12, command=self.view_command)
        button_1.grid(row=2, column=3)

        button_2 = Button(window, text='Search entry', width=12, command=self.search_command)
        button_2.grid(row=3, column=3)

        button_3 = Button(window, text='Add entry', width=12, command=self.add_command)
        button_3.grid(row=4, column=3)

        button_4 = Button(window, text='Update selected', width=12, command=self.update_command)
        button_4.grid(row=5, column=3)

        button_5 = Button(window, text='Delete selected', width=12, command=self.delete_command)
        button_5.grid(row=6, column=3)

        button_6 = Button(window, text='Close', width=12, command=window.destroy)
        button_6.grid(row=7, column=3)

    def get_selected_row(self):
        index = self.list_box.curselection()[0]   #curselection() = zobrazenie vybratých položiek
        self.selected_tuple = self.list_box.get(index)      #index of every selected row
        self.e_title.delete(0, END)     #delete everything from entry, if is there something
        self.e_title.insert(END, self.selected_tuple[1])
        self.e_author.delete(0, END)
        self.e_author.insert(END, self.selected_tuple[2])
        self.e_year.delete(0, END)
        self.e_year.insert(END, self.selected_tuple[3])
        self.e_isbn.delete(0, END)
        self.e_isbn.insert(END, self.selected_tuple[4])

    #view
    #potrebujeme najprv vymazat vsetko a potom zobrazit vsetky riadky
    def view_command(self):
        self.list_box.delete(0, END)   #vymazat vsetko z entry
        for row in database.view():     #zobrazit kazdy riadok v database
            self.list_box.insert(END, row)    #vlozime kazdy riadok do listboxu az do konca

    #search
    def search_command(self):
        self.list_box.delete(0, END)
        for row in database.search(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()):
            self.list_box.insert(END, row)   #search new values at the END of the list

    #add
    def add_command(self):
        database.insert(self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())
        self.list_box.delete(0, END)
        self.list_box.insert(END, (self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get()))
        #ukaze sa vlozena kniha v listbox hned ked ju vlozime nie az ked stlacime button 'View all'

    #delete
    def delete_command(self):
        database.delete(self.selected_tuple[0])

    #update
    def update_command(self):
        database.update(self.selected_tuple[0], self.title_text.get(), self.author_text.get(), self.year_text.get(), self.isbn_text.get())


window = Tk()
Window(window)
window.mainloop()
