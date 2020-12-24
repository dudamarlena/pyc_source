# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/lamino/tofu/TofuOptionLoader.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 3708 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '01/06/2018'
from collections import namedtuple
_getterSetter = namedtuple('_getterSetter', [
 'getter', 'setter'])

class _TofuOptionLoader(object):
    __doc__ = 'Simple class used to register the options managed by a TofuXWidget'

    def __init__(self, options, childs=None):
        self._options = options
        self._childs = childs or []
        self._addChild = self._childs.append

    def _hasOption(self, option):
        return option in self._options

    def _setOption(self, option, value):
        if not option in self._options:
            raise AssertionError
        elif value == '':
            self._options[option].setter()
        else:
            self._options[option].setter(value)

    def getParameters(self):
        """Add the value of the detain options + some extra parameters to be
        passed as 'free string'

        :return:
        :rtype: tuple (dict, list)
        """
        _ddict, extraParams = self._getNodeParameters()
        for child in self._childs:
            _childDict = child.getParameters()
            _ddict.update(_childDict)

        return _ddict

    def _getNodeParameters(self):
        """Add the value of the detain options + some extra parameters to be
        passed as 'free string'
        
        :return:
        :rtype: tuple (dict, list)
        """
        _ddict = {}
        for option in self._options:
            _ddict[option] = self._options[option].getter()

        return (
         _ddict, [])

    def setParameters(self, _ddict):
        """

        :param _ddict: 
        :return: initial dictionary less the parameters managed by this option
                 loader
         :rtype dict:
        """
        _lddict = _ddict.copy()
        for child in self._childs:
            _lddict = child.setParameters(_lddict)

        _lddict = self._setNodeParameters(_lddict)
        return _lddict

    def _setNodeParameters(self, _ddict):
        """
        
        :param _ddict: 
        :return: initial dictionary less the parameters managed by this option
                 loader
         :rtype dict:
        """
        updatedDict = _ddict.copy()
        for param, value in _ddict.items():
            if param in self._options:
                self._options[param].setter(value)
                del updatedDict[param]

        return updatedDict