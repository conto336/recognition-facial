
import os
from tkinter import *
from tkinter import ttk, font

def getInfo(name):
    if name == '' or name.isspace():
        message('El nombre no puede estar vacío', action=False)
    else:
        pathUser(name=name)

def init():
    raiz = Tk()
    raiz.title("App Reconocimiento Facial")

    raiz.resizable(0, 0)
    fuente = font.Font(weight='bold')

    marco = ttk.Frame(raiz, borderwidth=2, relief="raised", padding=(10, 10))

    labelName = ttk.Label(
        marco, text="Nombre:", font=fuente, padding=(5, 5))

    labelParent = ttk.Label(
        marco, text="Parentesco:", font=fuente, padding=(5, 5))

    labelCargo = ttk.Label(
        marco, font=fuente, text="Cargo", padding=(5, 5))

    usuario = StringVar()
    cargo = StringVar()
    parent = StringVar()

    inputName = ttk.Entry(marco, textvariable=usuario, width=30)

    inputParent = ttk.Entry(
        marco, textvariable=parent, width=30)

    inputCargo = ttk.Entry(
        marco, textvariable=cargo, width=30)

    btnConfirm = ttk.Button(marco, text="Aceptar", padding=(
        5, 5), command=lambda: getInfo(inputName.get()))

    btnCancel = ttk.Button(marco, text="Cancelar", padding=(
        5, 5), command=lambda: raiz.destroy())

    marco.grid(column=0, row=0)

    labelName.grid(column=0, row=0)
    labelParent.grid(column=0, row=1)
    labelCargo.grid(column=0, row=2)

    inputName.grid(column=1, row=0, columnspan=2)
    inputParent.grid(column=1, row=1, columnspan=3)
    inputCargo.grid(column=1, row=2, columnspan=4)

    btnConfirm.grid(column=1, row=4)

    btnCancel.grid(column=2, row=4)

    raiz.mainloop()


def message(message, action):
    windowMessage = Tk()
    windowMessage.title(message)

    windowMessage.resizable(0, 0)
    fuente = font.Font(weight='bold')

    marco = ttk.Frame(windowMessage, borderwidth=2,
                      relief="raised", padding=(10, 10))

    labelName = ttk.Label(
        marco, text=message, font=fuente, padding=(5, 5))

    marco.grid(column=0, row=0)
    labelName.grid(column=0, row=0)

    if action:
        btnConfirm = ttk.Button(marco, text="Ok", padding=(
            5, 5), command=quit)
        btnCancel = ttk.Button(marco, text="Cerrar", padding=(
            5, 5), command=lambda: windowMessage.destroy())

        btnConfirm.grid(column=0, row=4)
        btnCancel.grid(column=2, row=4)
    else:
        btnConfirm = ttk.Button(marco, text="cerrar", padding=(
            5, 5), command=lambda: windowMessage.destroy())
        btnConfirm.grid(column=1, row=4)


def pathUser(name, action):
    pathUser = f'./asset/{name}'
    if action:
        if not os.path.exists(pathUser):
            message(
                f'La carpeta {pathUser} no esta creada\nCarpeta creada: {pathUser}', action=False)
            os.makedirs(pathUser)
        else:
            message(
                f'Ya existe un directorio con el mismo nombre: {name}', action=True)
    else:
        return name

def rewrite(name):
        pathUser = f'./asset/{name}'
        os.makedirs(pathUser)
        


if __name__ == '__main__':
    init()
