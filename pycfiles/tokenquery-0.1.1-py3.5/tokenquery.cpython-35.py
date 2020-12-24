# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/tokenquery.py
# Compiled at: 2017-01-30 18:35:40
# Size of source mod 2**32: 18491 bytes
from tokenquery.models.fsa import StateMachine
from tokenquery.models.fsa import State
from tokenquery.models.stack import Stack
from tokenquery.acceptors.core.string_opr import str_eq
from tokenquery.acceptors.core.string_opr import str_reg
from tokenquery.acceptors.core.string_opr import str_len
from tokenquery.acceptors.core.int_opr import *
from tokenquery.acceptors.core.web_opr import *

class TokenQuery:

    def __init__(self, token_query_string, verbose=False):
        self.acceptors = {}
        self.acceptors['str_eq'] = str_eq
        self.acceptors['str_reg'] = str_reg
        self.acceptors['str_len'] = str_len
        self.verbose = verbose
        parsed_token_query_string = self.parse(token_query_string)
        if self.verbose:
            print(parsed_token_query_string)
        self.machine = self.compile(parsed_token_query_string)
        if self.verbose:
            self.machine.print_state_machine()

    def match_tokens(self, input_tokens):
        final_results = []
        last_matched = -1
        for start_point in range(len(input_tokens)):
            if start_point > last_matched:
                sub_input_tokens = input_tokens[start_point:]
                result_set = self.machine.runAll(sub_input_tokens)
                if result_set:
                    final_results += result_set
                    for result_item in result_set:
                        for group_key in result_item:
                            group = result_item[group_key]
                            if len(group) > 0:
                                last_matched_token = group[(-1)].get_token_id()
                                if last_matched_token > last_matched:
                                    last_matched = last_matched_token

        return final_results

    def parse(self, token_query_string):
        """
           Parsing token query string
        """
        parser_stack = Stack()
        parsed = []
        capturing_inside_a_token_mode = False
        capturing_expr_for_token_mode = False
        capture_chunk_id = 1
        capture_mode_name = None
        not_mode = False
        repetition_capture_mode = False
        repetition = 0
        expr_regex_shorthand_mode = False
        expr_string_shorthand_mode = False
        for next_char in token_query_string:
            if self.verbose:
                print('next char : ', next_char)
                print('current stack : ', parser_stack.items)
            if next_char.isspace():
                pass
            elif capturing_inside_a_token_mode:
                if capturing_expr_for_token_mode:
                    pass
            if expr_string_shorthand_mode:
                if next_char == '"':
                    active_operation['type'] = 'str_eq'
                    active_operation['opr_input'] = capturer
                    expr_string_shorthand_mode = False
                    capturer = ''
                    parser_stack.push(active_operation)
                    capturing_expr_for_token_mode = False
                    continue
                else:
                    capturer += next_char
            else:
                if expr_regex_shorthand_mode:
                    if next_char == '/':
                        active_operation['type'] = 'str_reg'
                        active_operation['opr_input'] = capturer
                        expr_regex_shorthand_mode = False
                        capturer = ''
                        parser_stack.push(active_operation)
                        capturing_expr_for_token_mode = False
                        continue
                    else:
                        capturer += next_char
                elif capturer == '"':
                    capturer = next_char
                    expr_string_shorthand_mode = True
                    continue
            if capturer == '/':
                capturer = next_char
                expr_regex_shorthand_mode = True
                continue
                if next_char == ':':
                    active_operation['label'] = capturer
                    capturer = ''
                else:
                    if next_char == '(':
                        active_operation['type'] = capturer
                        capturer = ''
                    else:
                        if next_char == ')':
                            if capturer:
                                active_operation['opr_input'] = capturer
                            if not_mode:
                                negated_operation = {'opr1': active_operation, 
                                 'type': 'comp_not'}
                                not_mode = False
                                parser_stack.push(negated_operation)
                            else:
                                parser_stack.push(active_operation)
                            capturing_expr_for_token_mode = False
                        else:
                            capturer += next_char
            else:
                if next_char == '(':
                    parser_stack.push('(')
                else:
                    if next_char == '&':
                        parser_stack.push('&')
                    else:
                        if next_char == '|':
                            parser_stack.push('|')
                        else:
                            if next_char == '!':
                                not_mode = True
                            else:
                                if next_char == ')':
                                    while parser_stack.size() > 2:
                                        item2 = parser_stack.pop()
                                        op = parser_stack.pop()
                                        item1 = parser_stack.pop()
                                        if op == '&':
                                            new_acceptor = {'opr1': item1, 
                                             'opr2': item2, 
                                             'type': 'comp_and'}
                                        if op == '|':
                                            new_acceptor = {'opr1': item1, 
                                             'opr2': item2, 
                                             'type': 'comp_or'}
                                        if parser_stack.size() == 0:
                                            parser_stack.push(new_acceptor)
                                            break
                                        if parser_stack.peek() == '(':
                                            parser_stack.pop()
                                            parser_stack.push(new_acceptor)
                                            break
                                        parser_stack.push(new_acceptor)

                                    if parser_stack.size() != 1:
                                        raise ValueError('Parssing error! parser stack: {} .'.format(parser_stack))
                                    if next_char == ']':
                                        parsed.append({'type': 'segment', 'value': active_operation})
                                        capturing_inside_a_token_mode = False
                                        capturer = ''
                                        continue
                                    else:
                                        if next_char == ']':
                                            while parser_stack.size() > 2:
                                                item2 = parser_stack.pop()
                                                op = parser_stack.pop()
                                                item1 = parser_stack.pop()
                                                if op == '&':
                                                    new_acceptor = {'opr1': item1, 
                                                     'opr2': item2, 
                                                     'type': 'comp_and'}
                                                if op == '|':
                                                    new_acceptor = {'opr1': item1, 
                                                     'opr2': item2, 
                                                     'type': 'comp_or'}
                                                if parser_stack.size() == 0:
                                                    parser_stack.push(new_acceptor)
                                                    break
                                                if parser_stack.peek() == '(':
                                                    parser_stack.pop()
                                                    parser_stack.push(new_acceptor)
                                                    break
                                                parser_stack.push(new_acceptor)

                                            if parser_stack.size() != 1:
                                                raise ValueError('Parssing error! parser stack: {} .'.format(parser_stack))
                                            active_operation = parser_stack.pop()
                                            parsed.append({'type': 'segment', 'value': active_operation})
                                            capturing_inside_a_token_mode = False
                                            capturer = ''
                                            continue
                                        else:
                                            capturer = next_char
                                    active_operation = {'type': '', 'label': 'text'}
                                    capturing_expr_for_token_mode = True
                                elif repetition_capture_mode:
                                    pass
            if next_char == '}':
                if start_repetition:
                    parsed.append({'type': 'repetition_range', 'start': start_repetition, 'end': repetition})
                else:
                    parsed.append({'type': 'repetition', 'value': repetition})
                repetition = 0
                start_repetition = None
                repetition_capture_mode = False
            else:
                if next_char.isdigit():
                    repetition = repetition * 10 + int(next_char)
                else:
                    if next_char == ',':
                        start_repetition = repetition
                        repetition = 0
                    else:
                        raise ValueError('Parser is not able to parse {} beacuse of invalid repetition char {} .'.format(token_query_string, char))
                        continue
                        if capture_mode_name != None:
                            if next_char in ('(', ' ', '['):
                                if capture_mode_name:
                                    name = capture_mode_name
                                else:
                                    name = 'chunk ' + str(capture_chunk_id)
                                capture_chunk_id += 1
                                parsed.append({'type': 'capture', 'value': 'On', 'name': name})
                                capture_mode_name = None
                            else:
                                capture_mode_name += next_char
                                continue
                            if next_char == '*':
                                parsed.append({'type': 'repetition', 'value': '*'})
                            if next_char == '?':
                                parsed.append({'type': 'repetition', 'value': '?'})
                            if next_char == '+':
                                parsed.append({'type': 'repetition', 'value': '+'})
                            if next_char == '{':
                                repetition = 0
                                start_repetition = None
                                repetition_capture_mode = True
                            if next_char == '(':
                                capture_mode_name = ''
                            if next_char == ')':
                                parsed.append({'type': 'capture', 'value': 'Off'})
                                capture_mode_name = None
                            if next_char == '[':
                                parser_stack = Stack()
                                capturing_inside_a_token_mode = True
                                continue

        return parsed

    def compile(self, parsed_token_regex):
        capture_name = None
        no_capture_at_all = True
        previous_connection = False
        start_state = State('start', capture_name, self.acceptors)
        states = [start_state]
        current_state = start_state
        prev_state = None
        prev_segment = None
        state_counter = 1
        for item in parsed_token_regex:
            if item['type'] == 'segment':
                next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                states.append(next_state)
                state_counter += 1
                current_state.add_a_next(item['value'], next_state)
                if previous_connection:
                    prev_state.add_a_next(item['value'], next_state)
                    previous_connection = False
                prev_state = current_state
                current_state = next_state
                prev_segment = item['value']
            else:
                if item['type'] == 'capture':
                    if item['value'] == 'On':
                        capture_name = item['name']
                        if len(states) == 1:
                            states[0].capture_name = capture_name
                        no_capture_at_all = False
                    else:
                        capture_name = None
                else:
                    if item['type'] == 'repetition':
                        if item['value'] == '*':
                            current_state.add_a_next(prev_segment, current_state)
                            previous_connection = True
                        else:
                            if item['value'] == '?':
                                previous_connection = True
                            else:
                                if item['value'] == '+':
                                    current_state.add_a_next(prev_segment, current_state)
                                elif item['value'] and item['value'] > 1:
                                    for i in range(item['value'] - 1):
                                        next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                                        states.append(next_state)
                                        state_counter += 1
                                        current_state.add_a_next(prev_segment, next_state)
                                        prev_state = current_state
                                        current_state = next_state

                    elif item['type'] == 'repetition_range':
                        source_state = prev_state
                        if item['end'] - item['start'] > 0:
                            for i in range(item['end'] - item['start']):
                                next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                                states.append(next_state)
                                state_counter += 1
                                current_state.add_a_next(prev_segment, next_state)
                                source_state.add_a_next(prev_segment, next_state)
                                prev_state = current_state
                                current_state = next_state

                        if item['start'] > 1:
                            for i in range(item['start'] - 1):
                                next_state = State('state ' + str(state_counter), capture_name, self.acceptors)
                                states.append(next_state)
                                state_counter += 1
                                current_state.add_a_next(prev_segment, next_state)
                                prev_state = current_state
                                current_state = next_state

        last_state = State('end', capture_name, self.acceptors, True)
        any_rule = {'type': 'str_reg', 
         'label': 'text', 
         'opr_input': '.*|[\r\n]+'}
        current_state.add_a_next(any_rule, last_state)
        states.append(last_state)
        if no_capture_at_all:
            for state in states:
                state.capture_name = 'chunk 1'

        return StateMachine(start_state, states)