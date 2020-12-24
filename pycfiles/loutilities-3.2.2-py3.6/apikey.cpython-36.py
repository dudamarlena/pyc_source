# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\apikey.py
# Compiled at: 2019-11-21 05:01:11
# Size of source mod 2**32: 5767 bytes
"""
apikey - manage api keys for a given package
===================================================
"""
import argparse, appdirs
from . import version
from . import extconfigparser

class unknownKey(Exception):
    pass


class ApiKey:
    __doc__ = '\n    base class for API key management\n    result of object creation is a apikeys.cfg file with an [apikeys] section, possibly empty\n    \n    keys are stored in the following locations\n    * Windows: C:\\Users\\<username>\\AppData\\Local\\<author>\\<appname>\\apikeys.cfg\n    * Linux: /home/<username>/.config/<appname>/apikeys.cfg\n    * Mac OS X: /Users/<username>/Library/Application Support/<appname>/apikeys.cfg\n    \n    use :meth:`addkey` to add a key, :meth:`getkey` to retrieve a key\n    \n    :param author: author of software for which keys are being managed\n    :param appname: application name for which keys are being managed\n    '
    keyssection = 'apikeys'

    def __init__(self, author, appname):
        """
        """
        configdir = appdirs.user_data_dir(appname, author)
        configfname = 'apikeys.cfg'
        self.cf = extconfigparser.ConfigFile(configdir, configfname)

    def getkey(self, keyname):
        """
        return the key indicated by keyname
        if key doesn't exist, unknownKey is raised
        
        :param keyname: name of key for later retrieval
        :rtype: value of key
        """
        try:
            return self.cf.get(self.keyssection, keyname)
        except extconfigparser.unknownSection:
            raise unknownKey
        except extconfigparser.unknownOption:
            raise unknownKey

    def updatekey(self, keyname, keyvalue):
        """
        update or add a key to key file
        
        :param keyname: name of key for later retrieval
        :param keyvalue: value of key
        """
        self.cf.update(self.keyssection, keyname, keyvalue)

    def list(self):
        """
        Return a list of (keyname, value) pairs for each option in the given section.
        
        :rtype: [(keyname,value),...]
        """
        return self.cf.items(self.keyssection)


def main():
    """
    add key to key file
    """
    parser = argparse.ArgumentParser(version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('application', help='name of application for which keys are to be stored')
    parser.add_argument('keyname', help='name of key to create/update in key configuration file', nargs='?', default=None)
    parser.add_argument('keyvalue', help='value of key to be put into key configuration file', nargs='?', default=None)
    parser.add_argument('-a', '--author', help='name of software author. (default %(default)s)', default='Lou King')
    parser.add_argument('-l', '--list', action='store_true', help='print list of keyname,values.  If set, keyname, value arguments are ignored')
    args = parser.parse_args()
    application = args.application
    author = args.author
    keyname = args.keyname
    keyvalue = args.keyvalue
    plist = args.list
    if not plist:
        if not (keyname and keyvalue):
            print('KEYNAME and VALUE must be supplied')
            return
        apikey = ApiKey(author, application)
        plist or apikey.updatekey(keyname, keyvalue)
    else:
        for keyname, value in apikey.list():
            print('{}={}'.format(keyname, value))


if __name__ == '__main__':
    main()