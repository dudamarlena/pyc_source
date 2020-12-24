# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fedservice/op/signing_service.py
# Compiled at: 2019-11-15 14:41:29
# Size of source mod 2**32: 959 bytes
import os
from oidcendpoint.util import importer

class SigningService:

    def __init__(self, conf, cwd=''):
        self.issuer = {}
        self.wd = cwd
        for attr, spec in conf.items():
            self.issuer[attr] = self.build_signing_service(spec)

    def build_signing_service(self, spec):
        spec['kwargs']['base_path'] = os.path.join(self.wd, spec['kwargs']['base_path'])
        if isinstance(spec['class'], str):
            _instance = (importer(spec['class']))(**spec['kwargs'])
        else:
            _instance = (spec['class'])(**spec['kwargs'])
        return _instance