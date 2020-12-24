# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cube\config.py
# Compiled at: 2007-04-06 00:38:03
"""Extends Python's built-in ConfigParser classes.

Config provides classes for working with configuration files in ways not
provided by the built-in ConfigParser classes.
"""
from ConfigParser import SafeConfigParser

class MixedConfigParser(SafeConfigParser):
    """Reads a series of configuration files, updating the configuration
    with the settings in each subsequent file.  Useful for having a default
    configuration and overriding it with a user-specific configuration.

    This class also provides the ability to read a mixture of file
    objects.  i.e. file objects and filenames.  A particular example is
    when it is desired to read a default configuration that sits within
    a zipped package and the precise location of that file cannot be
    known.  Explicitly, this happens when the zip file is not unpacked
    to the file system but rather is accessed via a zip library.
    
    For example:

    config = Config.MixedConfigParser()
    fname = 'userfile.cfg'
    defaults_fp = pkg_resources.resource_stream(__name__, 'default.cfg')
    config.read([defaults_fp, fname])
    """
    __module__ = __name__

    def read(self, filethings):
        """Read one or more configuration files into this configuration.

        filethings is a list of filenames and/or file objects.
        """
        if isinstance(filethings, basestring) or isinstance(filethings, file):
            filethings = [
             filethings]
        read_ok = []
        for filething in filethings:
            try:
                if isinstance(filething, file):
                    fp = filething
                    try:
                        filename = fp.name
                    except AttributeError:
                        filename = '<???>'

                else:
                    fp = open(filething)
                    filename = filething
            except IOError:
                continue

            self._read(fp, filename)


class TkinterConfigParser(MixedConfigParser):
    """Binds each configuration variable to a TK Variable so that updates to the variables are
    tracked and can be saved off from the configuration.  Also allows the configuration to be
    bound to a Tkinter UI.
    """
    __module__ = __name__

    def __init__(self, defaults=None):
        MixedConfigParser.__init__(self, defaults)
        self.cfgvars = {}
        self.vars = {}
        self.callbacks = {}

    def read(self, filethings):
        """Read a set of configuration files just as MixedConfigParser does.
        """
        MixedConfigParser.read(self, filethings)
        for sectionname in self.sections():
            if not self.callbacks.has_key(sectionname):
                self.callbacks[sectionname] = {}
            for optionname in self.options(sectionname):
                if not self.callbacks[sectionname].has_key(optionname):
                    self.callbacks[sectionname][optionname] = []

    def var_cb(self, var, varname, huh, event):
        """Update this parsers core configuration with new values provided by
        TKinter variables.  Called when a linked Variable is set."""
        if self.vars.has_key(varname):
            var = self.vars[varname]
            section = var.section
            option = var.option
            if self.cfgvars.has_key(section):
                if self.cfgvars[section].has_key(option):
                    self.cfgvars[var.section][var.option].pending = self.cfgvars[var.section][var.option].pending or True
                    self.set(var.section, var.option, var.get())
                    self.cfgvars[var.section][var.option].pending = False
            else:
                print "Error: received callback for variable '%s' but variable not found in config."
        else:
            print "Error: received callback for variable '%s' but variable not found in config."

    def set(self, section, option, value):
        """Overrides MixedConfigParser.set() in order to update the linked Variable."""
        MixedConfigParser.set(self, section, option, value)
        if not self.callbacks.has_key(section):
            self.callbacks[section] = {}
        if self.cfgvars.has_key(section) and self.cfgvars[section].has_key(option):
            if not self.cfgvars[section][option].pending:
                var = self.var_for(section, option)
                var.pending = True
                var.set(value)
                var.pending = False
        for cb in self.callbacks[section][option]:
            cb(section, option, value)

    def _ensurevar(self, section, option):
        """Make sure that this configuration has the section and option
        specified."""
        if not self.cfgvars.has_key(section):
            self.cfgvars[section] = {}
        options = self.cfgvars[section]
        if not options.has_key(option):
            import Tkinter
            var = Tkinter.Variable()
            var.section = section
            var.option = option
            var.pending = False
            var.trace('w', lambda *args: self.var_cb(var, *args))
            self.vars[var._name] = var
            options[option] = var
            val = self._sections[section][option]
            var.set(val)

    def trace(self, section, option, callback):
        """Add a callback to be called when the specified option is updated.
        This callback should take three parameters:  the section, option, and
        new value."""
        if self.callbacks.has_key(section):
            options = self.callbacks[section]
            if options.has_key(option):
                self.callbacks[section][option].append(callback)

    def var_for(self, section, option):
        """Returns the Tkinter Variable that corresponds to the specified
        configuration option."""
        self._ensurevar(section, option)
        return self.cfgvars[section][option]