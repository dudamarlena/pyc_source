# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sofc/sofc.py
# Compiled at: 2016-07-26 04:09:26
import urllib, click, requests
from pyquery import PyQuery as pq
STYLE = {'fore': {'black': 30, 
            'red': 31, 
            'green': 32, 
            'yellow': 33, 
            'blue': 34, 
            'purple': 35, 
            'cyan': 36, 
            'white': 37}, 
   'back': {'black': 40, 
            'red': 41, 
            'green': 42, 
            'yellow': 43, 
            'blue': 44, 
            'purple': 45, 
            'cyan': 46, 
            'white': 47}, 
   'mode': {'mormal': 0, 
            'bold': 1, 
            'underline': 4, 
            'blink': 5, 
            'invert': 7, 
            'hide': 8}, 
   'default': {'end': 0}}

def use_style(string, mode='', fore='', back=''):
    mode = '%s' % STYLE['mode'][mode] if mode in STYLE['mode'] else ''
    fore = '%s' % STYLE['fore'][fore] if fore in STYLE['fore'] else ''
    back = '%s' % STYLE['back'][back] if back in STYLE['back'] else ''
    style = (';').join([ s for s in [mode, fore, back] if s ])
    style = '\x1b[%sm' % style if style else ''
    end = '\x1b[%sm' % STYLE['default']['end'] if style else ''
    return '%s%s%s' % (style, string, end)


def get_url(word, page, num, is_tag=False):
    if is_tag == False:
        return 'http://stackoverflow.com/search?page=' + page + '&tab=relevance&pagesize=' + num + '&q=' + urllib.quote_plus(word)
    return 'http://stackoverflow.com/questions/tagged/' + word + '?page=' + page + '&tab=relevance&pagesize=' + num


@click.command()
@click.argument('word', required=True)
@click.option('-p', '--page', default='1', required=False, help='Page: 当前页码')
@click.option('-n', '--num', default='15', required=False, help='page Number: 每页显示条数')
@click.option('-s', '--simple', default='true', required=False, help='Simple: 是否为简单模式，true则只显示标题和URL, 否则显示全部')
@click.option('-t', '--tag', default='false', required=False, help='Tag: 是否为标签模式')
def search(word, page, num, simple, tag):
    print 'searching...'
    is_tag = False if tag == 'false' else True
    url = get_url(word, page, num, is_tag)
    response = requests.get(url)
    d = pq(response.text)
    results = d('div.question-summary')
    print 'len(results) = ' + str(len(results))
    for res in results:
        title = pq('div.result-link span a', res)
        if len(title) < 1:
            title = pq('h3 a', res)[0].text.strip()
            href = pq('h3 a', res)[0].get('href')
        else:
            title = title[0].text.strip()
            href = pq('div.result-link span a', res)[0].get('href')
        print ''
        print use_style(title, back='green', mode='bold')
        href = 'http://stackoverflow.com' + href
        print href
        if simple == 'true':
            continue
        selector = 'span.vote-count-post strong'
        item = pq(selector, res)
        if len(item) == 1:
            vote = item[0].text
        else:
            vote = '0'
        selector = 'div.answered-accepted strong'
        item = pq(selector, res)
        if len(item) == 1:
            answer = item[0].text
        else:
            answer = '0'
        desc = pq('div.excerpt', res).text().strip()
        print use_style('votes = ' + vote + ' answers = ' + answer, back='blue')
        print desc

    print ''
    print 'url: ' + response.url


def main():
    search()


if __name__ == '__main__':
    main()