# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/snipsskills/utils/speaker_setup.py
# Compiled at: 2017-10-25 10:07:24
import os, shutil
from .os_helpers import is_raspi_os, execute_command
from .. import ASOUNDRC_DEST_PATH, ASOUNDCONF_DEST_PATH

class SpeakerSetup:
    ASOUNDRC_CONFIG_PATH = '../config/asoundrc/'
    SOUND_DRIVER_PATH = '../config/drivers/'

    @staticmethod
    def setup_asoundrc(speaker_id):
        if not is_raspi_os():
            return
        if speaker_id == 'adafruit-bonnet':
            SpeakerSetup._copy_asoundrc('asoundrc.speakerbonnet')

    @staticmethod
    def setup_asoundconf(speaker_id):
        if not is_raspi_os():
            return
        if speaker_id == 'adafruit-bonnet':
            SpeakerSetup._copy_asoundconf('asound.conf.speakerbonnet')

    @staticmethod
    def setup_driver(speaker_id):
        if not is_raspi_os():
            return
        if speaker_id == 'adafruit-bonnet':
            SpeakerSetup._install_driver('adafruit_bonnet.sh')

    @staticmethod
    def _copy_asoundrc(asoundrc_file):
        """ Copy asoundrc configuration to local path.

        :param asoundrc_file: the name of the asoundrc configuration, as
                              present in the config folder.
        """
        this_dir, this_filename = os.path.split(__file__)
        asoundrc_path = os.path.join(this_dir, SpeakerSetup.ASOUNDRC_CONFIG_PATH, asoundrc_file)
        destination = os.path.expanduser(ASOUNDRC_DEST_PATH)
        shutil.copy2(asoundrc_path, destination)

    @staticmethod
    def _copy_asoundconf(asoundconf_file):
        """ Copy asoundconf to local path. """
        this_dir, this_filename = os.path.split(__file__)
        asoundrc_path = os.path.join(this_dir, SpeakerSetup.ASOUNDRC_CONFIG_PATH, asoundconf_file)
        destination = os.path.expanduser(ASOUNDCONF_DEST_PATH)
        shutil.copy2(asoundrc_path, destination)

    @staticmethod
    def _install_driver(driver_file):
        if not is_raspi_os():
            return
        this_dir, this_filename = os.path.split(__file__)
        driver_path = os.path.join(this_dir, SpeakerSetup.SOUND_DRIVER_PATH, driver_file)
        execute_command('sudo chmod a+x ' + driver_path)
        execute_command(driver_path + ' -y')