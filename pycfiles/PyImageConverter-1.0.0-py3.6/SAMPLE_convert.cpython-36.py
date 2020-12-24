# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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