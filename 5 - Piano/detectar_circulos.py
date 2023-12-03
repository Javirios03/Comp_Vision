import cv2
import numpy as np
from matplotlib import pyplot as plt

# Cargar la imagen
img = cv2.imread('paperpiano\data\shapes.png', cv2.IMREAD_COLOR)

def get_contours(img):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un desenfoque gaussiano para reducir el ruido
    gray = cv2.medianBlur(gray, 5)

    # Detectar los bordes
    edges = cv2.Canny(gray, 50, 150)

    edges = cv2.dilate(edges, None,iterations=4)

    edges = cv2.GaussianBlur(edges, (5, 5), 0)

    # dibujar los bordes de azul
    # plt.imshow(edges,cmap = 'gray')
    # plt.show()

    # Encontrar contornos
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # show edges and contours
    # for cnt in contours:
    #     # Obtener rectángulo de contorno
    #     x, y, w, h = cv2.boundingRect(cnt)

    #     # Dibujar el rectángulo
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Mostrar la imagen original con los contornos
    # plt.imshow(img)
    # plt.show()

    return contours



def get_circles(img):
    # Convertir la imagen a escala de grises
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Aplicar un desenfoque gaussiano para reducir el ruido
    gray = cv2.medianBlur(gray, 5)    

    # Usar la transformada de Hough para encontrar círculos
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1, 200, param1=50, param2=30, minRadius=20, maxRadius=450)

    # Verificar si se encontraron círculos
    # if circles is not None:
    #     circles = np.uint16(np.around(circles))
    #     for i in circles[0, :]:
    #         # Dibujar el círculo externo
    #         cv2.circle(img, (i[0], i[1]), i[2], (0, 255, 0), 2)
    #         # Dibujar el centro del círculo
    #         cv2.circle(img, (i[0], i[1]), 2, (0, 0, 255), 3)


    # # Mostrar la imagen con los círculos detectados
    # plt.imshow(img)
    # plt.show()

    return circles