# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Entropy.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 5841 bytes
import time, urllib.parse
from math import log
from xsrfprobe.core.colors import *
from xsrfprobe.modules.Token import Token
from xsrfprobe.core.verbout import verbout
from xsrfprobe.files.discovered import REQUEST_TOKENS
from xsrfprobe.core.logger import VulnLogger, NovulLogger

def Entropy(req, url, headers, form, m_action, m_name=''):
    """
    This function has the work of comparing and
      calculating Shannon Entropy and related
           POST Based requests' security.
    """
    found = 0
    min_length = 6
    max_length = 512
    min_entropy = 3.0
    _q, para = Token(req, headers)
    if (para and _q) == None:
        VulnLogger(url, 'Form Requested Without Anti-CSRF Token.', '[i] Form Requested: ' + form + '\n[i] Request Query: ' + req.__str__())
        return ('', '')
    else:
        verbout(color.RED, '\n +------------------------------+')
        verbout(color.RED, ' |   Token Strength Detection   |')
        verbout(color.RED, ' +------------------------------+\n')
        for para in REQUEST_TOKENS:
            value = '%s' % para
            verbout(color.CYAN, ' [!] Testing Anti-CSRF Token: ' + color.ORANGE + '%s' % value)
            if len(value) <= min_length:
                print(color.RED + ' [-] CSRF Token Length less than 5 bytes. ' + color.ORANGE + 'Token value can be guessed/bruteforced...')
                print(color.ORANGE + ' [-] Endpoint likely ' + color.BR + ' VULNERABLE ' + color.END + color.ORANGE + ' to CSRF Attacks...')
                print(color.RED + ' [!] Vulnerability Type: ' + color.BR + ' Very Short/No Anti-CSRF Tokens ' + color.END)
                VulnLogger(url, 'Very Short Anti-CSRF Tokens.', 'Token: ' + value)
            if len(value) >= max_length:
                print(color.ORANGE + ' [+] CSRF Token Length greater than ' + color.CYAN + '256 bytes. ' + color.GREEN + 'Token value cannot be guessed/bruteforced...')
                print(color.GREEN + ' [+] Endpoint likely ' + color.BG + ' NOT VULNERABLE ' + color.END + color.GREEN + ' to CSRF Attacks...')
                print(color.GREEN + ' [!] CSRF Mitigation Method: ' + color.BG + ' Long Anti-CSRF Tokens ' + color.END)
                NovulLogger(url, 'Long Anti-CSRF tokens with Good Strength.')
                found = 1
            verbout(O, 'Proceeding to calculate ' + color.GREY + 'Shannon Entropy' + color.END + ' of Token audited...')
            entropy = calcEntropy(value)
            verbout(GR, 'Calculating Entropy...')
            verbout(color.BLUE, ' [+] Entropy Calculated: ' + color.CYAN + str(entropy))
            if entropy >= min_entropy:
                verbout(color.ORANGE, ' [+] Anti-CSRF Token Entropy Calculated is ' + color.BY + ' GREATER than 3.0 ' + color.END + '... ')
                print(color.ORANGE + ' [+] Endpoint ' + color.BY + ' PROBABLY NOT VULNERABLE ' + color.END + color.ORANGE + ' to CSRF Attacks...')
                print(color.ORANGE + ' [!] CSRF Mitigation Method: ' + color.BY + ' High Entropy Anti-CSRF Tokens ' + color.END)
                NovulLogger(url, 'High Entropy Anti-CSRF Tokens.')
                found = 1
            else:
                verbout(color.RED, ' [-] Anti-CSRF Token Entropy Calculated is ' + color.BY + ' LESS than 3.0 ' + color.END + '... ')
                print(color.RED + ' [-] Endpoint likely ' + color.BR + ' VULNERABLE ' + color.END + color.RED + ' to CSRF Attacks inspite of CSRF Tokens...')
                print(color.RED + ' [!] Vulnerability Type: ' + color.BR + ' Low Entropy Anti-CSRF Tokens ' + color.END)
                VulnLogger(url, 'Low Entropy Anti-CSRF Tokens.', 'Token: ' + value)

        if found == 0:
            if m_name:
                print(color.RED + '\n +---------+')
                print(color.RED + ' |   PoC   |')
                print(color.RED + ' +---------+\n')
                print(color.BLUE + ' [+] URL : ' + color.CYAN + url)
                print(color.CYAN + ' [+] Name : ' + color.ORANGE + m_name)
                print(color.GREEN + ' [+] Action : ' + color.ORANGE + m_action)
            else:
                print(color.RED + '\n +---------+')
                print(color.RED + ' |   PoC   |')
                print(color.RED + ' +---------+\n')
                print(color.BLUE + ' [+] URL : ' + color.CYAN + url)
                print(color.GREEN + ' [+] Action : ' + color.ORANGE + m_action)
            print(color.ORANGE + ' [+] Query : ' + color.GREY + urllib.parse.urlencode(req))
            print('')
        return (
         _q, para)


def calcEntropy(data):
    """
    This function is used to calculate
              Shannon Entropy.
    """
    if not data:
        return 0
    else:
        entropy = 0
        for x in range(256):
            p_x = float(data.count(chr(x))) / len(data)
            if p_x > 0:
                entropy += -p_x * log(p_x, 2)

        return entropy