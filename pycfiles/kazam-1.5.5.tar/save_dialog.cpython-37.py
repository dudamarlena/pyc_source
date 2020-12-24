# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../kazam/frontend/save_dialog.py
# Compiled at: 2019-08-17 21:55:54
# Size of source mod 2**32: 2604 bytes
import os, logging
logger = logging.getLogger('Save Dialog')
from datetime import datetime
from gettext import gettext as _
from gi.repository import Gtk
from kazam.backend.prefs import *

def SaveDialog(title, old_path, codec, main_mode=MODE_SCREENCAST):
    logger.debug('Save dialog called with path: {0}'.format(old_path))
    dialog = Gtk.FileChooserDialog(title, None, Gtk.FileChooserAction.SAVE, (
     Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
     _('Save'), Gtk.ResponseType.OK))
    dt = datetime.today().strftime('%Y-%m-%d %H:%M:%S')
    if main_mode == MODE_SCREENCAST:
        dialog.set_current_name('{0} {1}{2}'.format(_('Screencast'), dt, CODEC_LIST[codec][3]))
    else:
        if main_mode == MODE_SCREENSHOT:
            dialog.set_current_name('{0} {1}.png'.format(_('Screenshot'), dt))
    dialog.set_do_overwrite_confirmation(True)
    if old_path and os.path.isdir(old_path):
        dialog.set_current_folder(old_path)
        logger.debug('Previous path is a valid destination')
    else:
        if main_mode in [MODE_SCREENCAST, MODE_WEBCAM, MODE_BROADCAST]:
            dialog.set_current_folder(prefs.video_dest)
            logger.debug('Previous path invalid, setting it to: {0}'.format(prefs.video_dest))
        else:
            if main_mode == MODE_SCREENSHOT:
                dialog.set_current_folder(prefs.picture_dest)
                logger.debug('Previous path invalid, setting it to: {0}'.format(prefs.picture_dest))
            dialog.show_all()
            result = dialog.run()
            old_path = dialog.get_current_folder()
            return (dialog, result, old_path)