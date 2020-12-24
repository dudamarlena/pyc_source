# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/xsrfprobe/core/logger.py
# Compiled at: 2020-01-29 10:31:04
# Size of source mod 2**32: 2598 bytes
import os
from xsrfprobe.core.colors import *
from xsrfprobe.files.config import *
from xsrfprobe.core.verbout import verbout
from xsrfprobe.files.discovered import INTERNAL_URLS, FILES_EXEC, SCAN_ERRORS
from xsrfprobe.files.discovered import VULN_LIST, FORMS_TESTED, REQUEST_TOKENS, STRENGTH_LIST

def logger(filename, content):
    """
    This module is for logging all the stuff we found
            while crawling and scanning.
    """
    output_file = OUTPUT_DIR + filename + '.log'
    with open(output_file, 'w+', encoding='utf8') as (f):
        if type(content) is tuple or type(content) is list:
            for m in content:
                f.write(m + '\n')

        else:
            f.write(content)
        f.write('\n')


def preqheaders(tup):
    """
    This module prints out the headers as received in the
                    requests normally.
    """
    verbout(GR, 'Receiving headers...\n')
    verbout(color.GREY, '  ' + color.UNDERLINE + 'REQUEST HEADERS' + color.END + color.GREY + ':' + '\n')
    for key, val in tup.items():
        verbout('  ', color.CYAN + key + ': ' + color.ORANGE + val)

    verbout('', '')


def presheaders(tup):
    """
    This module prints out the headers as received in the
                    requests normally.
    """
    verbout(GR, 'Receiving headers...\n')
    verbout(color.GREY, '  ' + color.UNDERLINE + 'RESPONSE HEADERS' + color.END + color.GREY + ':' + '\n')
    for key, val in tup.items():
        verbout('  ', color.CYAN + key + ': ' + color.ORANGE + val)

    verbout('', '')


def GetLogger():
    if INTERNAL_URLS:
        logger('internal-links', INTERNAL_URLS)
    else:
        if SCAN_ERRORS:
            logger('errored', SCAN_ERRORS)
        else:
            if FILES_EXEC:
                logger('files-found', FILES_EXEC)
            else:
                if REQUEST_TOKENS:
                    logger('anti-csrf-tokens', REQUEST_TOKENS)
                if FORMS_TESTED:
                    logger('forms-tested', FORMS_TESTED)
            if VULN_LIST:
                logger('vulnerabilities', VULN_LIST)
        if STRENGTH_LIST:
            logger('strengths', STRENGTH_LIST)


def ErrorLogger(url, error):
    con = '(i) ' + url + ' -> ' + error.__str__()
    SCAN_ERRORS.append(con)


def VulnLogger(url, vuln, content=''):
    tent = '[!] ' + url + ' -> ' + vuln + '\n\n' + str(content) + '\n\n'
    VULN_LIST.append(tent)


def NovulLogger(url, strength):
    tent = '[+] ' + url + ' -> ' + strength
    STRENGTH_LIST.append(tent)