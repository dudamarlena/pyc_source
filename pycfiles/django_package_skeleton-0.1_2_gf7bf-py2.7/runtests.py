# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/packageutils/runtests.py
# Compiled at: 2012-01-14 01:55:32
"""
Run Django Test with Python setuptools test command

REFERENCE:
    http://gremu.net/blog/2010/enable-setuppy-test-your-django-apps/

AUTHOR:
    lambdalisue[Ali su ae] (lambdalisue@hashnote.net)
    
Copyright:
    Copyright 2011 Alisue allright reserved.

License:
    Licensed under the Apache License, Version 2.0 (the "License"); 
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unliss required by applicable law or agreed to in writing, software
    distributed under the License is distrubuted on an "AS IS" BASICS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""
__AUTHOR__ = 'lambdalisue (lambdalisue@hashnote.net)'
import os, sys
os.environ['DJANGO_SETTINGS_MODULE'] = 'tests.settings'
test_dir = os.path.dirname(__file__)
sys.path.insert(0, test_dir)
from django.test.utils import get_runner
from django.conf import settings

def runtests(verbosity=1, interactive=True):
    """Run Django Test"""
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=verbosity, interactive=interactive)
    failures = test_runner.run_tests(['blogs'])
    sys.exit(bool(failures))


if __name__ == '__main__':
    runtests()