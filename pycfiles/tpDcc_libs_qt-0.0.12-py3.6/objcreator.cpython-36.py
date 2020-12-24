# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tpDcc/libs/qt/externals/pysideuic/objcreator.py
# Compiled at: 2020-05-03 00:26:03
# Size of source mod 2**32: 3918 bytes
import sys, os.path
from pysideuic.exceptions import NoSuchWidgetError, WidgetPluginError
if sys.hexversion >= 50331648:
    from pysideuic.port_v3.load_plugin import load_plugin
else:
    from pysideuic.port_v2.load_plugin import load_plugin
widgetPluginPath = [os.path.join(os.path.dirname(__file__), 'widget-plugins')]
MATCH = True
NO_MATCH = False
MODULE = 0
CW_FILTER = 1

class QObjectCreator(object):

    def __init__(self, creatorPolicy):
        self._cpolicy = creatorPolicy
        self._cwFilters = []
        self._modules = [
         self._cpolicy.createQtGuiWrapper()]
        for plugindir in widgetPluginPath:
            try:
                plugins = os.listdir(plugindir)
            except:
                plugins = []

            for filename in plugins:
                if not not filename.endswith('.py'):
                    if filename == '__init__.py':
                        pass
                    else:
                        filename = os.path.join(plugindir, filename)
                        plugin_globals = {'MODULE':MODULE, 
                         'CW_FILTER':CW_FILTER, 
                         'MATCH':MATCH, 
                         'NO_MATCH':NO_MATCH}
                        plugin_locals = {}
                        if load_plugin(open(filename), plugin_globals, plugin_locals):
                            pluginType = plugin_locals['pluginType']
                            if pluginType == MODULE:
                                modinfo = plugin_locals['moduleInformation']()
                                self._modules.append((self._cpolicy.createModuleWrapper)(*modinfo))
                            else:
                                if pluginType == CW_FILTER:
                                    self._cwFilters.append(plugin_locals['getFilter']())
                                else:
                                    raise WidgetPluginError('Unknown plugin type of %s' % filename)

        self._customWidgets = self._cpolicy.createCustomWidgetLoader()
        self._modules.append(self._customWidgets)

    def createQObject(self, classname, *args, **kwargs):
        classType = self.findQObjectType(classname)
        if classType:
            return (self._cpolicy.instantiate)(classType, *args, **kwargs)
        raise NoSuchWidgetError(classname)

    def invoke(self, rname, method, args=()):
        return self._cpolicy.invoke(rname, method, args)

    def findQObjectType(self, classname):
        for module in self._modules:
            w = module.search(classname)
            if w is not None:
                return w

    def getSlot(self, obj, slotname):
        return self._cpolicy.getSlot(obj, slotname)

    def addCustomWidget(self, widgetClass, baseClass, module):
        for cwFilter in self._cwFilters:
            match, result = cwFilter(widgetClass, baseClass, module)
            if match:
                widgetClass, baseClass, module = result
                break

        self._customWidgets.addCustomWidget(widgetClass, baseClass, module)