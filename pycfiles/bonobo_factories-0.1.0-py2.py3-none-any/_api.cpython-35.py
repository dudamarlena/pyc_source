# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/bonobo_docker/_api.py
# Compiled at: 2018-01-01 16:23:40
# Size of source mod 2**32: 1471 bytes
import os
from bonobo.util.api import ApiHelper
__all__ = []
api = ApiHelper(__all__=__all__)

@api.register_graph
def runc(graph, *, plugins=None, services=None, strategy=None, environ=None, shell=False, volumes=None, with_local_packages=False):
    from bonobo_docker.utils import run_docker, get_volumes_args, get_image
    site_volumes = get_volumes_args(with_local_packages=with_local_packages)
    if shell:
        command = '/bin/bash'
    else:
        if graph.file:
            target = os.path.realpath(os.path.join(os.getcwd(), graph.file))
            if os.path.isdir(target):
                site_volumes += ('-v ' + target + ':/home/bonobo/app',)
                command = 'bin/bonobo run --install app'
            else:
                if os.path.isfile(target):
                    site_volumes += ('-v ' + os.path.dirname(target) + ':/home/bonobo/app',)
                    command = 'bin/bonobo run --install app/' + os.path.basename(target)
                else:
                    raise IOError('File does not exist, or is of unsupported type (only directories and regular files are supported).')
        else:
            if graph.mod:
                raise NotImplementedError('Executing a module within a docker container is not yet implemented.')
            else:
                command = '/home/bonobo/bin/python'
    run_docker('run -it --rm', *[
     site_volumes,
     *['-v {}'.format(v) for v in volumes] if volumes else [],
     
      get_image(),
      command])