# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/tecutils/envvar.py
# Compiled at: 2012-08-03 14:55:14
"""
envvar
======

Provides:
    Reads a file containing <var>=<value> and loads in a container, 
    so you can use container.var
    
    getVarFromFile(filename,container)
    
Use:
    
::
db = getVarFromFile('config/db.cfg','db')
::
    
Notes: 
    In order to work the "container" parameter must be the name of the container <var>.
    In the example db is the <var> and container='db'
Reference:
    http://stackoverflow.com/questions/924700/
         best-way-to-retrieve-variable-values-from-a-text-file-python-json
"""

def getVarFromFile(filename, name):
    import imp
    f = open(filename)
    glbvar = imp.load_source(name, '', f)
    f.close()
    return glbvar


if __name__ == '__main__':
    test = getVarFromFile('test/file.cfg', 'test')
    print test.VAR2