# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/filipebatista/PycharmProjects/adbXtended/ezadb/gui/PreviewImageDialog.py
# Compiled at: 2018-01-20 05:28:45
from PIL import Image, ImageTk
from ezadb.utils.Utils import Utils
try:
    import tkinter as Tk
except:
    import Tkinter as Tk

class PreviewImageDialog:

    def __init__(self, parent, file_path, translator=None):
        self.translator = translator
        top = self.top = Tk.Toplevel(parent)
        screen_width = top.winfo_screenwidth()
        screen_height = top.winfo_screenheight()
        top.attributes('-topmost', 2)
        top.title(_('ScreenShot Capture'))
        top.wm_resizable(False, False)
        Utils.set_app_icon(self.top)
        image_pil = Image.open(file_path)
        zoom_sizes = PreviewImageDialog.calculate_aspect_ratio(image_pil.width, image_pil.height, screen_width, screen_height)
        image_pil = image_pil.resize((zoom_sizes['width'], zoom_sizes['height']), Image.ANTIALIAS)
        self.image = ImageTk.PhotoImage(image_pil)
        self.label = Tk.Label(top, image=self.image).pack()
        self.top.grab_set()

    @staticmethod
    def calculate_aspect_ratio(src_width, src_height, max_width, max_height):
        ratio = min(float(max_width) / src_width, float(max_height) / src_height)
        return {'width': int(src_width * ratio), 'height': int(src_height * ratio)}