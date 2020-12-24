# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/utils/microphone_setup.py
# Compiled at: 2017-10-25 10:07:24
""" Downloader for Snips assistants. """
import os, shutil
from .os_helpers import cmd_exists, is_raspi_os, execute_command, pipe_commands
from .. import ASOUNDRC_DEST_PATH

class MicrophoneSetup:
    """ Downloader for Snips assistants. """
    ASOUNDRC_CONFIG_PATH = '../config/asoundrc'

    @staticmethod
    def setup_asoundrc(microphone_id):
        if not is_raspi_os():
            return
        if microphone_id == 'respeaker':
            MicrophoneSetup._copy_asoundrc('asoundrc.respeaker')
        elif microphone_id == 'jabra':
            MicrophoneSetup._copy_asoundrc('asoundrc.jabra')
        else:
            MicrophoneSetup._copy_asoundrc('asoundrc.default')

    @staticmethod
    def _copy_asoundrc(asoundrc_file):
        """ Copy asoundrc configuration to local path.

        :param asoundrc_file: the name of the asoundrc configuration, as
                              present in the config folder.
        """
        this_dir, this_filename = os.path.split(__file__)
        asoundrc_path = os.path.join(this_dir, MicrophoneSetup.ASOUNDRC_CONFIG_PATH, asoundrc_file)
        destination = os.path.expanduser(ASOUNDRC_DEST_PATH)
        shutil.copy2(asoundrc_path, destination)


class RespeakerMicrophoneSetup:

    @staticmethod
    def setup(vendor_id, product_id):
        if not is_raspi_os():
            return
        execute_command('sudo rm -f /lib/udev/rules.d/50-rspk.rules')
        echo_command = ('echo ACTION=="add", SUBSYSTEMS=="usb", ATTRS{{idVendor}}=="{}", ' + 'ATTRS{{idProduct}}=="{}", MODE="660", GROUP="plugdev"').format(vendor_id, product_id)
        tee_command = 'sudo tee --append /lib/udev/rules.d/50-rspk.rules'
        pipe_commands(echo_command, tee_command, silent=True)
        execute_command('sudo adduser pi plugdev')
        execute_command('sudo udevadm control --reload')
        execute_command('sudo udevadm trigger')