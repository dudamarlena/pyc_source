# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shakespearelang/shakespeare_interpreter.py
# Compiled at: 2019-02-05 20:44:39
# Size of source mod 2**32: 16240 bytes
"""
Shakespeare -- An interpreter for the Shakespeare Programming Language
"""
from .shakespeare_parser import shakespeareParser
import argparse, math

class Shakespeare:
    __doc__ = '\n    Interpreter for the Shakespeare Programming Language.\n\n    Methods:\n    run_play -- Run an SPL play\n    play_over -- Return whether play has completed\n    step_forward -- Run the next event in the play\n    next_event_text -- Return the text of the next event\n    run_event -- Run a specified event in-place\n    run_sentence -- Run a specified sentence in-place\n    evaluate_question -- Return the boolean answer to a question\n    evaluate_expression -- Return the numeric value of an expression\n    run_dramatis_personae -- Run a dramatis personae, overwriting or adding to\n                             the characters of the play\n    run_dramatis_persona -- Run a dramatis persona, adding to the characters of\n                            the play\n    '

    def __init__(self):
        self.parser = shakespeareParser(parseinfo=True)
        self.characters = []
        self.global_boolean = False
        self.ast = None
        self.current_position = None
        self._input_buffer = ''

    class Character:
        __doc__ = 'A character in an SPL play.'

        def __init__(self, name):
            self.value = 0
            self.stack = []
            self.on_stage = False
            self.name = name

        def push(self, newValue):
            """Push a value onto the character's stack."""
            self.stack.append(newValue)

        def pop(self):
            """Pop a value off the character's stack, and set the character to
            that value."""
            self.value = self.stack.pop()

    def run_play(self, play, breakpoint_callback=None):
        """
        Run an SPL play.

        Arguments:
        play -- An AST or text representation of an SPL play
        breakpoint_callback -- An optional callback, to be called if a debug
                               breakpoint is hit
        """
        self.ast = self._parse_if_necessary(play, 'play')
        self.run_dramatis_personae(self.ast.dramatis_personae, destructive=True)
        self.current_position = {'act': 0, 'scene': 0, 'event': 0}
        while not self.play_over():
            self.step_forward(breakpoint_callback)

    def play_over(self):
        """Return whether the play has finished."""
        return self.current_position['act'] >= len(self.ast.acts)

    def step_forward(self, breakpoint_callback=None):
        """
        Run the next event in the play.

        Arguments:
        breakpoint_callback -- An optional callback, to be called if a debug
                               breakpoint is hit
        """
        event_to_run = self._next_event()
        self.run_event(event_to_run, breakpoint_callback)

    def next_event_text(self):
        """Return the contents of the next event in the play."""
        current_event = self._next_event()
        buffer = current_event.parseinfo.buffer
        lines = buffer.get_lines(current_event.parseinfo.line, current_event.parseinfo.endline)
        return ''.join(lines)

    def run_event(self, event, breakpoint_callback=None):
        """
        Run an event in the current executing context.

        Arguments:
        event -- A string or AST representation of an event (line, entrance,
                 exit, etc.)
        breakpoint_callback -- An optional callback, to be called if a debug
                               breakpoint is hit
        """
        event = self._parse_if_necessary(event, 'event')
        has_goto = False
        if event.parseinfo.rule == 'line':
            has_goto = self._run_line(event)
        else:
            if event.parseinfo.rule == 'breakpoint':
                if breakpoint_callback:
                    breakpoint_callback()
            else:
                if event.parseinfo.rule == 'entrance':
                    self._run_entrance(event)
                else:
                    if event.parseinfo.rule == 'exeunt':
                        self._run_exeunt(event)
                    elif event.parseinfo.rule == 'exit':
                        self._run_exit(event)
        if self.current_position and not has_goto:
            self._advance_position()

    def run_sentence(self, sentence, character):
        """
        Run a sentence in the current execution context.

        Arguments:
        sentence -- A string or AST representation of a sentence
        character -- A name or Shakespeare.Character representation of the
                     character speaking the sentence.
        """
        character = self._character_by_name_if_necessary(character)
        sentence = self._parse_if_necessary(sentence, 'sentence')
        if not character.on_stage:
            raise Exception(character.name + " isn't on stage.")
        if sentence.parseinfo.rule == 'assignment':
            self._run_assignment(sentence, character)
        else:
            if sentence.parseinfo.rule == 'question':
                self._run_question(sentence, character)
            else:
                if sentence.parseinfo.rule == 'output':
                    self._run_output(sentence, character)
                else:
                    if sentence.parseinfo.rule == 'input':
                        self._run_input(sentence, character)
                    else:
                        if sentence.parseinfo.rule == 'push':
                            self._run_push(sentence, character)
                        else:
                            if sentence.parseinfo.rule == 'pop':
                                self._run_pop(sentence, character)
                            elif sentence.parseinfo.rule == 'goto':
                                went_to = self._run_goto(sentence)
                                if went_to:
                                    pass
                                return True

    def evaluate_question(self, question, character):
        """
        Evaluate a question in the current execution context.

        Arguments:
        question -- A string or AST representation of a question
        character -- A name or Shakespeare.Character representation of the
                     character asking the question.
        """
        question = self._parse_if_necessary(question, 'question')
        values = [self.evaluate_expression(v, character) for v in [
         question.first_value, question.second_value]]
        if question.comparative.parseinfo.rule == 'positive_comparative':
            return values[0] > values[1]
        if question.comparative.parseinfo.rule == 'negative_comparative':
            return values[0] < values[1]
        if question.comparative.parseinfo.rule == 'neutral_comparative':
            return values[0] == values[1]

    def evaluate_expression(self, value, character):
        """
        Evaluate an expression in the current execution context.

        Arguments:
        expression -- A string or AST representation of an expression
        character -- A name or Shakespeare.Character representation of the
                     character speaking the expression.
        """
        value = self._parse_if_necessary(value, 'value')
        if value.parseinfo.rule == 'first_person_value':
            return character.value
        if value.parseinfo.rule == 'second_person_value':
            return self._character_opposite(character).value
        if value.parseinfo.rule == 'negative_noun_phrase':
            return -pow(2, len(value.adjectives))
        if value.parseinfo.rule == 'positive_noun_phrase':
            return pow(2, len(value.adjectives))
        if value.parseinfo.rule == 'character_name':
            return self._character_by_name(value.name).value
        if value.parseinfo.rule == 'nothing':
            return 0
        if value.parseinfo.rule == 'unary_expression':
            return self._evaluate_unary_operation(value, character)
        if value.parseinfo.rule == 'binary_expression':
            return self._evaluate_binary_operation(value, character)

    def run_dramatis_personae(self, personae, destructive=False):
        """
        Run a dramatis personae, adding to or overwriting the character list.

        Arguments:
        personae -- A string or AST representation of a dramatis personae
        destructive -- Whether to replace the current character list
                       (default False)
        """
        personae = self._parse_if_necessary(personae, 'dramatis_personae')
        characters = []
        for persona in personae:
            character = self._character_from_dramatis_persona(persona)
            characters.append(character)

        if destructive:
            self.characters = characters
        else:
            self.characters += characters

    def run_dramatis_persona(self, persona):
        """
        Run a dramatis persona, adding to the character list.

        Arguments:
        persona -- A string or AST representation of a dramatis persona
        """
        persona = self._parse_if_necessary(persona, 'dramatis_persona')
        character = self._character_from_dramatis_persona(persona)
        self.characters.append(character)

    def _parse_if_necessary(self, item, rule_name):
        if isinstance(item, str):
            return self.parser.parse(item, rule_name=rule_name)
        else:
            return item

    def _character_opposite(self, character):
        characters_opposite = [x for x in self.characters if x.on_stage and x.name != character.name]
        if len(characters_opposite) > 1:
            raise Exception('Ambiguous second-person pronoun')
        elif len(characters_opposite) == 0:
            raise Exception(character.name + ' is talking to nobody!')
        return characters_opposite[0]

    def _character_by_name(self, name):
        if not isinstance(name, str):
            name = ' '.join(name)
        for x in self.characters:
            if x.name.lower() == name.lower():
                return x

    def _character_by_name_if_necessary(self, character):
        if isinstance(character, str):
            return self._character_by_name(character)
        else:
            return character

    def _scene_number_from_roman_numeral(self, roman_numeral):
        for index, scene in enumerate(self.current_act.scenes):
            if scene.number == roman_numeral:
                return index

    def _next_event(self):
        act_head = self.ast.acts[self.current_position['act']]
        scene_head = act_head.scenes[self.current_position['scene']]
        return scene_head.events[self.current_position['event']]

    def _make_position_consistent(self):
        if self.play_over():
            return
        self.current_act = self.ast.acts[self.current_position['act']]
        current_scene = self.current_act.scenes[self.current_position['scene']]
        if self.current_position['event'] >= len(current_scene.events):
            self.current_position['event'] = 0
            self.current_position['scene'] += 1
        if self.current_position['scene'] >= len(self.current_act.scenes):
            self.current_position['scene'] = 0
            self.current_position['act'] += 1

    def _goto_scene(self, numeral):
        scene_number = self._scene_number_from_roman_numeral(numeral)
        self.current_position['scene'] = scene_number
        self.current_position['event'] = 0

    def _advance_position(self):
        self.current_position['event'] += 1
        self._make_position_consistent()

    def _character_from_dramatis_persona(self, persona):
        name = persona.character
        if not isinstance(name, str):
            name = ' '.join(name)
        return self.Character(name)

    def _evaluate_unary_operation(self, op, character):
        operand = self.evaluate_expression(op.value, character)
        if op.operation == ['the', 'cube', 'of']:
            return pow(operand, 3)
        if op.operation == ['the', 'factorial', 'of']:
            return math.factorial(operand)
        if op.operation == ['the', 'square', 'of']:
            return pow(operand, 2)
        if op.operation == ['the', 'square', 'root', 'of']:
            return math.sqrt(operand)
        if op.operation == 'twice':
            return operand * 2

    def _evaluate_binary_operation(self, op, character):
        first_operand = self.evaluate_expression(op.first_value, character)
        second_operand = self.evaluate_expression(op.second_value, character)
        if op.operation == ['the', 'difference', 'between']:
            return first_operand - second_operand
        if op.operation == ['the', 'product', 'of']:
            return first_operand * second_operand
        if op.operation == ['the', 'quotient', 'between']:
            return first_operand // second_operand
        if op.operation == ['the', 'remainder', 'of',
         'the', 'quotient', 'between']:
            return first_operand % second_operand
        if op.operation == ['the', 'sum', 'of']:
            return first_operand + second_operand

    def _run_assignment(self, sentence, character):
        character_opposite = self._character_opposite(character)
        character_opposite.value = self.evaluate_expression(sentence.value, character)

    def _run_question(self, question, character):
        self.global_boolean = self.evaluate_question(question, character)

    def _run_goto(self, goto):
        condition = goto.condition
        condition_type = condition and condition.parseinfo.rule == 'positive_if'
        if not condition or condition_type == self.global_boolean:
            self._goto_scene(goto.destination)
            return True

    def _run_output(self, output, character):
        if output.output_number:
            number = self._character_opposite(character).value
            print(number, end='')
        elif output.output_char:
            char = chr(self._character_opposite(character).value)
            print(char, end='')

    def _run_input(self, input_op, character):
        if not self._input_buffer:
            try:
                self._input_buffer = input() + '\n'
            except EOFError:
                if input_op.input_char:
                    self._character_opposite(character).value = -1
                    return
                raise Exception('End of file encountered.')

            if input_op.input_number:
                number_input = ''
                while self._input_buffer[0].isdigit():
                    number_input += self._input_buffer[0]
                    self._input_buffer = self._input_buffer[1:]

                if len(number_input) == 0:
                    raise Exception('No numeric input was given.')
                self._character_opposite(character).value = int(number_input)
        elif input_op.input_char:
            input_char = ord(self._input_buffer[0])
            self._input_buffer = self._input_buffer[1:]
            self._character_opposite(character).value = input_char

    def _run_push(self, push, speaking_character):
        pushing_character = self._character_opposite(speaking_character)
        value = self.evaluate_expression(push.value, speaking_character)
        pushing_character.push(value)

    def _run_pop(self, pop, speaking_character):
        popping_character = self._character_opposite(speaking_character)
        popping_character.pop()

    def _run_line(self, line):
        character = self._character_by_name(line.character)
        for sentence in line.contents:
            has_goto = self.run_sentence(sentence, character)
            if has_goto:
                return True

    def _run_entrance(self, entrance):
        for name in entrance.characters:
            self._character_by_name(name).on_stage = True

    def _run_exeunt(self, exeunt):
        if exeunt.characters:
            for name in exeunt.characters:
                self._character_by_name(name).on_stage = False

        else:
            for character in self.characters:
                character.on_stage = False

    def _run_exit(self, exit):
        character = self._character_by_name(exit.character)
        character.on_stage = False