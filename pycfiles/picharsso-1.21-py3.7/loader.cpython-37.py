# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/picharsso/loader.py
# Compiled at: 2019-11-08 16:27:15
# Size of source mod 2**32: 927 bytes
from cv2 import imread, COLOR_BGR2RGB, COLOR_BGR2GRAY, cvtColor
from os.path import exists, isfile

class Loader:
    __doc__ = 'A wrapper for loading images\n    '

    def load_image(self):
        """Loads source image
        
        Raises
        ------
        FileNotFoundError
            when the file does not exist
        ValueError
            when the loaded file is not an image
        """
        try:
            filename = self.args.image
            if not (exists(filename) and isfile(filename)):
                raise FileNotFoundError(f"File {filename} does not exist")
            self.image = imread(filename)
            if self.image is None:
                raise ValueError(f"File {filename} is not an image!")
            self.image = cvtColor(self.image, COLOR_BGR2RGB if self.args.color else COLOR_BGR2GRAY)
        except Exception as e:
            try:
                print(e)
                exit()
            finally:
                e = None
                del e