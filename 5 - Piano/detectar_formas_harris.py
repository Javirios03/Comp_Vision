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

if __name__ == '__main__':
    # Read image
    img = cv2.imread('paperpiano\data\shapes.png')
    points = get_corners_list(img)
    print(len(points))
    # Show the result
    plt.imshow(img, cmap='gray')
    # show the coorners_coords
    # error: plt.scatter(points[:,1],points[:,0],c='r') # list indices must be integers or slices, not tuple
    plt.scatter([p[1] for p in points],[p[0] for p in points],c='r')
    plt.show()