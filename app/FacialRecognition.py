import cv2
import imutils
import numpy as np
import os


class ReadingFace():

    def initCam(name, pathUser, action):
        if action == True:
            count = 0
            capture = cv2.VideoCapture(0)
            faceClassif = cv2.CascadeClassifier(
                cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

            while True:
                ret, frame = capture.read()
                if ret == False:
                    break
                frame = imutils.resize(frame, width=640)
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                auxFrame = frame.copy()
                faces = faceClassif.detectMultiScale(gray, 1.3, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(
                        frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    rostro = auxFrame[y:y+h, x:x+w]
                    rostro = cv2.resize(rostro, (150, 150),
                                        interpolation=cv2.INTER_CUBIC)
                    #cv2.imwrite(pathUser + '/rotro_{}.jpg'.format(count), rostro)
                    cv2.imwrite(
                        f'{pathUser}/rostro_{name}_{count}.jpg', rostro)
                    count = count + 1
                cv2.imshow(f'Escaneado a {name}', frame)
                k = cv2.waitKey(1)
                if k == 27 or count >= 300:
                    break
            capture.release()
            cv2.destroyAllWindows()
            return True
        else:
            print('fail')
            return True

    def training(dataPath):
        peopleList = os.listdir(dataPath)
        labels = []
        facesData = []
        label = 0
        for nameDir in peopleList:
            personPath = dataPath + '/' + nameDir
            print('Leyendo las imágenes')
            for fileName in os.listdir(personPath):
                print('Rostros: ', nameDir + '/' + fileName)
                labels.append(label)
                facesData.append(cv2.imread(personPath+'/'+fileName, 0))
                image = cv2.imread(personPath+'/'+fileName, 0)
                cv2.imshow('image', image)
                cv2.waitKey(10)
            label = label + 1
        print('labels= ', labels)
        print('Número de etiquetas 0: ', np.count_nonzero(np.array(labels) == 0))
        print('Número de etiquetas 1: ', np.count_nonzero(np.array(labels) == 1))

        # Métodos para entrenar el reconocedor
        face_recognizer = cv2.face.EigenFaceRecognizer_create()
        face_recognizer = cv2.face.FisherFaceRecognizer_create()
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()
        # Entrenando el reconocedor de rostros
        print("Entrenando...")
        face_recognizer.train(facesData, np.array(labels))
        # Almacenando el modelo obtenido
        face_recognizer.write('modeloEigenFace.xml')
        face_recognizer.write('modeloFisherFace.xml')
        face_recognizer.write('modeloLBPHFace.xml')
        print("Modelo almacenado...")

    def recognition(dataPath):
        imagePaths = os.listdir(dataPath)
        print('imagePaths=', imagePaths)

        face_recognizer = cv2.face.EigenFaceRecognizer_create()
        face_recognizer = cv2.face.FisherFaceRecognizer_create()
        face_recognizer = cv2.face.LBPHFaceRecognizer_create()

        # Leyendo el modelo
        face_recognizer.read('modeloEigenFace.xml')
        face_recognizer.read('modeloFisherFace.xml')
        face_recognizer.read('modeloLBPHFace.xml')

        cap = cv2.VideoCapture(0)
        #cap = cv2.VideoCapture('Video.mp4')

        faceClassif = cv2.CascadeClassifier(
            cv2.data.haarcascades+'haarcascade_frontalface_default.xml')
        while True:
            ret, frame = cap.read()
            if ret == False:
                break
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            auxFrame = gray.copy()

            faces = faceClassif.detectMultiScale(gray, 1.3, 5)

            for (x, y, w, h) in faces:
                rostro = auxFrame[y:y+h, x:x+w]
                rostro = cv2.resize(rostro, (150, 150), interpolation=cv2.INTER_CUBIC)
                result = face_recognizer.predict(rostro)

                cv2.putText(frame, '{}'.format(result), (x, y-5),
                            1, 1.3, (255, 255, 0), 1, cv2.LINE_AA)
                '''
                # EigenFaces
                if result[1] < 5700:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)

                # FisherFace
                if result[1] < 500:
                    cv2.putText(frame,'{}'.format(imagePaths[result[0]]),(x,y-25),2,1.1,(0,255,0),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,255,0),2)
                else:
                    cv2.putText(frame,'Desconocido',(x,y-20),2,0.8,(0,0,255),1,cv2.LINE_AA)
                    cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
        cv2.rectangle(frame, (x,y),(x+w,y+h),(0,0,255),2)
                '''
                # LBPHFace
                if result[1] < 70:
                    print(result[1])
                    cv2.putText(frame, '{}'.format(
                        imagePaths[result[0]]), (x, y-25), 2, 1.1, (0, 255, 0), 1, cv2.LINE_AA)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                elif result[1] <= 52:
                    print('No se esta capturando rostro')
                else:
                    cv2.putText(frame, 'Desconocido', (x, y-20), 2,
                                0.8, (0, 0, 255), 1, cv2.LINE_AA)

            cv2.imshow('frame', frame)
            k = cv2.waitKey(1)
            
            