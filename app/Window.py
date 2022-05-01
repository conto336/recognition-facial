#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
from time import sleep
from tkinter import *
from tkinter import ttk, font
from app.FacialRecognition import ReadingFace
# Gestor de geometría (pack)

class Aplicacion():
    def __init__(self):
        self.raiz = Tk()
        self.raiz.title("App Reconocimiento Facial")

        self.raiz.resizable(0, 0)
        fuente = font.Font(weight='bold')

        self.marco = ttk.Frame(self.raiz, borderwidth=2,
                               relief="raised", padding=(10, 10))

        self.labelName = ttk.Label(
            self.marco, text="Nombre:", font=fuente, padding=(5, 5))

        self.labelParent = ttk.Label(
            self.marco, text="Parentesco:", font=fuente, padding=(5, 5))

        self.labelCargo = ttk.Label(
            self.marco, font=fuente, text="Cargo", padding=(5, 5))

        self.usuario = StringVar()
        self.cargo = StringVar()
        self.parent = StringVar()

        self.inputName = ttk.Entry(self.marco, textvariable=self.usuario,
                                   width=30)

        self.inputParent = ttk.Entry(
            self.marco, textvariable=self.parent, width=30)

        self.inputCargo = ttk.Entry(
            self.marco, textvariable=self.cargo, width=30)

        self.separ1 = ttk.Separator(self.marco, orient=HORIZONTAL)

        self.btnConfirm = ttk.Button(self.marco, text="Aceptar",
                                     padding=(5, 5), command=self.aceptar)

        self.btnCancel = ttk.Button(self.marco, text="Cancelar",
                                    padding=(5, 5), command=quit)

        self.marco.grid(column=0, row=0)

        self.labelName.grid(column=0, row=0)
        self.labelParent.grid(column=0, row=1)
        self.labelCargo.grid(column=0, row=2)

        self.inputName.grid(column=1, row=0, columnspan=2)
        self.inputParent.grid(column=1, row=1, columnspan=3)
        self.inputCargo.grid(column=1, row=2, columnspan=4)

        self.btnConfirm.grid(column=1, row=4)

        self.btnCancel.grid(column=2, row=4)

        self.raiz.mainloop()

    def aceptar(self):
        if self.inputName.get() == '' or self.inputName.get().isspace():
            self.message('El nombre no puede estar vacío', action="close")
        else:
            self.pathUser(self.inputName.get(), action=True, raiz=None)

    def message(self, message, action):
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

        if action == "ok":
            btnConfirm = ttk.Button(marco, text="Ok", padding=(
                5, 5), command=lambda: self.pathUser(self.inputName.get(), action=False, raiz=windowMessage))
            btnCancel = ttk.Button(marco, text="Cerrar", padding=(
                5, 5), command=lambda: windowMessage.destroy())

            btnConfirm.grid(column=0, row=4)
            btnCancel.grid(column=2, row=4)

        if action == "ready":
            btnConfirm = ttk.Button(marco, text="cerrar", padding=(
                5, 5), command=lambda: self.pathUser(self.inputName.get(), action="ready", raiz=windowMessage))
            btnConfirm.grid(column=1, row=4)
        if action == "close":
            btnConfirm = ttk.Button(marco, text="cerrar", padding=(
                5, 5), command=lambda: windowMessage.destroy())
            btnConfirm.grid(column=1, row=4)

    def pathUser(self, name, action, raiz):
        pathUser = f'./asset/{name}'

        if action == True:
            if not os.path.exists(pathUser):
                self.message(
                    f'La carpeta {pathUser} no esta creada \nCarpeta creada: {pathUser}', action="ready")
                os.makedirs(pathUser)
            else:
                self.message(
                    f'Ya existe un directorio con el mismo nombre: {name}', action="close")

        if action == "close":
            raiz.destroy()
            self.raiz.destroy()

        if action == False:
            shutil.rmtree(pathUser)
            os.makedirs(pathUser)
            raiz.destroy()
            self.raiz.destroy()
            sleep(2)
            ReadingFace.initCam(name=name, pathUser=pathUser, action=True)
            self.raiz.destroy()
        if action == "ready":
            raiz.destroy()
            sleep(3)
            ReadingFace.initCam(name=name, pathUser=pathUser, action=True)
            sleep(1)
            self.raiz.destroy()

def main():
    Aplicacion()
    return 0
