import tracker_shapes as ds
import cv2
from picamera2 import Picamera2

def stream_video():
    picam = Picamera2()
    # picam.framerate = 30
    picam.preview_configuration.main.size = (500, 300)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.align()
    picam.set_controls({"FrameRate": 15})
    picam.configure("preview")
    picam.start()

    print("Press 'a' to start")
    while True:  # Don't start until the user presses 'a'
        frame = picam.capture_array()
        cv2.imshow("picam", frame)
        if cv2.waitKey(1) & 0xFF == ord("a"):
            break

    while True:
        frame = picam.capture_array()

        # Alter the frame so that the shape's contours are visible
        names, contours = ds.main(frame)
        for i, contour in enumerate(contours):
            cv2.drawContours(frame, [contour], 0, (0, 255, 0), 2)

        cv2.imshow("picam", frame)

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    picam.stop()


def main():
    stream_video()
