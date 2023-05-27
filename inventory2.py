import sqlite3
from tkinter import *
from tkinter import ttk
from tkinter import messagebox

root = Tk()
root.title("Inventory System")
root.geometry("1080x720")
my_tree = ttk.Treeview(root)

path = "/Users/bebi.a/Documents/CISP71/CISP71_Dictionary_Examples/CISP71_Tkinter_SQLite_Examples/CISP71_Tkinter_SQLite_Examples_Part_1/CRUD project/"

# Create a connection to the database
conn = sqlite3.connect(path+'inventory.db')
cursor = conn.cursor()


def add(id, name, price, location, quantity, status):
    conn = sqlite3.connect(path+'inventory.db')
    cursor = conn.cursor()

    cursor.execute("PRAGMA table_info(inventory)")
    columns = cursor.fetchall()

    column_names = [column[1] for column in columns]
    print("Inventory Columns:")
    print(column_names)

    cursor.execute("""CREATE TABLE IF NOT EXISTS inventory(
        itemId integer, 
        itemName TEXT,
        itemPrice integer, 
        itemLocation TEXT, 
        itemQuantity integer, 
        itemStatus TEXT);""")
    cursor.execute("INSERT INTO inventory VALUES (?, ?, ?, ?, ?, ?)",
                   (id, name, price, location, quantity, status))
    conn.commit()
    conn.close()


def update(id, name, price, location, quantity, status, idName):
    conn = sqlite3.connect(path+'inventory.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    inventory(itemId integer, 
    itemName TEXT,
    itemPrice integer,
    itemLocation TEXT, 
    itemQuantity integer, 
    itemStatus TEXT);""")

    cursor.execute("UPDATE inventory SET itemId = ?, itemName = ?, itemPrice = ?, itemLocation = ?, itemQuantity = ?, itemStatus = ? WHERE itemId = ?",
                   (id, name, price, location, quantity, status, idName))
    conn.commit()
    conn.close()


def delete(inventory):
    conn = sqlite3.connect(path+'inventory.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS
    inventory(itemId integer, 
    itemName TEXT,
    itemLocation TEXT, 
    itemPrice integer,
    itemQuantity integer, 
    itemStatus TEXT);""")
    cursor.execute("DELETE FROM INVENTORY WHERE itemId = '" +
                   str(inventory) + "'")
    conn.commit()


def read():
    conn = sqlite3.connect(path+'inventory.db')
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS
        inventory(itemId TEXT, itemName TEXT, itemPrice TEXT, itemQuantity TEXT)""")

    cursor.execute("SELECT * FROM inventory")
    rows = cursor.fetchall()
    conn.close()
    print(rows)

    return rows


def add_inventory():
    itemId = str(idEntry.get())
    itemName = str(nameEntry.get())
    itemPrice = str(priceEntry.get())
    itemLocation = str(locationEntry.get())
    itemQuantity = str(quantityEntry.get())
    itemStatus = str(statusEntry.get())

    if itemId.strip() == "":
        messagebox.showerror("Error", "Please enter a valid item ID")
        return
    if itemName.strip() == "":
        messagebox.showerror("Error", "Please enter a valid item name")
        return
    if itemPrice.strip() == "":
        messagebox.showerror("Error", "Please enter a valid item price")
        return
    if itemQuantity.strip() == "":
        messagebox.showerror("Error", "Please enter a valid item quantity")
        return

    itemIdInt = int(itemId)
    itemPriceInt = int(itemPrice)
    itemQuantityInt = int(itemQuantity)

    add(itemIdInt, itemName, itemPriceInt,
        itemLocation, itemQuantityInt, itemStatus)
    display_inventory()


def delete_inventory():
    selected_item = my_tree.selection()[0]
    deleteData = str(my_tree.item(selected_item)['values'][0])
    delete(deleteData)
    display_inventory()


def update_inventory():

    selected_items = my_tree.selection()
    if not selected_items:
        messagebox.showerror("Error", "No item selected.")
        return
    display_inventory()

    selected_item = selected_items[0]
    update_name = my_tree.item(selected_item)['values'][0]
    update(idEntry.get(), nameEntry.get(), priceEntry.get(), locationEntry.get(),
           quantityEntry.get(), statusEntry.get(), update_name)


def reset_invetory():
    conn = sqlite3.connect(path+'inventory.db')
    cursor = conn.cursor()

    cursor.execute("DROP TABLE IF EXISTS inventory")

    conn.commit()
    conn.close()

    display_inventory()


def display_inventory():
    for item in my_tree.get_children():
        my_tree.delete(item)

    for i, result in enumerate(read()):
        print(f"Index: {i}, Element: {result}\n")

        my_tree.insert(parent='', index='end', iid=i,
                       text="", values=result, tag="orow")

    my_tree.tag_configure('orow', background='#EEEEEE')


display_inventory()

# GUI
# root = Tk()
# root.title("Inventory management system")
# root.geometry("1080x600")

label = Label(root, text="Managing Inventory", font=('Arial Bold', 30), bd=2)
label.grid(row=0, column=0, columnspan=8, padx=20, pady=20)

idLabel = Label(root, text="ID", font=('Arial', 15))
nameLabel = Label(root, text="Name", font=('Arial', 15))
priceLabel = Label(root, text="Price", font=('Arial', 15))
locationLabel = Label(root, text="Location", font=('Arial', 15))
quantityLabel = Label(root, text="Quantity", font=('Arial', 15))
statusLabel = Label(root, text="Status", font=('Arial', 15))

idLabel.grid(row=1, column=0, padx=10, pady=10)
nameLabel.grid(row=2, column=0, padx=10, pady=10)
priceLabel.grid(row=3, column=0, padx=10, pady=10)
locationLabel.grid(row=4, column=0, padx=10, pady=10)
quantityLabel.grid(row=5, column=0,  padx=10, pady=10)
statusLabel.grid(row=6, column=0, padx=10, pady=10)


# textvariable later

idEntry = Entry(root, width=25, bd=5, font=('Arial', 15))
nameEntry = Entry(root, width=25, bd=5, font=('Arial', 15))
priceEntry = Entry(root, width=25, bd=5, font=('Arial', 15))
locationEntry = Entry(root, width=25, bd=5, font=('Arial', 15))
quantityEntry = Entry(root, width=25, bd=5, font=('Arial', 15))
statusEntry = Entry(root, width=25, bd=5, font=('Arial', 15))

idEntry.grid(row=1, column=1, columnspan=3, padx=5, pady=5)
nameEntry.grid(row=2, column=1, columnspan=3, padx=5, pady=5)
priceEntry.grid(row=3, column=1, columnspan=3, padx=5, pady=5)
locationEntry.grid(row=4, column=1, columnspan=3, padx=5, pady=5)
quantityEntry.grid(row=5, column=1, columnspan=3, padx=5, pady=5)
statusEntry.grid(row=6, column=1, columnspan=3, padx=5, pady=5)

buttonAdd = Button(
    root, text="Add", padx=5, pady=5, width=5, bd=3,
    font=('Arial', 15), bg="#a6cfd5", command=add_inventory
)
buttonAdd.grid(row=7, column=1, columnspan=1)

buttonUpdate = Button(
    root, text="Update", padx=5, pady=5, width=5, bd=3,
    font=('Arial', 15), background="#9c8570", command=update_inventory
)
buttonUpdate.grid(row=7, column=2, columnspan=1)


buttonDelete = Button(
    root, text="Delete", padx=5, pady=5, width=5, bd=3,
    font=('Arial', 15), bg="#901403", command=delete_inventory
)
buttonDelete.grid(row=8, column=1, columnspan=1)

buttonReset = Button(
    root, text="Reset", padx=5, pady=5, width=5, bd=3,
    font=('Arial', 15), bg="#901403", command=reset_invetory
)
buttonReset.grid(row=8, column=2, columnspan=1)

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial bold', 15))

my_tree['columns'] = ("ID", "Name", "Price", "Location", "Quantity", "Status")
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("ID", anchor=W, width=100)
my_tree.column("Name", anchor=W, width=200)
my_tree.column("Price", anchor=W, width=100)
my_tree.column("Location", anchor=W, width=100)
my_tree.column("Quantity", anchor=W, width=100)
my_tree.column("Status", anchor=W, width=100)

my_tree.heading("ID", text="ID", anchor=W)
my_tree.heading("Name", text="Name", anchor=W)
my_tree.heading("Price", text="Price", anchor=W)
my_tree.heading("Location", text="Location", anchor=W)
my_tree.heading("Quantity", text="Quantity", anchor=W)
my_tree.heading("Status", text="Status", anchor=W)

my_tree.tag_configure('orow', background="#ff0000", font=('Arial bold', 15))
my_tree.grid(row=1, column=5, columnspan=4, rowspan=5, padx=10, pady=10)


root.mainloop()
