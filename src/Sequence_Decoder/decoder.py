import decoder_shapes as ds
import cv2 
from picamera2 import Picamera2
from time import sleep


def stream_video():
    picam = Picamera2()
    # picam.framerate = 30
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.configure("preview")
    picam.start()

    # Initialise password
    password = ["triangle", "square", "pentagon", "star"]
    guess = []

    while True:
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        key = cv2.waitKey(1)
        # Take a picture
        if key & 0xFF == ord("a"):
            # We add the shape detected to the introduced password
            try:
                # Add the shape detected
                guess.append(ds.main(frame)[0])
            except IndexError:
                # The algorithm didn't recognise the shape
                print("No shapes found. Please, take another picture")
                continue
            if len(guess) == 4:
                if guess == password:
                    break
                else:
                    print("Password incorrect. Try again.")
                    guess = []

        elif key & 0xFF == ord("r"):   # Reset password
            guess = []
        print(guess)
        sleep(0.1)


def main():
    stream_video()
