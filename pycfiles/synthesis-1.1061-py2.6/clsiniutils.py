# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/clsiniutils.py
# Compiled at: 2010-12-12 22:28:56
import ConfigParser, string, sys, os, fileutils
from clsexceptions import fileNotFoundError

class clsConfigParser(fileNotFoundError):
    r"""
    >>> import clsIniUtils
    >>> cp = clsIniUtils.clsConfigParser('fileConverter.ini')
    >>> pd = cp.getConfig()
    >>> pd
    {'filelocations.basepath': 'C:\\Documents and Settings\\user.PC885314341208\\My Documents\\Development\\AlexandriaConsulting\\ManateeCountySchools\\Data', 'options.debug': '1', 'database.name': 'manateecountyschools', 'database.textdbname': 'manateecountyschools', 'options.debugfile': 'debug.txt', 'filelocations.used_file_extensions': '.used', 'options.first_line_header': 'False', 'filelocations.outputlocation': 'outputdir', 'database.filename': 'manateecountyschools.db', 'filelocations.file_extensions': 'csv', 'options.systemmode': 'Test', 'options.debuglevel': '1', 'database.path': 'C:\\Documents and Settings\\user.PC885314341208\\My Documents\\Development\\AlexandriaConsulting\\ManateeCountySchools\\Data\\database'}
    >>>
    >>> cp.setConfig("newSection", "newOption","newValue")
    >>> pd = cp.getConfig()
    >>> pd
    {'filelocations.basepath': 'C:\\Documents and Settings\\user.PC885314341208\\My Documents\\Development\\AlexandriaConsulting\\ManateeCountySchools\\Data', 'options.debug': '1', 'database.name': 'manateecountyschools', 'database.textdbname': 'manateecountyschools', 'options.debugfile': 'debug.txt', 'filelocations.used_file_extensions': '.used', 'options.first_line_header': 'False', 'filelocations.outputlocation': 'outputdir', 'database.filename': 'manateecountyschools.db', 'filelocations.file_extensions': 'csv', 'options.systemmode': 'Test', 'options.debuglevel': '1', 'newsection.newoption': 'newValue', 'database.path': 'C:\\Documents and Settings\\user.PC885314341208\\My Documents\\Development\\AlexandriaConsulting\\ManateeCountySchools\\Data\\database'}
    >>> pd['newsection.newoption']
    'newValue'
    >>> pd['newSection.newOption']
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 'newSection.newOption'
    >>> cp = clsIniUtils.clsConfigParser('fileConverter2.ini')
    Error 1001:
    Indicates: Configuration(INI) file: fileConverter2.ini was not found.  Please check and try again
    In Location: clsIniUtils
    
    """

    def __name__(self):
        print 'clsConfigParser'

    def __init__(self, file, config={}, pBackupFile=False):
        """
        __init__() method.
        
        should be called at minimum with a file as the first parameter.
        This will open the file defined/structured as an INI (win) style text file.
        
        [section]
        option=value
        option2=value2
        
        etc.
        
        These variables can be accessed by the variable declared in your program as
        
        PD['section.option']
        
        after the class has been instantiated, PD can be populated by calling the getConfig() method.
        
        """
        self.cp = ConfigParser.ConfigParser()
        self.backupFile = pBackupFile
        try:
            self.checkExists(file)
        except fileNotFoundError:
            theError = (
             'Configuration(INI) file: %s was not found.  Please check and try again' % file, 1001, self.__module__)
            raise fileNotFoundError, theError

        self.config = self.LoadConfig(file, config)

    def checkExists(self, file):
        if os.path.isfile(file):
            pass
        else:
            theError = (
             'Configuration(INI) file: %s was not found.  Please check and try again' % file, 1001, self.__module__)
            raise fileNotFoundError, theError

    def dumpConfig(self, file):
        """ Dumps the configuration object to a file (store the ini)"""
        if os.path.isfile(file):
            if self.backupFile == True:
                fileutils.backupFile(file)
        fo = open(file, 'w')
        self.cp.write(fo)
        fo.close()

    def getConfig(self):
        """
        Returns the dictionary defined as { ['section.option'] = value, ['section.option2'] = value }
        
        """
        return self.config

    def setConfig(self, section, option, value):
        """
        setConfig(section, option, value)
        
        This method allows updating of the values stored in the ConfigurationParser Object.
        It is mainly used for writing the INI file used in the dumpConfig() method.
        
        """
        try:
            self.cp.set(section, option, value)
        except ConfigParser.NoSectionError:
            try:
                self.cp.add_section(section)
                self.cp.set(section, option, value)
            except:
                return

        self.pd = self.refreshConfig()

    def LoadConfig(self, file, config={}):
        """
        returns a dictionary with keys of the form
        <section>.<option> and the corresponding values
        """
        config = config.copy()
        self.cp.read(file)
        return self.refreshConfig()

    def refreshConfig(self):
        config = {}
        for sec in self.cp.sections():
            name = string.lower(sec)
            for opt in self.cp.options(sec):
                config[name + '.' + string.lower(opt)] = string.strip(self.cp.get(sec, opt))

        return config


def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()
if __name__ == '__main__':
    _ConfigDefault = {}
    try:
        newConfig = clsConfigParser('fileConverter.ini', _ConfigDefault, True)
    except fileNotFoundError:
        sys.exit(-1)
    else:
        pd = newConfig.getConfig()
        print 'OldStyle: ', pd
        print newConfig.dumpConfig('fileConverter.new.ini')