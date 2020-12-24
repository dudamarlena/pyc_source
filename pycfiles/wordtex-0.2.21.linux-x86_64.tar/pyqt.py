# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/wordtex/cloudtb/extra/pyqt.py
# Compiled at: 2013-11-12 16:48:22
from PyQt4 import QtGui

class StdWidget(QtGui.QWidget):

    def __init__(self, parent=None):
        super(StdWidget, self).__init__(parent)

    def save_settings(self, application_settings):
        """Puts own settings into the application_settings dict
        
        This function is to-be extended by the parent class.
        It retuturns a dict of settings that still need to be gotten.
        
        All upper level functions should return the same thing -- the highest
        level function does error checking by ensuring that bool(need_settings)
            == False
        """
        assert self._NAME_ not in application_settings
        settings = {}
        need_settings = {}
        for key, value in self.std_settings.iteritems():
            getexec, setexec = key
            getval, setval = value
            if getval == None:
                need_settings[key] = (
                 getval, setval)
            else:
                try:
                    gotval = eval(getexec)(*getval)
                    settings[key] = (
                     getval, (gotval,))
                except Exception as E:
                    print 'ERROR: Failure to save settings!'
                    print 'Class name:', self._NAME_
                    print 'Error:', E
                    print 'SYNTAX:', getexec, getval

        application_settings[self._NAME_] = settings
        return need_settings

    def load_settings(self, application_settings):
        """Load settings given the previous settings from the 
        application settings
        
        Returns the settings that still need to be loaded. All
        implementations of this function should do the same (for error
            checking at top level)
        """
        std_settings = self.std_settings
        try:
            settings = application_settings[self._NAME_]
        except KeyError:
            settings = std_settings

        for key in tuple(settings.keys()):
            if key not in std_settings:
                del settings[key]

        for key in std_settings.iterkeys():
            if key not in settings:
                settings[key] = std_settings[key]

        need_settings = {}
        for key, item in settings.iteritems():
            getexec, setexec = key
            getval, setval = item
            if setval == None:
                need_settings[key] = (
                 getval, setval)
            else:
                try:
                    eval(setexec)(*setval)
                except Exception as E:
                    print 'ERROR: Failure to load settings!'
                    print 'Name', self._NAME_
                    print 'Error:', E
                    print 'SYNTAX:', setexec, setval
                    print '\n', 'Loading default setting'
                    eval(key[1])(*std_settings[key][1])

        return need_settings