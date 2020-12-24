# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/interfaces/plugin.py
# Compiled at: 2008-12-16 18:21:20
__doc__ = '\ncommon interface for a plugin dispatcher\n'
from zope.interface import Interface
from zope.interface import Attribute

class IPluginExporter(Interface):
    """
    unit class to export data
    """
    __module__ = __name__

    def exportData():
        """
        export an IPluginData
        """
        pass


class IPluginImporter(Interface):
    __module__ = __name__
    data = Attribute('IPlugin data')

    def importData(context):
        """
        import an IPluginData to the context
        """
        pass


class IPluginData(Interface):
    """
    data to import or export bay a IPluginDispatcher
    """
    __module__ = __name__

    def getData():
        """
        return data to be exported or imported
        """
        pass


class IFssImporter(IPluginImporter):
    """
    import fss data
    """
    __module__ = __name__


class IFssExporter(IPluginExporter):
    """
    export fss data
    """
    __module__ = __name__


class IZexpImporter(IPluginImporter):
    """
    import zexp data
    """
    __module__ = __name__


class IZexpExporter(IPluginExporter):
    """
    export zexp data
    """
    __module__ = __name__


class IDeleteImporter(IPluginImporter):
    """
    import delete data
    """
    __module__ = __name__


class IDeleteExporter(IPluginExporter):
    """
    export delete data
    """
    __module__ = __name__


class IFssPluginData(IPluginData):
    """
    specific data for fss dispatcher
    """
    __module__ = __name__


class IZexpPluginData(IPluginData):
    """
    specific data for  zexp dispatcher
    """
    __module__ = __name__


class IDeletePluginData(IPluginData):
    """
    specific data for  delete dispatcher
    """
    __module__ = __name__


class ILinguaPluginData(IPluginData):
    """
    specific data for lingua disptacher
    """
    __module__ = __name__