# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /www/elorus/local/lib/python2.7/site-packages/yawdadmin/middleware.py
# Compiled at: 2013-08-25 05:42:06


class PopupMiddleware(object):
    """
    This middleware must always be enabled when using yawd-elfinder.
    Place it **before** the :class:`django.middleware.common.CommonMiddleware`
    in your ``MIDLEWARE_CLASSESS`` setting.

    yawd-admin builds upon the original django admin application.
    Some admin widgets open pop-up windows where yawd-admin uses
    a modal window. Since original AdminModel views attempt to return
    pop-up window values to the parent through the ``opener`` javascript
    variable, the iframes used in yawd-elfinder will not work as expected.
    This middleare implements an easy fix, replacing ``opener`` with
    the ``parent`` variable, which is appropriate for iframes.
    """

    def process_response(self, request, resp):
        """
        This method is called right after a view is processed and has
        returned an HttpResponse object.
        """
        if resp.status_code == 200 and hasattr(resp, 'content') and resp.content.startswith('<!DOCTYPE html><html><head><title></title></head><body><script type="text/javascript">opener.dismissAddAnotherPopup(window,'):
            resp.content = resp.content.replace('<!DOCTYPE html><html><head><title></title></head><body><script type="text/javascript">opener.dismissAddAnotherPopup(window,', '<!DOCTYPE html><html><head><title></title></head><body><script>parent.dismissAddAnotherPopup(window,')
        return resp