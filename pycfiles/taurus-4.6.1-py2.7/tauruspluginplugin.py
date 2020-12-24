# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/qt/qtdesigner/tauruspluginplugin.py
# Compiled at: 2019-08-19 15:09:29
"""
tauruspluginplugin.py:
"""
from __future__ import absolute_import
from taurus.external.qt import QtDesigner

def build_qtdesigner_widget_plugin(klass):
    from taurus.qt.qtdesigner.taurusplugin import taurusplugin

    class Plugin(taurusplugin.TaurusWidgetPlugin):
        WidgetClass = klass

    Plugin.__name__ = klass.__name__ + 'QtDesignerPlugin'
    return Plugin


_SKIP = [
 'QLogo', 'QGroupWidget', 'TaurusGroupWidget']
_plugins = {}

def main():
    from taurus.core.util.log import Logger
    from taurus.qt.qtgui.util import TaurusWidgetFactory
    Logger.setLogLevel(Logger.Debug)
    _log = Logger(__name__)
    try:
        wf = TaurusWidgetFactory()
        klasses = wf.getWidgetClasses()
        ok_nb, skipped_nb, e1_nb, e2_nb, e3_nb, e4_nb = (0, 0, 0, 0, 0, 0)
        for widget_klass in klasses:
            name = widget_klass.__name__
            if name in _SKIP:
                skipped_nb += 1
                continue
            cont = False
            try:
                qt_info = widget_klass.getQtDesignerPluginInfo()
                if qt_info is None:
                    e1_nb += 1
                    cont = True
            except AttributeError:
                e2_nb += 1
                cont = True
            except Exception as e:
                e3_nb += 1
                cont = True

            if cont:
                continue
            for k in ('module', ):
                if k not in qt_info:
                    e4_nb += 1
                    cont = True

            if cont:
                continue
            plugin_klass = build_qtdesigner_widget_plugin(widget_klass)
            plugin_klass_name = plugin_klass.__name__
            globals()[plugin_klass_name] = plugin_klass
            _plugins[plugin_klass_name] = plugin_klass
            ok_nb += 1

        _log.info('Inpected %d widgets. %d (OK), %d (Skipped), %d (E1), %d (E2), %d (E3), %d(E4)' % (
         len(klasses), ok_nb, skipped_nb, e1_nb, e2_nb, e3_nb, e4_nb))
        _log.info('E1: getQtDesignerPluginInfo() returns None')
        _log.info("E2: widget doesn't implement getQtDesignerPluginInfo()")
        _log.info('E3: getQtDesignerPluginInfo() throws exception')
        _log.info("E4: getQtDesignerPluginInfo() returns dictionary with missing key (probably 'module' key)")
    except Exception as e:
        import traceback
        traceback.print_exc()

    return


class TaurusWidgets(QtDesigner.QPyDesignerCustomWidgetCollectionPlugin):

    def __init__(self, parent=None):
        QtDesigner.QPyDesignerCustomWidgetCollectionPlugin.__init__(parent)
        self._widgets = None
        return

    def customWidgets(self):
        if self._widgets is None:
            self._widgets = [ w(self) for w in _plugins.values() ]
        return self._widgets


if __name__ != '__main__':
    main()