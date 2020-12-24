# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/captcha/browser/form.py
# Compiled at: 2014-10-14 10:09:18
__docformat__ = 'restructuredtext'
from z3c.form import field
from zope.component import adapts
from zope.interface import Interface, implements
from ztfy.captcha.schema import Captcha
from ztfy.skin.form import EditSubForm
from ztfy.captcha import _

class ICaptchaInfo(Interface):
    """Captcha infos interface"""
    captcha = Captcha(title=_('Verification code'), description=_('This code is used to protect this form against automatic spams.\nCode is made of 6 characters (letters and numbers from 1 to 9).'), required=True)


class CaptchaAdapter(object):
    adapts(Interface)
    implements(ICaptchaInfo)

    def __init__(self, context):
        self.context = context

    def _getCaptcha(self):
        return

    def _setCaptcha(self, value):
        pass

    captcha = property(_getCaptcha, _setCaptcha)


class CaptchaSubForm(EditSubForm):
    """Generic captcha sub-form"""
    prefix = 'captcha.'
    tabLabel = _('Anti-spam code')
    fields = field.Fields(ICaptchaInfo)
    ignoreContext = True