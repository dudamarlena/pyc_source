# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/gmisclib/gpk_getopt.py
# Compiled at: 2007-08-13 06:22:58
import getopt

def parse(arglist, shortoptions, longoptions):
    """Splits apart an command line argument list, and puts the arguments into a dictionary.
        The arguments are a list to be parsed, a string of short one character options,
        and a list of long gnu-style options.  The function returns a dictionary
        mapping between option names and values (if any).   Names in the dictionary
        have had leading dashes removed. """
    optlist, args = getopt.getopt(arglist, shortoptions, longoptions)
    optdict = {}

    def add_to_dict(x, d=optdict):
        k, v = x
        while k[0] == '-':
            k = k[1:]

        d[k] = v

    map(add_to_dict, optlist)
    return (optdict, args)