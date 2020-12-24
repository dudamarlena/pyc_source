# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/color_matcher/io_handler.py
# Compiled at: 2020-04-18 14:24:17
# Size of source mod 2**32: 4116 bytes
__author__ = 'Christopher Hahne'
__email__ = 'info@christopherhahne.de'
__license__ = '\n    Copyright (c) 2020 Christopher Hahne <info@christopherhahne.de>\n\n    This program is free software: you can redistribute it and/or modify\n    it under the terms of the GNU General Public License as published by\n    the Free Software Foundation, either version 3 of the License, or\n    (at your option) any later version.\n\n    This program is distributed in the hope that it will be useful,\n    but WITHOUT ANY WARRANTY; without even the implied warranty of\n    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the\n    GNU General Public License for more details.\n\n    You should have received a copy of the GNU General Public License\n    along with this program.  If not, see <http://www.gnu.org/licenses/>.\n\n'
import os, numpy as np
try:
    from PIL import Image
except ImportError:
    raise ImportError('Please install pillow.')
else:
    from color_matcher.normalizer import Normalizer
    FILE_EXTS = ('bmp', 'png', 'tiff', 'tif', 'jpeg', 'jpg')

    def save_img_file(img, file_path=None, file_type=None):
        file_path = os.getcwd() if file_path is None else file_path
        ext = os.path.splitext(file_path)[(-1)][1:]
        if not file_type:
            file_type = ext if (ext == 'png' or ext == 'tiff') else ('tiff' if img.dtype == 'uint16' else 'png')
        file_path = os.path.splitext(file_path)[(-2)] if file_path.endswith(FILE_EXTS) else file_path
        file_type = 'png' if file_type is None else file_type
        file_path += '.' + file_type
        img = Normalizer(img).uint16_norm() if file_type.__contains__('tif') else Normalizer(img).uint8_norm()
        try:
            import imageio
            suppress_user_warning(True, category=UserWarning)
            imageio.imwrite(uri=file_path, im=img)
            suppress_user_warning(False, category=UserWarning)
        except ImportError:
            if file_type == 'png' or file_type == 'bmp':
                try:
                    Image.fromarray(img).save(file_path, file_type, optimize=True)
                except PermissionError as e:
                    try:
                        raise Exception(e)
                    finally:
                        e = None
                        del e

        else:
            return True


    def load_img_file(file_path):
        file_type = file_path.split('.')[(-1)]
        if any((file_type.lower() in ext for ext in FILE_EXTS)):
            try:
                import imageio
                suppress_user_warning(True, category=UserWarning)
                img = imageio.imread(uri=file_path, format=file_type)
                suppress_user_warning(False, category=UserWarning)
            except ImportError:
                try:
                    img = Image.open(file_path)
                except OSError or :
                    from PIL import ImageFile
                    ImageFile.LOAD_TRUNCATED_IMAGES = True
                    img = Image.open(file_path)

        else:
            raise TypeError('Filetype %s not recognized' % file_type)
        img = Normalizer(np.asarray(img)).type_norm()
        return img


    def suppress_user_warning(switch=None, category=None):
        import warnings
        switch = switch if switch is None else True
        if switch:
            warnings.filterwarnings('ignore', category=category)
        else:
            warnings.filterwarnings('default', category=category)


    def select_file(init_dir=None, title=''):
        """ get filepath from tkinter dialog """
        init_dir = os.path.expanduser('~/') if not init_dir else init_dir
        try:
            import tkinter as tk
            from tkinter.filedialog import askopenfilename
        except ImportError:
            import Tkinter as tk
            from tkFileDialog import askopenfilename
        else:
            root = tk.Tk()
            root.withdraw()
            root.update()
            file_path = askopenfilename(initialdir=[init_dir], title=title)
            root.update()
            if file_path:
                return file_path