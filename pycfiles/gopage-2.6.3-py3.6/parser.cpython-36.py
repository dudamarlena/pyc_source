# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/gopage/parser.py
# Compiled at: 2017-03-22 02:52:25
# Size of source mod 2**32: 1712 bytes
import bs4
from pprint import pprint
import util

@util.cache('json')
def parse(gpage):

    def parse_snippet(snippet):
        title = snippet.h3.a.contents[0]
        content = ''.join(snippet.find('span', class_='st').strings)
        return {'title':title, 
         'content':content}

    soup = bs4.BeautifulSoup(gpage, 'html.parser')
    snippets = soup.find_all('div', class_='rc')
    snippets = [parse_snippet(s) for s in snippets]
    nsnippets = len(snippets)
    for i in range(nsnippets):
        snippets[i]['pos'] = i + 1

    return snippets


def filt_email(snippets):

    def efilter(snippet):
        import re
        emails = []
        rough_pattern = re.compile('[a-z0-9-\\._]+(@| at | \\[at\\] |\\[at\\]| \\(at\\) |\\(at\\)| @ )(([a-z0-9\\-]+)(\\.| dot | \\. | \\[dot\\] ))+([a-z]+)')
        rough_match = rough_pattern.finditer(snippet['content'])
        for rm in rough_match:
            pattern = re.compile('(([a-z0-9-_]+)(\\.| dot | \\. )?)+(@| at | \\[at\\] |\\[at\\]| \\(at\\) |\\(at\\)| @ )(([a-z0-9\\-]+)(\\.| dot | \\. | \\[dot\\] ))+([a-z]+)')
            match = pattern.finditer(rm.group())
            for m in match:
                emails.append(m.group().replace(' dot ', '.').replace(' at ', '@').replace('[at]', '@').replace('(at)', '@').replace(' ', ''))

        snippet['emails'] = emails
        return snippet

    snippets = [efilter(s) for s in snippets]
    snippets = [s for s in snippets if s['emails']]
    return snippets


if __name__ == '__main__':
    with open('jietang.html', encoding='utf-8') as (f):
        gpage = f.read()
    items = parse(gpage)
    pprint(items)
    print(filt_email(items))