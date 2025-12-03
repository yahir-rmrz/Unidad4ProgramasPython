
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk
import random

def crearBaseDatos():
    con = sqlite3.connect("tienda.db")
    cursor = con.cursor()

    cursor.execute(""" CREATE TABLE IF NOT EXISTS productos(id INTEGER PRIMARY KEY AUTOINCREMENT, codigo TEXT NOT NULL, producto TEXT NOT NULL, precio REAL NOT NULL) """)

    cursor.execute(""" CREATE TABLE IF NOT EXISTS almacen(id INTEGER PRIMARY KEY AUTOINCREMENT,codigoProducto TEXT NOT NULL, stock REAL NOT NULL,descripcion TEXT NOT NULL)""")


class Principal():
    def __init__(self, master):
        self.ven = master
        ancho = 560
        alto = 410
        self.ven.title('Practica 2 Unidad 4')
        ventana_alto = self.ven.winfo_screenmmwidth()
        ventana_ancho = self.ven.winfo_screenheight()
        x = (ventana_alto // 2) - (ancho //2)
        y = (ventana_ancho //2) - (alto // 2)
        self.ven.geometry(f'{ancho}x{alto}+{x+480}+{y+15}')
        self.index = -1

    def inicio(self):
        self.us = Label(text=f"CRUD de productos")
        Label(self.ven,text="Producto").place(x=10, y=10)
        self.producto = Entry(self.ven, text= "Escribe el producto")
        self.producto.place(x=10, y=40)
        Label(self.ven,text="Descripcion").place(x=150, y=10)
        self.descripcion = Entry(self.ven, text= "Descripcion")
        self.descripcion.place(x=150, y=40)
        Label(self.ven,text="Precio").place(x=290, y=10)
        self.precio = Entry(self.ven, text= "Precio")
        self.precio.place(x=290, y=40)
        Label(self.ven,text="Cantidad").place(x=420, y=10)
        self.cantidad = Entry(self.ven, text= "Cantidad")
        self.cantidad.place(x=420, y=40)
        columnas = ("ID", "CODIGO", "PRODUCTO", "PRECIO", "DESCRIPCION", "STOCK")
        self.tabla = ttk.Treeview(self.ven, columns= columnas, show="headings")
        self.tabla.place(x=10,y=100, width=480, height=190)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=30)
        scrolly = ttk.Scrollbar(self.ven, orient="vertical", command=self.tabla.yview)
        scrollx = ttk.Scrollbar(self.ven, orient="horizontal", command=self.tabla.xview)

        scrolly.place(x=480, y=90, height=200)
        scrollx.place(x=10, y=280, width=470)
        self.agregar = Button(self.ven, text="Agregar", width=10, state="normal", command=self.agregarProducto)
        self.agregar.place(x=30, y=320)
        self.modificar = Button(self.ven, text="Modificar", width=10, state="disabled", command=self.modificarProdcuto)
        self.modificar.place(x=130, y=320)
        self.eliminar = Button(self.ven, text="Eliminar", width=10, state="disabled", command=self.eliminarProducto)
        self.eliminar.place(x=230, y=320)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila)
        self.mostrarDatos()

    def seleccionFila(self, event):
        self.limpiarCajas()
        try: 
            self.index = self.tabla.selection()[0]
        except:
            return

        valores = self.tabla.item(self.index, "values")
        self.producto.insert(0, valores[2])
        self.precio.insert(0, valores[3])
        self.descripcion.insert(0, valores[4])
        self.cantidad.insert(0, valores[5])
        self.agregar.config(state= "disabled")
        self.modificar.config(state= "normal")
        self.eliminar.config(state= "normal")

    def modificarProdcuto(self):
        if not self.verificar():
            messagebox.showinfo("Mensaje", "Ya existe")
            #UPDATE
        else: 
            try: 
                self.index = self.tabla.selection()[0]
            except:
                return

            valores = self.tabla.item(self.index, "values")
            id = valores[0]
            pro = self.producto.get()
            pre = self.precio.get()
            des = self.descripcion.get()
            can = self.cantidad.get()
            if len(pro) != 0 and len(pre) !=0 and len(des) != 0 and len(can)!=0:
                codigo = pro[:2].upper() + str(random.randint(0, 100)) + des[0].upper()
                con= sqlite3.connect("tienda.db")
                cursor=con.cursor()
                cursor.execute("UPDATE  Productos SET Codigo=?,Producto=?,Precio=? WHERE id =?",(codigo,pro,pre,id))
                cursor.execute("UPDATE  Almacen SET CodigoProducto=?,Stock=?,Descripcion=? WHERE id =?",(codigo,des,can,id))
                con.commit()
                con.close()
                self.limpiarCajas()
                self.actualizarTabla()
                self.agregar.config(state="normal")
                self.modificar.config(state="disabled")
                self.eliminar.config(state="disabled")
            else:
                messagebox.showerror("Error", "Faltan Datos")
       
    def verificar(self):
        p = self.producto.get()
        d = self.descripcion.get()
        pr = self.precio.get()
        s = self.cantidad.get()
        if len(p) != 0 and len(pr) !=0 and len(d) != 0 and len(s)!=0:
            con= sqlite3.connect("tienda.db")
            cursor=con.cursor()
            cursor.execute("SELECT producto FROM productos WHERE producto =? "),(p,)
            resultado = cursor.fetchone
            con.commit()
            cursor.close()
            if not resultado:
                return True
            else:
                return False

    def eliminarProducto(self):
        try:
            self.index = self.tabla.selection()[0]
        except:
            return
        valores = self.tabla.item(self.index, "values")
        id = valores[0]
        con = sqlite3.connect("tienda.db")
        cursor = con.cursor()
        cursor.execute("DELETE FROM productos WHERE id=?", (id))
        cursor.execute("DELETE FROM almacen WHERE id=?", (id))
        con.commit()
        con.close()
        self.actualizarTabla()
        self.limpiarCajas
        self.agregar.config(state="normal")
        self.modificar.config(state="disabled")
        self.eliminar.config(state="disabled")

    def mostrarDatos(self):
        con = sqlite3.connect("tienda.db")
        cursor = con.cursor()
        cursor.execute("""
           SELECT productos.id,
                    productos.codigo,
                    productos.producto,
                    productos.precio,
                    almacen.stock,
                    almacen.descripcion       
           FROM productos
           INNER JOIN almacen
           ON productos.codigo = almacen.codigoProducto
        """)
        #datos = cursor.fetchall()
        #print(datos)
        for i in cursor.fetchall():
            self.tabla.insert("", END, values=i)
        con.commit()
        con.close
        
    def limpiarCajas(self):
        self.producto.delete(0, END)
        self.precio.delete(0, END)
        self.descripcion.delete(0, END)
        self.cantidad.delete(0, END)
        

    def actualizarTabla(self):
        for i in self.tabla.get_children():
                self.tabla.delete(i)
        self.mostrarDatos()

    def agregarProducto(self):
        prf = 0.0
        st = 0
        p = self.producto.get()
        d = self.descripcion.get()
        pr = self.precio.get()
        s = self.cantidad.get()
        if len(p)!= 0 and len(d)!= 0 and len(pr)!= 0 and len(s)!= 0:
            prf = float(pr)
            st = int(s)
            codigo = p[:2].upper() + str(random.randint(0, 100)) + d[0].upper()
            con = sqlite3.connect("tienda.db")
            cursor = con.cursor()
            cursor.execute("INSERT INTO productos(codigo, producto, precio) VALUES (?,?,?)", (codigo, p, prf))
            cursor.execute("INSERT INTO almacen(codigoProducto, stock, descripcion) VALUES (?,?,?)", (codigo, d, st))
            con.commit()
            con.close
            self.actualizarTabla()
            self.limpiarCajas()
        else:
            messagebox.showerror("Error", "Faltan datos")


if __name__ == "__main__":
    crearBaseDatos()
    master = Tk()
    app = Principal(master)
    app.inicio()
    master.mainloop()

