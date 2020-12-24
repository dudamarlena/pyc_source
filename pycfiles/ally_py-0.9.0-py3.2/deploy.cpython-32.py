# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/__deploy__/ally_plugin/deploy.py
# Compiled at: 2013-10-02 09:54:40
"""
Created on Nov 7, 2012

@package: ally plugin
@copyright: 2011 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Special module that is used in deploying the application.
"""
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