# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /c/Users/Lee/Sync/projects/django-danceschool/currentmaster/django-danceschool/danceschool/core/utils/emails.py
# Compiled at: 2019-04-03 22:56:29
# Size of source mod 2**32: 1039 bytes
from bs4 import BeautifulSoup

def get_text_for_html(html_content):
    """
    Take the HTML content (from, for example, an email)
    and construct a simple plain text version of that content
    (for example, for inclusion in a multipart email message).
    """
    soup = BeautifulSoup(html_content)
    for script in soup(['script', 'style']):
        script.extract()

    for a in soup.findAll('a', href=True):
        a.replaceWith('%s <%s>' % (a.string, a.get('href')))

    text = soup.get_text()
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split('  '))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text