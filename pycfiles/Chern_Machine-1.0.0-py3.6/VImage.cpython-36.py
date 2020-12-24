# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ChernMachine/kernel/VImage.py
# Compiled at: 2018-06-06 05:58:57
# Size of source mod 2**32: 3831 bytes
import json, os, sys, subprocess
from Chern.utils import csys
from Chern.utils import metadata
from ChernMachine.kernel.VJob import VJob

class VImage(VJob):

    def __init__(self, file_name):
        super(VImage, self).__init__(file_name)

    def inspect(self):
        ps = subprocess.Popen(('docker inspect {0}'.format(self.image_id().decode())), shell=True, stdout=(subprocess.PIPE))
        info = ps.communicate()
        json_info = json.loads(info[0])
        return json_info[0]

    def is_locked(self):
        status_file = metadata.ConfigFile(os.path.join(self.path, 'status.json'))
        status = status_file.read_variable('status')
        return status == 'locked'

    def status(self):
        dirs = csys.list_dir(self.path)
        for run in dirs:
            if run.startswith('run.'):
                config_file = metadata.ConfigFile(os.path.join(self.path, run, 'status.json'))
                status = config_file.read_variable('status', 'submitted')
                print('status is ', status, file=(sys.stderr))
                if status != 'submitted':
                    return status

        if self.is_locked():
            return 'locked'
        else:
            return 'submitted'
            return status

    def image_id(self):
        dirs = csys.list_dir(self.path)
        for run in dirs:
            if run.startswith('run.'):
                config_file = metadata.ConfigFile(os.path.join(self.path, run, 'status.json'))
                status = config_file.read_variable('status', 'submitted')
                if status == 'built':
                    return config_file.read_variable('image_id')

        return ''

    def machine_storage(self):
        config_file = metadata.ConfigFile(os.path.join(os.environ['HOME'], '.ChernMachine/config.json'))
        machine_id = config_file.read_variable('machine_id')
        return 'run.' + machine_id

    def execute(self):
        run_path = os.path.join(self.path, self.machine_storage())
        csys.copy_tree(os.path.join(self.path, 'contents'), run_path)
        status_file = metadata.ConfigFile(os.path.join(run_path, 'status.json'))
        status_file.write_variable('status', 'building')
        entrypoint = open(os.path.join(run_path, 'entrypoint.sh'), 'w')
        entrypoint.write('#!/bin/bash\n$@\n')
        entrypoint.close()
        try:
            self.build()
        except Exception as e:
            self.append_error('Fail to build the image!\n' + str(e))
            status_file.write_variable('status', 'failed')
            raise e

        status_file.write_variable('status', 'built')

    def satisfied(self):
        return True

    def build(self):
        """
        Build the image to change the status of the Algorithm to builded.
        It will create a unique VImage object and the md5 of the VImage will be saved.
        """
        run_path = os.path.join(self.path, self.machine_storage())
        os.chdir(run_path)
        ps = subprocess.Popen('docker build .', shell=True, stdout=(subprocess.PIPE),
          stderr=(subprocess.PIPE))
        ps.wait()
        if ps.poll() != 0:
            raise Exception(ps.stderr.read().decode())
        info = ps.communicate()[0]
        image_id = info.split()[(-1)]
        status_file = metadata.ConfigFile(os.path.join(run_path, 'status.json'))
        status_file.write_variable('image_id', image_id.decode())