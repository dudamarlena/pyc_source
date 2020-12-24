# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/plugins/overlay_translator/plugin_overlay_translator_max_pilot_size.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru
from troy.constants import *
import troy
_DEFAULT_PILOT_SIZE = UNLIMITED
PLUGIN_DESCRIPTION = {'type': 'overlay_translator', 
   'name': 'max_pilot_size', 
   'version': '0.1', 
   'description': 'this translator creates n pilots of maximal size.', 
   'configuration': [
                   ('pilot size', 'INT as size of each pilot, or troy.UNLIMITED" (default: UNLIMITED)')]}

class PLUGIN_CLASS(troy.PluginBase):
    """
    This class implements the default overlay translator algorithm for
    TROY, which splits the requested overlay size over N pilots of configured
    size n.

    **Configuration Options:**

    * `pilot_size`: size for each pilot.  If the overlay size is not a multiple
      of `pilot_size`, the total number of cores will be larger than overlay
      size.  The pilot backend is expected to honor the pilot size, and not to
      create smaller or larger pilots.
      Example:

          "pilot_size" : 32
    """
    __metaclass__ = ru.Singleton

    def __init__(self):
        troy.PluginBase.__init__(self, PLUGIN_DESCRIPTION)

    def translate(self, overlay):
        """
        check if the overlay's description has a size specified.  If so,
        translate that into the necessary number of pilots of the configured
        size.
        """
        if 'pilot_size' in self.cfg:
            pilot_size = int(self.cfg['pilot_size'])
        else:
            pilot_size = _DEFAULT_PILOT_SIZE
        if pilot_size == UNLIMITED:
            pilot_size = int(overlay.description.cores)
        troy._logger.info('overlay  translate: max pilot size set to %d' % pilot_size)
        pilot_cnt = 0
        while pilot_cnt * pilot_size < overlay.description.cores:
            pilot_descr = troy.PilotDescription({'size': pilot_size, 'walltime': overlay.description.walltime})
            pilot_id = overlay._add_pilot(pilot_descr)
            pilot_cnt += 1
            troy._logger.info('overlay  translate: define   pilot %3d: %s (%s)' % (1, pilot_id, pilot_descr))