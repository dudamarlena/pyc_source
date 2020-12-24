# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/manage/propget.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 2502 bytes


def get(prop, choices=None):
    prompt = prop.verbose_name
    if not prompt:
        prompt = prop.name
    if choices:
        if callable(choices):
            choices = choices()
    else:
        choices = prop.get_choices()
    valid = False
    while not valid:
        if choices:
            min = 1
            max = len(choices)
            for i in range(min, max + 1):
                value = choices[(i - 1)]
                if isinstance(value, tuple):
                    value = value[0]
                print('[%d] %s' % (i, value))

            value = raw_input('%s [%d-%d]: ' % (prompt, min, max))
            try:
                int_value = int(value)
                value = choices[(int_value - 1)]
                if isinstance(value, tuple):
                    value = value[1]
                valid = True
            except ValueError:
                print('%s is not a valid choice' % value)
            except IndexError:
                print('%s is not within the range[%d-%d]' % (min, max))

        else:
            value = raw_input('%s: ' % prompt)
            try:
                value = prop.validate(value)
                if prop.empty(value) and prop.required:
                    print('A value is required')
                else:
                    valid = True
            except:
                print('Invalid value: %s' % value)

    return value