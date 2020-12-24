# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Ecust.py
# Compiled at: 2016-12-30 01:33:05


class Ecust(object):
    """import ME """

    def __init__(self, platformID, stuID, stuPW):
        """
                Login Module for the import action 
                Args:
                        platformID :
                                1 : JWC
                                2 : URP
                        stuID : Your Student ID 
                        stuPW : Your Student Password of the Student ID
                Return :
                        a cookie if it succeed , or False.
                """
        if platformID is '1':
            import JWC_login as login, JWC_functions as function
        elif platformID is '2':
            import URP_login as login, URP_function as function
        else:
            sys.exit('NO LOGIN!')
        login_cookie = login.Login(stuID, stuPW)
        return login_cookie