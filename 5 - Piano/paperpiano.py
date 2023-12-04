import cv2 as cv
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import pygame
import time
import threading
# from picamera2 import PiCamera2 as PiCamera

pygame.init()
# Inicializar el módulo mixer
pygame.mixer.init()




dictionary = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters =  aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

PIANO_NOTES = ["C5","D5","E5","F5","G5","A5","B5","C6"]
PATH = "5 - Piano/data"

PIANO_TILES = "piano_tiles.png"
# iniciar pantalla
screen = pygame.display.set_mode((1224/2, 768/2))
# cargar imagen
image = pygame.image.load(PATH + "/" + PIANO_TILES)
# escalar imagen
image = pygame.transform.scale(image, (1224/2, 768/2))
# mostrar imagen en pantalla
screen.blit(image, (0, 0))
# actualizar pantalla
pygame.display.flip()


def create_marker(id, size):
    for i in range(0, 13):
        marker = cv.aruco
        marker = aruco.generateImageMarker(dictionary, i, 12)
        cv.imwrite(PATH + "/markers/marker_" + str(i) + ".png", marker)


def read_markers(frame,show_frame=False):
    markerCorners, markerIds, rejectedCandidates = detector.detectMarkers(frame)
    # print(markerIds)

    if show_frame:
        frame = aruco.drawDetectedMarkers(frame, markerCorners, markerIds)
        plt.figure()
        plt.imshow(frame)
        plt.show()

    return markerIds

def play_song(note):
    # cargar el archivo de audio
    sound = pygame.mixer.Sound(PATH + "/notes/" + note + ".mp3")
    # reproducir el archivo de audio
    sound.play()
    # esperar a que termine de reproducirse
    time.sleep(1)
    # detener la reproducción
    sound.stop()

def piano(frame, playing, sound=False, show_piano=True):
    ids = read_markers(frame)
    piano_notes_played = PIANO_NOTES.copy()

    # si no hay un id, que suene la nota asociada al id
    if ids is not None:
        for i in ids:
            piano_notes_played.remove(PIANO_NOTES[i[0]])
    else:
        piano_notes_played = []

    if show_piano:
        # mostramos piano_tiles.png y encima las teclas que se están tocando (playing/{note}.png)})
        image = pygame.image.load(PATH + "/" + PIANO_TILES)
        image = pygame.transform.scale(image, (1224/2, 768/2))
        screen.blit(image, (0, 0))
        for note in piano_notes_played:
            image = pygame.image.load(PATH + "/playing/" + note + ".png")
            image = pygame.transform.scale(image, (1224/2, 768/2))
            screen.blit(image, (0, 0))
        pygame.display.flip()

        

    # crear un thread por cada nota que se va a reproducir
    if sound:
        if piano_notes_played:
            for note in piano_notes_played:
                if note not in playing:
                    threading.Thread(target=play_song, args=(note,)).start()

    return piano_notes_played    
 

def stream_video_rpi():
    camera = PiCamera()
    camera.preview_configuration.main.size = (640, 480)
    camera.preview_configuration.main.format = "RGB888"
    camera.preview_configuration.align()
    camera.video_configuration.controls.FrameRate = 10.0

    camera.configure("preview")
    camera.start()

    playing = []
    # Capture frames from the camera
    while True:
        # Grab a single frame of video
        frame = camera.capture_array()
        #frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Display the resulting frame
        playing = piano(frame, playing)
        cv.imshow('Video', frame)
        # Wait for Enter key to stop
        if cv.waitKey(1) == 13:
            break

    # When everything done, release the capture
    cv.destroyAllWindows()


def stream_video():
    cap = cv.VideoCapture(0)
    playing = []
    while True:
        ret, frame = cap.read()
        playing = piano(frame, playing, sound=True, show_piano=True)
        cv.imshow('frame', frame)
        
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()


if __name__ == "__main__":
    # create_marker(1, 12)
    # read_markers()
    # acceder a la camara y pasar la imagen frame a frame a main
    # stream_video()
    stream_video_rpi()