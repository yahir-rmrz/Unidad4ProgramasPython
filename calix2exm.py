# ======================================================
# PROGRAMA SIMPLE PARA EXAMEN
# Login + CRUD basico con SQLite y Tkinter
# ======================================================

from tkinter import *
from tkinter import messagebox, ttk
import sqlite3


# ======================================================
# CREAR BASE DE DATOS SI NO EXISTE
# ======================================================

def crearBD():
    con = sqlite3.connect("examen.db")
    cursor = con.cursor()

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Crear usuario admin si no existe
    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)",
                        ("admin", "123"))
    con.commit()
    con.close()


# ======================================================
# LOGIN
# ======================================================

class Login:
    def __init__(self, win):
        self.ven = win
        self.ven.title("Login")
        self.ven.geometry("220x160")

        Label(self.ven, text="Usuario").pack()
        self.u = Entry(self.ven)
        self.u.pack()

        Label(self.ven, text="Password").pack()
        self.p = Entry(self.ven, show="*")
        self.p.pack()

        Button(self.ven, text="Entrar", command=self.validar).pack(pady=10)

    def validar(self):
        u = self.u.get()
        p = self.p.get()

        con = sqlite3.connect("examen.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND password=?", (u, p))
        dato = cursor.fetchone()
        con.close()

        if dato:
            self.ven.withdraw()
            nueva = Toplevel(self.ven)
            CRUD(nueva).inicio()
        else:
            messagebox.showerror("Error", "Datos incorrectos")
            self.u.delete(0, END)
            self.p.delete(0, END)


# ======================================================
# CRUD MUY SIMPLE (AGREGAR + LISTAR)
# ======================================================

class CRUD:
    def __init__(self, win):
        self.ven = win
        self.ven.title("CRUD Examen")
        self.ven.geometry("350x280")

    def inicio(self):
        Label(self.ven, text="Nuevo Usuario:").place(x=10, y=10)
        self.u = Entry(self.ven)
        self.u.place(x=10, y=30)

        Label(self.ven, text="Password:").place(x=150, y=10)
        self.p = Entry(self.ven)
        self.p.place(x=150, y=30)

        Button(self.ven, text="Agregar", command=self.agregar).place(x=260, y=25)

        # Tabla
        columnas = ("ID", "Usuario", "Password")
        self.tabla = ttk.Treeview(self.ven, columns=columnas, show="headings")
        self.tabla.place(x=10, y=80, width=300, height=170)

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.mostrar()

    def mostrar(self):
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        con = sqlite3.connect("examen.db")
        cursor = con.cursor()
        cursor.execute("SELECT * FROM usuarios")
        for fila in cursor.fetchall():
            self.tabla.insert("", END, values=fila)
        con.close()

    def agregar(self):
        u = self.u.get()
        p = self.p.get()

        if len(u)==0 or len(p)==0:
            messagebox.showerror("Error", "Faltan datos")
            return

        con = sqlite3.connect("examen.db")
        cursor = con.cursor()
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)", (u, p))
        con.commit()
        con.close()

        self.mostrar()
        self.u.delete(0, END)
        self.p.delete(0, END)


# ======================================================
# INICIO DEL PROGRAMA
# ======================================================

if __name__ == "__main__":
    crearBD()
    root = Tk()
    app = Login(root)
    root.mainloop()
