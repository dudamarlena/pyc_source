# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/site-packages/microcsound/parser.py
# Compiled at: 2017-11-27 09:15:51
# Size of source mod 2**32: 6719 bytes
import re
from random import gauss
from microcsound.state import state_obj
from microcsound import constants, handlers
PARSER_PATTERN = re.compile('(?:(?:mix|pan|div|gr|gv|gs|t|i)[=](?:[0-9]{0,5}[.]?[0-9]{1,5}|\\"<\\"))|(?:(?:p[89]{1}|p[1-9][0-9])[=](?:[-0-9.<]+))|(?:key[=][0-9]+[:][0-9]+)|(?:\\"[-0-9.<%]+\\")|(?:[&][\\-+]?[0-9]*)|(?:\\[L:[0-9]{1,4}[/][0-9]{1,4}\\])|(?:[0-9]{1,4}[/][0-9]{1,4})|[rzx][0-9]{0,2}|[@](?:[0-9]?[.][0-9]{1,3}|[0-9A-Fa-f]{1,2}|[<])|PD[0-9]{1,3}|PU|(?:(?:[.\\(])?(?:\\^/2|_/2|[_^=/\\\\<>!?]|\\xc2\\xa1|\\xc2\\xbf)*[a-g](?:\\*)*[,\']*[0-9]{0,2}[-]?[)]?)|(?:(?:[.\\(])?(?:[0-9]+[:][0-9]+)\\)?(?:[| t](?![=]))*)|(?:(?:[.\\(])?(?:[0-9]+[.])?(?:[-]?[0-9]+)\\)?(?:[| t](?![=]))*)|\\[|\\]')

def parser(inst_line):
    state_obj.reset_voice()
    for event in PARSER_PATTERN.findall(inst_line):
        if event == '':
            continue
        else:
            if re.match('(?P<type>div|mix|pan|gr|gv|gs|t|i)[=](?P<value>(?:[0-9]{1,5}[.]?[0-9]{0,5}|\\"<\\"))', event):
                handlers.handle_global_variable_event(event)
                continue
            else:
                if re.match('(?:(?:p[89]{1}|p[1-9][0-9])[=](?:[-0-9.<]+))', event):
                    handlers.handle_instrument_parameter(event)
                    continue
                else:
                    if re.match('(?:\\"[-0-9.<%]+\\")', event):
                        handlers.handle_many_instrument_parameters(event)
                        continue
                    else:
                        if 'key' in event:
                            handlers.handle_JI_transpose(event)
                            continue
                        else:
                            if re.match('(?:\\[L:)?[0-9]{1,4}[/][0-9]{1,4}(?:\\])?', event):
                                handlers.handle_length(event)
                                continue
                            else:
                                if event[0] == 'r' or event[0] == 'z' or event[0] == 'x':
                                    handlers.handle_rest(event)
                                    continue
                                else:
                                    if event in '[]':
                                        handlers.handle_chord_status(event)
                                        continue
                                    else:
                                        if event.startswith('PD') or event.startswith('PU'):
                                            handlers.handle_pedal(event)
                                            continue
                                        else:
                                            if event[0] == '&':
                                                handlers.handle_time_travel(event)
                                                continue
                                            else:
                                                if event[0] == '@':
                                                    handlers.handle_attack(event)
                                                    continue
                                                else:
                                                    if re.match('(?:[.\\(])?(?:[0-9]+[:][0-9]+)', event):
                                                        pitch, length_factor, articulation, tie = handlers.handle_JI_notation(event)
                                                    else:
                                                        if re.match('(?:[.\\(])?(?:[0-9]+[.])?(?:[-]?[0-9]+)', event):
                                                            pitch, length_factor, articulation, tie = handlers.handle_numeric_notation(event)
                                                        else:
                                                            pitch, length_factor, articulation, tie = handlers.handle_symbolic_notation(event)
                pitch = float(pitch) * float(state_obj.key)
                on_time = state_obj.grid_time + gauss(0, 0.001) * state_obj.gaussian_rhythm * state_obj.tempo * 0.01666
                if on_time < 0:
                    on_time = 0
                if state_obj.default_attack != '<':
                    attack = state_obj.default_attack + int(gauss(0, state_obj.gaussian_volume))
                    if attack >= 1:
                        attack = 1
                else:
                    attack = state_obj.default_attack
        if state_obj.tie:
            if pitch not in state_obj.tie_dict[state_obj.instr]:
                state_obj.tie_dict[state_obj.instr][pitch] = [on_time, state_obj.length_factor, attack, state_obj.pan]
            else:
                state_obj.tie_dict[state_obj.instr][pitch][1] += state_obj.length_factor
        else:
            if pitch in state_obj.tie_dict[state_obj.instr]:
                tie_info = state_obj.tie_dict[state_obj.instr].pop(pitch)
                on_time = info[0]
                length_factor = tie_info[1] + state_obj.length_factor
                attack = tie_info[2]
                state_obj.pan = tie_info[3]
            else:
                if state_obj.pedal_down:
                    duration = state_obj.arrival - on_time
                else:
                    if state_obj.articulation == 'staccato':
                        duration = state_obj.tempo / 60.0 * state_obj.staccato_length + gauss(0, 0.001) * state_obj.gaussian_staccato * state_obj.tempo * 0.01666
                    else:
                        if state_obj.articulation == 'legato':
                            duration = state_obj.length * length_factor * -1
                        else:
                            duration = state_obj.length * length_factor
            state_obj.outstring = state_obj.outstring + 'i%1.1f %1.3f %1.3f  %s  %s  %s  %s  %s\n' % (
             state_obj.instr, on_time, duration,
             attack, pitch, state_obj.pan, state_obj.mix,
             ' '.join(state_obj.xtra).replace('"', ''))
            if not state_obj.chord_status:
                state_obj.grid_time += state_obj.length * length_factor