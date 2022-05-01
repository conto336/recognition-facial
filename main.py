#!/usr/bin/python3
from app.Window import main
from app.FacialRecognition import ReadingFace

if __name__ == '__main__':
    print('Desea iniciar el reconocimiento facial o escanear un nuevo rostro?')
    option = input(
        'Ingresa [E/e] para escanear o ingrese [R/r] para iniciar el reconocimiento: ')

    if option == "E" or option == "e":
        main()
    if option == "R" or option == "r":
        ReadingFace.training('./asset')
        ReadingFace.recognition('./asset')
