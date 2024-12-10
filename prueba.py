import tkinter

def suma():
    ventana = tkinter.Tk()
    ventana.geometry('500x500')
    ventana.title('suma')
    tx1 = tkinter.Label(ventana, text=' suma de dos numeros')
    tx1.pack(pady=5)
    tx2 = tkinter.Label(ventana, text='a')
    tx2.pack(pady=5)
    A = tkinter.Entry(ventana)
    A.pack(pady=5)
    tx3 = tkinter.Label(ventana, text='b')
    tx3.pack(pady=5)
    B = tkinter.Entry(ventana)
    B.pack(pady=5)
    suma = tkinter.Button(ventana, text='suma', command=lambda:sum(int(A.get()), int(B.get()),ventana))
    suma.pack(pady=5)
    resultado = tkinter.Label(ventana, text='')
    resultado.pack(pady=10)
    ventana.mainloop()

def sum(a, b, ventana):
    res = a + b
    resultado = tkinter.Label(ventana, text=str(res))
    




if __name__ == '__main__':
    suma()
