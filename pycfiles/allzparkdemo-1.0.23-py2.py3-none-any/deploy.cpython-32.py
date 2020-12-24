# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__deploy__/ally_plugin/deploy.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 7, 2012\n\n@package: ally plugin\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nSpecial module that is used in deploying the application.\n'
from ..ally.deploy import dumpAssembly, test, openSetups
from ..ally.prepare import OptionsCore
from __setup__.ally_plugin.deploy_plugin import configurations_file_path, loadPlugins
from ally.container import ioc, aop, context
from ally.container.impl.config import load, save
import application, os, sys, traceback

@ioc.start
def dump():
    assert isinstance(application.options, OptionsCore), 'Invalid application options %s' % application.options
    if not application.options.writeConfigurations:
        return
    if not __debug__:
        print('Cannot dump configuration file if python is run with "-O" or "-OO" option', file=sys.stderr)
        sys.exit(1)
    try:
        context.activate(dumpAssembly())
        try:
            loadPlugins()
            configFile = configurations_file_path()
            if os.path.isfile(configFile):
                with open(configFile, 'r') as (f):
                    config = load(f)
            else:
                config = {}
            context.open(aop.modulesIn('__plugin__.**'), config=config, included=True)
            try:
                if os.path.isfile(configFile):
                    os.rename(configFile, configFile + '.bak')
                with open(configFile, 'w') as (f):
                    save(context.configurations(force=True), f)
                print('Created "%s" configuration file' % configFile)
            finally:
                context.deactivate()

        finally:
            context.deactivate()

    except SystemExit:
        raise
    except:
        print('-' * 150, file=sys.stderr)
        print('A problem occurred while dumping configurations', file=sys.stderr)
        traceback.print_exc(file=sys.stderr)
        print('-' * 150, file=sys.stderr)


@ioc.before(test)
def testUpdatePlugins():
    assert isinstance(application.options, OptionsCore), 'Invalid application options %s' % application.options
    if not application.options.test:
        return
    try:
        try:
            openSetups()
            loadPlugins()
        except:
            print('-' * 150, file=sys.stderr)
            print('A problem occurred while opening setups for testing', file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            print('-' * 150, file=sys.stderr)
            return

    finally:
        context.deactivate()