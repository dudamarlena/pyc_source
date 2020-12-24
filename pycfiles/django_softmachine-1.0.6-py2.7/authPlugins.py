# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/protoLib/utils/authPlugins.py
# Compiled at: 2014-05-29 10:16:48


class PluginMount(type):

    def __init__(cls, name, bases, attrs):
        if not hasattr(cls, 'plugins'):
            cls.plugins = []
        else:
            cls.plugins.append(cls)


class PasswordValidator(object):
    """
    Plugins extending this class will be used to validate passwords.
    Valid plugins must provide the following method.
    
    validate(self, password)
    
    Receives a password to test, and either finishes silently or raises a
    ValueError if the password was invalid. The exception may be displayed
    to the user, so make sure it adequately describes what's wrong.
    """
    __metaclass__ = PluginMount


def is_valid_password(password):
    """
    Returns True if the password was fine, False if there was a problem.
    """
    for plugin in PasswordValidator.plugins:
        try:
            plugin().validate(password)
        except ValueError:
            return False

    return True


def get_password_errors(password):
    """
    Returns a list of messages indicating any problems that were found
    with the password. If it was fine, this returns an empty list.
    """
    errors = []
    for plugin in PasswordValidator.plugins:
        try:
            plugin().validate(password)
        except ValueError as e:
            errors.append(str(e))

    return errors


class MinimumLength(PasswordValidator):

    def validate(self, password):
        """Raises ValueError if the password is too short."""
        if len(password) < 6:
            raise ValueError('Passwords must be at least 6 characters.')


class SpecialCharacters(PasswordValidator):

    def validate(self, password):
        """Raises ValueError if the password doesn't contain any special characters."""
        if password.isalnum():
            raise ValueError('Passwords must contain at least one special character.')


if __name__ == '__main__':
    assert get_password_errors('pass') == ['Passwords must be at least 6 characters.',
     'Passwords must contain at least one special character.']
    assert is_valid_password('p@ssword')