# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\PyImageConverter\SAMPLE_convert.py
# Compiled at: 2019-07-21 10:02:11
# Size of source mod 2**32: 335 bytes
import PyImageConverter, cv2
from tkinter import Tk
from tkinter.filedialog import askopenfilename
Tk().withdraw()
filename = askopenfilename()
frmt = input('Enter the format (bmp/jpg/png):')
converted_image = PyImageConverter.convert(filename, frmt)
cv2.imshow('Converted Image', converted_image)
cv2.destroyAllWindows()