# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_plugin/deploy_plugin.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 9, 2012\n\n@package: ally plugin\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nSpecial module that is targeted by the application loader in order to deploy the components in the current system path.\n'
from .distribution import markers, persistMarkers
from ally.container import aop, ioc, context, event, support, app
from ally.container.error import SetupError
from ally.container.impl.config import load
from ally.support.util_sys import isPackage
from package_extender import PACKAGE_EXTENDER
import logging, os, re, sys
log = logging.getLogger(__name__)

def loadPlugins():
    """ Add the plugins to the python path"""
    if os.path.isdir(plugins_path()):
        if '__plugin__' in sys.modules:
            raise ImportError('The __plugin__ module is already present in the system modules, this means that adding plugin paths will have no effect. To correct this you need to remove from all components setups any import that contains __plugin__!')
        for name in os.listdir(plugins_path()):
            path = os.path.join(plugins_path(), name)
            for exclude in excluded_plugins():
                if name.startswith(exclude):
                    break
            else:
                path = os.path.abspath(path)
                if path not in sys.path:
                    sys.path.append(path)


def openPlugins():
    """ Add the plugins to the python path and also open the assembly for plugins"""
    loadPlugins()
    if not os.path.isfile(configurations_file_path()):
        print('The configuration file "%s" does not exist, create one by running the the application with "-dump" option' % configurations_file_path())
        sys.exit(1)
    with open(configurations_file_path(), 'r') as (f):
        config = load(f)
    PACKAGE_EXTENDER.addFreezedPackage('__plugin__.')
    pluginModules = aop.modulesIn('__plugin__.**')
    for module in pluginModules.load().asList():
        if not isPackage(module) and re.match('__plugin__\\.[^\\.]+$', module.__name__):
            raise SetupError("The plugin setup module '%s' is not allowed directly in the __plugin__ package it needs to be in a sub package" % module.__name__)
            continue

    context.open(pluginModules, config=config, included=True)


@ioc.config
def plugins_path():
    """
    The path where the plugin eggs are located.
    """
    return 'plugins'


@ioc.config
def configurations_file_path():
    """
    The name of the configuration file for the plugins.
    """
    return 'plugins.properties'


@ioc.config
def excluded_plugins():
    """
    The prefix for the plugins to be excluded, something like: gui-action, introspection-request.
    """
    return []


@ioc.start(priority=ioc.PRIORITY_FIRST)
def deploy():
    openPlugins()
    try:
        context.processStart()
    finally:
        context.deactivate()


@event.on(event.REPAIR)
def repair():
    openPlugins()
    used = set()
    try:
        for call, name, trigger in support.eventsFor(event.REPAIR, app.POPULATE):
            trigger = (
             trigger,)
            if app.POPULATE.isTriggered(trigger):
                used.add(name)
                executed = markers().get(name)
                if app.DEVEL.isTriggered(trigger) or app.REPAIR.isTriggered(trigger):
                    executed = None
                if executed is None:
                    executed = call()
                    log.info("Executed populate event call '%s' for the first time and got %s", name, executed)
                else:
                    if not executed:
                        executed = call()
                        log.info("Executed populate event call '%s' again and got %s", name, executed)
                    else:
                        log.info("No need to execute populate event call '%s'", name)
                markers()[name] = executed
            elif app.REPAIR.isTriggered(trigger):
                log.info("Executing plugins repair event call '%s'", name)
                call()
                continue

    finally:
        persistMarkers(used)
        context.deactivate()

    return