# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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