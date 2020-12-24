# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/customcontent/decorators.py
# Compiled at: 2011-05-29 08:44:55
from django.utils.decorators import decorator_from_middleware
from customcontent.middleware import CustomContentMiddleware
customcontented = decorator_from_middleware(CustomContentMiddleware)