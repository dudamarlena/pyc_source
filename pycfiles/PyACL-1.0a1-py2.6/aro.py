# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/acl/aro.py
# Compiled at: 2009-04-27 10:47:27
"""
Access Request Objects (i.e., user(s) or group(s)).

"""

class ARO(object):
    """
    Access Request Object.
    
    """

    def __init__(self, identifier, *groups):
        """
        
        :param identifier: The identifier for this ARO instance.
        
        """
        self.identifier = identifier
        self.groups = groups

    def get_groups(self):
        pass


class CompoundARO(ARO):
    """
    Compound Access Request Object.
    
    An ARO made up of one or more AROs.
    
    """

    def __init__(self, *aros):
        super(CompoundARO, self).__init__(None)
        self.aros = list(aros)
        return


class User(ARO):

    def __new__(cls, user_id):
        if user_id is None:
            return Anonymous.__new__()
        else:
            return AuthenticatedUser.__new__(user_id)


class AuthenticatedUser(User):
    pass


class Anonymous(User):

    def __init__(self):
        super(Anonymous, self).__init__(None)
        return


class Anyone(User):

    def __init__(self):
        super(Anyone, self).__init__(None)
        return


class Group(ARO):
    pass