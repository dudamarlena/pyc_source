# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/gametex_django_print/tests.py
# Compiled at: 2013-01-13 18:48:35
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.test import TestCase
from random import randint, choice
from obfuscate import obfuscate, deobfuscate

class CipherTest(TestCase):

    def test_ciphers(self):
        for i in range(10000):
            str = ('').join(list([ choice(list(map(chr, range(0, 255)))) for _ in range(randint(0, 3000)) ]))
            try:
                if str != deobfuscate(obfuscate(str)):
                    print 'FAILED: %s\n\n\n' % str
            except:
                print 'EXCEPTION: %s' % str