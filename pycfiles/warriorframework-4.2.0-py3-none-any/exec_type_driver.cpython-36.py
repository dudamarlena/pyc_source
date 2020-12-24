# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /data/users/snayak/WARRIOR-4.2.0/warriorframework_py3/warrior/WarriorCore/exec_type_driver.py
# Compiled at: 2020-02-05 00:22:48
# Size of source mod 2**32: 15634 bytes
"""
Copyright 2017, Fujitsu Network Communications, Inc.
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from warrior.Framework.Utils.data_Utils import get_object_from_datarepository, verify_data
from warrior.Framework.Utils.print_Utils import print_error, print_info
from .Classes.argument_datatype_class import ArgumentDatatype
from warrior.Framework.Utils.testcase_Utils import pNote
MATH_OPERATION = {'ge':lambda data_repo_var, exec_cond_var: data_repo_var >= exec_cond_var, 
 'gt':lambda data_repo_var, exec_cond_var: data_repo_var > exec_cond_var, 
 'le':lambda data_repo_var, exec_cond_var: data_repo_var <= exec_cond_var, 
 'lt':lambda data_repo_var, exec_cond_var: data_repo_var < exec_cond_var}

class ElseException(Exception):
    __doc__ = '\n        Raise an exception when a rule fails with individual else action\n    '

    def __init__(self, else_action):
        super(ElseException, self).__init__(else_action)
        self.action = else_action


def math_decision(exec_condition, exec_cond_var, operator):
    """
        Handle the math operator decision
        :param:
            exec_condition: value from data_repo to be compared
            exec_cond_var: user provided value to be compared
            operator: math operator in plain English
        :return:
            True if operator condition match
            for repo value on left and user value on right
            Else False
    """
    operator = operator.lower()
    if operator in MATH_OPERATION:
        return MATH_OPERATION[operator](get_object_from_datarepository(exec_condition), exec_cond_var)
    else:
        pNote('Unknown error occur when deciding value, please check condition value of the step', 'Error')
        return False


def logical_decision(exec_condition, exec_cond_var, operator='eq'):
    """
        Handle the logical decision for the value comparison
        :param:
            exec_condition: value from data_repo to be compared
            exec_cond_var: user provided value to be compared
            operator: math operator in plain English
        :return:
            True if condition match, else return False
    """
    status = True
    result = None
    if type(get_object_from_datarepository(exec_condition)) != type(exec_cond_var):
        pNote('Comparing different type of value, please check the conditional value type', 'ERROR')
        status = False
    else:
        if operator in MATH_OPERATION:
            if not isinstance(exec_condition, int):
                if not isinstance(exec_condition, float):
                    pNote('Comparing non-numerical value using numerical operator,please check value and operator type', 'ERROR')
                    status = False
    if status:
        if operator == 'eq':
            result = True if get_object_from_datarepository(exec_condition) == exec_cond_var else False
    elif status:
        if operator == 'ne':
            result = True if get_object_from_datarepository(exec_condition) != exec_cond_var else False
    elif status:
        if operator in MATH_OPERATION:
            result, _ = verify_data(exec_cond_var, exec_condition, 'float' if exec_condition.startswith('float_') else 'int', operator)
    else:
        pNote('Execution condition failed for expected value: {} , operator: {}, actual value: {}'.format(exec_cond_var, operator, get_object_from_datarepository(exec_condition)), 'WARNING')
    return result


def rule_parser(rule):
    """
        Parse an xml rule element and call logical decision function
        :param:
            rule: xml element for a single rule
        :return:
            status of the rule
    """
    exec_condition = rule.get('Condition', None)
    exec_cond_var = rule.get('Condvalue', None)
    else_action = rule.get('Else', None)
    if else_action is not None:
        if else_action.upper() == 'GOTO':
            else_action = rule.get('Elsevalue')
    support_operators = ['ge', 'gt', 'le',
     'lt', 'eq', 'ne']
    operator = rule.get('Operator', 'eq')
    if operator is not None:
        if operator.lower() not in support_operators:
            pNote('Invaid Operator value, please use the following: {}'.format(support_operators))
            operator = None
    supported_prefix = ['bool_', 'str_', 'int_', 'float_', 'list_', 'tuple_', 'dict_']
    if any([exec_condition.startswith(i) for i in supported_prefix]):
        exec_condition = exec_condition[exec_condition.find('_') + 1:]
    else:
        arg_datatype_object = ArgumentDatatype(exec_condition, exec_cond_var)
        exec_cond_var = arg_datatype_object.convert_arg_to_datatype()
        status = logical_decision(exec_condition, exec_cond_var, operator)
        if status is False and else_action is not None:
            raise ElseException(else_action)
        else:
            return status


def int_split(expression_str):
    """
        split the expression into list of rules and logical symbols/words
        only be used with simple rule, no parenthesis
        :param:
            expression_str: a string of expression ex. 1 & 2 & 3
        :return:
            list of rules and logical symbols/words
            ex. [1, "&", 2, "&", 3]
    """
    elements = expression_str.split()
    for ind, ele in enumerate(elements):
        if str.isdigit(ele):
            elements[ind] = int(ele)

    return elements


def simple_exp_parser(expression_str, rules):
    """
        Parse a expression string which only contains rule numbers and logical symbols/words
        calculate the final status of the expression string
        :param:
            expression_str: a string of simple expression ex. 1 | 2 & 3
            rules: list of rule xml elements
        :return:
            status of the expression
    """
    elements = int_split(expression_str)
    status = None
    if not elements:
        raise Exception('expression_str invalid or not found')
    else:
        if len(elements) == 1:
            status = rule_parser(rules[elements[0]])
        else:
            status = rule_parser(rules[elements[0]])
            for ind in range(0, len(elements) - 2, 2):
                if elements[(ind + 1)].lower() == 'and' or elements[(ind + 1)] == '&':
                    status = status & rule_parser(rules[elements[(ind + 2)]])
                else:
                    if elements[(ind + 1)].lower() == 'or' or elements[(ind + 1)] == '|':
                        status = status | rule_parser(rules[elements[(ind + 2)]])
                    else:
                        raise Exception('invalid operator in expression_str: {}'.format(expression_str))

    return status


def special_exp_parser(expression_str, rules, status_first, status_last):
    """
        Parse a partial expression string which
        1. only contains rule numbers and logical symbols/words
        2. doesn't start and end with a rule
        calculate the final status of the expression string
        :param:
            expression_str: a string of simple expression ex. 1 | 2 & 3
            rules: list of rule xml elements
            status_first: status to be used with the left most logical symbol/word
            status_last: status to be used with the right most logical symbol/word
        :return:
            status of the expression
    """
    status = status_first
    elements = int_split(expression_str)
    if not elements or len(elements) < 3:
        raise Exception('expression_str invalid or not found')
    else:
        for ind in range(0, len(elements) - 1, 2):
            if elements[ind].lower() == 'and' or elements[ind] == '&':
                status = status & rule_parser(rules[elements[(ind + 1)]])
            else:
                if elements[ind].lower() == 'or' or elements[ind] == '|':
                    status = status | rule_parser(rules[elements[(ind + 1)]])
                else:
                    raise Exception('invalid operator in expression_str: {}'.format(expression_str))

        if elements[(-1)].lower() == 'and' or elements[(-1)] == '&':
            status = status & status_last
        else:
            if elements[(-1)].lower() == 'or' or elements[(-1)] == '|':
                status = status | status_last
            else:
                raise Exception('invalid operator in expression_str: {}'.format(expression_str))
    return status


def expression_split(src):
    """
        parse a string and return a list of pair with
        open and close parenthesis
        The result is generated in the order that the inner-most and left-most
        parenthesis will be at the start of the list, which logically should be processed first
        :param:
            src: input string
        :return:
            list of pair contains the index of ( and )
    """
    result = []
    open_index = []
    for ind, _ in enumerate(src):
        if src[ind] == '(':
            open_index.append(ind)
        if src[ind] == ')':
            result.append((open_index.pop(), ind))

    return result


def expression_parser(src, rules):
    """
        parse the expression string and break it up into simple expression
        pass each simple expression into other functions
        combine the results of each pieces and return a final result
        :param:
            src: unparsed expression string
            rules: list of rule xml elements
        :return:
            the status of the parsed expression string
    """
    src = src.strip()
    opening = src.count('(')
    closing = src.count(')')
    if opening != closing:
        raise Exception('expression: {} is invalid'.format(src))
    exps = expression_split(src)
    status = None
    if not exps:
        status = simple_exp_parser(src, rules)
    else:
        if len(exps) == 1:
            status = simple_exp_parser(src[exps[0][0] + 1:exps[0][1]], rules)
            if exps[0][0] != 0:
                status = special_exp_parser(' & ' + src[:exps[0][0] - 1], rules, True, status)
            if exps[0][1] + 1 != len(src):
                status = special_exp_parser(src[exps[0][1] + 1:] + ' & ', rules, status, True)
        else:
            status = simple_exp_parser(src[exps[0][0] + 1:exps[0][1]], rules)
            for x in range(len(exps) - 1):
                if exps[(x + 1)][0] > exps[x][1]:
                    operator = src[exps[x][1] + 1:exps[(x + 1)][0]].strip()
                    if operator.lower() == 'and' or operator == '&':
                        status = status & simple_exp_parser(src[exps[(x + 1)][0] + 1:exps[(x + 1)][1]], rules)
                    else:
                        if operator.lower() == 'or' or operator == '|':
                            status = status | simple_exp_parser(src[exps[(x + 1)][0] + 1:exps[(x + 1)][1]], rules)
                        else:
                            if any([x.isdigit() for x in operator]):
                                status_2 = simple_exp_parser(src[exps[(x + 1)][0] + 1:exps[(x + 1)][1]], rules)
                                status = special_exp_parser(operator, rules, status, status_2)
                            else:
                                raise Exception('invalid operator in expression string: {}'.format(src))
                else:
                    if src[exps[(x + 1)][0] + 1:exps[x][0]].strip() != '':
                        exp_start = exps[(x + 1)][0] + 1
                        exp_end = exps[(x + 1)][0] + 1 + src[exps[(x + 1)][0] + 1:].find('(')
                        status = special_exp_parser(' & ' + src[exp_start:exp_end], rules, True, status)
                    if src[exps[x][1] + 1:exps[(x + 1)][1]].strip() != '':
                        exp_build = src[exps[x][1] + 1:exps[(x + 1)][1]] + ' & '
                        status = special_exp_parser(exp_build, rules, status, True)

    if src[0] != '(':
        status = special_exp_parser(' & ' + src[:src.find('(')], rules, True, status)
    if src[(-1)] != ')':
        status = special_exp_parser(src[src.rfind(')') + 1:] + ' & ', rules, status, True)
    return status


def decision_maker(exec_node):
    """
        return the status, action combo for the step exec node
        :param:
            exec_node: the xml element exectype in the step element
        :return:
            status of the expression
            action to be executed when status is not True
    """
    exec_type = exec_node.get('ExecType', '')
    expression = exec_node.get('Expression', '')
    action = exec_node.get('Else', 'next')
    if exec_node.get('Elsevalue', '') != '':
        action = exec_node.get('Elsevalue')
    rules = exec_node.findall('Rule')
    rules.insert(0, '')
    if expression == '':
        expression = ' & '.join([str(x) for x in range(1, len(rules))])
    try:
        status = expression_parser(expression, rules)
        if exec_type.upper() == 'IF NOT':
            status = not status
    except ElseException as else_action:
        status = False
        if else_action.action is not None:
            action = else_action.action

    return (
     status, action)


def main(step, skip_invoked=True):
    """
        Entry function for execute nodes in a step
        Handle checking and call the logical decision functions
        combine the final result and return
        :param:
            step: the step Element
        :return:
            decision: Whether the step should be executed or not
            trigger_action: When decision failed, what kind of action to perform
    """
    exec_node = step.find('Execute')
    if exec_node is None:
        return (True, None)
    else:
        trigger_action = None
        exec_type = exec_node.get('ExecType', '')
        if exec_type.upper() == 'IF' or exec_type.upper() == 'IF NOT':
            decision, trigger_action = decision_maker(exec_node)
        else:
            if exec_type.upper() == 'NO':
                decision = False
                trigger_action = 'SKIP'
            else:
                if exec_type.upper() == 'YES':
                    decision = True
                else:
                    if exec_type.upper() == 'INVOKED':
                        decision = not skip_invoked
                        trigger_action = 'SKIP_INVOKED'
                    else:
                        decision = False
                        supported_values = ['no', 'yes', 'if', 'if not', 'invoked']
                        print_error('Unsupported value used for ExecType, supported values are:{0} and case-insensitive'.format(supported_values))
        return (
         decision, trigger_action)