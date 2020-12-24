# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/merzky/saga/troy/troy/strategy.py
# Compiled at: 2014-02-27 11:31:04
__author__ = 'TROY Development Team'
__copyright__ = 'Copyright 2013, RADICAL'
__license__ = 'MIT'
import radical.utils as ru, troy

def manage_workload(workload, config):
    """
    Parse and execute a given workload (see `execute_workload()`)
    """
    session = troy.Session(config)
    planner = troy.Planner(session)
    overlay_mgr = troy.OverlayManager(session)
    workload_mgr = troy.WorkloadManager(session)
    strategy = troy.AUTOMATIC
    if 'plugin_strategy' in session.cfg:
        strategy = session.cfg['plugin_strategy']
    if strategy == troy.AUTOMATIC:
        strategy = 'basic_late_binding'
    parsed_workload = workload_mgr.parse_workload(workload)
    return troy.execute_workload(parsed_workload, planner, overlay_mgr, workload_mgr, strategy)


def execute_workload(workload, planner, overlay_mgr, workload_mgr, strategy=troy.AUTOMATIC):
    """
    Execute the given workload -- i.e., translate, bind and dispatch it, and
    then wait until its execution is completed.  For that to happen, we also
    need to plan, translate, schedule and dispatch an overlay, obviously...
    """
    if strategy == troy.AUTOMATIC:
        if 'plugin_strategy' in workload.session.cfg:
            strategy = workload.session.cfg['plugin_strategy']
        else:
            strategy = 'basic_late_binding'
    plugin_mgr = ru.PluginManager('troy')
    strategy = plugin_mgr.load('strategy', strategy)
    if not strategy:
        raise RuntimeError('Could not load troy strategy plugin')
    strategy.init_plugin(planner.session, 'strategy')
    if isinstance(workload, basestring):
        workload_id = workload
    elif isinstance(workload, troy.Workload):
        workload_id = workload.id
    else:
        raise TypeError('strategy apply to troy workloads, not to %s' % type(workload))
    strategy.execute(workload_id, planner, overlay_mgr, workload_mgr)