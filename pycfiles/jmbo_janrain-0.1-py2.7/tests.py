# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/janrain/tests.py
# Compiled at: 2013-06-20 04:08:20
import unittest
from django.contrib.sites.models import Site
from django.core.urlresolvers import reverse
from django.http import Http404
from django.test import TestCase
from django.test.client import Client