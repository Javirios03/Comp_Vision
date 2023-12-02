import cv2
import numpy as np

class Piano_Keyboard:
    __white_map = {
        0:0,
        1:2,
        2:4,
        3:5,
        4:7,
        5:9,
        6:11,
        7:12,
        8:14,
        9:16,
        10:17,
        11:19,
        12:21,
        13:23,
        14:24,
    }

    __black_map = {
        0:1,
        1:3,
        2:6,
        3:8,
        4:10,
        5:13,
        6:15,
        7:18,
        8:20,
        9:22,
    }

    __white_keys = [
        "C",
        "D",
        "E",
        "F",
        "G",
        "A",
        "B",
        "C",
        "D",
        "E",
        "F",
        "G",
        "A",
        "B",
        "C",
    ]

    __black_keys = [
        "C#",
        "D#",
        "F#",
        "G#",
        "A#",
        "C#",
        "D#",
        "F#",
        "G#",
        "A#",
    ]

    def __init__(self):
        self.images = []
        self.calibration_params = None
        self.white_keys = []
        self.black_keys = []

        self.__get_images()
        self.__calibrate_camera(self.images)
        self.__find_keys()
        self.__sort_keys()
        self.__assign_keys()

    def __find_keys(self):
        '''Find the keys in the image'''
        # Convert the image to grayscale
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Find corners or keypoints
        ret, corners = cv2.findChessboardCorners(gray, (15, 3), None)

        if ret:
            # If corners are found, store object points and image points
            self.white_keys = corners[0:15]
            self.black_keys = corners[15:25]
    
    def __sort_keys(self):
        self.white_keys = sorted(self.white_keys, key=lambda x: x[0][0])
        self.black_keys = sorted(self.black_keys, key=lambda x: x[0][0])
    
    def __assign_keys(self):
        for i in range(len(self.white_keys)):
            self.white_keys[i] = (self.__white_keys[i], self.white_keys[i])
        
        for i in range(len(self.black_keys)):
            self.black_keys[i] = (self.__black_keys[i], self.black_keys[i])
    
    def __get_key(self, key):
        if key in self.__white_map:
            return self.white_keys[self.__white_map[key]]
        else:
            return self.black_keys[self.__black_map[key]]
        
    def __get_images(self):
        '''Get images from the camera'''
        path = "Calib_Images/"
        for i in range(16):
            image = cv2.imread(path + f"image{i}" + ".jpg")
            self.images.append(image)
            self.images.append(cv2.imread("Pattern/piano.png"))
        
    def __calibrate_camera(self, images):
        '''Given a list of images of the piano (pattern to use), calibrate the camera'''
        # Define the chessboard size or custom pattern size
        pattern_size = (15, 3)

        # Arrays to store object points and image points from all images
        object_points = []
        image_points = []

        # Define the 3D coordinates of the pattern
        objp = np.zeros((np.prod(pattern_size), 3), dtype=np.float32)
        objp[:, :2] = np.mgrid[0:pattern_size[0], 0:pattern_size[1]].T.reshape(-1, 2)

        for image in images:
            # Convert the image to grayscale
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            # Find corners or keypoints
            ret, corners = cv2.findChessboardCorners(gray, pattern_size, None)

            if ret:
                # If corners are found, store object points and image points
                object_points.append(objp)
                image_points.append(corners)
        
        # Perform camera calibration
        ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(object_points, image_points, gray.shape[::-1], None, None)

        # Save the calibration parameters (mtx, dist) for later use
        self.calibration_params = (mtx, dist)


# Try the class
piano = Piano_Keyboard()
print(piano.calibration_params)
