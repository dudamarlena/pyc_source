# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pytest_resource.py
# Compiled at: 2018-11-14 00:24:01
# Size of source mod 2**32: 471 bytes
import pytest

@pytest.fixture(scope='function')
def resource(request):
    """
    指定されたpathからファイルを読み込む

    @pytest.mark.resource(PATH)
    def test_hoge(resource):
        pass
    """
    resource = request.node.get_closest_marker('resource')
    if resource:
        path = resource.args[0]
        with open(path, 'r') as (f):
            data = f.read()
        return data
    raise ValueError('Resource not found')