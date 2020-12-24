# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\extconfigparser.py
# Compiled at: 2019-11-25 16:46:41
# Size of source mod 2**32: 10771 bytes
"""
extconfigparser - extended configuration handling
=============================================================================

extend ConfigParser.ConfigParser option interpretation
provide ConfigFile high level configuration file handling

"""
import tempfile, string, os, os.path, shutil
from configparser import ConfigParser, NoSectionError, NoOptionError

class unknownSection(Exception):
    pass


class unknownOption(Exception):
    pass


def _parsevalue(value):
    """
    try to interpret value as dict, list or number
    """
    if value[0] in '[{.' + string.digits:
        try:
            rval = eval(value)
        except SyntaxError:
            rval = value

    else:
        rval = value
    return rval


class ExtConfigParser(ConfigParser):
    __doc__ = '\n    extend :class:`ConfigParser.ConfigParser` to allow list and dict values\n    \n    :params params: see http://docs.python.org/2/library/configparser.html#configparser-objects\n    '

    def get(self, section, option, **kwargs):
        """
        Get an option value for the named section. If vars is provided, it must be a dictionary. The option is looked up in vars (if provided), section, and in defaults in that order.

        All the '%' interpolations are expanded in the return values, unless the raw argument is true. Values for interpolation keys are looked up in the same manner as the option.

        Try to interpret value as int, float, boolean, list, or dict
        """
        value = (ConfigParser.get)(self, section, option, **kwargs)
        return _parsevalue(value)

    def items(self, section, **kwargs):
        """
        Return a list of (name, value) pairs for each option in the given section. Optional arguments have the same meaning as for the get() method.
        
        Try to interpret values as int, float, boolean, list, or dict
        """
        retlist = []
        for name, value in (ConfigParser.items)(self, section, **kwargs):
            rval = (
             name, _parsevalue(value))
            retlist.append(rval)

        return retlist


class ConfigFile:
    __doc__ = '\n    configuration file handler\n    result of object creation is a named configuration file, possibly empty\n    \n    use :meth:`update` to add or update a config option, :meth:`get` to retrieve a config option\n    \n    :param configdir: where configuration file is to be stored\n    :param configfname: filename for configuration file\n    '

    def __init__(self, configdir, configfname):
        """
        """
        if not os.path.exists(configdir):
            os.makedirs(configdir)
        else:
            self.fname = os.path.join(os.path.abspath(configdir), configfname)
            if not os.path.exists(self.fname):
                if os.path.exists(self.fname + '.save'):
                    os.rename(self.fname + '.save', self.fname)
                else:
                    touch = open(self.fname, 'w')
                    touch.close()
        self.cp = ExtConfigParser()
        self.cp.read(self.fname)

    def get(self, section, option):
        """
        return the value of the option indicated by option
        if option doesn't exist, unknownOption is raised
        
        :param section: section within which option should be found
        :param option: name of option for later retrieval
        """
        try:
            return self.cp.get(section, option)
        except NoSectionError:
            raise unknownSection("section '{sec}' not found in {file}".format(sec=section, file=(self.fname)))
        except NoOptionError:
            raise unknownOption("option '{opt}' not found in section '{sec}' within {file}".format(opt=option, sec=section, file=(self.fname)))

    def items(self, section, **kwargs):
        """
        Return a list of (name, value) pairs for each option in the given section. Optional arguments have the same meaning as for the get() method.
        
        Try to interpret values as int, float, boolean, list, or dict
        """
        try:
            return (self.cp.items)(section, **kwargs)
        except NoSectionError:
            raise unknownSection("section '{sec}' not found in {file}".format(sec=section, file=(self.fname)))

    def update(self, section, option, value):
        """
        update or add an option to a configuration file
        
        :param section: section within which option should be updated
        :param option: name of option to be updated or created
        :param value: value of option
        """
        if not self.cp.has_section(section):
            self.cp.add_section(section)
        self.cp.set(section, option, value)
        temp = tempfile.NamedTemporaryFile(delete=False)
        self.cp.write(temp)
        tempname = temp.name
        temp.close()
        os.rename(self.fname, self.fname + '.save')
        shutil.copyfile(tempname, self.fname)
        os.remove(self.fname + '.save')
        os.remove(tempname)
        del self.cp
        self.cp = ExtConfigParser()
        self.cp.read(self.fname)

    def delopt(self, section, option):
        """
        delete an option from a configuration file
        
        :param section: section within which option should be updated
        :param option: name of option to be updated or created
        """
        if not self.cp.has_section(section):
            return
        if not self.cp.has_option(section, option):
            return
        self.cp.remove_option(section, option)
        temp = tempfile.NamedTemporaryFile(delete=False)
        self.cp.write(temp)
        tempname = temp.name
        temp.close()
        os.rename(self.fname, self.fname + '.save')
        shutil.copyfile(tempname, self.fname)
        os.remove(self.fname + '.save')
        os.remove(tempname)
        del self.cp
        self.cp = ExtConfigParser()
        self.cp.read(self.fname)