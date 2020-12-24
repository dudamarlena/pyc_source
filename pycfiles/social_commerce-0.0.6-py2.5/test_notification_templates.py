# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/socialcommerce/tests/test_notification_templates.py
# Compiled at: 2009-10-31 23:19:40
from notification.models import NoticeType, get_formatted_messages
FORMATS = [
 'short.txt',
 'full.txt',
 'notice.html',
 'full.html']

class MockDict:

    def __contains__(self, key):
        return True

    def __getitem__(self, key):
        return '{{%s}}' % key

    def __setitem__(self, key, value):
        pass

    def update(self, e, **f):
        pass

    def pop(self):
        pass


MOCK_CONTEXT = MockDict()

def run():
    for notice_type in NoticeType.objects.all():
        label = notice_type.label
        print '-' * 72
        print 'testing %s...' % label
        try:
            messages = get_formatted_messages(FORMATS, label, MOCK_CONTEXT)
        except Exception, e:
            print e

        for format in FORMATS:
            print '%s:' % format
            print messages[format]

        print