from tkinter import *
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
import tkinter.messagebox
import datetime
import math

class Database:
    def __init__(self,master,*args,**kwargs):
         self.master=master
         self.heading=Label(master,text="DATABASE UPDATION",font=('arial 40 bold'),fg='Red')
         self.heading.place(x=400,y=0)

         #label and entry for id
         self.id_le=Label(master,text="Please enter the ID",font=('Calibri 20 bold'))
         self.id_le.place(x=0,y=100)

         self.id_leb=Entry(master,font=('Calibri 20 bold'),width=10)
         self.id_leb.place(x=380,y=100)

         self.btn_search=Button(master,text="Search",width=15,height=2,bg='Blue',command=self.search)
         self.btn_search.place(x=550,y=100)

         #lables  for the window
         self.name_l=Label(master,text="What's the product",font=('Calibri 20 bold'))
         self.name_l.place(x=0,y=180)

         self.stock_l=Label(master,text="How much is the stock",font=('Calibri 20 bold'))
         self.stock_l.place(x=0,y=260)

         self.cp_l = Label(master, text="Please enter the price ", font=('Calibri 20 bold'))
         self.cp_l.place(x=0, y=340)


        #enteries for window

         self.name_e=Entry(master,width=25,font=('Calibri 20 bold'))
         self.name_e.place(x=380,y=180)

         self.stock_e = Entry(master, width=25, font=('Calibri 20 bold'))
         self.stock_e.place(x=380, y=260)

         self.cp_e = Entry(master, width=25, font=('Calibri 20 bold'))
         self.cp_e.place(x=380, y=340)


         #button to add to the database
         self.btn_add=Button(master,text='Fill in the database',width=30,height=2,bg='SkyBlue',fg='black',command=self.update,font=2)
         self.btn_add.place(x=400,y=400)
         
    def search(self, *args, **kwargs):
        self.conn = mysql.connector.connect(host='localhost',database='inventory_system',user='root',password='Sreethu@12345')
        self.mycursor = self.conn.cursor()
        self.mycursor.execute("SELECT * FROM inventory WHERE id=%s",[self.id_leb.get()])
        result = self.mycursor.fetchall()
        if result:
            for r in result:
                self.n1 = r[1]  # name
                self.n2 = r[2]  # stock
                self.n3 = r[3]  # cp

            # insert into the entries to update
            self.name_e.delete(0, END)
            self.name_e.insert(0, str(self.n1))

            self.stock_e.delete(0, END)
            self.stock_e.insert(0, str(self.n2))

            self.cp_e.delete(0, END)
            self.cp_e.insert(0, str(self.n3))
        else:
            messagebox.showerror("Error", "No record found for the provided ID.")

        self.conn.commit()

    def update(self,*args,**kwargs):
        self.u1=self.name_e.get()
        self.u2 = self.stock_e.get()
        self.u3 = self.cp_e.get()

        self.conn = mysql.connector.connect(host='localhost',database='inventory_system',user='root',password='Sreethu@12345')
        self.mycursor = self.conn.cursor()
        self.mycursor.execute("UPDATE  inventory SET name=%s,stock=%s,price=%s WHERE id=%s",[self.u1,self.u2,self.u3,self.id_leb.get()])
        self.conn.commit()
        tkinter.messagebox.showinfo("Success","Database updated successfully")


master=Tk()

ob=Database(master)

master.mainloop()
