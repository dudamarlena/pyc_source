# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\turbogears\widgets\rpc.py
# Compiled at: 2011-03-26 09:20:21
"""TurboGears RPC base widget"""
__all__ = [
 'RPC']
from turbogears.widgets.base import Widget, JSLink, static, mochikit
from turbojson import jsonify

class RPC(Widget):
    """RPC base widget."""
    __module__ = __name__
    params = [
     'action', 'update', 'data', 'on_success', 'on_failure', 'on_complete', 'before', 'after', 'loading', 'loaded', 'confirm']
    javascript = [
     mochikit, JSLink(static, 'ajax.js')]

    def update_params(self, d):
        super(RPC, self).update_params(d)
        d['js'] = "return ! remoteRequest(self, '%s', '%s', %s, %s)" % (d.get('action'), d.get('update'), jsonify.encode(d.get('data')), jsonify.encode(self.get_options(d)))

    def get_options(self, d):
        return dict(on_success=d.get('on_success'), on_failure=d.get('on_failure'), on_complete=d.get('on_complete'), before=d.get('before'), after=d.get('after'), loading=d.get('loading'), loaded=d.get('loaded'), confirm=d.get('confirm'))