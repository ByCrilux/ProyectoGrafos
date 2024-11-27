import tkinter 

import mysql.connector
from grafo import GrafoTransacciones
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox

try:
    c = mysql.connector.connect(
        host="localhost",   
        user="root", 
        password="ByCrilux", 
        database="cuentasBancarias"
    )
    if c.is_connected():
        print("Conexión exitosa")
except mysql.connector.Error as err:
    print(f"Error: {err}")


def verificarUser(nombre_cliente, nro_cuenta):
    cur = c.cursor()
    cur.execute('select nombre_cliente from cuenta')
    tabla = cur.fetchall()
    if any(nombre_cliente == nombre[0] for nombre in tabla):
        cur.execute('select nro_cuenta from cuenta')
        tabla = cur.fetchall()
        if any(nro_cuenta == cuenta[0] for cuenta in tabla):
            print('inicio correcto')
            messagebox.showinfo("Inicio de sesión", "¡Inicio exitoso!")
            dentroCuenta(nombre_cliente, nro_cuenta)          
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos.")
    else:
        messagebox.showerror("Error", "Usuario o contraseña incorrectos.")

def dentroCuenta(nombre, nro):
    ventana = tkinter.Tk()
    ventana.title(f'cuenta de {nombre}')
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    ventana_ancho = 700
    ventana_alto = 400
    pos_x = (pantalla_ancho // 2) - (ventana_ancho // 2)
    pos_y = (pantalla_alto // 2) - (ventana_alto // 2)
    ventana.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")
    realizar_tran = tkinter.Button(ventana, text='realizas transaccion', command=lambda: starTransaccion(nro))
    realizar_tran.pack(pady=10)

    bt = tkinter.Button(ventana, text='ver movimiento de salida', command=lambda:grafo.gradoUsuarioSaliente(nro))
    bt.pack(pady=10)
    bt2 = tkinter.Button(ventana, text='ver movimiento de entrada', command=lambda:grafo.gradoUsuarioEntrante(nro))
    bt2.pack(pady=10)
    
    gastoMayor = tkinter.Button(ventana, text='Pagos Mas alto a las Cuentas', command=lambda: pagoMayorACuentas(nro))
    gastoMayor.pack(pady=10)

    ventana.mainloop()

def pagoMayorACuentas(nroCuenta):
    grafo.pr1(nroCuenta)

def starTransaccion(origen):
    ventana = tkinter.Tk()
    ventana.title('Transaccion')
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    ventana_ancho = 700
    ventana_alto = 400
    pos_x = (pantalla_ancho // 2) - (ventana_ancho // 2)
    pos_y = (pantalla_alto // 2) - (ventana_alto // 2)
    ventana.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")
    hacia = tkinter.Label(ventana, text='numero cuenta destino')
    hacia.pack(pady=10)
    haciaEntrada = tkinter.Entry(ventana)
    haciaEntrada.pack(pady=10)
    monto = tkinter.Label(ventana, text='monto a transferir')
    monto.pack(padx=10)
    montoEntrada = tkinter.Entry(ventana)
    montoEntrada.pack(pady=10)
    tran = tkinter.Button(ventana, text='realizar transaccion',
                          command=lambda: pasar(origen, int(haciaEntrada.get()), float(montoEntrada.get())))
    tran.pack(pady=10)
    ventana.mainloop()

def pasar(desde, hacia, monto):
    if hacia in grafo.cuentas:  
        grafo.insertar_transaccion(desde, hacia, monto)
        messagebox.showinfo("BIEN", "¡Trasaccion exitosa!")
    else:
        messagebox.showerror("Error", "No pertence a una cuenta.")

def inicio():
    ventana = tkinter.Tk()
    ventana.title('inicio')
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    ventana_ancho = 700
    ventana_alto = 400
    pos_x = (pantalla_ancho // 2) - (ventana_ancho // 2)
    pos_y = (pantalla_alto // 2) - (ventana_alto // 2)
    ventana.geometry(f"{ventana_ancho}x{ventana_alto}+{pos_x}+{pos_y}")
    labelUser = tkinter.Label(ventana, text= 'Usuario')
    labelUser.pack(pady=20)
    EntradaUser = tkinter.Entry(ventana) # entrada de user
    EntradaUser.pack(pady=5)
    labelNro = tkinter.Label(ventana, text='nro de cuenta')
    labelNro.pack(pady=5)
    EntradaNro = tkinter.Entry(ventana)
    EntradaNro.pack(pady=5)
    ingresar = tkinter.Button(ventana, text='Ingresar', command = lambda: verificarUser(EntradaUser.get(), int(EntradaNro.get())))
    ingresar.pack()
    ver = tkinter.Button(ventana, text='ver relaciones', command= lambda : graficar())
    ver.pack()
    patronesRep = tkinter.Button(ventana, text='deterctar \ntransferencias \nrepetitivas',
                                 command = lambda: detectarPatrones())
    patronesRep.pack()
    tranIns = tkinter.Button(ventana, text='transacciones atipicas', command=lambda: transaccionesAtipicas())
    tranIns.pack()
    ventana.mainloop()

def transaccionesAtipicas():
    umbral_anomalia = 4999
    #anomalias_dfs_directas = grafo.bfs_detectar_anomalias_directas(umbral_anomalia)
    anomalias_dfs_directas = grafo.dfs_detectar_anomalias_directas(umbral_anomalia)
    print("Anomalías directas detectadas con DFS:")
    for patron in anomalias_dfs_directas:
        messagebox.showinfo("Transferencias sospechosas detectadas:", f"Transferencias sospechosas de {patron[0]} a {patron[1]} con monto: {patron[2]}")


def detectarPatrones():
    patrones = grafo.detectar_transferencias_repetitivas(2,1200)
    for patron in patrones:
        messagebox.showinfo("Transferencias sospechosas detectadas:", f"Transferencias sospechosas de {patron[0]} a {patron[1]} con frecuencia: {patron[2]}")

def graficar():
    grafo.crear_grafo()

if __name__ == '__main__':
    grafo = GrafoTransacciones()
    cur = c.cursor()
    cur.execute('select * from cuenta')
    tabla = cur.fetchall()

    for t in tabla:
        grafo.insertar_cuenta(t[0],t[1])

    cur.execute('select desde, hacia, importe from transaccion')
    tabla = cur.fetchall()

    for t in tabla:
        grafo.insertar_transaccion(t[0], t[1], t[2])

    inicio()