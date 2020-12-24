# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tuvok/anaconda3/envs/church/lib/python3.6/site-packages/flask_optional_routes/tests/route_branch_manager_tests.py
# Compiled at: 2018-03-04 17:14:51
# Size of source mod 2**32: 558 bytes
from ..optional_routes import OptionalRoutes
from .test_cases import TEST_CASES
if __name__ == '__main__':
    route_branch_manager = OptionalRoutes(None)
    for test_case in TEST_CASES:
        _input = test_case[0]
        _expected_output = test_case[1]
        actual_output = route_branch_manager.generate_optional_routes(_input)
        actual_output = set(actual_output)
        print(_input, _expected_output, actual_output)
        assert actual_output == _expected_output, "Expected Output Doesn't Match Actual"

    print('All Tests Done')