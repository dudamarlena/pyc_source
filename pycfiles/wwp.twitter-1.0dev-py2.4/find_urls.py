# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/wwp/twitter/browser/find_urls.py
# Compiled at: 2009-07-31 09:32:27
import re

def fix_urls(text):
    pat_url = re.compile('(?x) (((\\s((http|ftp|https)://(\\S*)\\.)|((http|ftp|https)://))\\S+\\.\\S+)|((\\S+)\\.(\\S+)\\.(\\S+))) ')
    pat_email = re.compile('(?x) ((\\S+)@(\\S+)\\.(\\S+))')
    for url in re.findall(pat_url, text):
        if url[0].startswith('http'):
            text = text.replace(url[0], '<a href="%(url)s">%(url)s</a>' % {'url': url[0]})
        else:
            text = text.replace(url[0], '<a href="http://%(url)s">%(url)s</a>' % {'url': url[0]})

    for email in re.findall(pat_email, text):
        text = your_string.replace(email[1], '<a href="mailto:%(email)s">%(email)s</a>' % {'email': email[1]})

    return text


if __name__ == '__main__':
    print fix_urls('test http://google.com asdasdasd some more text')