# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python27\Lib\site-packages\ucli\UCloudApiConfig.py
# Compiled at: 2016-10-14 04:39:14
import ConfigParser, os, sys, platform

class UCloudApiConfig(object):
    """this is the file use to handle config"""

    def __init__(self, configParser=None):
        if configParser is None:
            configParser = ConfigParser.ConfigParser()
        self.configParser = configParser
        self.home = '.ucli'
        self.configure = 'ucloud.cfg'
        self.ucliConfigPath = os.path.join(self.findConfigPath(), self.home)
        return

    def makeConfigDirs(self):
        if not os.path.exists(self.ucliConfigPath):
            os.makedirs(self.ucliConfigPath)

    def findConfigPath(self):
        homePath = ''
        if platform.system() == 'Windows':
            homePath = os.environ['HOMEPATH']
        else:
            homePath = os.environ['HOME']
        return homePath

    def getConfigFileName(self):
        configFileName = os.path.join(self.ucliConfigPath, self.configure)
        return configFileName

    def readConfig(self):
        configFileName = self.getConfigFileName()
        self.configParser.read(configFileName)

    def newCredentials(self):
        self.readConfig()
        try:
            self.configParser.add_section('credentials')
        except Exception as e:
            pass

        self.configParser.set('credentials', 'base_url', 'https://api.ucloud.cn')

    def updateCreadentialsUseValue(self, private_key, public_key, project_id):
        self.readConfig()
        self.configParser.set('credentials', 'public_key', public_key)
        self.configParser.set('credentials', 'private_key', private_key)
        self.configParser.set('credentials', 'project_id', project_id)
        self.makeConfigDirs()
        self.configParser.write(open(self.getConfigFileName(), 'w'))

    def getCredentialsValueByKey(self, key):
        self.readConfig()
        return self.configParser.get('credentials', key)


if __name__ == '__main__':
    pass