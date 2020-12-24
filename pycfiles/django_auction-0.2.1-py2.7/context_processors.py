# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/auction/context_processors.py
# Compiled at: 2013-04-22 04:27:13
from auction.utils.generic import get_or_create_bidbasket

def bidbasket(request):
    user = request.user
    bidbasket = get_or_create_bidbasket(request)
    result = {'bidbasket': bidbasket}
    return result