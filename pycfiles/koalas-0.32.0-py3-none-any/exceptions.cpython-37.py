# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./build/lib/databricks/koalas/exceptions.py
# Compiled at: 2019-10-03 20:45:45
# Size of source mod 2**32: 3741 bytes
"""
Exceptions/Errors used in Koalas.
"""

class SparkPandasIndexingError(Exception):
    pass


def code_change_hint(pandas_function, spark_target_function):
    if pandas_function is not None:
        if spark_target_function is not None:
            return 'You are trying to use pandas function {}, use spark function {}'.format(pandas_function, spark_target_function)
    else:
        if pandas_function is not None:
            if spark_target_function is None:
                return 'You are trying to use pandas function {}, checkout the spark user guide to find a relevant function'.format(pandas_function)
        if pandas_function is None and spark_target_function is not None:
            return 'Use spark function {}'.format(spark_target_function)
    return 'Checkout the spark user guide to find a relevant function'


class SparkPandasNotImplementedError(NotImplementedError):

    def __init__(self, pandas_function=None, spark_target_function=None, description=''):
        self.pandas_source = pandas_function
        self.spark_target = spark_target_function
        hint = code_change_hint(pandas_function, spark_target_function)
        if len(description) > 0:
            description += ' ' + hint
        else:
            description = hint
        super(SparkPandasNotImplementedError, self).__init__(description)


class PandasNotImplementedError(NotImplementedError):

    def __init__(self, class_name, method_name=None, arg_name=None, property_name=None, deprecated=False, reason=''):
        if not (method_name is None) != (property_name is None):
            raise AssertionError
        else:
            self.class_name = class_name
            self.method_name = method_name
            self.arg_name = arg_name
            if method_name is not None:
                if arg_name is not None:
                    msg = 'The method `{0}.{1}()` does not support `{2}` parameter. {3}'.format(class_name, method_name, arg_name, reason)
                elif deprecated:
                    msg = 'The method `{0}.{1}()` is deprecated in pandas and will therefore not be supported in Koalas. {2}'.format(class_name, method_name, reason)
                else:
                    if reason == '':
                        reason = ' yet.'
                    else:
                        reason = '. ' + reason
                    msg = 'The method `{0}.{1}()` is not implemented{2}'.format(class_name, method_name, reason)
            elif deprecated:
                msg = 'The property `{0}.{1}()` is deprecated in pandas and will therefore not be supported in Koalas. {2}'.format(class_name, property_name, reason)
            else:
                if reason == '':
                    reason = ' yet.'
                else:
                    reason = '. ' + reason
                msg = 'The property `{0}.{1}()` is not implemented{2}'.format(class_name, property_name, reason)
        super(NotImplementedError, self).__init__(msg)