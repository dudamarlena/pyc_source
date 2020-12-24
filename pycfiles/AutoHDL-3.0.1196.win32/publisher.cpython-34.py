# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Python34\Lib\site-packages\autohdl\publisher.py
# Compiled at: 2014-08-07 10:29:11
# Size of source mod 2**32: 3346 bytes
import os, re, sys, logging
from io import StringIO
from autohdl import webdav
alog = logging.getLogger(__name__)

def form_message(config):
    if config['hdlManager']['cl']['message']:
        mes = config['hdlManager']['cl']['message']
    else:
        mes = input('Enter some information about firmware: ')
    config['publisher']['message'] = '{comment}; \ntechnology: {technology}; part: {part}; package: {package}; PROM size: {size} kilobytes; '.format(comment=mes, technology=config['hdlManager'].get('technology'), part=config['hdlManager'].get('part'), package=config['hdlManager'].get('package'), size=config['hdlManager'].get('size'))


def scan_for_firmwares(config, patterns):
    files = []
    path = os.path.join(config['hdlManager']['dsn_root'], 'resource')
    for afile in os.listdir(path):
        for pattern in patterns:
            res = re.search(pattern, afile)
            print('search', pattern, afile)
            print(res)
            input('next')
            if res:
                files.append(os.path.join(path, afile))
                continue

    return files


def publish(config):
    config['publisher'] = dict()
    form_message(config)
    config['publisher']['webdave_files'] = []
    root = os.path.join(config['hdlManager']['dsn_root'], 'resource')
    if config['hdlManager'].get('webdav_files'):
        names = config['hdlManager'].get('webdav_files')
        config['publisher']['webdave_files'] = scan_for_firmwares(config, names)
    else:
        names = [
         '{}_{}'.format(config['hdlManager']['dsn_name'], config['hdlManager']['top'])]
        for i in os.listdir(root):
            for k in ['bit', 'mcs']:
                for name in names:
                    res = re.search('{name}_build_(\\d)+_(\\d)+\\.{ext}'.format(name=name, ext=k), i)
                    if res:
                        config['publisher']['webdave_files'].append(os.path.join(root, i))
                        continue

    if config['publisher']['webdave_files']:
        for i in config['publisher']['webdave_files']:
            src = i
            dst = '/'.join(['http:/',
             config['hdlManager']['host'],
             config['hdlManager']['webdavBuildPath'],
             config['hdlManager']['dsn_name'],
             os.path.basename(i)])
            webdav.upload(src, dst)

        src = StringIO()
        src.write('charset=utf-8\n')
        src.write(config['publisher']['message'])
        src.seek(0)
        i = config['publisher']['webdave_files'][0]
        name, _ = os.path.splitext(os.path.basename(i))
        dst = '/'.join(['http:/',
         config['hdlManager']['host'],
         config['hdlManager']['webdavBuildPath'],
         config['hdlManager']['dsn_name'],
         name + '_info'])
        webdav.upload(src.read(), dst, src_type='string')
    else:
        alog.error('No file to publish')