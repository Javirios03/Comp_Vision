import cv2 as cv
import cv2.aruco as aruco
import matplotlib.pyplot as plt
import os
import pygame
import time
import threading

pygame.init()
# Inicializar el módulo mixer
pygame.mixer.init()


dictionary = aruco.getPredefinedDictionary(cv.aruco.DICT_4X4_50)
parameters =  aruco.DetectorParameters()
detector = aruco.ArucoDetector(dictionary, parameters)

PIANO_NOTES = ["C5","D5","E5","F5","G5","A5","B5","C6"]

def create_marker(id, size):
    for i in range(0, 13):
        marker = cv.aruco
        marker = aruco.generateImageMarker(dictionary, i, 12)
        cv.imwrite("data/markers/marker_" + str(i) + ".png", marker)


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
    sound = pygame.mixer.Sound("data/notes/" + note + ".mp3")
    # reproducir el archivo de audio
    sound.play()
    # esperar a que termine de reproducirse
    time.sleep(1)
    # detener la reproducción
    sound.stop()

def piano(frame):
    ids = read_markers(frame)
    piano_notes_played = PIANO_NOTES.copy()

    # si no hay un id, que suene la nota asociada al id
    for i in ids:
        piano_notes_played.remove(PIANO_NOTES[i[0]])

    # crear un thread por cada nota que se va a reproducir
    for note in piano_notes_played:
        threading.Thread(target=play_song, args=(note,)).start()




        

    

if __name__ == "__main__":
    # create_marker(1, 12)
    # read_markers()
    frame = cv.imread("data/WIN_20231201_17_34_08_Pro.jpg")
    piano(frame)
