# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.4-x86_64/egg/abl/jquery/plugins/form/widgets.py
# Compiled at: 2011-02-18 13:05:59
"""
abl.jquery.plugin.form widgets

"""
from tw.api import Widget, js_callback
from abl.jquery.core import jQuery
from abl.jquery.core.widgets import update_content_js
from abl.jquery.plugins.form.resources import form_widget_js

class AjaxFormMixin(Widget):
    """
    A mixin for a form to submit the data
    via Ajax.

    More info here:
    http://jquery.malsup.com/form
    """
    javascript = [
     form_widget_js]
    params = dict(config="A dictionary that configures the jQuery form plugin.\n                            Per default the response target (config['target'])\n                            is the form element so the form gets replaced by the response.")
    config = dict()
    default_config = dict()

    def update_params(self, d):
        super(AjaxFormMixin, self).update_params(d)
        config = self.default_config.copy()
        config.update(d.config)
        self.add_call(jQuery('#%s' % d.id).ajax_form(config))


class AjaxFormUpdateMixin(AjaxFormMixin):
    """
    Like AjaxFormMixin but instead of only updating itself
    it can update multiple containers on success
    """
    javascript = [
     form_widget_js,
     update_content_js]
    params = dict(config='A dictionary that configures the jQuery form plugin.\n                            The success callback is update_content from\n                            from abl.jquery.core.widgets.AjaxUpdateContentWidget.')
    config = dict()
    default_config = dict(success=js_callback('submit_success'), target=None)