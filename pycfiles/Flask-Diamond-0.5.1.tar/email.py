# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/idm/Work/flask-diamond/flask_diamond/facets/email.py
# Compiled at: 2016-11-26 11:00:09
from flask_mail import Mail
mail = Mail()

def init_email(self):
    """
    Initialize email facilities.

    :returns: None

    `Flask-Mail <http://pythonhosted.org/Flask-Mail/>`_ is a
    useful tool for creating and sending emails from within a Flask application.
    There are a number of configuration settings beginning with ``MAIL_``
    that permit control over the SMTP credentials used to send email.
    """
    mail.init_app(self.app)