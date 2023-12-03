from detect_shapes import *
import cv2

def pattern_rec():
    for i in range(1, 5):
        img = cv2.imread("Patterns/pattern{}.jpg".format(i))
        main(img)

def blob_rec():
    from math import sqrt
    from skimage import data
    from skimage.feature import blob_dog, blob_log, blob_doh
    from skimage.color import rgb2gray

    import matplotlib.pyplot as plt

    image = cv2.imread('Patterns/Kindle.jpg')
    #image = data.hubble_deep_field()[0:500, 0:500]
    image_gray = rgb2gray(image)

    blobs_dog = blob_dog(image_gray, threshold=0.1)
    blobs_dog[:, 2] = blobs_dog[:, 2] * sqrt(2)


    # Implementa aquí tu código para visualizar los blobs calculados usando LoG y DoG
    fig, ax = plt.subplots(1, 3, figsize=(12, 6))
    ax[0].imshow(image, cmap='gray')
    ax[0].set_title('Original image')

    for blob in blobs_dog:
        y, x, r = blob
        c = plt.Circle((x, y), r, color='red', linewidth=2, fill=False)
        ax[2].add_patch(c)
    ax[2].imshow(image, cmap='gray')
    ax[2].set_title('Blobs using DoG')

    plt.show()


def pattern_rec1():
    img = cv2.imread("Patterns/Kindle.jpg")
    main(img)

if __name__ == '__main__':
    # pattern_rec()
    # blob_rec()
    pattern_rec1()
