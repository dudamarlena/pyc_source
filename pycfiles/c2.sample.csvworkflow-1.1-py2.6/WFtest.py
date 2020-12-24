# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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