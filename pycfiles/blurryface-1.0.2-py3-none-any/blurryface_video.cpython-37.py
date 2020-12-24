# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\jmd0421\dev\blurryface\blurryface\blurryface_video.py
# Compiled at: 2019-10-17 15:11:12
# Size of source mod 2**32: 6594 bytes
import os
from time import time, sleep
import sys, cv2, argparse
from threading import Event
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QPixmap, QImage, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QPushButton, QVBoxLayout, QHBoxLayout

def variance_of_laplacian(image):
    return cv2.Laplacian(image, cv2.CV_64F).var()


def get_blurriness(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    fm = variance_of_laplacian(gray)
    return fm


class App(QMainWindow):

    def __init__(self, camera, threshold):
        super().__init__()
        self.camera = camera
        self.threshold = threshold
        os.makedirs('blurryface-out/blurry', exist_ok=True)
        os.makedirs('blurryface-out/not-blurry', exist_ok=True)
        self.title = 'Blurryface'
        self._save_as_blurry = Event()
        self._save_as_not_blurry = Event()
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        image_view = QLabel(self)
        image_view.setText('')
        self._blur_label = QLabel(self)
        newfont = QFont('Times', 16, QFont.Bold)
        self._blur_label.setFont(newfont)
        self._btn_save_blurry = QPushButton('Save image as blurry')
        self._btn_save_blurry.clicked.connect(self._set_save_as_blurry)
        self._btn_save_not_blurry = QPushButton('Save image as not blurry')
        self._btn_save_not_blurry.clicked.connect(self._set_save_as_not_blurry)
        self.central_widget = QWidget()
        self.layout = QVBoxLayout(self.central_widget)
        hbox = QHBoxLayout()
        hbox.addStretch(1)
        hbox.addWidget(self._blur_label)
        l2 = QLabel(self)
        l2.setText(f"Threshold: {self.threshold}".rjust(50))
        hbox.addWidget(l2)
        self.layout.addLayout(hbox)
        self.layout.addWidget(image_view)
        self.layout.addWidget(self._btn_save_blurry)
        self.layout.addWidget(self._btn_save_not_blurry)
        self.setCentralWidget(self.central_widget)
        self.th = VideoThread(parent=self)
        self.th.changePixmap.connect(image_view.setPixmap)
        self.th.changeLabel.connect(self._update_blur_label)
        self.th.start()

    def _set_save_as_blurry(self):
        self._save_as_blurry.set()

    def _set_save_as_not_blurry(self):
        self._save_as_not_blurry.set()

    def _update_blur_label(self, text):
        self._blur_label.setText(text)
        text_lower = text.lower()
        if 'blurry' in text_lower:
            color = 'green' if 'not blurry' in text_lower else 'red'
        else:
            color = 'black'
        self._blur_label.setStyleSheet(f"color: {color}")
        self._blur_label.adjustSize()

    def closeEvent(self, event):
        self.th.stop()
        QWidget.closeEvent(self, event)


class VideoThread(QThread):
    changePixmap = pyqtSignal(QPixmap)
    changeLabel = pyqtSignal(str)

    def __init__(self, parent=None):
        QThread.__init__(self, parent=parent)
        self.is_running = True
        self._n = 150
        self._past_blurriness = []
        self._blurry = None
        self._last_check = 0
        self._save_as_blurry = parent._save_as_blurry
        self._save_as_not_blurry = parent._save_as_not_blurry
        self.threshold = parent.threshold
        self.camera = parent.camera

    def _check_past_blurry(self):
        return sum(self._past_blurriness) / len(self._past_blurriness)

    def _past_is_blurry(self):
        return self._check_past_blurry() < self.threshold

    def run(self):
        cap = cv2.VideoCapture(self.camera)
        self.changeLabel.emit('Loading....')
        while self.is_running:
            ret, frame = cap.read()
            current_blurriness = round(get_blurriness(frame), 1)
            self._past_blurriness.append(current_blurriness)
            self._past_blurriness = self._past_blurriness[-self._n:]
            rgbImage = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            if time() - self._last_check >= 0.5:
                recent_blurriness = round(self._check_past_blurry(), 1)
                blurry = self._past_is_blurry()
                if blurry:
                    self.changeLabel.emit(f"Blurry ({current_blurriness} / {recent_blurriness})")
                else:
                    self.changeLabel.emit(f"Not blurry ({current_blurriness} / {recent_blurriness})")
                self._blurry = blurry
                if self._save_as_blurry.is_set():
                    print('Saving as blurry!')
                    cv2.imwrite(f"blurryface-out/blurry/{time()}.jpg", frame)
                    self._save_as_blurry.clear()
                if self._save_as_not_blurry.is_set():
                    print('Saving as not blurry!')
                    cv2.imwrite(f"blurryface-out/not-blurry/{time()}.jpg", frame)
                    self._save_as_not_blurry.clear()
            convertToQtFormat = QImage(rgbImage.data, rgbImage.shape[1], rgbImage.shape[0], QImage.Format_RGB888)
            convertToQtFormat = QPixmap.fromImage(convertToQtFormat)
            p = convertToQtFormat.scaled(640, 480, Qt.KeepAspectRatio)
            self.changePixmap.emit(p)

    def stop(self):
        self.is_running = False
        self.quit()
        self.wait()


def main():
    parser = argparse.ArgumentParser(description='Blurryface')
    parser.add_argument('--camera', help='Camera number.', type=int, default=0)
    parser.add_argument('--threshold', help='Blurriness threshold.', type=int, default=100)
    args = parser.parse_args()
    app = QApplication(sys.argv)
    ex = App(args.camera, args.threshold)
    ex.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()