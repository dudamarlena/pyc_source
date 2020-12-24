# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/extfile/namechooser/interfaces.py
# Compiled at: 2012-06-20 11:22:54
__docformat__ = 'restructuredtext'
from zope.configuration.fields import Path, GlobalObject
from zope.interface import Interface
from zope.schema import TextLine
from ztfy.extfile import _

class IExtFileNameChooserConfig(Interface):
    """Informations required to define a name chooser"""
    name = TextLine(title=_('Configuration name'), description=_('Name of the ExtFile name chooser configuration'), default='', required=False)
    temp_path = Path(title=_('Temporary path name'), description=_('Absolute path of temporary files'), default='/var/tmp', required=True)
    base_path = Path(title=_('Base path name'), description=_('Absolute base path of final files'), default='/var/local/zope/files', required=True)
    chooser = GlobalObject(title=_('Filename chooser class'), description=_('Name of an external files names chooser, implementing IExtFileNameChooser'), required=True)


class IExtFileNameChooser(Interface):
    """An interface called to define the final name of an external file"""

    def getName(parent, extfile, name):
        """Generate a new relative file path
        
        This file is relative to NameChooser base_path parameter, but can start with 'os.path.sep'.
        WARNING : when using several name choosers, each one may generate "statistically" unique names,
        otherwise conflicts and errors may occur
        """
        pass