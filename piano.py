import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen original y la imagen de entrada
img_original = cv2.imread('Pattern/piano.png')
img_entrada = cv2.imread('Calib_Images/image0.jpg')

# quedarnos con los pizeles que esten en el rango de blancos y negros de imagen de entrada
white_min,white_max = np.array
black_min,


width_original, height_original = img_original.shape[:2]
width_entrada, height_entrada = img_entrada.shape[:2]



# Convertir las imágenes a escala de grises
gray_original = cv2.cvtColor(img_original, cv2.COLOR_BGR2GRAY)
gray_entrada = cv2.cvtColor(img_entrada, cv2.COLOR_BGR2GRAY)

# Detectar esquinas con el algoritmo de Harris
corners_original = cv2.cornerHarris(gray_original, 2, 3, 0.04)
corners_entrada = cv2.cornerHarris(gray_entrada, 2, 3, 0.04)

# Normalizar las imágenes de esquinas para que los valores estén entre 0 y 1
corners_original = cv2.normalize(corners_original, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)
corners_entrada = cv2.normalize(corners_entrada, None, alpha=0, beta=1, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_32F)

# Ploteamos las imágenes de esquinas
plt.figure(figsize=(15, 15))
plt.subplot(1, 2, 1)
plt.imshow(corners_original, cmap='gray')
plt.title('Esquinas de la imagen original')
plt.subplot(1, 2, 2)
plt.imshow(corners_entrada, cmap='gray')
plt.title('Esquinas de la imagen de entrada')
plt.show()

# Guardamos las coordenadas de las esquinas de la imagen original
lista_esquinas_original = np.array([])
lista_esquinas_entrada = np.array([])
for i in range(width_original):
    for j in range(height_original):
        if corners_original[i, j] > 0.6:
            lista_esquinas_original = np.append(lista_esquinas_original, [i, j])

for i in range(width_entrada):
    for j in range(height_entrada):
        if corners_entrada[i, j] > 0.6:
            lista_esquinas_entrada = np.append(lista_esquinas_entrada, [i, j])


plt.figure(figsize=(15, 15))
plt.subplot(1, 2, 1)
plt.imshow(img_original)
plt.scatter(lista_esquinas_original[1::2], lista_esquinas_original[::2], c='r', s=100)
plt.title('Esquinas de la imagen original')
plt.subplot(1, 2, 2)
plt.imshow(img_entrada)
plt.scatter(lista_esquinas_entrada[1::2], lista_esquinas_entrada[::2], c='r', s=100)
plt.title('Esquinas de la imagen de entrada')
plt.show()


# encontrar la esquina que esté mas cerca de la esquina superior izquierda (0,0)


origen = (0, 0)

# esquinas mas cercanas al origen



plt.figure(figsize=(15, 15))
plt.subplot(1, 2, 1)
plt.imshow(img_original)
plt.scatter(esquina_superior_izquierda[1], esquina_superior_izquierda[0], c='r', s=100)
plt.title('Esquina superior izquierda de la imagen original')
plt.subplot(1, 2, 2)
plt.imshow(img_entrada)
plt.scatter(esquina_superior_izquierda_entrada[1], esquina_superior_izquierda_entrada[0], c='r', s=100)
plt.title('Esquina superior izquierda de la imagen de entrada')
plt.show()


# Aplicar la transformación de perspectiva a la imagen de entrada
h, w = img_original.shape[:2]
img_salida = cv2.warpPerspective(img_entrada, M, (w, h))

# Guardar la imagen de salida
cv2.imwrite('salida.jpg', img_salida)

