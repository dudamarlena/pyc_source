# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/getpaid/emailcheckout/options.py
# Compiled at: 2010-05-31 16:45:40
from getpaid.core.options import PersistentOptions
from getpaid.emailcheckout.interfaces import IEmailOptions
EmailOptions = PersistentOptions.wire('EmailOptions', 'getpaid.emailcheckout', IEmailOptions)