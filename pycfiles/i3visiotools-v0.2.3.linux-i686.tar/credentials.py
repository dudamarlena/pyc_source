# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/i3visiotools/credentials.py
# Compiled at: 2014-12-25 06:48:18
import os, logging, config_credentials as c_creds

def getCredentials():
    """ 
                Recovering the credentials from a file with the following structure:
                
                :return: A dictionary with the following struture:
                        { "platform1": [C1<Credential>, C2<Credential>], "platform2": [C3<Credential>]}
        """
    logger = logging.getLogger('i3visiotools')
    creds = {}
    try:
        contenido = c_creds.returnListOfCreds()
        for l in contenido:
            plat, user, password = l
            c = Credential(user, password)
            if plat not in creds.keys():
                creds[plat] = [
                 c]
            else:
                creds[plat] = creds[plat].append(c)

        logger.info(str(len(contenido)) + ' credentials have been loaded.')
        return creds
    except:
        logger.error('The user credentials file could not be opened. Check if you have installed it in python.')

    logger.debug('No credentials were loaded.')
    return {}


class Credential:
    """ 
                Class to match the credentials needed by a platform.
        """

    def __init__(self, user, password):
        """ 
                        Creation of the credentials.
                        
                        :param user:    Login name.
                        :param password:        Password.
                """
        self.user = user
        self.password = password