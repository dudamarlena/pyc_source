# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mkcode/resolver.py
# Compiled at: 2007-05-28 19:09:59
"""
Routines for figuring out who should handle a command, and how they
should go about doing it.
"""
import pkg_resources, sys
from mkcode import registry
from mkcode.registry import NoSuchTaskError

def do_command(target, args=None, mkfile=None):
    """
    Find and execute the specified target, passing it the args from
    the command-line, if and (for it's own processing).
    """
    try:
        goals = path_to_goal(target)
    except NoSuchTaskError:
        task = registry.lookup(registry.namespace('setup').qname(target))
        goals = [
         task]

    if args:
        goals[0](*args)
        goals = goals[1:]
    for task in goals:
        task()


def path_to_goal(goal, _visited=None):
    """
    Build a sequence of tasks necessary to reach the specified task
    goal.  `goal' is a task name.
    """
    if not _visited:
        _visited = []
    if isinstance(goal, basestring):
        goal = registry.lookup(goal)
    if goal in _visited:
        return []
    _visited.append(goal)
    order = []
    for dep in goal.dependencies:
        order.extend(path_to_goal(dep, _visited))

    order.append(goal)
    return order