# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/external/test/test_qt.py
# Compiled at: 2019-08-19 15:09:29
import sys, taurus, unittest

def _import(name):
    __import__(name)
    return sys.modules[name]


class QtTestCase(unittest.TestCase):
    _api_name = None

    def setUp(self):
        taurus.setLogLevel(taurus.Critical)
        self.opt_mods = ('QtDesigner', 'QtNetwork', 'Qt', 'QtSvg', 'QtUiTools', 'QtWebKit',
                         'Qwt5', 'uic')
        self._orig_mods = set(sys.modules.keys())
        from taurus.external.qt import Qt, API_NAME
        self._api_name = API_NAME
        self.__qt = Qt

    def test_qt_base_import(self):
        mods = set(sys.modules.keys())
        other_apis = set(('PyQt5', 'PySide2', 'PyQt4', 'PySide'))
        other_apis.remove(self._api_name)
        self.assertTrue(self._api_name in mods, self._api_name + ' not loaded')
        self.assertTrue(self._api_name + '.QtCore' in mods, 'QtCore not loaded')
        for other_api in other_apis:
            self.assertFalse(other_api in mods, other_api + ' loaded in ' + self._api_name + ' test')

        for opt_mod in self.opt_mods:
            mod = ('{0}.{1}').format(self._api_name, opt_mod)
            self.assertFalse(mod in mods - self._orig_mods, mod + ' is loaded')

    def __test_qt_module(self, qt_mod_name):
        """Checks that the given shim is complete"""
        taurus_qt_mod_name = ('taurus.external.qt.{0}').format(qt_mod_name)
        orig_qt_mod_name = ('{0}.{1}').format(self._api_name, qt_mod_name)
        TaurusQtMod = _import(taurus_qt_mod_name)
        OrigQtMod = _import(orig_qt_mod_name)
        taurus_qt_mod_members = [ m for m in dir(TaurusQtMod) if not m.startswith('_')
                                ]
        orig_qt_mod_members = [ m for m in dir(OrigQtMod) if not m.startswith('_')
                              ]
        for orig_member_name in orig_qt_mod_members:
            self.assertTrue(orig_member_name in taurus_qt_mod_members, ('Taurus {0} does not contain {1}').format(qt_mod_name, orig_member_name))

    def test_qt_core(self):
        """Check the QtCore shim"""
        return self.__test_qt_module('QtCore')

    def test_qt_gui(self):
        """Check the QtGui shim"""
        return self.__test_qt_module('QtGui')


def main():
    unittest.main(verbosity=2)


if __name__ == '__main__':
    main()