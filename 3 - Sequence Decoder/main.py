from detect_shapes import *
import cv2

if __name__ == '__main__':
    for i in range(1, 5):
        img = cv2.imread("Patterns/pattern{}.jpg".format(i))
        main(img)
