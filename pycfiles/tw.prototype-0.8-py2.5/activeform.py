# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tw/prototype/frameworks/tg2/activeform.py
# Compiled at: 2008-06-02 11:15:04
from decorator import decorator
import pylons
from tg import validate, TGController, expose
from tg.controllers import object_dispatch

class ajax_validate(validate):

    def __init__(self, error_handler=None, *args, **kw):
        self.error_handler = error_handler
        super(validate, self).__init__(*args, **kw)

        class Validators(object):

            def validate(self, params):
                controller = pylons.request.environ['pylons.controller']
                url_path = pylons.request.path.split('/')[1:]
                (controller, remainder) = object_dispatch(controller, url_path)
                res = controller.im_self.form.validate(params)
                return res

        self.validators = Validators()


class AjaxFormResponseHandler(TGController):

    def __init__(self, form, onSuccessFunc=None, *args, **kw):
        """(form, onSuccessFunc=None, *args, **kw)
        This class creates a handler which handles all of the 
        
        
        """
        self.form = form
        self.onSuccessFunc = onSuccessFunc
        TGController.__init__(self, args, kw)

    @expose('json')
    def ajax_error(self, **kw):
        pylons.response.status = '406 FAILED_VALIDATION'
        return dict(form_errors=pylons.c.form_errors)

    @expose('json')
    @ajax_validate(error_handler=ajax_error)
    def ajax_submit(self, **kw):
        controller = pylons.request.environ['pylons.controller']
        url_path = pylons.request.path.split('/')[1:-1]
        for item in url_path:
            controller = getattr(controller, item)

        if self.onSuccessFunc:
            self.onSuccessFunc(controller, **kw)
        return {'response': 'successful submit'}