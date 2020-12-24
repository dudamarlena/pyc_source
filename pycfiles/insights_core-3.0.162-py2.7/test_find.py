# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/tests/test_find.py
# Compiled at: 2019-11-14 13:57:46
import operator
from functools import reduce
from insights import datasource, dr, rule, make_info
from insights.core.spec_factory import DatasourceProvider, find, RegistryPoint, SpecSet

class Specs(SpecSet):
    the_data = RegistryPoint(filterable=True)


class MySpecs(Specs):

    @datasource()
    def the_data(broker):
        data = ('\n        foo bar baz\n        baz bar\n        ').strip()
        return DatasourceProvider(data, 'the_data')


foos = find(Specs.the_data, 'foo')
direct_foos = find(MySpecs.the_data, 'foo')

@rule(foos, direct_foos)
def report(f, d):
    all_foos = reduce(operator.__iadd__, f.values(), [])
    all_direct_foos = reduce(operator.__iadd__, d.values(), [])
    return make_info('FOO', num_all_foos=len(all_foos), num_direct_foos=len(all_direct_foos))


def test_find():
    broker = dr.run(report)
    results = broker[report]
    assert 'num_all_foos' in results
    assert 'num_direct_foos' in results