# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/cache_headers/management/commands/generate_vcl.py
# Compiled at: 2017-11-17 03:42:00
from __future__ import print_function
from django.conf import settings
from django.contrib.auth.models import User
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from django.http.response import HttpResponse
from django.test.client import RequestFactory
from cache_headers.middleware import POLICIES, rules
TEMPLATE_A = "\nsub vcl_hash {\n    # Cache even with cookies present. Note we don't delete the cookies. Also,\n    # we only consider cookies listed in the Hash-Cookies variable as part\n    # of the hash. This list is determined by the relevant Django Cache Headers\n    # policy."
TEMPLATE_B = '\n    set req.http.Hash-Value = "x";\n    if (req.http.Hash-Cookies) {\n        # todo: softcode these checks\n        if (req.http.Hash-Cookies ~ "messages") {\n            if (req.http.Cookie ~ "messages=") {\n                set req.http.Hash-Value = req.http.Hash-Value + regsub(req.http.Cookie, ".*messages=([^;]+).*", "\\1");\n            }\n        }\n        if (req.http.Hash-Cookies == "messages|isauthenticated") {\n            if (req.http.Cookie ~ "isauthenticated=1") {\n                set req.http.Hash-Value = req.http.Hash-Value + "1";\n            }\n        }\n        else if (req.http.Hash-Cookies == "messages|%(sessionid)s") {\n            if (req.http.Cookie ~ "%(sessionid)s=") {\n                set req.http.Hash-Value = req.http.Hash-Value + regsub(req.http.Cookie, ".*%(sessionid)s=([^;]+).*", "\\1");\n            }\n        }\n    }\n\n    hash_data(req.http.Hash-Value);\n\n    unset req.http.Hash-Cookies;\n    unset req.http.Hash-Value;\n}' % {'sessionid': settings.SESSION_COOKIE_NAME}

class Command(BaseCommand):
    help = 'Generate a Varnish VCL snippet from the cache headers settings.'

    @transaction.atomic
    def handle(self, *args, **options):
        request = RequestFactory().get('/')
        response = HttpResponse()
        user = User()
        n = 0
        print(TEMPLATE_A)
        for pattern, age, cache_type, dc in rules:
            policy = POLICIES[cache_type]
            policy(request, response, user, age)
            if n == 0:
                print('if', end='')
            else:
                print('else if', end='')
            print(' (req.url ~ "%s") {' % pattern.pattern)
            print('set req.http.Hash-Cookies = "%s";' % response['X-Hash-Cookies'])
            print('}')
            n += 1

        print(TEMPLATE_B)