# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil_lib/test/test_programs.py
# Compiled at: 2017-05-10 17:49:05
import os

def test_docker_call(tmpdir):
    from toil_lib.programs import docker_call
    work_dir = str(tmpdir)
    parameter = ['--help']
    tool = 'quay.io/ucsc_cgl/samtools'
    docker_call(work_dir=work_dir, parameters=parameter, tool=tool)
    fpath = os.path.join(work_dir, 'test')
    with open(fpath, 'w') as (f):
        docker_call(tool='ubuntu', env=dict(foo='bar'), parameters=['printenv', 'foo'], outfile=f)
    assert open(fpath).read() == 'bar\n'