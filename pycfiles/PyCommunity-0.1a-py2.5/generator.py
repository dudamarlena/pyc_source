# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/pycommunity/generator.py
# Compiled at: 2007-02-12 09:02:44
""" Generator
"""
import logging

class BaseTask(object):
    """base class for task"""

    def _getName(self):
        raise NotImplementedError

    def _run(self, configuration):
        raise NotImplementedError

    def _writeFile(self, path, content):
        """helper to write a file"""
        f = open(path, 'w')
        logging.info('writing %s' % path)
        try:
            f.write(content)
        finally:
            f.close()


tasks = None

def registerTask(task):
    """registers a task"""
    global tasks
    if tasks is None:
        tasks = {}
    instance = task()
    tasks[instance._getName()] = instance
    return


def run(steps, configuration):
    """runs a sequence"""
    for step in steps:
        tasks[step]._run(configuration)