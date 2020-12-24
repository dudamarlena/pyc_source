# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/contentsync/eventhandlers.py
# Compiled at: 2009-05-11 14:25:19


def onSynchronizeStateChange(state, event):
    if state.view is None:
        return
    response = state.view.request.RESPONSE
    if state.initializing:
        response.write(str(state.view()))
        response.write('<input style="display: none;" name="contentSyncLabel" value="">')
    response.write('<input style="display: none;" name="contentSyncStep" value="%s">' % state.step)
    response.write('<input style="display: none;" name="contentSyncTotal" value="%s">' % state.total)
    response.write('<input style="display: none;" name="contentSyncProgress" value="%s">' % state.index)
    if state.label is not None:
        response.write('<input style="display: none;" name="contentSyncLabel" value="%s">' % state.label)
    if state.message:
        response.write('<input style="display: none;" name="contentSyncLog" value="%s">' % state.message)
    if state.done:
        response.write('<input style="display: none;" name="contentSyncLabel" value="%s">' % 'Synchronization complete')
    return