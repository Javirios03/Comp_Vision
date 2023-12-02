import cv2
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.colors import hsv_to_rgb
import numpy as np
import cv2 
import numpy as np


def convolution(image, kernel):
    # Volteamos el kernel
    kernel = np.flipud(np.fliplr(kernel))

    # añadimos padding
    pad = int((kernel.shape[0] - 1) / 2)
    shape = (image.shape[0] + 2 * pad, image.shape[1] + 2 * pad, image.shape[2])
    image_padded = np.zeros(shape)
    image_padded[pad:-pad, pad:-pad, :] = image

    # aplicamos la convolucion
    conv = np.zeros(image.shape)
    for x in range(image.shape[1]):
        for y in range(image.shape[0]):
            for z in range(image.shape[2]):
                conv[y, x, z] = (kernel * image_padded[y: y + kernel.shape[0], x: x + kernel.shape[1], z]).sum()

    return conv

def normalize(image):
    image_norm = image / image.max()
    image_norm[image_norm < 0] = 0
    return image_norm

def togray(image, image_format):
    if image_format == 'RGB':
        img = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)
        img = img[:, :, 2]
    elif image_format == 'HSV':
        img = image[:, :, 2]
    elif image_format == 'HLS':
        img = cv2.cvtColor(image, cv2.COLOR_HLS2HSV)
        img = img[:, :, 2]
    elif image_format == 'BGR':
        img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        img = img[:, :, 2]
    else:
        img = image
    img = np.expand_dims(img, axis=2) 
    return img  

def sobel_edge_detection(image, filter):
    # eje x
    gradient_x = convolution(image, filter)
    gradient_x = normalize(gradient_x)

    # volteamos el filtro
    gradient_x2 = convolution(image, np.fliplr(filter))
    gradient_x2 = normalize(gradient_x2)

    gradient_x = gradient_x + gradient_x2
    gradient_x[gradient_x > 255] = 25

    # eje y
    gradient_y = convolution(image, filter.T)
    gradient_y = normalize(gradient_y)

    # volteamos el filtro
    gradient_y2 = convolution(image, np.flipud(filter.T))
    gradient_y2 = normalize(gradient_y2)

    gradient_y = gradient_y + gradient_y2
    gradient_y[gradient_y > 255] = 255

    # sumamos los gradientes
    gradient_magnitude = gradient_x + gradient_y
    gradient_magnitude[gradient_magnitude > 255] = 255

    return gradient_x , gradient_y, gradient_magnitude

def gaussianBlur(img, sigma, filter_shape):
    
    # creamos el filtro
    gaussian_filter = np.zeros(filter_shape)
    for x in range(filter_shape[0]):
        for y in range(filter_shape[1]):
            gaussian_filter[x, y] = np.exp(-((x - int(filter_shape[0] / 2)) ** 2 + (y - int(filter_shape[1] / 2)) ** 2) / (2 * sigma ** 2))
    gaussian_filter = gaussian_filter / gaussian_filter.sum()

    # aplicamos el filtro
    filtered = convolution(img, gaussian_filter)
    filtered = normalize(filtered)

    return gaussian_filter, filtered

def sobelEdgeDetection(image, sigma, image_format, filter_shape):
    img = togray(image, image_format)
    
    # filtro gaussiano
    filter, filtered = gaussianBlur(img, sigma, filter_shape)

    # filtro sobel
    filter_sobel = np.array([[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]])
    # filtro que reconozca doble bordes
    filter_sobel = np.array([[-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2], [-4, -2, 0, 2, 4], [-2, -1, 0, 1, 2], [-2, -1, 0, 1, 2]])
    Ix, Iy, gradient_magnitude = sobel_edge_detection(filtered, filter_sobel)


    G = np.hypot(Ix, Iy) #Ix e Iy: convolución de los filtros por las filas y columnas (derivadas parciales respecto a X e Y)
    G = G / G.max() * 255
    theta = np.arctan2(Iy, Ix)

    return np.squeeze(G), np.squeeze(theta)



img = cv2.imread('paperpiano/data/shapes.png')
sigma = 1
filter_shape = (31,31)
image_format = 'RGB'
G, theta = sobelEdgeDetection(img, sigma, image_format, filter_shape)
print(G.shape)

plt.figure(figsize=(15, 15))
plt.subplot(1, 2, 1)
plt.imshow(G, cmap='gray')
plt.title('Gradiente')
plt.subplot(1, 2, 2)
plt.imshow(theta, cmap='gray')
plt.title('Dirección del gradiente');

plt.show()