# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtgui/qwt5/monitor.py
# Compiled at: 2019-08-19 15:09:30
"""
monitor.py: Specialized mini-trend widget to monitor some scalar value
"""
from __future__ import print_function
from taurus.external.qt import Qt
from taurus.qt.qtgui.qwt5 import TaurusTrend

class TaurusMonitorTiny(TaurusTrend):
    """
    A specialised :class:`TaurusTrend` widget for monitoring scalar values and show
    their evolution over time. It is designed to be small (e.g. to fit in a
    toolbar). It is inspired by the SysMon applet in old KDE3.

    .. seealso:: :class:`TaurusTrend`,
                 :ref:`TaurusTrend User's Interface Guide <trend_ui>`,
                 :ref:`The TaurusTrend coding examples <examples_taurustrend>`
    """
    DEFAULT_MAX_BUFFER_SIZE = 8192

    def __init__(self, parent=None, designMode=False):
        TaurusTrend.__init__(self, parent=parent, designMode=designMode)
        self.setXIsTime(True)
        self.setAxisScale(self.xBottom, 0, 300)
        self.setXDynScale(True)
        self.setCanvasBackground(Qt.Qt.black)
        self.showLegend(False)
        self.enableAxis(self.xBottom, False)
        self.enableAxis(self.xTop, False)
        self.enableAxis(self.yLeft, False)
        self.enableAxis(self.yRight, False)
        self.setAllowZoomers(False)
        self.toggleDataInspectorMode(enable=True)
        self.setMaximumSize(60, 60)

    def autoShowYAxes(self):
        """reimplemented to avoid auto-enabling of axes"""
        pass

    def event(self, event):
        if event.type() == Qt.QEvent.ToolTip:
            event.accept()
        return TaurusTrend.event(self, event)


if __name__ == '__main__':
    import sys
    from taurus.qt.qtgui.application import TaurusApplication
    app = TaurusApplication(sys.argv, cmd_line_parser=None)
    args = sys.argv[1:]
    KLASS = TaurusTrend
    SHOW = True
    EXPORT = None
    CONFIG = None
    MODELS = []
    XISTIME = True
    for a in args:
        if a == '-xt':
            XISTIME = True
        elif a == '-xe':
            XISTIME = False
        elif a.startswith('-config='):
            CONFIG = a.split('=')[(-1)]
        elif a.startswith('-'):
            print('\n Usage: \n%s [-xe|-xt] [-config=configfilename] [model1 [model2] ...]\n' % sys.argv[0])
            sys.exit(1)
        else:
            MODELS.append(a)

    form = TaurusMonitorTiny()
    form.setXIsTime(XISTIME)
    if CONFIG is not None:
        form.loadConfig(CONFIG)
    if MODELS:
        form.setModel(MODELS)
    if SHOW:
        form.show()
        if len(MODELS) == 0 and CONFIG is None:
            form.showDataImportDlg()
    sys.exit(app.exec_())