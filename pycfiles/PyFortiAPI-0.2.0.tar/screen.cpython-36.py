# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: C:\Users\Joseph\PycharmProjects\pyformulas\_formulas\screen.py
# Compiled at: 2018-05-22 12:42:44
# Size of source mod 2**32: 865 bytes
import numpy as np, cv2

class screen:

    def __init__(self, canvas=None, title='Display'):
        self.title = title
        if canvas is None:
            self.canvas = np.zeros((480, 640), dtype=(np.uint8))
        else:
            self.canvas = canvas
        cv2.imshow(self.title, self.canvas)
        self._closed = False

    def update(self, canvas=None):
        if cv2.getWindowProperty(self.title, 0) < 0:
            return self.close()
        if canvas is not None:
            self.canvas = canvas
        cv2.imshow(self.title, self.canvas)
        cv2.waitKey(1)

    def exists(self):
        return not self._closed

    def close(self):
        try:
            cv2.destroyWindow(self.title)
        except:
            pass

        self._closed = True