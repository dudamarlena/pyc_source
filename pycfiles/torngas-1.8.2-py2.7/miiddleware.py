# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/torngas/mixins/miiddleware.py
# Compiled at: 2016-02-16 00:41:00


class MiddlewareHandlerMixin(object):
    _url_kwargs = {}

    def __init__(self, application, request, **kwargs):
        if kwargs:
            self._url_kwargs.update(kwargs)
            kwargs.clear()
        super(MiddlewareHandlerMixin, self).__init__(application, request, **kwargs)

    def prepare(self):
        res = self.application.middleware_fac.run_request(self)
        self.on_prepare()
        return res

    def on_prepare(self):
        pass

    def render_string(self, template_name, **kwargs):
        self.application.middleware_fac.run_render(self, template_name, **kwargs)
        return super(MiddlewareHandlerMixin, self).render_string(template_name, **kwargs)

    def finish(self, chunk=None):
        if chunk:
            self.write(chunk)
            chunk = None
        self.application.middleware_fac.run_response(self, self._write_buffer)
        super(MiddlewareHandlerMixin, self).finish(chunk)
        return

    def write(self, chunk, status=None):
        if status:
            self.set_status(status)
        super(MiddlewareHandlerMixin, self).write(chunk)

    def log_exception(self, typ, value, tb):
        u"""重写404请求的异常处理
        """
        if not self.application.middleware_fac.run_exception(self, typ, value, tb):
            super(MiddlewareHandlerMixin, self).log_exception(typ, value, tb)

    def on_finish(self):
        super(MiddlewareHandlerMixin, self).on_finish()
        self.application.middleware_fac.run_endcall(self)
        self.complete_finish()

    def complete_finish(self):
        pass