# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/breinify/demo.py
# Compiled at: 2016-08-08 13:58:32
# Size of source mod 2**32: 713 bytes
import breinify
breinify.setup('YOURAPIKEY')

def fancy_print(email):
    result = breinify.lookup(breinify.user(email=email), ['firstname', 'gender'])
    name = result['firstname']['result']
    honorific = ' '
    if result['gender']['result'] == 'MALE' and result['gender']['accuracy'] > 0.8:
        honorific = ' Mr. '
    if result['gender']['result'] == 'FEMALE' and result['gender']['accuracy'] > 0.8:
        honorific = ' Mrs. '
    if result['firstname']['accuracy'] < 0.8:
        honorific = ''
        name = ''
    print('Hi' + honorific + name + '! What can we at Breinify do for you today?')


fancy_print('john.doe@email.com')