# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Axon/debugConfigFile.py
# Compiled at: 2008-10-19 12:19:52
"""=====================================
Reading debugging configuration files
=====================================

The readConfig() method reads debugging configuration from the specified file.

* Axon.debug.debug uses this to read configuration for itself.

Each call to output debugging information specifies what section it belongs to
and the level of detail it represents. A configuration file specifies what
sections should be expected and what maximum level of detail should be output
for each.

Debugging configuration file format
-----------------------------------

Debugging configuration files are simple text files.

* **Comments** are lines beginning with a hash '#' character

* **Blank lines** are permitted

* **Configuration lines** are a space (not tab) separated triple of *section*
  name, *level* of detail, and *location*
  
For example::
    
    # The following tags are for debugging the debug system
    #
    
    debugTestClass.even         5  default
    debugTestClass.triple       10 default
    debugTestClass.run          1  default
    debugTestClass.__init__     5  default
    debugTestClass.randomChange 10 default

For a given *section*, the *level* number specifies the maximum level of detail
that you want outputted. Any calls to output debugging information for that
section but with a higher level number will be filtered out.

The final *location* field is currently not used. It is recommended to specify
"default" for the moment.

"""
import re
from string import atoi
debugConfig = dict()

def readConfig(filename):
    """   Reads debug configuration from the specified file.
   
   Returns a dictionary mapping debugging section names to maximum levels of
   detail to be output for that section.
   """

    def readfile(filename):
        f = open(filename)
        data = f.readline()
        yield data
        while data:
            yield data
            data = f.readline()

    def comment(line):
        """Comments are allowed in the config, starting with #,
      blank lines are also allowed"""
        return re.match('^(#|$|  *$)', line)

    def applyFuncs(data, default, funcs=()):
        result = 0
        if funcs == ():
            result = default(data)
        else:
            for func in funcs:
                result = result or func(data)

        return result

    def nextLine(lines, filterFuncs=comment):
        """Return next line, filtering out undesirable lines, eg. comments"""
        data = lines.next()
        if data:
            while applyFuncs(data, filterFuncs):
                data = lines.next()
                if not data:
                    break

        return data

    def parseline(line):
        """      Parse a configuration line, returning (tag,level,location) tuple
      """
        (tag, level, location) = re.split(' *', line)
        level = atoi(level)
        location = location[0:len(location) - 1]
        return (tag, level, location)

    def addConfig(debugConfig, tag, level, location):
        debugConfig[tag] = (
         level, location)

    try:
        lines = readfile(filename)
        data = nextLine(lines)
        while data:
            (tag, level, location) = parseline(data)
            addConfig(debugConfig, tag, level, location)
            data = nextLine(lines)

    except StopIteration:
        return debugConfig


if __name__ == '__main__':
    config = readConfig('debug.conf')
    for tag in config.keys():
        (level, location) = config[tag]
        print tag, level, location