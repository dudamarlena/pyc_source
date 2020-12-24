# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\loutilities\applytemplate.py
# Compiled at: 2019-11-21 05:14:04
# Size of source mod 2**32: 5327 bytes
"""
applytemplate - apply a template to files in a directory
===============================================================

Usage::

    applytemplate [-h] [-v] [-e EXTENSION]
    
    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -e EXTENSION, --extension EXTENSION
                            extension for files to be processed (default htmli)
                            
Reads all the input files (*.<EXTENSION>) in the directory, and applies indicated templates to those files.

Input files are of the form::

    [template]
    
    templatefile = <template filename>
    outputdir = <output directory>
    outputext = <output extension>
    
    [substitutions]
    
    sub1 = <sub1 text>
    
All strings of form {{{sub1}}} in the template file are substituted with <sub1 text> (e.g.).
The format of the template file is defined in http://mustache.github.io/mustache.5.html .  Due to the nature of the
input file, not all mustache features are supported.  E.g., there is currently no way to configure lists.

The input file follows the rules for configuration files defined in http://docs.python.org/2/library/configparser.html#module-ConfigParser .
As an example, long substitutions can be extended over several lines.
After the first line, the subsequent lines of the same substitution must start with some white space.

NOTE: all white space at the beginning of each line is deleted when applied to the template.  This is due to implementation of python's ConfigParser class.
    
"""
import argparse, glob, os.path
from configparser import ConfigParser
import pystache
from . import version
TEMPLATESEC = 'template'
SUBSEC = 'substitutions'

def main():
    """
    add key to key file
    """
    parser = argparse.ArgumentParser(version=('{0} {1}'.format('loutilities', version.__version__)))
    parser.add_argument('-e', '--extension', help='extension for files to be processed (default %(default)s)', default='htmli')
    args = parser.parse_args()
    extension = args.extension
    files = glob.glob('*.{}'.format(extension))
    for f in files:
        cfg = ConfigParser()
        cfg.read(f)
        templatefile = cfg.get(TEMPLATESEC, 'templatefile')
        outputdir = cfg.get(TEMPLATESEC, 'outputdir')
        outputext = cfg.get(TEMPLATESEC, 'outputext')
        thisbase, thisext = os.path.splitext(f)
        outputfile = thisbase + '.' + outputext
        outputpath = os.path.join(outputdir, outputfile)
        substitutions = {}
        for sub in cfg.options(SUBSEC):
            substitutions[sub] = cfg.get(SUBSEC, sub)

        TEMPLATE = open(templatefile)
        template = TEMPLATE.read()
        outstring = (pystache.render)(template, **substitutions)
        TEMPLATE.close()
        updateneeded = True
        if os.path.exists(outputpath):
            CURR = open(outputpath)
            curr = CURR.read()
            CURR.close()
            if curr == outstring:
                updateneeded = False
            if updateneeded:
                OUT = open(outputpath, 'w')
                OUT.write(outstring)
                OUT.close()


if __name__ == '__main__':
    main()