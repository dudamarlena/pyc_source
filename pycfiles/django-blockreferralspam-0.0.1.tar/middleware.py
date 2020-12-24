# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/www/html/blockreferralspam/blockreferralspam/blockreferralspam/middleware.py
# Compiled at: 2015-07-13 05:40:17
import re, os
from django.http import HttpResponse, Http404

class KillSpam:

    def process_request(self, request):
        if 'HTTP_REFERER' in request.META:
            f = open(os.path.dirname(os.path.realpath(__file__)) + '/spammers.txt', 'r')
            for line in f.readlines():
                my_regex = '.*' + re.escape(line.rstrip()) + '.*'
                if re.search(my_regex, request.META['HTTP_REFERER'], re.IGNORECASE):
                    raise Http404