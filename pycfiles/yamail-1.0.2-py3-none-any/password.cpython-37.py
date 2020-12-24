# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/didi/PycharmProjects/nnmail/yamail/password.py
# Compiled at: 2019-04-23 17:03:06
# Size of source mod 2**32: 1319 bytes
try:
    import keyring
except (ImportError, NameError, RuntimeError):
    pass

def handle_password(user, password):
    """ Handles getting the password"""
    if password is None:
        try:
            password = keyring.get_password('yagmail', user)
        except NameError as e:
            try:
                print("'keyring' cannot be loaded. Try 'pip install keyring' or continue without. See https://github.com/kootenpv/yagmail")
                raise e
            finally:
                e = None
                del e

        if password is None:
            import getpass
            password = getpass.getpass('Password for <{0}>: '.format(user))
            answer = ''
            while answer != 'y' and answer != 'n':
                prompt_string = 'Save username and password in keyring? [y/n]: '
                try:
                    answer = raw_input(prompt_string).strip()
                except NameError:
                    answer = input(prompt_string).strip()

            if answer == 'y':
                register(user, password)
    return password


def register(username, password):
    """ Use this to add a new gmail account to your OS' keyring so it can be used in yagmail """
    keyring.set_password('yagmail', username, password)