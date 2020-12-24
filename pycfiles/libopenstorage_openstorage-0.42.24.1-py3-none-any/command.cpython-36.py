# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/grpcio-tools/grpc_tools/command.py
# Compiled at: 2020-01-10 16:25:23
# Size of source mod 2**32: 2496 bytes
import os, pkg_resources, sys, setuptools
from grpc_tools import protoc

def build_package_protos(package_root, strict_mode=False):
    proto_files = []
    inclusion_root = os.path.abspath(package_root)
    for root, _, files in os.walk(inclusion_root):
        for filename in files:
            if filename.endswith('.proto'):
                proto_files.append(os.path.abspath(os.path.join(root, filename)))

    well_known_protos_include = pkg_resources.resource_filename('grpc_tools', '_proto')
    for proto_file in proto_files:
        command = [
         'grpc_tools.protoc',
         '--proto_path={}'.format(inclusion_root),
         '--proto_path={}'.format(well_known_protos_include),
         '--python_out={}'.format(inclusion_root),
         '--grpc_python_out={}'.format(inclusion_root)] + [
         proto_file]
        if protoc.main(command) != 0:
            if strict_mode:
                raise Exception('error: {} failed'.format(command))
            else:
                sys.stderr.write('warning: {} failed'.format(command))


class BuildPackageProtos(setuptools.Command):
    __doc__ = 'Command to generate project *_pb2.py modules from proto files.'
    description = 'build grpc protobuf modules'
    user_options = [
     ('strict-mode', 's', 'exit with non-zero value if the proto compiling fails.')]

    def initialize_options(self):
        self.strict_mode = False

    def finalize_options(self):
        pass

    def run(self):
        build_package_protos(self.distribution.package_dir[''], self.strict_mode)