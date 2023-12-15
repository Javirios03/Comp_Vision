import cv2
import numpy as np


def get_corners_list(img):
    # Convert to gray scale
    gray = np.float32(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
    # gaussian blur
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    # Detect corners. The parameters used are the same as in the previous part
    corners = cv2.cornerHarris(gray, 2, 3, 0.04)
    # Dilate to mark the corners (used from the OpenCV documentation) (not important)
    corners = cv2.dilate(corners, None)
    # We wont use the same threshold
    threshold = 0.05
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

    edges = cv2.dilate(edges, None, iterations=4)

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


def points_in_contours(points, contour):
    # points: list of points
    # contour: x,y,w,h
    # returns: list of points that are inside the contours
    points_in = []
    x, y, w, h = cv2.boundingRect(contour)
    extra = 10
    for point in points:
        if x-extra <= point[1] <= x+w+extra and y-extra <= point[0] <= y+h+extra:
            points_in.append(point)
    return points_in


def main(img):
    points = get_corners_list(img)
    contours = get_contours(img)

    shapes_names = []
    contours_to_show = []

    for contour in contours:
        points_in = points_in_contours(points, contour)
        if len(points_in) == 3:
            contours_to_show.append(contour)
            shapes_names.append('triangle')
        elif len(points_in) == 4:
            contours_to_show.append(contour)
            shapes_names.append('square')
        elif len(points_in) == 5:
            contours_to_show.append(contour)
            shapes_names.append('pentagon')
        elif len(points_in) > 5:
            contours_to_show.append(contour)
            shapes_names.append('star')
        else:
            pass
        # print(len(points_in))

    return shapes_names, contours_to_show

    # show contours and shapes names
    # for i, contour in enumerate(contours_to_show):
    #     x, y, w, h = cv2.boundingRect(contour)
    #     cv2.putText(img, shapes_names[i], (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
    #     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
    # plt.imshow(img)
    # # show points
    # plt.scatter([p[1] for p in points], [p[0] for p in points], c='r')
    # plt.show()
