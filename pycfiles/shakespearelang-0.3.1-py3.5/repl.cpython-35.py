# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shakespearelang/repl.py
# Compiled at: 2019-02-05 20:16:34
# Size of source mod 2**32: 6325 bytes
from .shakespeare_interpreter import Shakespeare

def _collect_characters(interpreter):
    while True:
        persona = input('Dramatis persona or "done">> ')
        if persona == 'exit' or persona == 'quit':
            return False
        if persona == 'done':
            if not interpreter.characters:
                raise Exception('No characters!')
            break
        interpreter.run_dramatis_persona(persona)


def _print_stage(interpreter):
    print('On stage:')
    for x in interpreter.characters:
        if x.on_stage:
            print(x.name)

    print('\nOff stage:')
    for x in interpreter.characters:
        if not x.on_stage:
            print(x.name)


def _prefix_input_output(sentence, opposite_character):
    if sentence.parseinfo.rule == 'output' and sentence.output_number:
        print(opposite_character.name, 'outputted self as number:')
    else:
        if sentence.parseinfo.rule == 'output' and sentence.output_char:
            print(opposite_character.name, 'outputted self as character:')
        else:
            if sentence.parseinfo.rule == 'input' and sentence.input_number:
                print(opposite_character.name, 'taking input number:')
            elif sentence.parseinfo.rule == 'input' and sentence.input_char:
                print(opposite_character.name, 'taking input character:')


def _show_result_of_sentence(sentence, opposite_character, interpreter):
    if sentence.parseinfo.rule == 'question':
        print(interpreter.global_boolean)
    else:
        if sentence.parseinfo.rule == 'assignment':
            print(opposite_character.name, 'set to', opposite_character.value)
        else:
            if sentence.parseinfo.rule == 'push':
                print(opposite_character.name, 'pushed', opposite_character.stack[0])
            elif sentence.parseinfo.rule == 'pop':
                print(opposite_character.name, 'popped', opposite_character.value)


def _print_character(character_name, interpreter):
    character = interpreter._character_by_name(character_name)
    if not character.on_stage:
        print(character.name, 'is off stage right now.')
    else:
        print(character.name)
        print('Value:', character.value)
        print('Stack:')
        for index, item in enumerate(character.stack):
            if index >= 10:
                print('...')
                break
            print(item)


def _run_sentences(sentences, speaking_character, opposite_character, interpreter):
    for sentence in sentences:
        _prefix_input_output(sentence, opposite_character)
        try:
            control_flow = interpreter.run_sentence(sentence, speaking_character)
        except Exception as runtimeException:
            print('Error:\n', runtimeException)
            return

        if sentence.parseinfo.rule == 'output':
            print('\n')
        _show_result_of_sentence(sentence, opposite_character, interpreter)
        if control_flow:
            print("Control flow isn't allowed in REPL.")
            return


def start_console():
    interpreter = Shakespeare()
    print('\n\nA REPL-tastic Adventure.\n\n')
    _collect_characters(interpreter)
    print('\n\n                    Act I: All the World\n\n')
    print('                    Scene I: A Stage\n\n')
    run_repl(interpreter)


def debug_play(text):
    interpreter = Shakespeare()

    def on_breakpoint():
        print(interpreter.next_event_text(), '\n')
        run_repl(interpreter, debug_mode=True)

    interpreter.run_play(text, on_breakpoint)


def run_repl(interpreter, debug_mode=False):
    current_character = None
    while 1:
        event = input('>> ')
        if event in ('exit', 'quit') or event == 'continue' and debug_mode:
            return
        if event == 'stage':
            _print_stage(interpreter)
            continue
        else:
            if event == 'next' and debug_mode:
                interpreter.step_forward()
                if interpreter.play_over():
                    return
                print('\n', interpreter.next_event_text())
                continue
            try:
                ast = interpreter.parser.parse(event, rule_name='repl_input')
            except Exception as parseException:
                print("\n\nThat doesn't look right:\n", parseException)
                continue

            event = ast.event
            sentences = ast.sentences
            character = ast.character
            value = ast.value
            if event and event.parseinfo.rule == 'line':
                current_character = event.character
                sentences = event.contents
                event = None
            if event:
                try:
                    control_flow = interpreter.run_event(event)
                except Exception as runtimeException:
                    print('Error:\n', runtimeException)
                    continue

                if event.parseinfo.rule in ('entrance', 'exeunt', 'exit'):
                    _print_stage(interpreter)
        if control_flow:
            print("Control flow isn't allowed in REPL.")
            continue
        elif sentences:
            if not current_character:
                print("Who's saying this?")
                continue
                try:
                    speaking_character = interpreter._character_by_name(current_character)
                    opposite_character = interpreter._character_opposite(speaking_character)
                except Exception as runtimeException:
                    print('Error:\n', runtimeException)
                    continue

                _run_sentences(sentences, speaking_character, opposite_character, interpreter)
            else:
                if value:
                    if character:
                        current_character = character
                    try:
                        speaking_character = interpreter._character_by_name(current_character)
                        result = interpreter.evaluate_expression(value, speaking_character)
                    except Exception as runtimeException:
                        print('Error:\n', runtimeException)
                        continue

                    print(result, '\n')
                elif character:
                    _print_character(character, interpreter)