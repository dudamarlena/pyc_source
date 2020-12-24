# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sdktool/checkout.py
# Compiled at: 2020-04-01 02:49:00
import os, sys, json, boto3
from util.utils import BasicConfig
from util.Config import *
import pprint

class Checkout(object):

    def __init__(self, version, erp, id, mnt_path='', dst=''):
        self.version = version
        self.id = id
        self.prefix_url = prefix + '/projects/single?projectIdOrPath='
        self.erp = erp
        self.mnt_path = mnt_path
        self.dst = dst

    def get_prefix(self):
        url = self.prefix_url + self.id
        r = BasicConfig.deal_get(url)
        if isinstance(r, int) or r['code'] != '200':
            return r
        group, project = r['data'].get('group_name', ''), r['data'].get('project_name', '')
        return group + '/' + project + '/'

    def checkout(self):
        if self.id.isdigit():
            prefix_path = self.get_prefix()
            project_id = self.id
        else:
            project_id = BasicConfig.path2id(self.id)
        url = prefix + '/projects/' + project_id + '/deploy/checkout?erp=' + self.erp + '&ref=' + self.version
        r = BasicConfig.deal_get(url)
        result = {}
        for item in r['meta']:
            for k, v in item.items():
                try:
                    v = json.loads(v)
                    filepath, cfspath = prefix_path + v.get('filePath'), v.get('cfspath')
                    if filepath and cfspath:
                        result[filepath] = cfspath
                except:
                    pass

        return result

    def checkout_sl(self):
        r = self.checkout()
        dir = ('/').join(self.dst.split('/')[:-1])
        if not os.path.exists(dir):
            os.mkdir(dir)
        for k, v in r.items():
            src, dst = os.path.join(self.mnt_path, v), os.path.join(self.dst, k)
            self.soft_link(src, dst)

    def soft_link(self, src, dst):
        if os.path.islink(dst):
            os.unlink(dst)
        else:
            dir = ('/').join(dst.split('/')[:-1])
            if not os.path.exists(dir):
                os.makedirs(dir)
            os.symlink(src, dst)