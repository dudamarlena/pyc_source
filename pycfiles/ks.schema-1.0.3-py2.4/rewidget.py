# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/textline/browser/rewidget.py
# Compiled at: 2008-12-22 08:23:21
"""The widget regular expression classes.

$Id: rewidget.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Arvid'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
from zope.schema.interfaces import ValidationError
from zope.app.form.browser.textwidgets import TextWidget, PasswordWidget
from zope.app.form.interfaces import WidgetInputError
from zope.app.form.browser.widget import SimpleInputWidget
from zope.schema.interfaces import InvalidValue
from ks.schema.textline import _
import re
dot_atom = "[-A-Za-z0-9!#$%&\\'*+/=?^_{|}~]+"
domain = '[-A-Za-z0-9]'
emailConstraint = re.compile('^%(dot_atom)s(?:\\.%(dot_atom)s)*@%(domain)s+(?:\\.%(domain)s+)*(?:\\.%(domain)s{2,})+$' % {'dot_atom': dot_atom, 'domain': domain})
nameConstraint = re.compile('^[a-zA-Z0-9_-]{2,}$', flags=re.U)

class NotValidName(ValidationError):
    __module__ = __name__
    __doc__ = _('Alias must be min 2 characters length and consist of a-z A-Z, -, _ and 0-9')


class NotValidEmail(ValidationError):
    __module__ = __name__
    __doc__ = _("Email must be in format:\n        local part (symbols, separated by .),\n        sign @, domain (characters, 0-9, -,\n        separated by ., and length of first-level domain 2 characters min).\n        symbols - это latin characters, numbers,\n        !, #, $, %, &, ', *, +, -, /, =, ?, ^, _, {, |, }, ~\n    ")


class WidgetREBase(TextWidget):
    """widget re checker"""
    __module__ = __name__
    reObj = None
    exceptionRE = ValidationError

    def getInputValue(self):
        value = super(WidgetREBase, self).getInputValue()
        if value and not (hasattr(self, '_error') and self._error):
            try:
                if self.reObj.match(value) is None:
                    raise self.exceptionRE
            except self.exceptionRE, v:
                self._error = WidgetInputError(self.context.__name__, self.label, v)
                raise self._error

        return value


class EmailWidget(WidgetREBase):
    """e-mail widget"""
    __module__ = __name__
    reObj = emailConstraint
    exceptionRE = NotValidEmail


class NameWidget(WidgetREBase):
    """name widget"""
    __module__ = __name__
    reObj = nameConstraint
    exceptionRE = NotValidName