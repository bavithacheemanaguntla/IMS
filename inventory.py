from tkinter import *
from tkinter import messagebox, filedialog
import time
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

class Application():
    def __init__(self, master, *args, **kwargs):
        self.master = master

        self.left = Frame(master, width=750, height=768, bg='SkyBlue')
        self.left.pack(side=LEFT)

        self.right = Frame(master, width=500, height=500, bg='white')
        self.right.pack(side=RIGHT)

        # components
        self.heading = Label(self.left, text="NEEDS AND DEEDS STORE", font=('ALGERIAN 40 bold'), fg='Black')
        self.heading.place(x=100, y=10)
        current_date = datetime.datetime.now()
        abhi = current_date.strftime("%Y-%m-%d %H:%M:%S")
        self.date_l = Label(self.right, text="Date: " + str(abhi), font=('Calibri 18 bold'), fg='black')
        time.sleep(1)
        self.date_l.place(x=140, y=0)

        # table invoice=======================================================
        self.tproduct = Label(self.right, text="Products", font=('Calibri 20 bold'), fg='Black')
        self.tproduct.place(x=0, y=60)

        self.tquantity = Label(self.right, text="Quantity", font=('Calibri 20 bold'), fg='Black')
        self.tquantity.place(x=150, y=60)

        self.tamount = Label(self.right, text="Price", font=('Calibri 20 bold'), fg='Black')
        self.tamount.place(x=300, y=60)

        # enter stuff
        self.enterid = Label(self.left, text="ID Number", font=('calibri 20 bold'), fg='black')
        self.enterid.place(x=50, y=80)

        self.enteride = Entry(self.left, width=25, font=('Calibri 18 bold'), bg='lightblue')
        self.enteride.place(x=220, y=80)
        self.enteride.focus()

        # button
        self.search_btn = Button(self.left, text="Find", width=18, height=2, bg='green', command=self.ajax)
        self.search_btn.place(x=580, y=70)
        # fill it later by the function ajax

        self.productname = Label(self.left, text="", font=('Calibri 27 bold'), bg='white', fg='steelblue')
        self.productname.place(x=0, y=200)

        self.pprice = Label(self.left, text="", font=('Calibri 27 bold'), bg='white', fg='steelblue')
        self.pprice.place(x=0, y=250)

        # total label
        self.total_l = Label(self.right, text="", font=('arial 40 bold'), bg='lightblue', fg='white')
        self.total_l.place(x=0, y=400)

        # Initialize lists
        self.products_list = []
        self.product_quantity = []
        self.product_id = []
        self.product_price = []

    def ajax(self, *args, **kwargs):
        self.conn = mysql.connector.connect(host='localhost', user='root', password='Sreethu@12345',
                                            database='inventory_system', port=3306)
        self.get_id = self.enteride.get()
        # get the product info with that id and fill in the labels above
        self.mycursor = self.conn.cursor()
        self.mycursor.execute("SELECT * FROM inventory WHERE id= %s", [self.get_id])
        self.pc = self.mycursor.fetchall()
        if self.pc:
            for self.r in self.pc:
                self.get_id = self.r[0]
                self.get_name = self.r[1]
                self.get_price = self.r[3]
                self.get_stock = self.r[2]

            self.productname.configure(text="Product's Name: " + str(self.get_name), fg='black', bg='white',
                                       font=('calibri,20,bold'))
            self.productname.place(x=50, y=200)

            # Create the quantity and the discount label
            self.quantityl = Label(self.left, text="Enter the qty ", font=('Calibri 18 bold'), fg='black',
                                   bg='white')
            self.quantityl.place(x=0, y=300)

            self.quantity_e = Entry(self.left, width=10, font=('Calibri 18 bold'), bg='lightblue')
            self.quantity_e.place(x=170, y=300)
            self.quantity_e.focus()

            # Discount
            self.discount_l = Label(self.left, text="Discount offered", font=('Calibri 20 bold'), fg='black',
                                    bg='white')
            self.discount_l.place(x=320, y=300)

            self.discount_e = Entry(self.left, width=10, font=('Calibri 20 bold'), bg='lightblue')
            self.discount_e.place(x=530, y=300)
            self.discount_e.insert(END, 0)

            # Add to cart button
            self.add_to_cart_btn = Button(self.left, text="Display on the bill receipt", width=40, height=2,
                                           bg='green', command=self.add_to_cart)
            self.add_to_cart_btn.place(x=200, y=370)

            # Generate bill and change
            self.change_l = Label(self.left, text="Enter the amount paid", font=('Calibri 20 bold'), fg='black',
                                  bg='white')
            self.change_l.place(x=0, y=450)

            self.change_e= Entry(self.left, width=10, font=('Calibri 18 bold'), bg='lightblue')
            self.change_e.place(x=280, y=450)

            self.change_btn = Button(self.left, text="Calculate the difference", width=22, height=2, bg='green',
                                     command=self.change_func)
            self.change_btn.place(x=430, y=450)

            # Generate bill button
            self.bill_btn = Button(self.left, text="Create a bill of the items purchased", width=30, height=2,
                                   bg='Purple', fg='white', command=self.generate_bill)
            self.bill_btn.place(x=0, y=550)
        else:
            messagebox.showinfo("Error", "No product found with this ID.")

    def add_to_cart(self, *args, **kwargs):
        self.quantity_value = int(self.quantity_e.get())

        if self.quantity_value > int(self.get_stock):
            tkinter.messagebox.showinfo("Error", "Not that many products in our stock.")
        else:
            # Calculate the price first
            self.final_price = (float(self.quantity_value) * float(self.get_price)) - (
                    float(self.discount_e.get()))
            self.products_list.append(self.get_name)
            self.product_quantity.append(self.quantity_value)
            self.product_id.append(self.get_id)
            self.product_price.append(self.final_price)

            self.x_index = 0
            self.y_index = 100
            self.counter = 0
            for self.p in self.products_list:
                self.tempname = Label(self.right, text=str(self.products_list[self.counter]), font=('arial 18 bold'),
                                      bg='gray', fg='white')
                self.tempname.place(x=0, y=self.y_index)
                self.tempqt = Label(self.right, text=str(self.product_quantity[self.counter]),
                                    font=('arial 18 bold'), bg='gray', fg='white')
                self.tempqt.place(x=150, y=self.y_index)
                self.tempprice = Label(self.right, text=str(self.product_price[self.counter]),
                                       font=('arial 18 bold'), bg='gray', fg='white')
                self.tempprice.place(x=300, y=self.y_index)

                self.y_index += 40
                self.counter += 1

            # Total configure
            self.total_l.configure(text="Final amount=Rs. " + str(sum(self.product_price)), bg='gray', fg='white',
                                   font=('20'))
            self.total_l.place(x=180, y=450)

            # Delete
            self.quantity_e.place_forget()
            self.discount_l.place_forget()
            self.discount_e.place_forget()
            self.productname.configure(text="")
            self.pprice.configure(text="")
            self.add_to_cart_btn.destroy()

            # Autofocus to the enter id
            self.enteride.focus()
            self.quantityl.focus()
            self.enteride.delete(0, END)

    def change_func(self, *args, **kwargs):
        try:
            self.amount_given = float(self.change_e.get())
        except ValueError:
            tkinter.messagebox.showerror("Error", "Please enter a valid amount.")
            return
    
        self.our_total = float(sum(self.product_price))
        self.to_give = self.amount_given - self.our_total

    # Calculate concession amount
        self.concession_amount = self.our_total - sum(self.product_price)

    # Label change
        self.c_amount = Label(self.left, text="Change is Rs. {:.2f}, Concession: Rs. {:.2f}".format(self.to_give, self.concession_amount),font=('Calibri 20 bold'),fg = 'Black', bg='white')
        self.c_amount.place(x=0, y=500)



    def generate_bill(self, *args, **kwargs):
        self.mycursor.execute("SELECT * FROM inventory WHERE id=%s", [self.get_id])
        self.pc = self.mycursor.fetchall()
        for r in self.pc:
            self.old_stock = r[2]
        for i in self.products_list:
            for r in self.pc:
                self.old_stock = r[2]
            self.new_stock = int(self.old_stock) - int(self.quantity_value)
            # Updating the stock
            self.mycursor.execute("UPDATE inventory SET stock=%s WHERE id=%s", [self.new_stock, self.get_id])
            self.conn.commit()

            # Insert into transaction
            current_date = datetime.datetime.now()
            self.mycursor.execute("INSERT INTO transaction (product_name,quantity,amount,date) VALUES(%s,%s,%s,%s)",
                                  [self.get_name, self.quantity_value, self.get_price, current_date])
            self.conn.commit()

        # Prompt user to select the destination folder to save the PDF
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
        if file_path:
            # Generate PDF and save it
            c = canvas.Canvas(file_path, pagesize=letter)
            c.drawString(100, 750, "Bill of Purchased Items")
            c.drawString(100, 730, "Date: " + str(datetime.datetime.now()))
            c.drawString(100, 710, "Product Name: " + self.get_name)
            c.drawString(100, 690, "Quantity: " + str(self.quantity_value))
            c.drawString(100, 670, "Price: " + str(self.get_price))
            c.drawString(100, 650, "Total Amount: " + str(sum(self.product_price)))
            c.save()

            tkinter.messagebox.showinfo("Success", "Bill generated successfully and saved at:\n" + file_path)

master = Tk()

ob = Application(master)

master.mainloop()
