# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/util/storage/resolv.py
# Compiled at: 2018-06-20 22:18:48
# Size of source mod 2**32: 2525 bytes
import requests
from requests_file import FileAdapter
from irk.resolvers import ALL_RESOLVER_TYPES
from . import etcfile
CONFIG_DIR = etcfile.EtcConcatDir('sources.list.d')
CACHE_FILE = etcfile.EtcFile('sources')
s = requests.Session()
s.mount('file://', FileAdapter())

def download_temporarily(url):
    resp = s.get(url)
    if resp.status_code != 200:
        print(f"WARN: Failed to get {url}")
        return ''
    else:
        return resp.text


def update_cache():
    print('Updating source lists')
    configs = []
    datas = []
    i = 0
    with CONFIG_DIR.open() as (f):
        while True:
            line = f.readline()
            if line == '':
                break
            if line[0] == '#':
                pass
            else:
                if line.strip() == '':
                    pass
                else:
                    i += 1
                    print(f"Get:{i} {line.strip()}")
                    split = download_temporarily(line.strip()).split('CONFIGLINE\n')
                    configs.append(split[0])
                    datas.append(split[1])
                    config_line = split[0].splitlines(keepends=False)[0]
                    resolver_type = [x for x in ALL_RESOLVER_TYPES if x.get_check_line() == config_line][0]
                    resolver = resolver_type(split[0], split[1])
                    resolver.update_resolver()

    print('Writing cache...', end='')
    with CACHE_FILE.open('w') as (f):
        for c, d in zip(configs, datas):
            f.write(str(len(c)))
            f.write('\n')
            f.write(c)
            f.write(str(len(d)))
            f.write('\n')
            f.write(d)

    print(' done')
    print('Source list updated')


loaded = []
f_seek = 0

def get_matching_resolvers(package):
    global f_seek
    global loaded
    with CACHE_FILE.open('r') as (f):
        for i in loaded:
            if i.provides(package):
                yield i

        while 1:
            c_len = f.readline()
            if c_len == '':
                return
            c_len = int(c_len[:-1])
            c = f.read(c_len)
            config_line = c.splitlines(keepends=False)[0]
            d_len = f.readline()
            d_len = int(d_len[:-1])
            d = f.read(d_len)
            f_seek = f.tell()
            try:
                resolver_type = [x for x in ALL_RESOLVER_TYPES if x.get_check_line() == config_line][0]
            except IndexError:
                print("WARN: Can't interpret type {}".format(config_line))
                continue

            resolver = resolver_type(c, d)
            loaded.append(resolver)
            if resolver.provides(package):
                yield resolver