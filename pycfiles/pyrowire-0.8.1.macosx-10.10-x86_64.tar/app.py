# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/tmp/test/lib/python2.7/site-packages/pyrowire/resources/sample/app.py
# Compiled at: 2014-11-25 17:55:11
import pyrowire, settings
pyrowire.configure(settings)

@pyrowire.handler(topic='my_topic')
def my_processor(message_data):
    if not message_data:
        raise TypeError('message_data must not be None')
    return message_data


@pyrowire.validator(name='my_validator')
def my_filter(message_data):
    if not message_data:
        raise TypeError('message_data must not be None')
    return True


if __name__ == '__main__':
    pyrowire.run()