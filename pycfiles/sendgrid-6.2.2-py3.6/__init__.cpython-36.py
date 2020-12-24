# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sendgrid/__init__.py
# Compiled at: 2020-04-15 16:00:33
# Size of source mod 2**32: 777 bytes
"""
This library allows you to quickly and easily use the Twilio SendGrid Web API v3 via
Python.

For more information on this library, see the README on GitHub.
    http://github.com/sendgrid/sendgrid-python
For more information on the Twilio SendGrid v3 API, see the v3 docs:
    http://sendgrid.com/docs/API_Reference/api_v3.html
For the user guide, code examples, and more, visit the main docs page:
    http://sendgrid.com/docs/index.html

Available subpackages
---------------------
helpers
    Modules to help with common tasks.
"""
from .version import __version__
from .sendgrid import SendGridAPIClient
from .helpers.mail import *
from .helpers.endpoints import *
from .helpers.stats import *