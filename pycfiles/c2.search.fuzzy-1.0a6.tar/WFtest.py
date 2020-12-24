# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/c2/sample/csvworkflow/tests/WFtest.py
# Compiled at: 2010-06-16 04:21:46


class WFtest(object):

    def doActionLoop(self, obj, trans):
        for tran in trans:
            obj.portal_workflow.doActionFor(obj, tran)

        return

    def getWorkflowStateById(self, pwf, wf_id):
        wf = pwf.getWorkflowById(str(wf_id))
        return [ state for state in getattr(wf, 'states', None) ]