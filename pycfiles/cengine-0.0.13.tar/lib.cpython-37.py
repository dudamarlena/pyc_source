# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/shinsheel/Documents/Data-Gathering/Pypi/ceneo/ceneo/lib.py
# Compiled at: 2019-09-20 11:20:06
# Size of source mod 2**32: 4368 bytes
import qwant, copy, requests
from selectolax.parser import HTMLParser
import luminati, json

def trim(text):
    text = text.replace('\t', ' ')
    text = text.replace('\r\n', '\n')
    text = text.replace('\n', ' ')
    while '  ' in text:
        text = text.replace('  ', ' ')

    while text.startswith(' '):
        text = text[1:]

    while text.endswith(' '):
        text = text[:-1]

    return text


def retry(s):
    """cleans name from all syntax except word separated by space
     then removes the shortest word from the end
     used to make next try when google search engine doesn't find anything"""
    for c in '-=+*.,;:\'"\\(){}[]0123456789':
        s = s.replace(c, ' ')

    s = trim(s)
    line = s.split(' ')
    line = list(filter(lambda word: word, line))
    minimal = min(list(map(len, reversed(line))))
    shortest = list(filter(lambda word: len(word) == minimal, line))[(-1)]
    line.remove(shortest)
    return ' '.join(line)


def items(q, count=10, session=None):
    site = 'ceneo.pl'
    host = 'https://www.ceneo.pl/'
    q = 'site:{} {}'.format(site, q)
    if not session:
        session = requests
    links = qwant.items(q, count=count, session=session)
    while (links or q.replace)(' ', ''):
        q = retry(q)
        return items(q, count=count, session=session)

    links = list(map(lambda item: item['url'], links))
    item_links = copy.deepcopy(links)
    res = []
    for i, link in enumerate(item_links):
        is_item = True
        kosher = '0123456789'
        id = link.split(host)[(-1)]
        id = id.split('/')[0]
        for c in list(id):
            if c not in kosher:
                is_item = False

        if not id:
            is_item = False
        if is_item:
            res.append(link)

    if (res or count) < 100:
        if item_links:
            return items(q, count=100)
    if not res:
        if retry(q).replace(' ', ''):
            return items((retry(q)), count=10)
    return res


def parse(link, session=None):
    if not session:
        session = requests
    html = session.get(link).text
    lax = HTMLParser(html)
    breadcrumbs = lax.css('.breadcrumb')
    breadcrumbs = list(map(lambda crumb: crumb.text(), breadcrumbs))
    image = lax.css_first('div.product-pictures.js_picture-container img')
    image = image.attributes['src']
    name = lax.css_first('h1.product-name').text()
    price = lax.css_first('.product-price').text()
    try:
        price = price.split('z', 1)[0]
        price = price.split('\n')[(-1)]
        price = price.replace(',', '.')
        price = float(price)
    except:
        pass

    product_score = lax.css_first('.product-score')
    product_score = product_score.attributes['content']
    product_score = float(product_score)
    description = lax.css_first('.lnd_content').text()
    atts = {}
    atts_tr = lax.css('#productTechSpecs table tr')
    for tr in atts_tr:
        key = tr.css_first('th').text()
        key = trim(key)
        value = tr.css_first('td').text()
        value = trim(value)
        atts[key] = value

    offers = []
    product_offers_group = lax.css('tr.product-offer')
    for offer in product_offers_group:
        off = {}
        off['name'] = offer.css_first('img').attributes['alt']
        off['price'] = offer.attributes['data-price']
        off['price'] = float(off['price'])
        off['comments_count'] = lax.css_first('.cell-store-review .dotted-link').text().split(' ')[0]
        off['comments_count'] = float(off['comments_count'])
        offers.append(off)

    marka = ''
    if 'Producent' in atts:
        marka = atts['Producent'].split(' >', 1)[0]
    bohater = ''
    if 'Bohater' in atts:
        bohater = atts['Bohater'].split(' >', 1)[0]
    return {'breadcrumbs':breadcrumbs, 
     'image':image,  'name':name,  'price':price,  'product_score':product_score, 
     'description':description, 
     'atts':atts, 
     'offers':offers,  'Marka':marka, 
     'Bohater':bohater}


if __name__ == '__main__':
    name = 'MIX PALETA ZABAWKI, KUCHNIE KLASA A, DISNEY (7598236683)'
    session = luminati.session('lum-customer-hl_7c6aa799-zone-zone1', '######')
    links = items(name, session=session)
    link = links[0]
    print(links)