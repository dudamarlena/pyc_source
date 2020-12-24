# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/data/validators/email_validator.py
# Compiled at: 2013-04-04 15:36:37
"""String validator for e-mail addresses."""
from muntjac.data.validators.regexp_validator import RegexpValidator

class EmailValidator(RegexpValidator):
    """String validator for e-mail addresses. The e-mail address syntax is not
    complete according to RFC 822 but handles the vast majority of valid e-mail
    addresses correctly.

    See L{AbstractStringValidator} for more information.

    @author: Vaadin Ltd.
    @author: Richard Lincoln
    @version: 1.1.2
    """

    def __init__(self, errorMessage):
        """Creates a validator for checking that a string is a syntactically
        valid e-mail address.

        @param errorMessage:
                   the message to display in case the value does not validate.
        """
        super(EmailValidator, self).__init__('^([a-zA-Z0-9_\\.\\-+])+@(([a-zA-Z0-9-])+\\.)+([a-zA-Z0-9]{2,4})+$', True, errorMessage)