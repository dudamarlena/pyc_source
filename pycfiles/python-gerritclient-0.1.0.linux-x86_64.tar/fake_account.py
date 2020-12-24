# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/machin/.virtualenvs/twine/lib/python2.7/site-packages/gerritclient/tests/utils/fake_account.py
# Compiled at: 2017-05-29 09:15:44


def get_fake_account(_account_id=1000226, name='John Doe', email='john.doe@example.com', username='john'):
    """Creates a fake account

    Returns the serialized and parametrized representation of a dumped
    Gerrit Code Review environment.
    """
    return {'_account_id': _account_id, 
       'name': name, 
       'email': email, 
       'username': username, 
       'secondary_emails': [
                          'fake-email@example.com'], 
       'registered_on': '2017-02-16 07:33:57.000000000'}


def get_fake_accounts(account_count):
    """Creates a random fake list of accounts."""
    return [ get_fake_account(_account_id=i, username=('john-{}').format(i)) for i in range(1, account_count + 1)
           ]


def get_fake_account_email_info(email='jdoe@example.com', preferred=False, no_confirmation=False):
    """Creates a random fake email info of accounts."""
    return {'email': email, 'preferred': preferred, 
       'no_confirmation': no_confirmation}