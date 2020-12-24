# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\dev\scrapgo\scrapgo\utils\fileutils.py
# Compiled at: 2019-07-07 15:19:35
# Size of source mod 2**32: 822 bytes
import os, json, configparser

def mkdir_p(path):
    if not os.path.isdir(path):
        os.makedirs(path, exist_ok=True)


def cp(content, path, overwrite=True):
    if not overwrite:
        if os.path.exists(path):
            return
    with open(path, 'wb') as (fp):
        fp.write(content)


def read_json(path):
    with open(path, encoding='utf-8') as (fp):
        return json.loads(fp.read())


def read_conf(path, header=None):
    conf = configparser.ConfigParser()
    conf.read(path)
    if header:
        return conf[header]
    return conf


def parse_jsonp(jsonp, **kwargs):
    js = jsonp[jsonp.index('(') + 1:jsonp.rindex(')')]
    return (json.loads)(js, **kwargs)


def get_file_extension(path):
    fn, ext = os.path.splitext(path)
    return ext