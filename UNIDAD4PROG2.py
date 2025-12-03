from doctest import master
from imaplib import Commands
from pydoc import text
from re import A
import select
from tkinter import *
from tkinter import messagebox
import sqlite3
from tkinter import ttk
import tkinter as tk

def crearBaseDatos():
    con =sqlite3.connect("usuarios.db")
    cursor = con.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios(id INTEGER PRIMARY KEY AUTOINCREMENT, usuario TEXT NOT NULL,password TEXT NOT NULL) """)

    cursor.execute("SELECT * FROM usuarios WHERE usuario = 'admin'")
    
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)", ("admin", "12345"))

    con.commit()
    con.close
class principal():
    def __init__(self, master):
        self.ven = master
        ancho = 250
        alto = 200
        self.ven.title('Practica 2 Unidad 4')
        ventana_alto = self.ven.winfo_screenmmwidth()
        ventana_ancho = self.ven.winfo_screenheight()
        x = (ventana_alto // 2) - (ancho //2)
        y = (ventana_ancho //2) - (alto // 2)
        self.ven.geometry(f'{ancho}x{alto}+{x+480}+{y+15}')

    def inicio(self):
        Label(self.ven, text="Usuario").place(x=50, y=20)
        Label(self.ven, text="Password").place(x=50, y=75)
        self.n1 = Entry(self.ven)
        self.n1.place(x=50, y=40)
        self.n2 = Entry(self.ven)
        self.n2 = Entry(self.ven, show="*")
        self.n2.place(x=50, y=95)
        
        Button(self.ven, text="Enviar", width=15, command=self.enviar).place(x=50,y=130)
        Button(self.ven, text="Cerar", width=15, command=self.cerrar).place(x=50,y=160)
        self.ven.mainloop()

    def enviar(self):
        u = self.n1.get()
        p = self.n2.get()
        # revisar en la base de datos si existe el usuairio
        con = sqlite3.connect('usuarios.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario = ? AND password =?", (u,p))
        resultado = cursor.fetchone()
        con.close()
        if resultado:
        #if u == "admin" and p =="12345":
            self.ven.withdraw() #ocultar ventana antes de llamar a la segunda ventana
            otra = Toplevel(self.ven)
            ventanados(otra, self.ven, u)
        else:
            messagebox.showerror("Error", "Datos Incorrectos")
            self.n1.delete(0, END)
            self.n2.delete(0, END)

    def cerrar(self):
        self.ven.destroy()


class ventanados():
    def __init__(self, master, ven, u):
        self.dos = master
        ancho = 550
        alto = 320
        self.dos.title('Practica 1 Unidad 4')
        ventana_alto = self.dos.winfo_screenmmwidth()
        ventana_ancho = self.dos.winfo_screenheight()
        x = (ventana_alto // 2) - (ancho //2)
        y = (ventana_ancho //2) - (alto // 2)
        self.dos.geometry(f'{ancho}x{alto}+{x+480}+{y+15}')
        #Label(self.dos, text="Bienvenido \n usuario").place(x=420,y=5)
        self.ven = ven
        self.usuariologin = u
        self.us=Label(self.dos, text="")
        self.us.place(x=420,y=5)
        self.mostrar()
        self.mostrarTabla()
        self.menus = tk.Menu(self.dos)
        self.dos.config(menu=self.menus)
        self.archivo = tk.Menu(self.menus, tearoff=0)
        self.archivo.add_command(label="Agregar", command= self.crearUsuario)
        self.archivo.add_command(label="Modificar", command= self.modificarUsuario)
        self.archivo.add_command(label="Eliminar", command= self.eliminarUsuario)
        self.archivo.add_command(label="salir", command= self.salir)
        self.menus.add_cascade(label = "Archivo", menu=self.archivo)

    def salir(self):
        self.dos.destroy()
        self.ven.destroy()

    def crearUsuario(self):
        if len(self.usuario.get()) != 0 and len(self.password.get()) != 0:
            con =sqlite3.connect("usuarios.db")
            cursor = con.cursor()
            cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)", (self.usuario.get(), self.password.get()))
            con.commit()
            con.close

        else:
            messagebox.showerror("Error", "Faltan Datos")

    def actualizarTabla(self):
        for i in self.tabla.get_children():
                self.tabla.delete()
        self.mostrarTabla()

    def seleccionFila(self, event):
        try:
            index = self.tabla.selection()[0]
            valores = self.tabla.item(index, "values")
            self.usuario.delete(0, END)
            self.password.delete(0, END)
            self.usuario.insert(0,valores[1])
            self.password.insert(0,valores[2])

        except:
            if not index:
                messagebox.showerror("Error", "Elige una fila")

    def modificarUsuario(self):
        pass

    def eliminarUsuario(self):
        try:
            index = self.tabla.selection()[0]
            valores = self.tabla.item(index, "values")
            id = valores[0]
            usuario = valores[1]
            if usuario == self.ususariologin:
                messagebox.showerror("Error", "No te puedes eliminar a ti mismo")
            else:
                con =sqlite3.connect("usuarios.db")
                cursor = con.cursor()
                cursor.execute("DELETE FROM usuarios WHERE id=?", (id))
                con.commit()
                con.close
                self.actualizarTabla()
        except:
            if not index:
                messagebox.showerror("Error", "Elige una fila")
        


    def mostrarTabla(self):
        con = sqlite3.connect('usuarios.db')
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios")
        for i in cursor.fetchall():
            self.tabla.insert("", END, values=i)
        con.close()
        

    def mostrar(self):
        self.us.config(text=f"Bienvenido \n {self.usuario}")
        Label(self.dos,text="Escribe el usuario").place(x=10, y=10)
        self.usuario = Entry(self.dos, text= "Escribe el usuario")
        self.usuario.place(x=10, y=40)
        Label(self.dos,text="Escribe el Password").place(x=150, y=10)
        self.password = Entry(self.dos, text= "Escribe el password")
        self.password.place(x=150, y=40)
        columnas = ("ID", "Usuario", "Password")
        self.tabla = ttk.Treeview(self.dos, columns= columnas, show="headings")
        self.tabla.place(x=10,y=100, width=350, height=290)
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, anchor="center", width=30)
        scrolly = ttk.Scrollbar(self.dos, orient="vertical", command=self.tabla.yview)
        scrollx = ttk.Scrollbar(self.dos, orient="horizontal", command=self.tabla.xview)

        scrolly.place(x=355, y=90, height=210)
        scrollx.place(x=10, y=280, width=340)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionFila)
          

if __name__ == '__main__':
    crearBaseDatos()
    master = Tk()
    app = principal(master)
    app.inicio()
    master.mainloop()

 