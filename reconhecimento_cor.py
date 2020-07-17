# importação das bibliotecas OpenCV e Numpy do Python
import cv2
import numpy as np
'''
    Documentação OpenCV: https://docs.opencv.org/3.4/index.html
    Documentação Numpy: https://numpy.org/doc/
'''

# definindo os extremos das tonalidades do azul
azul_escuro = np.array([105, 50, 0], dtype='uint8')
azul_claro = np.array([255, 200, 50], dtype='uint8')

# definindo a variável camera como a captura do vídeo da câmera(webcam)
camera = cv2.VideoCapture(0)  # Saiba mais: https://docs.opencv.org/2.4/modules/highgui/doc/reading_and_writing_images_and_video.html#videocapture-videocapture

# o código para fazer o reconhecimento da cor é feito de um while True para a câmera ficar ativa durante o tempo que vc quiser
while True:
    # capturar frame a frame
    (sucesso, frame) = camera.read()

    # fazendo a limiarização da imagem do video onde o que estiver entre as tonalidades do azul definidas ficará branca na imagem
    obj = cv2.inRange(frame, azul_escuro, azul_claro)  # Saiba mais: https://docs.opencv.org/3.4/da/d97/tutorial_threshold_inRange.html

    # localizando contornos na imagem limiarizada. São passados por parâmetro uma cópia da imagem, a hierarquia de contorno e o algoritmo de aproximação de contorno
    (cnts, _) = cv2.findContours(obj.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    '''
        Saiba mais sobre:
         - cv2.findContours(): https://docs.opencv.org/trunk/d3/dc0/group__imgproc__shape.html#gadf1ad6a0b82947fa1fe3c3d497f260e0
         - Contorno: https://docs.opencv.org/trunk/d4/d73/tutorial_py_contours_begin.html
         - Hieraquia de contorno: https://docs.opencv.org/3.4/d9/d8b/tutorial_py_contours_hierarchy.html
    '''

    # verificando se existe um contorno
    if len(cnts) > 0:
        # definindo os contornos ordenados em ordem decrescente
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]

        # identificando os pontos pra criar o retângulo que contorna o objeto azul no vídeo
        rect = np.int32(cv2.boxPoints(cv2.minAreaRect(cnt)))

        # desenhando o contorno em volta do objeto azul no vídeo
        cv2.drawContours(frame, [rect], -1, (0, 255, 255), 2)

    # inicializando a janela da câmera e a janela com a imagem limiarizada que mostra o objeto azul na câmera
    cv2.imshow('Câmera', frame)
    cv2.imshow('Limiar', obj)

    # definindo a letra 's'(sair) como botão para parar a execução do programa
    if cv2.waitKey(1) & 0xFF == ord('s'):
        break

# liberando a captura do video e destruindo todas as janelas
camera.release()
cv2.destroyAllWindows()
