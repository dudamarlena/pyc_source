# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ben/dev/signalbox/signalbox/utilities/extra_content_view.py
# Compiled at: 2014-08-27 19:26:12
from django.views.generic import TemplateView

class ExtraContextView(TemplateView):
    """Like the built in Templateview, but compensates for the missing
    extra_context argument which was available with the old-style generic views.

    Usage example:

        urlpatterns = patterns('',
            (r'^myurl/$', ExtraContextView.as_view(
                template_name='mytemplate.html',
                extra_context={
                    ...
                },
            )),

    """
    extra_context = {}

    def get_context_data(self, **kwargs):
        context = super(ExtraContextView, self).get_context_data(**kwargs)
        context.update(self.extra_context)
        return context