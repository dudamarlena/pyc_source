# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/validatish/messages.py
# Compiled at: 2009-01-21 16:29:40
{'Required': {'error': _('is required')}, 
   'String': {'error': _('must be a string')}, 
   'PlainText': {'error': _('must consist of numbers and characters only'), 
                 'error_extra': _('must consist of numbers and characters plus any of %(extras)s')}, 
   'Integer': {'error': _('must be an integer')}, 
   'Number': {'error': _('must be a number')}, 
   'Email': {'error': _('must be an email'), 
             'error_no_at': _('must contain one @'), 
             'error_username_incorrect': _('name part before @ is invalid'), 
             'error_domain_incorrect': _('domain part after @ is invalid')}, 
   'DomainName': {'error': _('must be a valid domain name')}, 
   'URL': {'error': _('must be a url')}, 
   'OneOf': {'error': _('must be one of %(set_of_values)s')}}