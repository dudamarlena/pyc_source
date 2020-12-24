# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/cisco_decrypt/cisco_decrypt.py
# Compiled at: 2007-08-02 06:51:42
import re, sys
from optparse import OptionParser

class CiscoPassword(object):
    """COPYRIGHT, LICENSE, and WARRANTY
   ================================
   GNU General Public License, v3

   This software is (c) 2007 by David Michael Pennington.  It can be
   reused under the terms of the GPL v3 license provided that proper
   credit for the work of the author is preserved in the form  of this
   copyright notice and license for this package.

   No warranty of any kind is expressed or implied.  By using this software, you
   are agreeing to assume ALL risks and David M Pennington shall NOT be liable
   for ANY damages resulting from its use."""
    __module__ = __name__

    def __init__(self):
        self

    def decrypt(self, ep):
        r"""Cisco Type 7 password decryption.  Converted from perl code that was  
      written by jbash /|at|\ cisco.com"""
        xlat = (100, 115, 102, 100, 59, 107, 102, 111, 65, 44, 46, 105, 121, 101, 119,
                114, 107, 108, 100, 74, 75, 68, 72, 83, 85, 66)
        dp = ''
        regex = re.compile('^(..)(.+)')
        if not len(ep) & 1:
            result = regex.search(ep)
            try:
                s, e = int(result.group(1)), result.group(2)
            except ValueError:
                (s, e) = (0, '')
            else:
                for ii in range(0, len(e), 2):
                    magic = int(re.search('.{%s}(..)' % ii, e).group(1), 16)
                    print 'S = %s' % s
                    if s <= 25:
                        newchar = '%c' % (magic ^ int(xlat[int(s)]))
                    else:
                        newchar = '?'
                    dp = dp + str(newchar)
                    s = s + 1

        if s > 25:
            print 'WARNING: password decryption failed.'
        return dp


if __name__ == '__main__':
    parser = OptionParser()
    parser.add_option('-e', dest='ep', help='Cisco type 7 password string', metavar='STRING')
    (opts, args) = parser.parse_args()
    passwd = CiscoPassword().decrypt(opts.ep)
    print passwd