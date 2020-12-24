# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hpppm/bin/hpppm_demand_management.py
# Compiled at: 2012-12-13 05:10:39
import hpppm.field_parser
from hpppm.demand_management import *
if __name__ == '__main__':
    hpdm = DemandManagement()
    fields = hpdm.validate_read_cmdargs(sys.argv)
    tags = hpdm.get_inputs(hpdm.get_current_oper())
    inputs = hpppm.field_parser.parser(fields, tags)
    ret = hpdm.validate_inputs(inputs)
    if 'fields' in tags:
        ret = hpdm.validate_tokens(inputs['fields'])
    req = hpdm.create_request(inputs)
    res = hpdm.post_request(inputs['serviceUrl'][0], req)
    ret = hpdm.extract(res, to_extract=['faultcode', 'faultstring', 'exception:detail', 'id', 'return'])
    print res