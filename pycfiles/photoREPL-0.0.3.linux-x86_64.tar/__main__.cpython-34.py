# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.4/site-packages/photorepl/__main__.py
# Compiled at: 2015-07-09 20:38:36
# Size of source mod 2**32: 2284 bytes
import atexit, photorepl, sys, threading
try:
    import pgi
    pgi.install_as_gi()
except ImportError:
    pass

from gi.repository import GLib
from photorepl.threads import UIThread
from .photo import Photo

def edit(filename, cache=True):
    """
    Opens the given filename and spawns a preview window.
    """
    global photos
    global ui_thread
    photo = Photo(filename=filename, ui_thread=ui_thread)
    if cache:
        photos.append(photo)
    return photo


if __name__ == '__main__':
    GLib.set_application_name(photorepl.app_name)
    import libraw, rawkit
    from rawkit.options import Options
    from rawkit.options import WhiteBalance
    from rawkit.raw import Raw
    ui_thread = UIThread()
    ui_thread.start()
    if len(sys.argv) > 1:
        photos = [edit(arg, cache=False) for arg in sys.argv[1:]]
    else:
        photos = []
    print("\n    Good morning (UGT)! Welcome to photoREPL, an experimental interface for raw\n    photo editing from the command line with `rawkit'.\n\n    The following packages, modules, and classes are imported for you (among\n    others):\n\n        libraw\n\n        photorepl\n        photorepl.photo.Photo\n\n        rawkit\n        rawkit.options.Options\n        rawkit.options.WhiteBalance\n        rawkit.raw.Raw\n\n    The following functions are also available:\n\n        edit(filename)\n\n    For help, use the `help()' function, eg. `help(Photo)'.\n    ")
    if len(sys.argv) == 1:
        print('\n    To get started, why not try opening a photo with:\n\n        myphoto = edit(filename=somephoto)\n        ')
    else:
        if len(sys.argv) == 2:
            print("The file `{}' is available as photos[0].".format(sys.argv[1]))
        elif len(sys.argv) > 2:
            print('The files {} are available in the photos[] array.'.format(sys.argv[1:]))

    @atexit.register
    def on_exit():
        for photo in photos:
            photo.close()

        print("\n        Goodbye. If photoREPL immediately exited, be sure you're running\n        photoREPL with `python -i -m photorepl' so that it can fall back to a\n        prompt.\n        ")