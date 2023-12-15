# paper-piano
# Project Description
Welcome to paper-piano! We are Pepe Ridruejo and Fco. Javier Ríos, students of the 3º year of IMAT (*Ingeniería Matemática e Inteligencia Artificial*) in ICAI.
This is our final project for the subject of Computer Vision. It has 2 main parts: One devoted towards detecting patterns (specifically, shapes), using them to decode a system and tracking the shapes. The other one, which we loved making, is an implementation of a virtual piano on keyboard
In order to know how to try the project, please refer to the Report PDF included in the Repository's doc folder. We really hope you like it!

## Calibration
Calibration is an essential step in our project. We use a cheesboard pattern to calibrate the camera. This process allows us to correct any distortion caused by the camera lens and obtain an accurate representation of the scene. The resulting values of the calibration, including the RMS, are displayed when running calibration.py. The distortion obtained is not significant enough to be taken into account.

## Pattern Detection
Our system is capable of differentiating simple patterns through image processing. It is specifically programmed to recognize triangles, squares, pentagons, and stars. The algorithms used to recognize shapes are: findContours and Harris to count corners found in each contour.

## Sequence Decoder
We have implemented a decoder that memorizes up to 4 consecutive patterns. If the patterns are in the correct order, the system allows the passage to the next block, the paperpiano.

## Tracker
Once the correct pattern sequence is introduced, the tracker is executed. This component displays a bounding box around the geometric shapes and follows them as they move.

# Metodology
The first thing that should be done is downloading the src folder, where the codes are included (as well as the documents the modules need). In such folder, 5 folders and a python file (main). The folders have the different modules necessary for each part of the system (Calibration, Pattern detection, Sequence decoder, Tracker and the Paper piano).
The system is structured as a State Machine with 3 states: Blocked, Tracking and Paper Piano, the transitions of which are shown in the diagram. To run the project, then, just run the main.py file, which will create an interactive menu in the command prompt	

