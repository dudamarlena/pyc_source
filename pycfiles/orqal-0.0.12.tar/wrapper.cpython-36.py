# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scampion/src/tamis/madlab/orqal/orqal/wrapper.py
# Compiled at: 2019-07-12 04:38:17
# Size of source mod 2**32: 950 bytes
from orqal import conf
import os, sys
from orqal.abstract import AbstractWrapper

class Rabin2(AbstractWrapper):
    docker_url = 'madlab:5000/radare2'
    volumes = {'/database': {'bind':'/database',  'mode':'ro'}}
    threads = 1
    memory_in_gb = 1

    def get_cmd(self, params):
        return 'rabin2 -I %s' % self.job.input

    def set_result(self, job):
        r = {l.split()[0].replace('.', '_'):l.split()[1] for l in job.stdout if len(l.split()) == 2 if len(l.split()) == 2}
        job.set_result(r)


if os.path.exists(os.path.expanduser(conf.services)):
    import importlib.util
    spec = importlib.util.spec_from_file_location('services', os.path.expanduser(conf.services))
    services = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(services)
    sys.modules['services'] = services
    from services import *