# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/quhujun/.pyenv/versions/3.6.0/Python.framework/Versions/3.6/lib/python3.6/site-packages/youtiao/utils/grpc.py
# Compiled at: 2018-05-04 05:37:57
# Size of source mod 2**32: 1064 bytes
from typing import Tuple
from pathlib import Path
from pkg_resources import resource_filename
from grpc_tools import _protoc_compiler

def protoc(proto_path: str, output_path: str) -> Tuple[(Path, Path)]:
    """compile .proto file

    Args:
        proto_path (str): proto file path
        output_path (str): output files directory

    Returns:
        tuple of paths for pb2 python file and pb2 grpc file
    """
    proto_path = str(proto_path)
    output_path = str(output_path)
    if not Path(proto_path).is_file():
        raise FileNotFoundError('proto file not found')
    if not Path(output_path).is_dir():
        raise FileNotFoundError('output dir not found')
    args = [resource_filename('grpc_tools', 'protoc.py'),
     '-I{}'.format(output_path),
     '--python_out={}'.format(output_path),
     '--grpc_python_out={}'.format(output_path),
     proto_path,
     '-I{}'.format(resource_filename('grpc_tools', '_proto'))]
    return _protoc_compiler.run_main([arg.encode() for arg in args])