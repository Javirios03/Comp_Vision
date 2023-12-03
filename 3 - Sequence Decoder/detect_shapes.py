import cv2
import numpy as np
from matplotlib import pyplot as plt


def get_corners_list(img):
    # Convert to gray scale
    gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    # gaussian blur
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # Detect corners. The parameters used are the same as in the previous part
    block_size = 5
    ksize = 5
    k = 0.04
    corners = cv2.cornerHarris(gray, 2, 3, 0.04)
    # Dilate to mark the corners (used from the OpenCV documentation) (not important)
    corners = cv2.dilate(corners, None)
    # We wont use the same threshold
    threshold = 0.01
    corners_coords = np.argwhere(corners > threshold * corners.max())
    points = []
    # quitamos los bordes muy cercanos a otros bordes
    min_dist = 20
    for point in corners_coords:
        if len(points) == 0:
            points.append(point)
        else:
            for p in points:
                if np.linalg.norm(point-p) < min_dist:
                    break
            else:
                points.append(point)
        
    return points

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

def point_in_contour(point, contour):
    # point: x,y
    # contour: x,y,w,h
    # returns: True if point is inside contour
    x, y, w, h = cv2.boundingRect(contour)
    extra = 10
    if x-extra <= point[1] <= x+w+extra and y-extra <= point[0] <= y+h+extra:
        return True
    else:
        return False
    
def points_in_contours(points, contour):
    # points: list of points
    # contour: x,y,w,h
    # returns: list of points that are inside the contours
    points_in = []
    for point in points:
        if point_in_contour(point, contour):
            points_in.append(point)
    return points_in
        

def main(img):
    points = get_corners_list(img)
    contours = get_contours(img)
    circles = get_circles(img)

    shapes_names = []
    contours_to_show = []

    for contour in contours:
        if circles is not None:
            x,y,r = circles[0][0]
            # si el centro está dentro del contorno
            if point_in_contour((x,y), contour):
                contours_to_show.append(contour)
                shapes_names.append('circle')
                break
        else:
            points_in = points_in_contours(points, contour)
            if len(points_in) == 0:
                contours_to_show.append(contour)
                shapes_names.append('circle')
            
            elif len(points_in) == 3:
                contours_to_show.append(contour)
                shapes_names.append('triangle')
            elif len(points_in) == 4:
                contours_to_show.append(contour)
                shapes_names.append('square')
            elif 7 < len(points_in)< 11:
                contours_to_show.append(contour)
                shapes_names.append('star')
            else:
                pass
            print(len(points_in))

    # show contours and shapes names
    for i, contour in enumerate(contours_to_show):
        x, y, w, h = cv2.boundingRect(contour)
        cv2.putText(img, shapes_names[i], (x,y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,0), 2)
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
    
    return img
    


if __name__ == '__main__':
    # acceder a la camara y pasar la imagen frame a frame a main
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        img = main(frame)
        cv2.imshow('frame', img)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

