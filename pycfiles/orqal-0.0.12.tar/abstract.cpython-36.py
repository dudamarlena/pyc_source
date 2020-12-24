# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/scampion/src/tamis/madlab/orqal/orqal/abstract.py
# Compiled at: 2019-07-09 10:56:28
# Size of source mod 2**32: 1982 bytes
import json, logging, conf, os

class AbstractWrapper:
    docker_url = None
    volumes = None
    volumes = {'/scratch':{'bind':'/scratch',  'mode':'rw'},  '/database':{'bind':'/database', 
      'mode':'ro'}}
    threads = None
    memory_in_gb = None
    create_dir = False

    def __init__(self, job):
        self.log = logging.getLogger(str(self.__class__))
        self.job = job
        if self.create_dir:
            if not os.path.exists(self.job.wd):
                self.setup_dir()

    def setup_dir(self):
        os.mkdir(self.job.wd, 511)
        os.chmod(self.job.wd, 511)
        with open(os.path.join(self.job.wd, 'params.json'), 'w') as (f):
            json.dump(self.job.params, f)

    def run(self, docker, tag='latest'):
        client = docker['docker']
        self.log.debug('Pull image %s', self.docker_url)
        client.images.pull((self.docker_url), tag, auth_config=(conf.registry_auth_config))
        mem_limit = int(self.memory_in_gb * 1000000000 if self.memory_in_gb else client.info()['MemTotal'])
        cpu_count = self.threads if self.threads else client.info()['NCPU']
        cmd = self.get_cmd(self.job.params.get('app', None))
        self.job.host = client.api.base_url
        self.job.image = self.docker_url + ':' + tag
        self.job.cmd = cmd
        self.job.save()
        self.log.debug(cmd)
        name = '%s_%s' % (self.docker_url.split('/')[(-1)], self.job._id)
        self.job.run(docker['api'], client.containers.run((self.docker_url + ':' + tag), cmd,
          mem_limit=mem_limit, cpu_count=cpu_count, volumes=(self.volumes),
          working_dir=(self.job.wd),
          detach=True,
          auto_remove=False,
          name=name))
        self.set_result(self.job)