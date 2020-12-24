# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/modules/Checkpost.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 3958 bytes
import re, time, difflib
from urllib.parse import urlencode
from xsrfprobe.core.colors import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.core.logger import VulnLogger
from xsrfprobe.files.config import POC_GENERATION, GEN_MALICIOUS
from xsrfprobe.modules.Generator import GenNormalPoC, GenMalicious

def PostBased(url, r1, r2, r3, m_action, result, genpoc, form, m_name=''):
    """
    This method is for detecting POST-Based Request Forgeries
        on basis of fuzzy string matching and comparison
            based on Ratcliff-Obershelp Algorithm.
    """
    verbout(color.RED, '\n +------------------------------+')
    verbout(color.RED, ' |   POST-Based Forgery Check   |')
    verbout(color.RED, ' +------------------------------+\n')
    verbout(O, 'Matching response query differences...')
    checkdiffx1 = difflib.ndiff(r1.splitlines(1), r2.splitlines(1))
    checkdiffx2 = difflib.ndiff(r1.splitlines(1), r3.splitlines(1))
    result12 = []
    verbout(O, 'Matching results...')
    for n in checkdiffx1:
        if re.match('\\+|-', n):
            result12.append(n)

    result13 = []
    for n in checkdiffx2:
        if re.match('\\+|-', n):
            result13.append(n)

    if len(result12) <= len(result13):
        print(color.GREEN + ' [+] CSRF Vulnerability Detected : ' + color.ORANGE + url + '!')
        print(color.ORANGE + ' [!] Vulnerability Type: ' + color.BR + ' POST-Based Request Forgery ' + color.END)
        VulnLogger(url, 'POST-Based Request Forgery on Forms.', '[i] Form: ' + form.__str__() + '\n[i] POST Query: ' + result.__str__() + '\n')
        time.sleep(0.3)
        verbout(O, 'PoC of response and request...')
        if m_name:
            print(color.RED + '\n +-----------------+')
            print(color.RED + ' |   Request PoC   |')
            print(color.RED + ' +-----------------+\n')
            print(color.BLUE + ' [+] URL : ' + color.CYAN + url)
            print(color.CYAN + ' [+] Name : ' + color.ORANGE + m_name)
            if m_action.count('/') > 1:
                print(color.GREEN + ' [+] Action : ' + color.END + '/' + m_action.rsplit('/', 1)[1])
            else:
                print(color.GREEN + ' [+] Action : ' + color.END + m_action)
        else:
            print(color.RED + '\n +-----------------+')
            print(color.RED + ' |   Request PoC   |')
            print(color.RED + ' +-----------------+\n')
            print(color.BLUE + ' [+] URL : ' + color.CYAN + url)
            if m_action.count('/') > 1:
                print(color.GREEN + ' [+] Action : ' + color.END + '/' + m_action.rsplit('/', 1)[1])
            else:
                print(color.GREEN + ' [+] Action : ' + color.END + m_action)
            print(color.ORANGE + ' [+] POST Query : ' + color.GREY + urlencode(result).strip())
            if POC_GENERATION:
                if GEN_MALICIOUS:
                    GenMalicious(url, genpoc.__str__())
                else:
                    GenNormalPoC(url, genpoc.__str__())