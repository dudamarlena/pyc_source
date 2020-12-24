# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/modules/getemails.py
# Compiled at: 2018-07-01 06:52:30
# Size of source mod 2**32: 1208 bytes
from modules.bcolors import Bcolors
from bs4 import BeautifulSoup

def getMails(soup):
    """
        Searches for <a href> tags for links then checks if link contains the
        substring 'mailto' indicating that it's an email. If it is determined
        to be an email then the link is split and the username is appeneded to
        the list

        Args:
            soup: BeautifulSoup isntance that will be used for parsing

        Returns:
            emails: list of email IDs
    """
    b_colors = Bcolors()
    if isinstance(type(soup), type(BeautifulSoup)):
        emails = []
        links = soup.find_all('a')
        for ref in links:
            url = ref.get('href')
            if url and 'mailto' in url:
                email_addr = url.split(':')
                if len(email_addr) > 1:
                    emails.append(email_addr[1])

        print('')
        print(b_colors.OKGREEN + 'Mails Found - ' + b_colors.ENDC + str(len(emails)))
        print('-------------------------------')
        return emails
    raise 'Method parameter is not of instance BeautifulSoup'