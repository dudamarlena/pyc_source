# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-intel/egg/kyoka/domain/domain_validator.py
# Compiled at: 2016-09-17 04:18:17


class DomainValidator:

    def __init__(self, target_domain):
        self.domain = target_domain

    def implementation_check(self):

        def check(method, arg):
            try:
                method(*arg)
            except Exception as e:
                if isinstance(e, NotImplementedError):
                    return e

        method_names = [('generate_inital_state', 0),
         ('is_terminal_state', 1),
         ('transit_state', 2),
         ('generate_possible_actions', 1),
         ('calculate_reward', 1)]
        methods = [ (getattr(self.domain, method_name), range(arg_num)) for method_name, arg_num in method_names
                  ]
        errors = [ check(method, arg) for method, arg in methods ]
        message = ('\n').join([ str(err) for err in errors if err is not None ])
        return (len(errors) == 0, message)