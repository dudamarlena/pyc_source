# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jace/Dropbox/projects/hasgeek/baseframe/baseframe/signals.py
# Compiled at: 2016-06-10 05:36:58
from flask.signals import Namespace
baseframe_signals = Namespace()
form_validation_error = baseframe_signals.signal('form-validation-error')
form_validation_success = baseframe_signals.signal('form-validation-success')
exception_catchall = baseframe_signals.signal('exception-catchall')