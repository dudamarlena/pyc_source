# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/iw/fss/config.py
# Compiled at: 2008-10-23 05:55:17
"""
Global FileSystemStorage configuration data
$Id: config.py 69081 2008-07-28 13:39:24Z b_mathieu $
"""
__author__ = ''
__docformat__ = 'restructuredtext'
PROJECTNAME = 'iw.fss'
GLOBALS = globals()
I18N_DOMAIN = PROJECTNAME.lower()
PROPERTYSHEET = 'filesystemstorage_properties'
(ZCONFIG, dummy_handler, CONFIG_FILE) = (None, None, None)

def loadConfig():
    """Loads configuration from a ZConfig file"""
    global CONFIG_FILE
    global ZCONFIG
    global dummy_handler
    from customconfig import ZOPETESTCASE
    import os
    from Globals import INSTANCE_HOME
    from ZConfig.loader import ConfigLoader
    from iw.fss.configuration.schema import fssSchema
    INSTANCE_ETC = os.path.join(INSTANCE_HOME, 'etc')
    _this_directory = os.path.abspath(os.path.dirname(__file__))
    FSS_ETC = os.path.join(_this_directory, 'etc')

    def filePathOrNone(file_path):
        return os.path.isfile(file_path) and file_path or None

    CONFIG_FILENAME = 'plone-filesystemstorage.conf'
    INSTANCE_CONFIG = filePathOrNone(os.path.join(INSTANCE_ETC, CONFIG_FILENAME))
    FSS_CONFIG = filePathOrNone(os.path.join(FSS_ETC, CONFIG_FILENAME))
    FSS_CONFIG_IN = filePathOrNone(os.path.join(FSS_ETC, CONFIG_FILENAME + '.in'))
    CONFIG_FILE = [ fp for fp in (INSTANCE_CONFIG, FSS_CONFIG, FSS_CONFIG_IN) if fp is not None ][0]
    if ZOPETESTCASE:
        (ZCONFIG, dummy_handler) = ConfigLoader(fssSchema).loadURL(FSS_CONFIG_IN)
    else:
        (ZCONFIG, dummy_handler) = ConfigLoader(fssSchema).loadURL(CONFIG_FILE)
    return


loadConfig()