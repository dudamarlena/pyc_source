# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pylocator/resources.py
# Compiled at: 2012-04-18 08:21:33
import os.path
main_window = os.path.join(os.path.split(__file__)[0], 'resources/mainWindow.glade')
edit_label_dialog = os.path.join(os.path.split(__file__)[0], 'resources/editLabel.glade')
edit_coordinates_dialog = os.path.join(os.path.split(__file__)[0], 'resources/editCoordinates.glade')
edit_settings_dialog = os.path.join(os.path.split(__file__)[0], 'resources/editSettings.glade')
about_dialog = os.path.join(os.path.split(__file__)[0], 'resources/about.glade')
camera_fn = os.path.join(os.path.split(__file__)[0], 'resources/camera48.png')
camera_small_fn = os.path.join(os.path.split(__file__)[0], 'resources/camera24.png')
if __name__ == '__main__':
    import gtk
    builder = gtk.Builder()
    builder.add_from_file(main_window)
    win = builder.get_object('pylocatorMainWindow')
    win.show_all()
    gtk.main()