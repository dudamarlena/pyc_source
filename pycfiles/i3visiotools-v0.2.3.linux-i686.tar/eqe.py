# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/wrappers/eqe.py
# Compiled at: 2014-12-25 06:48:18
from platforms import Platform
import random, logging

class Eqe(Platform):
    """ 
                A <Platform> object for Demo using Eqe.
        """

    def __init__(self):
        """ 
                        Constructor... 
                """
        self.platformName = 'Eqe'
        self.tags = [
         'professional']
        self.NICK_WILDCARD = '<HERE_GOES_THE_NICK>'
        self.url = 'http://www.eqe-online.org/forum/member.php?username=' + self.NICK_WILDCARD
        self.notFoundText = [
         '<title>EQE Forum</title>']
        self.forbiddenList = [
         ' ', '?']
        self._needsCredentials = True
        self.creds = []

    def _getAuthenticated(self, uBrowser):
        """ 
                       Getting authenticated to a given browser <UsufyBrowser> type.
                """
        logger = logging.getLogger('usufy')
        if len(self.creds) > 0:
            c = random.choice(self.creds)
            urlLogin = 'http://www.eqe-online.org/forum/login.php?do=login'
            r = uBrowser.br.open(urlLogin)
            DEVELOPING = False
            if DEVELOPING:
                print 'Printing forms'
                for i, form in enumerate(uBrowser.br.forms()):
                    print '----------------------'
                    print 'This form is form number:\t' + str(i)
                    print str(form)
                    print '----------------------'

                return False
            formNumber = 0
            uBrowser.br.select_form(nr=formNumber)
            loginField = 'vb_login_username'
            passwordField = 'vb_login_password'
            uBrowser.br.form[loginField] = c.user
            uBrowser.br.form[passwordField] = c.password
            uBrowser.br.submit()
            return True
        else:
            logger.debug('No credentials have been added and this platform needs them.')
            return False