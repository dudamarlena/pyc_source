# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\paps\crowd\pluginInterface.py
# Compiled at: 2016-03-31 03:40:20
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
__author__ = b'd01'
__email__ = b'jungflor@gmail.com'
__copyright__ = b'Copyright (C) 2015-16, Florian JUNG'
__license__ = b'MIT'
__version__ = b'0.2.0'
__date__ = b'2016-03-29'
from abc import ABCMeta
from flotils.runable import StartStopable, StartException
from flotils.loadable import Loadable
from ..papsException import PapsException
from ..changeInterface import ChangeInterface

class PluginException(PapsException):
    """
    Class for plugin exceptions
    """
    pass


class PluginStartException(PapsException, StartException):
    """
    Class for plugin start exceptions
    """
    pass


class Plugin(Loadable, StartStopable, ChangeInterface):
    """
    Abstract interface for plugin
    """
    __metaclass__ = ABCMeta

    def __init__(self, settings=None):
        """
        Initialize object

        :param settings: Settings to be passed for init (default: None)
        :type settings: dict | None
        :rtype: None
        :raises TypeError: Controller missing
        """
        if settings is None:
            settings = {}
        super(Plugin, self).__init__(settings)
        self.controller = settings.get(b'controller')
        return