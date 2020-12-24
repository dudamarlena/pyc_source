# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/_input.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 12875 bytes
import re, pdb
from ._edit_descriptors import *
from ._misc import expand_edit_descriptors, has_next_iterator
from . import config
WIDTH_OPTIONAL_EDS = [
 A]
NON_WIDTH_EDS = [BN, BZ, P, SP, SS, S, X, T, TR, TL, Colon, Slash]
FORBIDDEN_EDS = [QuotedString, H]

def input(eds, reversion_eds, records, num_vals=None):
    state = {'position':0, 
     'scale':0, 
     'incl_plus':False, 
     'blanks_as_zeros':config.PROC_BLANKS_AS_ZEROS, 
     'halt_if_no_vals':False, 
     'exception_on_fail':True}
    for ed in eds + reversion_eds:
        if isinstance(ed, tuple(FORBIDDEN_EDS)):
            raise InvalidFormat('%d edit descriptr not permitted on input')

    eds = expand_edit_descriptors(eds)
    reversion_eds = expand_edit_descriptors(reversion_eds)
    num_out_eds = 0
    for ed in eds:
        if isinstance(ed, OUTPUT_EDS):
            num_out_eds += 1

    num_rev_out_eds = 0
    if num_vals is None:
        num_vals = num_out_eds
    for ed in reversion_eds:
        if isinstance(ed, OUTPUT_EDS):
            num_rev_out_eds += 1

    if num_out_eds == 0:
        return []
    if num_vals > num_out_eds:
        if num_rev_out_eds == 0:
            raise ValueError('Not enough output edit descriptors in reversion format to output %d values' % num_vals)
    if not hasattr(records, 'next'):
        records = iter(re.split('\r\n|\r|\n', records))
    record = _next(records, None)
    if record is None:
        return []
    else:
        vals = []
        finish_up = False
        ed_ind = -1
        while 1:
            ed_ind += 1
            if len(vals) >= num_vals:
                finish_up = True
            if ed_ind < len(eds):
                ed = eds[ed_ind]
            else:
                rev_ed_ind = (ed_ind - len(eds)) % len(reversion_eds)
                if finish_up:
                    if rev_ed_ind == 0:
                        break
                ed = reversion_eds[rev_ed_ind]
            if isinstance(ed, QuotedString):
                raise InvalidFormat('Cannot have string literal in an input format')
            elif isinstance(ed, BN):
                state['blanks_as_zeros'] = False
            elif isinstance(ed, BZ):
                state['blanks_as_zeros'] = True
            elif isinstance(ed, P):
                state['scale'] = ed.scale
            elif isinstance(ed, SP):
                state['incl_plus'] = True
            elif isinstance(ed, SS):
                state['incl_plus'] = False
            elif isinstance(ed, S):
                state['incl_plus'] = config.PROC_INCL_PLUS
            elif isinstance(ed, (X, TR)):
                state['position'] = min(state['position'] + ed.num_chars, len(record))
            elif isinstance(ed, TL):
                state['position'] = max(state['position'] - ed.num_chars, 0)
            elif isinstance(ed, T):
                if ed.num_chars - 1 < 0:
                    state['position'] = 0
                else:
                    if ed.num_chars > len(record):
                        state['position'] = len(record)
                    else:
                        state['position'] = ed.num_chars - 1
            elif isinstance(ed, Slash):
                record = _next(records, None)
                state['position'] = 0
                if record is None:
                    break
            elif isinstance(ed, Colon):
                if finish_up:
                    break
            elif isinstance(ed, (Z, O, B, I)):
                val, state = read_integer(ed, state, record)
                vals.append(val)
            elif isinstance(ed, A):
                val, state = read_string(ed, state, record)
                vals.append(val)
            elif isinstance(ed, L):
                val, state = read_logical(ed, state, record)
                vals.append(val)
            elif isinstance(ed, (F, E, D, EN, ES)):
                val, state = read_float(ed, state, record)
                vals.append(val)
            elif isinstance(ed, G):
                resolved = False
                g_trial_eds = iter(config.G_INPUT_TRIAL_EDS)
                while not resolved:
                    ed_name = _next(g_trial_eds, '')
                    if ed_name.upper() in ('F', 'E', 'D', 'EN', 'ES'):
                        trial_ed = F()
                        trial_ed.width = ed.width
                        trial_ed.decimal_places = ed.decimal_places
                        try:
                            val, state = read_float(trial_ed, state.copy(), record)
                            vals.append(val)
                            resolved = True
                        except ValueError:
                            continue

                    else:
                        if ed_name.upper() in ('Z', 'O', 'B', 'I'):
                            trial_ed = globals()[ed_name]()
                            trial_ed.width = ed.width
                            trial_ed.min_digits = ed.decimal_places
                            try:
                                val, state = read_integer(trial_ed, state.copy(), record)
                                vals.append(val)
                                resolved = True
                            except ValueError:
                                continue

                        else:
                            if ed_name.upper() in 'L':
                                trial_ed = L()
                                trial_ed.width = ed.width
                                try:
                                    val, state = read_logical(trial_ed, state.copy(), record)
                                    vals.append(val)
                                    resolved = True
                                except ValueError:
                                    continue

                            else:
                                if ed_name.upper() in 'A':
                                    trial_ed = A()
                                    trial_ed.width = ed.width
                                    try:
                                        val, state = read_string(trial_ed, state.copy(), record)
                                        vals.append(val)
                                        resolved = True
                                    except ValueError:
                                        continue

                                else:
                                    if ed_name in 'G':
                                        raise ValueError('G edit descriptor not permitted in config.G_INPUT_TRIAL_EDS')
                                    else:
                                        raise ValueError('Unrecognised trial edit descriptor string in config.G_INPUT_TRIAL_EDS')

        if config.RET_WRITTEN_VARS_ONLY:
            vals = [val for val in vals if val is not None]
        return vals[:num_vals]


def _interpret_blanks(substr, state):
    len_str = len(substr)
    if state['blanks_as_zeros']:
        substr = substr.replace(' ', '0')
    else:
        substr = substr.replace(' ', '')
    if len(substr) == 0:
        if len_str > 0:
            substr = '0'
    return substr


def _get_substr(w, record, state):
    start = max(state['position'], 0)
    end = start + w
    substr = record[start:end]
    state['position'] = min(state['position'] + w, len(record))
    return (substr, state)


def _next(it, default=None):
    try:
        val = next(it)
    except StopIteration:
        val = default

    return val


def read_string(ed, state, record):
    if ed.width is None:
        ed.width = len(record) - state['position']
    substr, state = _get_substr(ed.width, record, state)
    val = substr.ljust(ed.width, config.PROC_PAD_CHAR)
    return (val, state)


def read_integer(ed, state, record):
    substr, state = _get_substr(ed.width, record, state)
    if '-' in substr:
        if not config.PROC_ALLOW_NEG_BOZ:
            if isinstance(ed, (Z, O, B)):
                if state['exception_on_fail']:
                    raise ValueError('Negative numbers not permitted for binary, octal or hex')
                else:
                    return (
                     None, state)
    if isinstance(ed, Z):
        base = 16
    else:
        if isinstance(ed, I):
            base = 10
        else:
            if isinstance(ed, O):
                base = 8
            else:
                if isinstance(ed, B):
                    base = 2
    if re.match('^ *- +$', substr):
        substr = '0'
    if config.PROC_NEG_AS_ZERO:
        if isinstance(ed, I):
            if re.match('^( *- *| +)$', substr):
                substr = '0'
    if substr == '':
        if config.RET_UNWRITTEN_VARS_NONE or config.RET_WRITTEN_VARS_ONLY:
            return (
             None, state)
        substr = '0'
    teststr = _interpret_blanks(substr, state)
    try:
        val = int(teststr, base)
    except ValueError:
        if state['exception_on_fail']:
            raise ValueError('%s is not a valid input for one of integer, octal, hex or binary' % substr)
        else:
            return (
             None, state)

    return (
     val, state)


def read_logical(ed, state, record):
    substr, state = _get_substr(ed.width, record, state)
    if substr == '':
        if config.RET_UNWRITTEN_VARS_NONE or config.RET_WRITTEN_VARS_ONLY:
            return (
             None, state)
    else:
        teststr = substr.upper().lstrip().lstrip('.')
        if len(teststr):
            teststr = teststr[0]
        else:
            raise ValueError('%s is not a valid boolean input' % substr)
        if teststr == 'T':
            val = True
        else:
            if teststr == 'F':
                val = False
            else:
                if state['exception_on_fail']:
                    raise ValueError('%s is not a valid boolean input' % substr)
                else:
                    val = None
    return (
     val, state)


def read_float(ed, state, record):
    substr, state = _get_substr(ed.width, record, state)
    teststr = _interpret_blanks(substr, state)
    if teststr == '':
        if config.RET_UNWRITTEN_VARS_NONE or config.RET_WRITTEN_VARS_ONLY:
            return (
             None, state)
        teststr = '0'
    teststr = teststr.upper().replace('D', 'E')
    if 'E' not in teststr:
        teststr = teststr[0] + teststr[1:].replace('+', 'E+').replace('-', 'E-')
    if re.match('^ *\\. *$', teststr):
        teststr = '0'
    if re.match('^ *- *$', teststr):
        teststr = '0'
    res = re.match('(.*)(E|E\\+|E\\-)$', teststr)
    if res:
        teststr = res.group(1)
    try:
        val = float(teststr)
    except ValueError:
        if state['exception_on_fail']:
            raise ValueError('%s is not a valid input as for an E, ES, EN or D edit descriptor' % substr)
        else:
            return (
             None, state)

    if '.' not in teststr:
        if ed.decimal_places is not None:
            val = val / 10 ** ed.decimal_places
    if 'E' not in teststr:
        val = val / 10 ** state['scale']
    return (
     val, state)