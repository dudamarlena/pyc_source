# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: d:\CODE\VScode\autowork\ymm-automation\ymmuim-library\YmmuimLibrary\__init__.py
# Compiled at: 2019-07-01 08:44:10
# Size of source mod 2**32: 975 bytes
__author__ = '8034.com'
__date__ = '2019-07-01'
from YmmuimLibrary.keywords import _YmmiumKeywords
from AppiumLibrary.version import VERSION
__version__ = VERSION

class YmmuimLibrary(_YmmiumKeywords):
    __doc__ = ''
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, run_on_failure='Capture Page Screenshot'):
        """YmmuimLibrary can be imported with optional arguments.

        Examples:
        | Library | AppiumLibrary | 10 | # Sets default timeout to 10 seconds                                                                             |
        | Library | AppiumLibrary | timeout=10 | run_on_failure=No Operation | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        for base in YmmuimLibrary.__bases__:
            base.__init__(self)

        self.click_element('name')