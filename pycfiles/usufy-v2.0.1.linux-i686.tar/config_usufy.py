# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/usufy/lib/config_usufy.py
# Compiled at: 2014-12-26 04:35:45
import os, logging, i3visiotools.wrappers.platforms as platforms, i3visiotools.credentials as credentials

def getPlatforms(sites=[
 'all'], tags=[], fileCreds='./creds.txt'):
    """ 
                Method that defines the list of <Platform> objects to be processed... Note that <Facebook> or <Twitter> objects inherit from <Platform>.

                Parameters:
                        :param sites:   A list of platforms: 'all', 'twitter', facebook', ...
                        :param tags:    A list of the tags of the looked platforms: 'news', 'social', ...
                        :param fileCreds: the path to the credentials file.
                
                Return values:
                        Returns a list [] of <Platform> objects.
        """
    logger = logging.getLogger('usufy')
    logger.debug('Recovering all usufy platforms...')
    listAllUsufy = platforms.getAllPlatformsByMode(mode='usufy')
    logger.info('Recovering all the credentials stored in the i3visiotools.config_credentials.py file.')
    creds = credentials.getCredentials()
    for p in listAllUsufy:
        if p.platformName.lower() in creds.keys():
            p.setCredentials(creds[p.platformName.lower()])

    listSelected = []
    logger.debug('Selecting the platforms to be queried according to the input parameters...')
    if 'all' in sites:
        return listAllUsufy
    else:
        for plat in listAllUsufy:
            added = False
            for s in sites:
                if s in str(plat).lower():
                    listSelected.append(plat)
                    added = True
                    break

            if not added:
                for t in plat.tags:
                    if t in tags:
                        listSelected.append(plat)
                        added = True
                        break

        return listSelected