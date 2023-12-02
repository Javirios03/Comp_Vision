import cv2 
from picamera2 import Picamera2

def stream_video():
    picam = Picamera2()
    # picam.framerate = 30
    picam.preview_configuration.main.size=(500,300)
    picam.preview_configuration.main.format="RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    while True:
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        # si se presiona la tecla a, saca una foto en carpeta data y con el nombre piano_n.jpg
        if cv2.waitKey(1) & 0xFF == ord("a"):
            n = 0
            cv2.imwrite("data/piano_{}.jpg".format(n), frame)
            n += 1
            


    cv2.destroyAllWindows()

if __name__ == "__main__":
    stream_video()