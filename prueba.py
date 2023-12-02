import cv2
import numpy as np
import matplotlib.pyplot as plt

# Cargar la imagen original y la imagen de entrada
img_original = cv2.imread('Pattern/piano.png')
img_entrada = cv2.imread('Calib_Images/image0.jpg')

# quedarnos con los pizeles que esten en el rango de blancos y negros de imagen de entrada:
