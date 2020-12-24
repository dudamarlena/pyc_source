# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/tests/test_repo.py
# Compiled at: 2014-11-09 11:12:37
import unittest
from seafileapi import client
from seafileapi.exceptions import DoesNotExist
from tests.base import SeafileApiTestCase
from tests.utils import randstring

class RepoTest(SeafileApiTestCase):
    pass