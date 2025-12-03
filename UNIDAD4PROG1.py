from doctest import master
from re import A
from tkinter import *
from tkinter import messagebox

class principal():
    def __init__(self, master):
        self.ven = master
        ancho = 250
        alto = 200
        self.ven.title('Practica 1 Unidad 4')
        ventana_alto = self.ven.winfo_screenmmwidth()
        ventana_ancho = self.ven.winfo_screenheight()
        x = (ventana_alto // 2) - (ancho //2)
        y = (ventana_ancho //2) - (alto // 2)
        self.ven.geometry(f'{ancho}x{alto}+{x+480}+{y+15}')

    def inicio(self):
        Label(self.ven, text="Escribe un numero").place(x=50, y=20)
        Label(self.ven, text="Escribe un numero").place(x=50, y=75)
        self.n1 = Entry(self.ven)
        self.n1.place(x=50, y=50)
        self.n2 = Entry(self.ven)
        self.n2.place(x=50, y=100)
        Button(self.ven, text="Enviar", width=15, command=self.enviar).place(x=50,y=130)
        Button(self.ven, text="Cerar", width=15, command=self.cerrar).place(x=50,y=160)
        self.ven.mainloop()

    def enviar(self):
        try:
            n1 = int(self.n1.get())
            n2 = int(self.n2.get())
            self.n1.delete(0, END)
            self.n2.delete(0, END)
            self.ven.withdraw()
            otra = Toplevel(self.ven)
            ventanados(otra, self.ven, n1, n2)
        except ValueError:
            messagebox.showerror("Error", "Algun dato no es un numero")
            self.n1.delete(0, END)
            self.n2.delete(0, END)
            

    def cerrar(self):
        self.ven.destroy()

class ventanados():
    def __init__(self, master, ven, a, b):
        self.dos = master
        ancho = 250
        alto = 200
        self.dos.title('Practica 1 Unidad 4')
        ventana_alto = self.dos.winfo_screenmmwidth()
        ventana_ancho = self.dos.winfo_screenheight()
        x = (ventana_alto // 2) - (ancho //2)
        y = (ventana_ancho //2) - (alto // 2)
        self.dos.geometry(f'{ancho}x{alto}+{x+480}+{y+15}')
        Label(self.dos, text="Hola mundo").place(x=50,y=50)
        Button(self.dos, text="Regresar",width=15 ,command=self.regresar).place(x=50, y=100)
        self.ven = ven
        Button(self.dos, text="Sumar", width=10, command=self.sumar).place(x=50,y=50)
        self.n1 = a 
        self.n2 = b 
     
    def sumar(self):
        messagebox.showinfo("suma",f"La suma es: {self.n1+self.n2}")

    def regresar(self):
        self.dos.destroy()
        self.ven.deiconify()

   


if __name__ == '__main__':
    master = Tk()
    app = principal(master)
    app.inicio()
    master.mainloop()
    