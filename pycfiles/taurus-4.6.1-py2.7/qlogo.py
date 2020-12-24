# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/display/qlogo.py
# Compiled at: 2019-08-19 15:09:29
"""
qlogo.py:
"""
__all__ = [
 'QLogo']
__docformat__ = 'restructuredtext'
from taurus import tauruscustomsettings
from taurus.external.qt import Qt
from taurus.qt.qtgui.icon import getCachedPixmap

class QLogo(Qt.QLabel):

    def __init__(self, parent=None, designMode=False):
        self.__name = self.__class__.__name__
        Qt.QLabel.__init__(self, parent)
        sizePolicy = Qt.QSizePolicy(Qt.QSizePolicy.Policy(0), Qt.QSizePolicy.Policy(0))
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(sizePolicy)
        self.setScaledContents(True)
        logo = getattr(tauruscustomsettings, 'ORGANIZATION_LOGO', 'logos:taurus.png')
        self.setPixmap(getCachedPixmap(logo))

    @classmethod
    def getQtDesignerPluginInfo(cls):
        """Returns pertinent information in order to be able to build a valid
        QtDesigner widget plugin.

        The dictionary returned by this method should contain *at least* the
        following keys and values:

            - 'module' : a string representing the full python module name (ex.: 'taurus.qt.qtgui.base')
            - 'icon' : a string representing valid resource icon (ex.: 'designer:combobox.png')
            - 'container' : a bool telling if this widget is a container widget or not.

        This default implementation returns the following dictionary:

            { 'module'    : 'taurus.qt.qtgui.base',
              'group'     : 'Taurus Widgets',
              'icon'      : 'logos:taurus.svg',
              'container' : False }

        :return: (dict) a map with pertinent designer information"""
        return {'group': 'Taurus Widgets', 
           'icon': 'logos:taurus.png', 
           'container': False}


def main():
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    w = QLogo()
    w.show()
    sys.exit(app.exec_())
    return


if __name__ == '__main__':
    main()