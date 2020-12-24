# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/testing.py
# Compiled at: 2013-09-23 12:05:53
# Size of source mod 2**32: 1629 bytes
from mediagoblin.tools import common
from mediagoblin.tools.template import clear_test_template_context
from mediagoblin.tools.mail import EMAIL_TEST_INBOX, EMAIL_TEST_MBOX_INBOX

def _activate_testing():
    """
    Call this to activate testing in util.py
    """
    common.TESTS_ENABLED = True


def clear_test_buckets():
    """
    We store some things for testing purposes that should be cleared
    when we want a "clean slate" of information for our next round of
    tests.  Call this function to wipe all that stuff clean.

    Also wipes out some other things we might redefine during testing,
    like the jinja envs.
    """
    global EMAIL_TEST_INBOX
    global EMAIL_TEST_MBOX_INBOX
    global SETUP_JINJA_ENVS
    SETUP_JINJA_ENVS = {}
    EMAIL_TEST_INBOX = []
    EMAIL_TEST_MBOX_INBOX = []
    clear_test_template_context()