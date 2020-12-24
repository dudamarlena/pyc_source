# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__deploy__/ally_http_mongrel2_server/prepare.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 7, 2012\n\n@package: ally http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nSpecial module that is used in preparing the application deploy.\n'
from ..ally.prepare import OptionsCore, prepareCoreOptions, prepareCoreActions
from ally.container import ioc
from argparse import ArgumentParser
from inspect import isclass
import application

class OptionsMongrel2(OptionsCore):
    """
    The prepared option class.
    """

    def __init__(self):
        super().__init__()
        self._configMongrel2 = False

    def setConfigMongrel2(self, value):
        """Setter for the mongrel2 configure"""
        if value is None:
            value = 'workspace'
        self._configMongrel2 = value
        self._start = self._start and not value
        return

    configMongrel2 = property(lambda self: self._configMongrel2, setConfigMongrel2)


@ioc.after(prepareCoreOptions)
def prepareMongrel2Options():
    assert isclass(application.Options), 'Invalid options class %s' % application.Options

    class Options(OptionsMongrel2, application.Options):
        pass

    application.Options = Options


@ioc.after(prepareCoreActions)
def prepareMongrel2Actions():
    assert isinstance(application.parser, ArgumentParser), 'Invalid parser %s' % application.parser
    application.parser.add_argument('-cfg-mongrel2', metavar='folder', dest='configMongrel2', nargs='?', default=False, help='Provide this option to create the mongrel2 workspace, by default the mongrel2 workspace will be created by default in "workspace" in the application folder, just provide a new mongrel2 workspace if thats the case, the path can be relative to the application folder or absolute')