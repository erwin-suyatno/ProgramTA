import numpy as np
import cv2


class Pupil(object):
    """
    Kelas ini mendeteksi iris mata dan memperkirakan
     posisi pupil
    """

    def __init__(self, eye_frame, threshold):
        self.iris_frame = None
        self.threshold = threshold
        self.x = None
        self.y = None

        self.detect_iris(eye_frame)

    @staticmethod
    def image_processing(eye_frame, threshold):
        """Melakukan operasi pada bingkai mata untuk mengisolasi iris

        Arguments:
            eye_frame (numpy.ndarray): Bingkai berisi mata dan tidak ada yang lain
            threshold (int): Nilai ambang yang digunakan untuk binerisasi bingkai mata

        Returns:
            Bingkai dengan satu elemen yang mewakili iris
        """
        kernel = np.ones((3, 3), np.uint8)
        new_frame = cv2.bilateralFilter(eye_frame, 10, 15, 15)
        new_frame = cv2.erode(new_frame, kernel, iterations=3)
        new_frame = cv2.threshold(new_frame, threshold, 255, cv2.THRESH_BINARY)[1]

        return new_frame

    def detect_iris(self, eye_frame):
        """Mendeteksi iris dan memperkirakan posisi pupil dengan
         menghitung titik pusat.

        Arguments:
            eye_frame (numpy.ndarray): Bingkai berisi mata dan tidak ada yang lain
        """
        self.iris_frame = self.image_processing(eye_frame, self.threshold)

        contours, _ = cv2.findContours(self.iris_frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)[-2:]
        contours = sorted(contours, key=cv2.contourArea)

        try:
            moments = cv2.moments(contours[-2])
            self.x = int(moments['m10'] / moments['m00'])
            self.y = int(moments['m01'] / moments['m00'])
        except (IndexError, ZeroDivisionError):
            pass
