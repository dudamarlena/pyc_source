# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ditio/site.py
# Compiled at: 2018-01-30 14:51:01
import os, re, json, BaseHTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler
from . import system
from . import log

def new(params):
    site_name = params[0]
    system.create_dir(site_name)
    system.create_dir('%s/assets' % site_name)
    system.create_dir('%s/images' % site_name)
    system.create_dir('%s/content' % site_name)
    package_site_dir = '/home/sven/0/_sdks/python/sven-2.7/local/lib/python2.7/site-packages/ditio-0.0.1-py2.7.egg/ditio/site'
    system.copy(package_site_dir, site_name)


def server(params, options):
    site_name = params[0]
    port = int(options['port'])
    server_address = (options['address'], port)
    httpd = BaseHTTPServer.HTTPServer(server_address, SimpleHTTPRequestHandler)
    sa = httpd.socket.getsockname()
    print 'Serving HTTP on', sa[0], 'port', sa[1], '...'
    os.chdir(site_name)
    httpd.serve_forever()


def index(params):
    site_name = params[0]
    property_matcher = re.compile('^([a-z\\-]+\\:.*)$')
    index = []
    for entry in os.listdir('%s/content' % site_name):
        if entry.find('.md') < 0:
            continue
        full_path = '%s/content/%s' % (site_name, entry)
        properties = {}
        with open(full_path) as (f):
            for line in f:
                prop = property_matcher.findall(line)
                if len(prop) < 1:
                    break
                k, v = prop[0].split(':', 1)
                properties[k.strip()] = v.strip()

            limit = 3
            preview_text = ''
            for line in f:
                if line.strip() == '':
                    continue
                if line[0] == '#':
                    continue
                if line.find('.png') > -1:
                    continue
                if line.find('```') > -1:
                    break
                limit = limit - 1
                preview_text = preview_text + ' ' + line.strip()
                if limit == 0:
                    break

        properties.update({'file': entry.replace('.md', '')})
        properties.update({'assets': ' i am the assets  '})
        if 'title' not in properties:
            properties.update({'title': properties['doc-title']})
        properties.update({'preview': preview_text})
        log('* markdown: %s ' % entry)
        index.append(properties)

    with open('%s/content/%s' % (site_name, 'index.json'), 'w') as (f):
        f.write(json.dumps(index))