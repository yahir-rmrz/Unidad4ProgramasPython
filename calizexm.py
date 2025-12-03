# ============================================================
#   PROGRAMA FINAL - UNIDAD 4 (SIN ACENTOS Y CON COMENTARIOS)
#   Combina:
#   - Login
#   - CRUD de usuarios
#   - CRUD de productos
#   - Ventanas multiples
#   - Tkinter + SQLite
# ============================================================

from tkinter import *                 # Libreria principal de interfaces graficas
from tkinter import messagebox, ttk   # Mensajes y tablas Treeview
import sqlite3                        # Base de datos SQLite
import random                         # Generar codigos aleatorios

# ============================================================
#   CREACION DE BASE DE DATOS (TABLAS USUARIOS, PRODUCTOS, ALMACEN)
# ============================================================

def crearBases():
    con = sqlite3.connect("final.db")     # Conectar a la base de datos
    cursor = con.cursor()                 # Crear cursor

    # Tabla de usuarios
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL,
            password TEXT NOT NULL
        )
    """)

    # Crear usuario administrador por defecto
    cursor.execute("SELECT * FROM usuarios WHERE usuario='admin'")
    if not cursor.fetchone():             # Si no existe
        cursor.execute("INSERT INTO usuarios(usuario, password) VALUES (?,?)",
                        ("admin", "12345"))

    # Tabla de productos
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT NOT NULL,
            producto TEXT NOT NULL,
            precio REAL NOT NULL
        )
    """)

    # Tabla de almacen (stock)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS almacen(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigoProducto TEXT NOT NULL,
            stock REAL NOT NULL,
            descripcion TEXT NOT NULL
        )
    """)

    con.commit()                           # Guardar cambios
    con.close()                            # Cerrar base de datos


# ============================================================
#   CLASE LOGIN (VENTANA PRINCIPAL)
# ============================================================

class Login:
    def __init__(self, master):
        self.ven = master
        self.ven.title("Login Proyecto Final")
        self.ven.geometry("250x200")       # Configuracion basica de ventana

    def inicio(self):
        # Etiquetas
        Label(self.ven, text="Usuario").place(x=80, y=20)
        Label(self.ven, text="Password").place(x=80, y=80)

        # Entrada de usuario
        self.u = Entry(self.ven)
        self.u.place(x=50, y=45)

        # Entrada de password
        self.p = Entry(self.ven, show="*")
        self.p.place(x=50, y=105)

        # Botones
        Button(self.ven, text="Entrar", command=self.enviar).place(x=50, y=140)
        Button(self.ven, text="Salir", command=self.ven.destroy).place(x=130, y=140)

    # Funcion que valida usuario y password
    def enviar(self):
        usuario = self.u.get()
        password = self.p.get()

        con = sqlite3.connect("final.db")
        cursor = con.cursor()

        # Validar usuario en base de datos
        cursor.execute("SELECT * FROM usuarios WHERE usuario=? AND password=?",
                        (usuario, password))
        dato = cursor.fetchone()
        con.close()

        # Si existe el usuario, entrar al menu
        if dato:
            self.ven.withdraw()                # Ocultar ventana login
            nueva = Toplevel(self.ven)         # Crear nueva ventana
            MenuPrincipal(nueva, self.ven, usuario).inicio()
        else:
            messagebox.showerror("Error", "Datos incorrectos")
            self.u.delete(0, END)
            self.p.delete(0, END)


# ============================================================
#   MENU PRINCIPAL
# ============================================================

class MenuPrincipal:
    def __init__(self, master, login, usuario):
        self.ven = master
        self.login = login                    # Referencia a ventana login
        self.usuario = usuario                # Usuario que inicio sesion

        self.ven.title("Menu Principal")
        self.ven.geometry("300x200")

    def inicio(self):
        # Texto de bienvenida
        Label(self.ven, text=f"Bienvenido {self.usuario}").pack(pady=20)

        # Botones del menu principal
        Button(self.ven, text="CRUD Usuarios", width=20,
               command=self.abrirUsuarios).pack(pady=10)

        Button(self.ven, text="CRUD Productos", width=20,
               command=self.abrirProductos).pack(pady=10)

        Button(self.ven, text="Salir", width=20,
               command=self.cerrarTodo).pack(pady=10)

    # Abrir CRUD usuarios
    def abrirUsuarios(self):
        v = Toplevel(self.ven)
        CrudUsuarios(v, self.usuario).inicio()

    # Abrir CRUD productos
    def abrirProductos(self):
        v = Toplevel(self.ven)
        CrudProductos(v).inicio()

    # Cerrar todas las ventanas
    def cerrarTodo(self):
        self.ven.destroy()
        self.login.destroy()


# ============================================================
#   CRUD DE USUARIOS
# ============================================================

class CrudUsuarios:
    def __init__(self, master, usuarioActual):
        self.ven = master
        self.usuarioActual = usuarioActual
        self.ven.title("Usuarios")
        self.ven.geometry("400x350")

    def inicio(self):
        # Etiquetas
        Label(self.ven, text="Usuario").place(x=20, y=10)
        Label(self.ven, text="Password").place(x=150, y=10)

        # Entradas de texto
        self.u = Entry(self.ven)
        self.u.place(x=20, y=40)

        self.p = Entry(self.ven)
        self.p.place(x=150, y=40)

        # Boton agregar
        Button(self.ven, text="Agregar", command=self.agregar).place(x=300, y=30)

        # Configuracion de tabla
        columnas = ("ID", "Usuario", "Password")
        self.tabla = ttk.Treeview(self.ven, columns=columnas, show="headings")
        self.tabla.place(x=20, y=90, width=350, height=200)

        # Titulos de columnas
        for col in columnas:
            self.tabla.heading(col, text=col)

        # Evento al seleccionar fila
        self.tabla.bind("<<TreeviewSelect>>", self.filaSeleccionada)

        self.mostrar()

    # Mostrar usuarios en tabla
    def mostrar(self):
        # Limpiar tabla
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        con = sqlite3.connect("final.db")
        cursor = con.cursor()

        # Consultar usuarios
        cursor.execute("SELECT * FROM usuarios")
        for i in cursor.fetchall():
            self.tabla.insert("", END, values=i)

        con.close()

    # Funcion al seleccionar una fila
    def filaSeleccionada(self, event):
        try:
            index = self.tabla.selection()[0]
            val = self.tabla.item(index, "values")

            self.u.delete(0, END)
            self.p.delete(0, END)

            self.u.insert(0, val[1])
            self.p.insert(0, val[2])
        except:
            pass

    # Agregar usuario nuevo
    def agregar(self):
        usuario = self.u.get()
        password = self.p.get()

        if len(usuario) == 0 or len(password) == 0:
            messagebox.showerror("Error", "Faltan datos")
            return

        con = sqlite3.connect("final.db")
        cursor = con.cursor()

        cursor.execute("INSERT INTO usuarios(usuario,password) VALUES(?,?)",
                        (usuario, password))

        con.commit()
        con.close()

        self.mostrar()
        self.u.delete(0, END)
        self.p.delete(0, END)


# ============================================================
#   CRUD DE PRODUCTOS
# ============================================================

class CrudProductos:
    def __init__(self, master):
        self.ven = master
        self.ven.title("Productos")
        self.ven.geometry("600x420")

    def inicio(self):
        # Etiquetas y entradas de texto
        Label(self.ven, text="Producto").place(x=10, y=10)
        Label(self.ven, text="Descripcion").place(x=150, y=10)
        Label(self.ven, text="Precio").place(x=300, y=10)
        Label(self.ven, text="Stock").place(x=430, y=10)

        self.p = Entry(self.ven)
        self.p.place(x=10, y=40)

        self.d = Entry(self.ven)
        self.d.place(x=150, y=40)

        self.pr = Entry(self.ven)
        self.pr.place(x=300, y=40)

        self.s = Entry(self.ven)
        self.s.place(x=430, y=40)

        # Boton agregar
        Button(self.ven, text="Agregar", command=self.agregar).place(x=40, y=80)

        # Tabla productos
        columnas = ("ID","CODIGO","PRODUCTO","PRECIO","DESCRIPCION","STOCK")
        self.tabla = ttk.Treeview(self.ven, columns=columnas, show="headings")
        self.tabla.place(x=10, y=130, width=550, height=250)

        for col in columnas:
            self.tabla.heading(col, text=col)

        self.mostrar()

    # Mostrar productos en tabla
    def mostrar(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        con = sqlite3.connect("final.db")
        cursor = con.cursor()

        # Consulta utilizando INNER JOIN
        cursor.execute("""
            SELECT productos.id,
                   productos.codigo,
                   productos.producto,
                   productos.precio,
                   almacen.descripcion,
                   almacen.stock
            FROM productos
            INNER JOIN almacen
            ON productos.codigo = almacen.codigoProducto
        """)

        # Insertar filas en tabla
        for i in cursor.fetchall():
            self.tabla.insert("", END, values=i)

        con.close()

    # Agregar productos
    def agregar(self):
        pro = self.p.get()
        des = self.d.get()
        pre = self.pr.get()
        sto = self.s.get()

        if len(pro)==0 or len(des)==0 or len(pre)==0 or len(sto)==0:
            messagebox.showerror("Error","Faltan datos")
            return

        # Generar codigo automatico
        codigo = pro[:2].upper() + str(random.randint(10,99)) + des[0].upper()

        con = sqlite3.connect("final.db")
        cursor = con.cursor()

        # Insertar en tabla productos
        cursor.execute("INSERT INTO productos(codigo,producto,precio) VALUES(?,?,?)",
                        (codigo, pro, float(pre)))

        # Insertar en tabla almacen
        cursor.execute("INSERT INTO almacen(codigoProducto,stock,descripcion) VALUES(?,?,?)",
                        (codigo, int(sto), des))

        con.commit()
        con.close()

        self.mostrar()

        # Limpiar cajas
        self.p.delete(0, END)
        self.d.delete(0, END)
        self.pr.delete(0, END)
        self.s.delete(0, END)


# ============================================================
#   INICIO DEL PROGRAMA
# ============================================================

if __name__ == "__main__":
    crearBases()          # Crear BD si no existe
    master = Tk()         # Crear ventana principal
    app = Login(master)   # Cargar login
    app.inicio()          # Mostrar login
    master.mainloop()     # Ciclo principal
