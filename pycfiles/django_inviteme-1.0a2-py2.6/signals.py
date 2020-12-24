# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/inviteme/signals.py
# Compiled at: 2012-04-10 18:32:51
"""
Signals relating to django-inviteme.
"""
from django.dispatch import Signal
confirmation_will_be_requested = Signal(providing_args=['data', 'request'])
confirmation_will_be_requested.__doc__ = "\nSent just before a confirmation message is requested.\n\nA message is sent to the user right after the contact form is been posted and \nvalidated to verify the user's email address. This signal may be used to ban \nemail addresses or check message content. If any receiver returns False the \nprocess is discarded and the user receives a discarded message. \n"
confirmation_requested = Signal(providing_args=['data', 'request'])
confirmation_requested.__doc__ = "\nSent just after a confirmation message is requested.\n\nA message is sent to the user right after the contact form is been posted \nand validated to verify the user's email address. This signal may be uses to\ntrace contact messages posted but never confirmed.\n"
confirmation_received = Signal(providing_args=['data', 'request'])
confirmation_received.__doc__ = '\nSent just after a confirmation has been received.\n\nA confirmation is received when the user clicks on the link provided in the\nconfirmation message sent by email. This signal may be used to validate that\nthe submit date stored in the URL is no older than a certain time. If any \nreceiver returns False the process is discarded and the user receives a \ndiscarded message. \n'