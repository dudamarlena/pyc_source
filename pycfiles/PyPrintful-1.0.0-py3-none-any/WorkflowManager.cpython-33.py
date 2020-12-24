# uncompyle6 version 3.6.7
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/printflow2/WorkflowManager.py
# Compiled at: 2014-04-03 03:33:52
# Size of source mod 2**32: 1497 bytes
__doc__ = '\nCreated on Sep 16, 2013\n\n@author: "Colin Manning"\n'
import traceback, utils

class WorkflowManager(object):
    """WorkflowManager"""
    workflows = {}
    logger = None

    def __init__(self, logger):
        self.logger = logger

    def registerWorkflow(self, workflow_config):
        workflow_class = utils.get_class(workflow_config['class_name'])
        workflow_object = workflow_class(workflow_config)
        self.workflows[workflow_config['name']] = workflow_object

    def execute(self, workflow_name):
        if workflow_name in self.workflows:
            try:
                workflow = self.workflows[workflow_name]
                workflow.prepare()
                workflow.start()
                workflow.stop()
            except:
                workflow.abort()
                self.logger.error(traceback.format_exc())
                traceback.print_exc()

    def findFolderWorkflow(self, path):
        result = None
        for name in self.workflows:
            wf = self.workflows[name]
            if self.workflows[name].source_folder is None:
                continue
            wf_folder_bits = self.workflows[name].source_folder.split('/')
            path_bits = path.split('/')
            if len(path_bits) == len(wf_folder_bits) and path_bits[(-1)] == wf_folder_bits[(-1)]:
                result = name
                break

        return result