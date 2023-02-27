import csv
import tkinter as tk
from tkinter import ttk
from tkinter.ttk import Treeview


class AccountManager:
    account_list_tree: Treeview

    def __init__(self, master):
        self.master = master
        master.title("Account Manager")

        self.account_list_tree = ttk.Treeview(master)


        # Labels
        self.game_label = tk.Label(master, text="Game:")
        self.username_label = tk.Label(master, text="Username:")
        self.password_label = tk.Label(master, text="Password:")
        self.note_label = tk.Label(master, text="Note:")

        # Entries
        self.game_entry = tk.Entry(master)
        self.username_entry = tk.Entry(master)
        self.password_entry = tk.Entry(master)
        self.note_entry = tk.Entry(master)

        self.save_button = tk.Button(master, text="Save", command=self.save_data)

        # Create a frame for the account list
        self.account_list_frame = tk.LabelFrame(master, text="Account List")
        self.account_list_frame.grid(row=0, column=0, columnspan=10, padx=10, pady=10)

        # Grid Layout
        self.game_label.grid(row=1, column=0, sticky="e")
        self.username_label.grid(row=1, column=2, sticky="e")
        self.password_label.grid(row=1, column=4, sticky="e")
        self.note_label.grid(row=1, column=6, sticky="e")

        self.game_entry.grid(row=1, column=1, padx=5, pady=5)
        self.username_entry.grid(row=1, column=3, padx=5, pady=5)
        self.password_entry.grid(row=1, column=5, padx=5, pady=5)
        self.note_entry.grid(row=1, column=7, padx=5, pady=5)

        self.save_button.grid(row=1, column=8, pady=10)



        # Create a Treeview widget for the account list
        self.account_list_tree = ttk.Treeview(self.account_list_frame,
                                              columns=("Game", "Username", "Password", "Note"))
        self.account_list_tree.column("#0", width=25, minwidth=25)
        self.account_list_tree.column("Game", width=50, minwidth=50)
        self.account_list_tree.column("Username", width=300, minwidth=100)
        self.account_list_tree.column("Password", width=300, minwidth=100)
        self.account_list_tree.column("Note", width=500, minwidth=400)
        self.account_list_tree.heading("#0", text="ID")
        self.account_list_tree.heading("Game", text="Game")
        self.account_list_tree.heading("Username", text="Username")
        self.account_list_tree.heading("Password", text="Password")
        self.account_list_tree.heading("Note", text="Note")

        # Add the Treeview widget to the account list frame
        self.account_list_tree.pack(fill="both", expand=True)

        # Load saved data and populate the account list
        self.populate_account_list()

        self.account_list_tree.bind("<ButtonRelease-1>", self.on_cell_click)

    def on_cell_click(self, event):
        # Get the row and column of the clicked cell
        row = self.account_list_tree.identify_row(event.y)
        column = self.account_list_tree.identify_column(event.x)

        # Get the text from the clicked cell
        if row and column:
            cell_value = self.account_list_tree.item(row)["values"][int(column[1])-1]

            # Copy the text to the clipboard
            self.master.clipboard_clear()
            self.master.clipboard_append(cell_value)


    def populate_account_list(self):
        # Delete all existing rows from the account list
        for row in self.account_list_tree.get_children():
            self.account_list_tree.delete(row)

        # Load saved data and add each account to the account list
        try:
            with open("accounts.csv", mode="r") as file:
                reader = csv.reader(file)
                for i, row in enumerate(reader):
                    if i > 0:
                        self.account_list_tree.insert("", "end", text=i, values=row)

        except FileNotFoundError:
            pass

    def load_data(self):
        try:
            with open("accounts.csv", mode="r") as file:
                reader = csv.reader(file)
                rows = list(reader)
                if len(rows) > 0:
                    self.game_entry.insert(0, rows[-1][0])
                    self.username_entry.insert(0, rows[-1][1])
                    self.password_entry.insert(0, rows[-1][2])
                    self.note_entry.insert(0, rows[-1][3])
        except FileNotFoundError:
            pass

    def save_data(self):
        with open("accounts.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                [self.game_entry.get(), self.username_entry.get(), self.password_entry.get(), self.note_entry.get()])




root = tk.Tk()
app = AccountManager(root)
root.mainloop()
