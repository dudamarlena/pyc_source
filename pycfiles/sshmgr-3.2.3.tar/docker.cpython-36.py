# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/bugnofree/DevSpace/sshmgr/src/docker.py
# Compiled at: 2019-04-22 23:30:05
# Size of source mod 2**32: 988 bytes
import re, docker_general

class Docker:

    def __init__(self):
        self._docker = {'general': {'build':self._build_general_docker, 
                     'description':docstr('\n                        > general docker\n                            Features:\n                                - A\n                                - B\n                                    - C\n                    ')}}
        print(self._docker['general']['description'])

    def build(self, docker_type):
        if docker_type == 'general':
            self._build_general_docker()
        else:
            if docker_type == 'nvidia':
                self._build_nvidia_docker()
            else:
                print('[x] Unkonwn docker type!')

    def show_docker_type(self):
        pass

    def _build_nvidia_docker(self):
        pass


if __name__ == '__main__':
    docker = Docker()