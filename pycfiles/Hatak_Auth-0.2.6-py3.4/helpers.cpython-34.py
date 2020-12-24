# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/auth/helpers.py
# Compiled at: 2015-05-01 11:57:01
# Size of source mod 2**32: 513 bytes
from jinja2.exceptions import TemplateNotFound
from haplugin.formskit.helpers import FormWidget

class LoginFormWidget(FormWidget):
    prefix = 'haplugin.auth:templates/forms'

    def render_for(self, name, data, prefix=None):
        self.generate_data()
        self.data.update(data)
        prefix = prefix or self.prefix
        try:
            return self.render(self.get_template(name, prefix))
        except TemplateNotFound:
            return self.render(self.get_template(name, super().prefix))