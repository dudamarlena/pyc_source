# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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