# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/generations/evolve1.py
# Compiled at: 2012-10-22 06:18:07
"""This ztfy.package generation modifies registered schedulers tasks
to remove scheduling modes marker interfaces which could be already included
due to a bug in a previous intermediate release.
"""
import logging
logger = logging.getLogger('ztfy.scheduler')
from zope.component.interfaces import ISite
from zope.interface import providedBy, noLongerProvides
from ztfy.scheduler.interfaces import IScheduler, ISchedulerTaskSchedulingMarker
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtilitiesFor
from zope.site import hooks

def evolve(context):
    """Reset tasks provided interfaces"""
    logger.info('Evolving ztfy.scheduler database to level 1...')
    root_folder = context.connection.root().get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            for _name, scheduler in getUtilitiesFor(IScheduler):
                for task in scheduler.tasks:
                    for intf in providedBy(task):
                        if issubclass(intf, ISchedulerTaskSchedulingMarker):
                            noLongerProvides(task, intf)

    return