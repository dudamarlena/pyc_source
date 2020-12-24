# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/hdfs_kernel/kernels/hdfs/hdfskernel.py
# Compiled at: 2020-01-16 03:10:17
# Size of source mod 2**32: 948 bytes
from hdfs_kernel.constants import LANG_HDFS
from hdfs_kernel.kernels.wrapperkernel.hdfsbase import HdfsKernelBase

class HdfsKernel(HdfsKernelBase):
    banner = 'Hdfs REPL'

    def __init__(self, **kwargs):
        implementation = 'Hdfs'
        implementation_version = '1.0'
        language = 'no-op'
        language_version = '0.1'
        language_info = {'name':'hdfs', 
         'mimetype':'text/x-python', 
         'codemirror_mode':{'name':'python', 
          'version':3}, 
         'pygments_lexer':'python3'}
        (super(HdfsKernel, self).__init__)(implementation, implementation_version, language, language_version, 
         language_info, **kwargs)


if __name__ == '__main__':
    from ipykernel.kernelapp import IPKernelApp
    IPKernelApp.launch_instance(kernel_class=HdfsKernel)