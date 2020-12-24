# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/tgcaptcha/widgets.py
# Compiled at: 2007-06-02 21:58:45
import pkg_resources, turbogears as tg, controller
from tgcaptcha.validator import CaptchaFieldValidator
import gettext
_ = gettext.gettext
from turbogears.widgets import CSSLink, JSLink, Widget, WidgetDescription, register_static_directory, CompoundFormField, FormField, HiddenField
from turbogears import widgets
js_dir = pkg_resources.resource_filename('tgcaptcha', 'static/javascript')
register_static_directory('tgcaptcha', js_dir)
captcha_controller = controller.CaptchaController()

class CaptchaInputField(FormField):
    """Basic captcha widget.
    
    This widget doesn't do any validation, and should only be used if you 
    want to do your own validation.
    """
    __module__ = __name__
    template = '\n    <span xmlns:py="http://purl.org/kid/ns#">\n        <img id="${field_id}_img" \n            src="${controller}/image/${payload}" \n            alt="${alt}"/>\n        <input \n            type="text"\n            name="${name}"\n            class="${field_class}"\n            id="${field_id}"\n            py:attrs="attrs"/> \n    </span>\n    '
    params = [
     'controller', 'payload', 'alt', 'attrs']
    controller = tg.url(tg.config.get('tgcaptcha.controller', '/captcha'))
    alt = _('obfuscated letters')
    attrs = {}


class CaptchaField(CompoundFormField):
    """Basic validating captcha widget."""
    __module__ = __name__
    name = 'Captcha'
    fields = [CaptchaInputField(name='captchainput'), HiddenField(name='captchahidden')]
    validator = CaptchaFieldValidator()

    def update_params(self, d):
        mwp = d['member_widgets_params']
        payload = captcha_controller.create_payload()
        mwp['payload'] = {'captchainput': payload}
        if not d['value']:
            d['value'] = {'captchahidden': payload}
        else:
            d['value']['captchahidden'] = payload
        super(CaptchaField, self).update_params(d)

    template = '\n    <span xmlns:py="http://purl.org/kid/ns#">\n        <div py:for="field in hidden_fields"\n            py:replace="field.display(value_for(field), **params_for(field))" />\n        <div py:for="field in fields" py:strip="True">\n            <span py:replace="field.display(value_for(field), \n                **params_for(field))"/>\n        </div>\n    </span>\n    '


class CaptchaFieldDesc(widgets.WidgetDescription):
    __module__ = __name__
    name = 'CaptchaField'
    for_widget = CaptchaField()


__all__ = [
 'CaptchaField', 'CaptchaInputField']