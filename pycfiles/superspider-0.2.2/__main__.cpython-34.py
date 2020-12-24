# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\calder\Documents\GitHub\superspider\superspider\__main__.py
# Compiled at: 2017-03-18 13:22:41
# Size of source mod 2**32: 892 bytes
if __name__ == '__main__':
    from superspider import scraper
    import sys, datetime
    from jinja2 import Template
    args = sys.argv[1:]
    prefix = sys.argv[0].replace(__name__ + '.py', '')
    if len(args) < 1:
        print('No website was specified.')
    else:
        myTitle = args[0].replace('https://', '').replace('http://', '')
        myTitle = myTitle[:myTitle.find('/')].split('.')[0] + "'s Summary Data"
        myTitle = myTitle[0].upper() + myTitle[1:]
        x = scraper.scrape(args[0], silent=True)
        t = Template(open(prefix + 'template.html', 'r').read())
        for p in range(len(x['data'])):
            x['data'][p][0] = ','.join(x['data'][p][0])
            x['data'][p][1] = x['data'][p][1]

        z = {}
        for a, b in x['data']:
            z[a] = b

        with open('yourdata.html', 'wb') as (w):
            xs = t.render(content=z, title=myTitle, time=str(datetime.datetime.now()), url=args[0], Stype=x['type'])
            w.write(xs.encode('utf-8'))