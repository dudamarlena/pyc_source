# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/cap1/Documents/GitHub/gesture-recognizer/gesture_recognizer/FistRecognizer.py
# Compiled at: 2018-11-18 05:22:30
# Size of source mod 2**32: 2774 bytes
import cv2, os, time

class FistRecognizer(object):

    def __init__(self, interval=0.03333333333333333, print_pos=True):
        """
                Threading
                The recognize_fist method will be started and it will run in the background
                until the application exits.
                :type interval: int
                :param interval: Check interval, in seconds
                """
        self.interval = interval
        dir_path = os.path.dirname(os.path.realpath(__file__))
        print(dir_path)
        filename_fist = 'haarcascade_fist.xml'
        full_path_fist = '%s/%s' % (dir_path, filename_fist)
        self.fist_cascade = cv2.CascadeClassifier(full_path_fist)
        filename_palm = 'haarcascade_palm.xml'
        full_path_palm = '%s/%s' % (dir_path, filename_palm)
        self.palm_cascade = cv2.CascadeClassifier(full_path_palm)
        self.prev_pos = None
        self.x_dir = 0
        self.y_dir = 0
        self.print_pos = print_pos

    def recognize_gesture(self, hand_pos=None):
        if self.prev_pos is None:
            self.prev_pos = hand_pos
        prev_pos = self.prev_pos
        x_dif = prev_pos[0] - hand_pos[0]
        y_dif = prev_pos[1] - hand_pos[1]
        if abs(x_dif) < 30:
            if abs(y_dif) < 30:
                self.prev_pos = hand_pos
                return
        while abs(x_dif) > 1.0 or abs(y_dif) > 1.0:
            x_dif /= 2.0
            y_dif /= 2.0

        self.x_dir = x_dif
        self.y_dir = y_dif
        self.prev_pos = hand_pos

    def recognize_fist(self):
        """
                Method that runs forever
                """
        cap = cv2.VideoCapture(0)
        while True:
            if self.print_pos:
                if self.x_dir > 0:
                    print('moving right')
                else:
                    print('moving left')
                if self.y_dir > 0:
                    print('moving up')
                else:
                    print('moving down')
                print('x:', self.x_dir)
                print('y:', self.y_dir)
            ret, img = cap.read()
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            hands = self.fist_cascade.detectMultiScale(gray)
            biggest_fist = [(0, 0, 0, 0)]
            for x, y, w, h in hands:
                if w > biggest_fist[0][3]:
                    biggest_fist[0] = (
                     x, y, w, h)

            self.recognize_gesture(biggest_fist[0])
            for x, y, w, h in biggest_fist:
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 0), 2)

            k = cv2.waitKey(30) & 255
            if k == 27:
                break
            time.sleep(self.interval)

        cap.release()
        cv2.destroyAllWindows()