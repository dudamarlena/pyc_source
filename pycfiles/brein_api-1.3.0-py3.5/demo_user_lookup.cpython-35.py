# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/breinify/demo_user_lookup.py
# Compiled at: 2017-04-18 14:24:51
# Size of source mod 2**32: 872 bytes
from breinify import Breinify, User

def fancy_print(email):
    """
    Generates a sample email based of an email address
    :param email: The user's email address
    """
    brein = Breinify('YOURAPIKEY')
    result = brein.lookup(User(email=email), ['firstname', 'gender'])
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


if __name__ == '__main__':
    fancy_print('john.doe@email.com')