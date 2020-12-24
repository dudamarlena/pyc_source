# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Encoding.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 2866 bytes
from time import sleep
from re import search
from xsrfprobe.core.colors import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.files.dcodelist import HASH_DB

def Encoding(val):
    """
    This function is for detecting the encoding type of
            Anti-CSRF tokens based on pre-defined
                    regular expressions.
    """
    found = 0
    if not val:
        return (found, None)
    else:
        verbout(color.RED, '\n +------------------------------+')
        verbout(color.RED, ' |   Token Encoding Detection   |')
        verbout(color.RED, ' +------------------------------+\n')
        verbout(GR, 'Proceeding to detect encoding of Anti-CSRF Token...')
        for h in HASH_DB:
            txt = hashcheck(h[0], h[1], val)
            if txt is not None:
                found = 1
                verbout(color.RED, '\n [+] Anti-CSRF Token is detected to be String Encoded!')
                print(color.GREEN + ' [+] Token Encoding Detected: ' + color.BG + ' ' + txt + ' ' + color.END)
                print(color.ORANGE + ' [-] Endpoint likely ' + color.BR + ' VULNERABLE ' + color.END + color.ORANGE + ' to CSRF Attacks inspite of CSRF Tokens.')
                print(color.ORANGE + ' [!] Vulnerability Type: ' + color.BR + ' String Encoded Anti-CSRF Tokens ' + color.END)
                print(color.RED + ' [-] The Tokens might be easily Decrypted and can be Forged!')
                break

        if found == 0:
            print((color.RED + '\n [-] ' + color.BR + ' No Token Encoding Detected. ' + color.END), end='\n\n')
        sleep(0.8)
        return (found, txt)


def hashcheck(hashtype, regexstr, data):
    try:
        print(O, ('Matching Encoding Type: %s' % hashtype), end='\r', flush=True)
        sleep(0.1)
        if search(regexstr, data):
            return hashtype
    except KeyboardInterrupt:
        pass