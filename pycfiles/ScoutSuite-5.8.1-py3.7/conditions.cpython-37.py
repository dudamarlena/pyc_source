# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ScoutSuite/core/conditions.py
# Compiled at: 2020-04-02 05:37:10
# Size of source mod 2**32: 9626 bytes
import datetime, dateutil.parser, json, netaddr, re
from policyuniverse.expander_minimizer import get_actions_from_statement, _expand_wildcard_action
from ScoutSuite.core.console import print_error, print_exception
re_get_value_at = re.compile('_GET_VALUE_AT_\\((.*?)\\)')
re_nested_get_value_at = re.compile('_GET_VALUE_AT_\\(.*')

def pass_conditions(all_info, current_path, conditions, unknown_as_pass_condition=False):
    """
    Check that all conditions are passed for the current path.

    :param all_info:        All of the services' data
    :param current_path:    The value of the `path` variable defined in the finding file
    :param conditions:      The conditions to check as defined in the finding file
    :param unknown_as_pass_condition:   Consider an undetermined condition as passed
    :return:
    """
    from ScoutSuite.providers.base.configs.browser import get_value_at
    if len(conditions) == 0:
        return True
    condition_operator = conditions.pop(0)
    for condition in conditions:
        if condition[0] in ('and', 'or'):
            res = pass_conditions(all_info, current_path, condition, unknown_as_pass_condition)
        else:
            path_to_value, test_name, test_values = condition
            path_to_value = fix_path_string(all_info, current_path, path_to_value)
            target_obj = get_value_at(all_info, current_path, path_to_value)
            if type(test_values) != list:
                dynamic_value = re_get_value_at.match(test_values)
                if dynamic_value:
                    test_values = get_value_at(all_info, current_path, dynamic_value.groups()[0], True)
        try:
            res = pass_condition(target_obj, test_name, test_values)
        except Exception as e:
            try:
                res = True if unknown_as_pass_condition else False
                print_exception("Unable to process testcase '%s' on value '%s', interpreted as %s: %s" % (
                 test_name, str(target_obj), res, e))
            finally:
                e = None
                del e

        if condition_operator == 'and':
            if not res:
                return False
            if condition_operator == 'or' and res:
                return True

    return not condition_operator == 'or'


def pass_condition(b, test, a):
    """
    Generic test function used by Scout
                                        .
    :param b:                           Value to be tested against
    :param test:                        Name of the test case to run
    :param a:                           Value to be tested

    :return:                            True of condition is met, False otherwise
    """
    result = False
    if test == 'equal':
        a = str(a)
        b = str(b)
        result = a == b
    else:
        if test == 'notEqual':
            result = not pass_condition(b, 'equal', a)
        else:
            if test == 'lessThan':
                result = int(b) < int(a)
            else:
                if test == 'lessOrEqual':
                    result = int(b) <= int(a)
                else:
                    if test == 'moreThan':
                        result = int(b) > int(a)
                    else:
                        if test == 'moreOrEqual':
                            result = int(b) >= int(a)
                        else:
                            if test == 'empty':
                                result = type(b) == dict and b == {} or type(b) == list and b == [] or type(b) == list and b == [None]
                            else:
                                if test == 'notEmpty':
                                    result = not pass_condition(b, 'empty', 'a')
                                else:
                                    if test == 'null':
                                        result = b is None or type(b) == str and b == 'None'
                                    else:
                                        if test == 'notNull':
                                            result = not pass_condition(b, 'null', a)
                                        else:
                                            if test == 'true':
                                                result = str(b).lower() == 'true'
                                            else:
                                                if test == 'notTrue' or test == 'false':
                                                    result = str(b).lower() == 'false'
                                                else:
                                                    if test == 'lengthLessThan':
                                                        result = len(b) < int(a)
                                                    else:
                                                        if test == 'lengthMoreThan':
                                                            result = len(b) > int(a)
                                                        else:
                                                            if test == 'lengthEqual':
                                                                result = len(b) == int(a)
                                                            else:
                                                                if test == 'withKey':
                                                                    result = a in b
                                                                else:
                                                                    if test == 'withoutKey':
                                                                        result = a not in b
                                                                    else:
                                                                        if test == 'containString':
                                                                            if not type(b) == str:
                                                                                b = str(b)
                                                                            if not type(a) == str:
                                                                                a = str(a)
                                                                            result = a in b
                                                                        else:
                                                                            if test == 'notContainString':
                                                                                if not type(b) == str:
                                                                                    b = str(b)
                                                                                if not type(a) == str:
                                                                                    a = str(a)
                                                                                result = a not in b
                                                                            else:
                                                                                if test == 'containAtLeastOneOf':
                                                                                    result = False
                                                                                    if not type(b) == list:
                                                                                        b = [
                                                                                         b]
                                                                                    if not type(a) == list:
                                                                                        a = [
                                                                                         a]
                                                                                    for c in b:
                                                                                        if type(c):
                                                                                            c = str(c)
                                                                                        if c in a:
                                                                                            result = True
                                                                                            break

                                                                                else:
                                                                                    if test == 'containAtLeastOneDifferentFrom':
                                                                                        result = False
                                                                                        if not type(b) == list:
                                                                                            b = [
                                                                                             b]
                                                                                        if not type(a) == list:
                                                                                            a = [
                                                                                             a]
                                                                                        for c in b:
                                                                                            if c and c != '' and c not in a:
                                                                                                result = True
                                                                                                break

                                                                                    else:
                                                                                        if test == 'containNoneOf':
                                                                                            result = True
                                                                                            if not type(b) == list:
                                                                                                b = [
                                                                                                 b]
                                                                                            if not type(a) == list:
                                                                                                a = [
                                                                                                 a]
                                                                                            for c in b:
                                                                                                if c in a:
                                                                                                    result = False
                                                                                                    break

                                                                                        else:
                                                                                            if test == 'match':
                                                                                                if type(a) != list:
                                                                                                    a = [
                                                                                                     a]
                                                                                                b = str(b)
                                                                                                for c in a:
                                                                                                    if re.match(c, b):
                                                                                                        result = True
                                                                                                        break

                                                                                            else:
                                                                                                if test == 'notMatch':
                                                                                                    result = not pass_condition(b, 'match', a)
                                                                                                else:
                                                                                                    if test == 'priorToDate':
                                                                                                        b = dateutil.parser.parse(str(b)).replace(tzinfo=None)
                                                                                                        a = dateutil.parser.parse(str(a)).replace(tzinfo=None)
                                                                                                        result = b < a
                                                                                                    else:
                                                                                                        if test == 'olderThan':
                                                                                                            age, threshold = __prepare_age_test(a, b)
                                                                                                            result = age > threshold
                                                                                                        else:
                                                                                                            if test == 'newerThan':
                                                                                                                age, threshold = __prepare_age_test(a, b)
                                                                                                                result = age < threshold
                                                                                                            else:
                                                                                                                if test == 'inSubnets':
                                                                                                                    result = False
                                                                                                                    grant = netaddr.IPNetwork(b)
                                                                                                                    if type(a) != list:
                                                                                                                        a = [
                                                                                                                         a]
                                                                                                                    for c in a:
                                                                                                                        known_subnet = netaddr.IPNetwork(c)
                                                                                                                        if grant in known_subnet:
                                                                                                                            result = True
                                                                                                                            break

                                                                                                                else:
                                                                                                                    if test == 'notInSubnets':
                                                                                                                        result = not pass_condition(b, 'inSubnets', a)
                                                                                                                    else:
                                                                                                                        if test == 'containAction':
                                                                                                                            result = False
                                                                                                                            if type(b) != dict:
                                                                                                                                b = json.loads(b)
                                                                                                                            statement_actions = get_actions_from_statement(b)
                                                                                                                            rule_actions = _expand_wildcard_action(a)
                                                                                                                            for action in rule_actions:
                                                                                                                                if action.lower() in statement_actions:
                                                                                                                                    result = True
                                                                                                                                    break

                                                                                                                        else:
                                                                                                                            if test == 'notContainAction':
                                                                                                                                result = not pass_condition(b, 'containAction', a)
                                                                                                                            else:
                                                                                                                                if test == 'containAtLeastOneAction':
                                                                                                                                    result = False
                                                                                                                                    if type(b) != dict:
                                                                                                                                        b = json.loads(b)
                                                                                                                                    if type(a) != list:
                                                                                                                                        a = [
                                                                                                                                         a]
                                                                                                                                    actions = get_actions_from_statement(b)
                                                                                                                                    for c in a:
                                                                                                                                        if c.lower() in actions:
                                                                                                                                            result = True
                                                                                                                                            break

                                                                                                                                else:
                                                                                                                                    if test == 'isCrossAccount':
                                                                                                                                        result = False
                                                                                                                                        if type(b) != list:
                                                                                                                                            b = [
                                                                                                                                             b]
                                                                                                                                        for c in b:
                                                                                                                                            if c != a:
                                                                                                                                                result = re.match('arn:aws:iam:.*?:%s:.*' % a, c) or True
                                                                                                                                                break

                                                                                                                                    else:
                                                                                                                                        if test == 'isSameAccount':
                                                                                                                                            result = False
                                                                                                                                            if type(b) != list:
                                                                                                                                                b = [
                                                                                                                                                 b]
                                                                                                                                            for c in b:
                                                                                                                                                if not c == a:
                                                                                                                                                    if re.match('arn:aws:iam:.*?:%s:.*' % a, c):
                                                                                                                                                        pass
                                                                                                                                                    result = True
                                                                                                                                                    break

                                                                                                                                        else:
                                                                                                                                            print_error('Error: unknown test case %s' % test)
                                                                                                                                            raise Exception
    return result


def fix_path_string(all_info, current_path, path_to_value):
    from ScoutSuite.providers.base.configs.browser import get_value_at
    while 1:
        dynamic_path = re_get_value_at.findall(path_to_value)
        if len(dynamic_path) == 0:
            break
        for dp in dynamic_path:
            tmp = dp
            while True:
                nested = re_nested_get_value_at.findall(tmp)
                if len(nested) == 0:
                    break
                tmp = nested[0].replace('_GET_VALUE_AT_(', '', 1)

            dv = get_value_at(all_info, current_path, tmp)
            path_to_value = path_to_value.replace('_GET_VALUE_AT_(%s)' % tmp, dv)

    return path_to_value


def __prepare_age_test(a, b):
    if type(a) != list:
        print_error("Error: olderThan requires a list such as [ N , 'days' ] or [ M, 'hours'].")
        raise Exception
    else:
        number = int(a[0])
        unit = a[1]
        if unit not in ('days', 'hours', 'minutes', 'seconds'):
            print_error('Error: only days, hours, minutes, and seconds are supported.')
            raise Exception
        if unit == 'hours':
            number *= 3600
            unit = 'seconds'
        else:
            if unit == 'minutes':
                number *= 60
                unit = 'seconds'
    age = getattr(datetime.datetime.today() - dateutil.parser.parse(str(b)).replace(tzinfo=None), unit)
    return (age, number)