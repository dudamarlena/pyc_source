# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/utils/fortranformat/_output.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 24486 bytes
import math, itertools
from ._edit_descriptors import *
from ._misc import expand_edit_descriptors, has_next_iterator
from . import config
PROC_SIGN_ZERO = config.PROC_SIGN_ZERO
PROC_MIN_FIELD_WIDTH = config.PROC_MIN_FIELD_WIDTH
PROC_DECIMAL_CHAR = config.PROC_DECIMAL_CHAR
G0_NO_BLANKS = config.G0_NO_BLANKS
PROC_NO_LEADING_BLANK = config.PROC_NO_LEADING_BLANK

def output(eds, reversion_eds, values):
    """
    a function to take a list of valid f77 edit descriptors and respective values
    and output the corresponding string
    """
    record = ''
    state = {'position':0, 
     'scale':0, 
     'incl_plus':False, 
     'blanks_as_zeros':False, 
     'halt_if_no_vals':False}
    reversion_contains_output_ed = False
    for ed in reversion_eds:
        if isinstance(ed, OUTPUT_EDS):
            reversion_contains_output_ed = True
            break

    eds = expand_edit_descriptors(eds)
    reversion_eds = expand_edit_descriptors(reversion_eds)
    get_ed = has_next_iterator(eds)
    get_value = has_next_iterator(values)
    tmp_reversion_eds = []
    while 1:
        if not get_ed.has_next():
            if not get_value.has_next():
                break
        else:
            if get_ed.has_next():
                ed = next(get_ed)
            else:
                if reversion_contains_output_ed == True:
                    while True:
                        if len(tmp_reversion_eds):
                            ed = tmp_reversion_eds.pop()
                            if not isinstance(ed, NON_REVERSION_EDS):
                                break
                        else:
                            record = record + config.RECORD_SEPARATOR
                            state['position'] = len(record)
                            tmp_reversion_eds = reversion_eds[::-1]

                else:
                    break
        if isinstance(ed, OUTPUT_EDS):
            if get_value.has_next():
                val = next(get_value)
            else:
                break
            if isinstance(ed, I):
                sub_string = _compose_i_string(ed.width, ed.min_digits, state, val)
            elif isinstance(ed, B):
                w = ed.width
                m = ed.min_digits
                sub_string = _compose_boz_string(w, m, state, val, 'B')
            else:
                if isinstance(ed, O):
                    w = ed.width
                    m = ed.min_digits
                    sub_string = _compose_boz_string(w, m, state, val, 'O')
                if isinstance(ed, Z):
                    w = ed.width
                    m = ed.min_digits
                    sub_string = _compose_boz_string(w, m, state, val, 'Z')
                else:
                    if isinstance(ed, F):
                        w = ed.width
                        e = None
                        d = ed.decimal_places
                        sub_string = _compose_float_string(w, e, d, state, val, 'F')
                    else:
                        if isinstance(ed, E):
                            w = ed.width
                            e = ed.exponent
                            d = ed.decimal_places
                            sub_string = _compose_float_string(w, e, d, state, val, 'E')
                        else:
                            if isinstance(ed, D):
                                w = ed.width
                                e = None
                                d = ed.decimal_places
                                sub_string = _compose_float_string(w, e, d, state, val, 'D')
                            else:
                                if isinstance(ed, G):
                                    w = ed.width
                                    e = ed.exponent
                                    d = ed.decimal_places
                                    sub_string = _compose_float_string(w, e, d, state, val, 'G')
                                else:
                                    if isinstance(ed, EN):
                                        w = ed.width
                                        e = ed.exponent
                                        d = ed.decimal_places
                                        sub_string = _compose_float_string(w, e, d, state, val, 'EN')
                                    else:
                                        if isinstance(ed, ES):
                                            w = ed.width
                                            e = ed.exponent
                                            d = ed.decimal_places
                                            sub_string = _compose_float_string(w, e, d, state, val, 'ES')
                                        else:
                                            if isinstance(ed, L):
                                                sub_string = _compose_l_string(ed.width, state, val)
                                            elif isinstance(ed, A):
                                                sub_string = _compose_a_string(ed.width, state, val)
            state['position'], record = _write_string(record, sub_string, state['position'])
        else:
            if isinstance(ed, (S, SS)):
                state['incl_plus'] = False
            if isinstance(ed, SP):
                state['incl_plus'] = True
            elif isinstance(ed, P):
                state['scale'] = ed.scale
            elif isinstance(ed, BN):
                state['blanks_as_zeros'] = False
            elif isinstance(ed, BZ):
                state['blanks_as_zeros'] = True
            elif isinstance(ed, Colon):
                state['halt_if_no_vals'] = True
            elif isinstance(ed, Slash):
                state['position'], record = _write_string(record, config.RECORD_SEPARATOR, state['position'])
            elif isinstance(ed, (X, TR)):
                state['position'] = state['position'] + ed.num_chars
            elif isinstance(ed, TL):
                state['position'] = state['position'] - ed.num_chars
            elif isinstance(ed, T):
                state['position'] = ed.num_chars - 1
            else:
                if isinstance(ed, QuotedString):
                    sub_string = ed.char_string
                    state['position'], record = _write_string(record, sub_string, state['position'])

    return record


def _compose_nan_string(w, ftype):
    if ftype in ('B', 'O', 'Z'):
        return ''
    else:
        if w == 0:
            w = 4
        if w < 3:
            return '*' * w
        return 'NaN'.rjust(w)


def _compose_inf_string(w, ftype, sign_bit):
    if ftype in ('B', 'O', 'Z'):
        return ''
    else:
        sign = '+'
        if w == 0:
            w = 4
        if w < 3:
            return '*' * w
        if sign_bit:
            sign = '-'
            if w == 3:
                return '*' * w
        if w > 8:
            return (sign + 'Infinity').rjust(w)
        if w > 3:
            return (sign + 'Inf').rjust(w)
        return 'Inf'


def _compose_float_string(w, e, d, state, val, ftype):
    """
    Adapted from code in glibfortran which is written in C so is somwhat
    'bit-pushy' in nature. Writes the value to an initial string (buffer)
    and then pulls the subsequent strings from that
    """
    if d < 0 or d is None:
        raise InvalidFormat('Unspecified precision')
    else:
        d = int(round(d))
        if e is not None:
            e = int(round(e))
        if w is not None:
            w = int(round(w))
        edigits = 4
        if ftype in ('F', 'EN', 'G') or ftype in ('D', 'E') and state['scale'] != 0:
            ndigits = PROC_MIN_FIELD_WIDTH - 4 - edigits
        else:
            if ftype == 'ES':
                ndigits = d + 1
            else:
                ndigits = d
            if ndigits > PROC_MIN_FIELD_WIDTH - 4 - edigits:
                ndigits = PROC_MIN_FIELD_WIDTH - 4 - edigits
            if val == 0.0:
                sign_bit = '-' in str(val)
            else:
                sign_bit = val < 0
        if type(val) is float:
            if val != val:
                return _compose_nan_string(w, ed)
    Infinity = float('inf')
    if val in (-Infinity, Infinity):
        return _compose_inf_string(w, ed, sign_bit)
    else:
        tmp = abs(val)
        if ftype == 'F':
            if d == state['scale']:
                if d == 0:
                    if tmp < 1.0:
                        tmp = round(tmp)
        zero_flag = tmp == 0
        if ndigits <= 0:
            fmt = '%+-#' + str(PROC_MIN_FIELD_WIDTH) + 'e'
        else:
            fmt = '%+-#' + str(PROC_MIN_FIELD_WIDTH) + '.' + str(ndigits - 1) + 'e'
        buff = fmt % tmp
        if ftype != 'G':
            return _output_float(w, d, e, state, ftype, buff, sign_bit, zero_flag, ndigits, edigits)
        nb = 0
        save_scale_factor = state['scale']
        exp_d = 10 ** d
        if 0.0 <= tmp < 0.1 - 0.05 / exp_d or tmp >= exp_d - 0.5:
            ftype = 'E'
        else:
            mag = int(abs(round(math.log10(tmp))))
            low = lambda mag, d: 10 ** (mag - 1) - 5 * 10 ** (-d - 1 + mag)
            high = lambda mag, d: 10 ** mag - 0.5 * 10 ** (-d + mag)
            while tmp < low(mag, d):
                mag = mag - 1

            while tmp >= high(mag, d):
                mag = mag + 1

            assert low(mag, d) <= tmp < high(mag, d)
            if e < 0:
                nb = 4
            else:
                nb = e + 2
            ftype = 'F'
            w = w - nb
            if tmp == 0.0:
                d = d - 1
            else:
                d = d - mag
            state['scale'] = 0
        out = _output_float(w, d, e, state, ftype, buff, sign_bit, zero_flag, ndigits, edigits)
        state['scale'] = save_scale_factor
        if nb > 0:
            if '*' in out:
                out = out + '*' * nb
            else:
                out = out + ' ' * nb
        if len(out) > w + nb:
            out = '*' * (w + nb)
        return out


def _output_float(w, d, e, state, ft, buff, sign_bit, zero_flag, ndigits, edigits):
    if w is None:
        w = -1
    else:
        if e is None:
            e = -1
        else:
            nzero_real = -1
            sign = _calculate_sign(state, sign_bit)
            if d != 0:
                assert buff[2] in ('.', ',')
                if not buff[(ndigits + 2)] == 'e':
                    raise AssertionError
            ex = int(buff[ndigits + 3:]) + 1
            if zero_flag:
                ex = 0
                if PROC_SIGN_ZERO:
                    sign = _calculate_sign(state, sign_bit)
                else:
                    sign = _calculate_sign(state, False)
                if w == 0:
                    w = d + 2
                if w == 1:
                    if ft == 'F':
                        if state['incl_plus']:
                            return '*'
                        return '.'
            digits = buff[1] + buff[3:]
            if ft == 'F':
                nbefore = ex + state['scale']
                if nbefore < 0:
                    nzero = -nbefore
                    nzero_real = nzero
                    if nzero > d:
                        nzero = d
                    nafter = d - nzero
                    nbefore = 0
                else:
                    nzero = 0
                    nafter = d
                expchar = None
            else:
                if ft in ('E', 'D'):
                    i = state['scale']
                    if d <= 0:
                        if i == 0:
                            raise InvalidFormat("Precision not greater than zero in format specifier 'E' or 'D'")
                    if i <= -d or i >= d + 2:
                        raise InvalidFormat("Scale factor out of range in format specifier 'E' or 'D'")
                    if not zero_flag:
                        ex = ex - i
                    if i < 0:
                        nbefore = 0
                        nzero = -i
                        nafter = d + i
                    else:
                        if i > 0:
                            nbefore = i
                            nzero = 0
                            nafter = d - i + 1
                        else:
                            nbefore = 0
                            nzero = 0
                            nafter = d
                    expchar = ft
                else:
                    if ft == 'EN':
                        if not zero_flag:
                            ex = ex - 1
                        if ex >= 0:
                            nbefore = ex % 3
                        else:
                            nbefore = -ex % 3
                        if nbefore != 0:
                            nbefore = 3 - nbefore
                        ex = ex - nbefore
                        nbefore = nbefore + 1
                        nzero = 0
                        nafter = d
                        expchar = 'E'
                    else:
                        if ft == 'ES':
                            if not zero_flag:
                                ex = ex - 1
                            nbefore = 1
                            nzero = 0
                            nafter = d
                            expchar = 'E'
                    if nbefore + nafter == 0:
                        ndigits = 0
                        if nzero_real == d:
                            if int(digits[0]) >= 5:
                                nzero = nzero - 1
                                nafter = 1
                                digits = '1' + digits[1:]
                                ndigits = 1
                    else:
                        if nbefore + nafter < ndigits:
                            ndigits = nbefore + nafter
                            i = ndigits
                            if int(digits[i]) >= 5:
                                i = i - 1
                                while i >= 0:
                                    digit = int(digits[i])
                                    if digit != 9:
                                        digits = _swapchar(digits, i, str(digit + 1))
                                        break
                                    else:
                                        digits = _swapchar(digits, i, '0')
                                    i = i - 1

                                if i < 0:
                                    digits = '1' + digits
                                    if ft == 'F':
                                        if nzero > 0:
                                            nzero = nzero - 1
                                            nafter = nafter + 1
                                        else:
                                            nbefore = nbefore + 1
                                    else:
                                        if ft == 'EN':
                                            nbefore = nbefore + 1
                                            if nbefore == 4:
                                                nbefore = 1
                                                ex = ex + 3
                                        else:
                                            ex = ex + 1
                            if expchar is not None:
                                if e < 0:
                                    if ex > 999 or ex < -999:
                                        edigits = -1
                                    else:
                                        edigits = 4
                                        if ex > 99 or ex < -99:
                                            expchar = ' '
                                elif not isinstance(ex, int):
                                    raise AssertionError
                            else:
                                edigits = len(str(abs(ex)))
                                if edigits > e:
                                    edigits = -1
                                else:
                                    edigits = e + 2
                        else:
                            edigits = 0
            i = 0
            while i < ndigits:
                if digits[i] != '0':
                    break
                i = i + 1

            if i == ndigits:
                if PROC_SIGN_ZERO:
                    sign = _calculate_sign(state, sign_bit)
                else:
                    sign = _calculate_sign(state, False)
            if w <= 0:
                w = nbefore + nzero + nafter + 1 + len(sign)
            nblanks = w - (nbefore + nzero + nafter + edigits + 1)
            if sign != '':
                nblanks = nblanks - 1
        if G0_NO_BLANKS:
            w = w - nblanks
            nblanks = 0
    if nblanks < 0 or edigits == -1:
        return '*' * w
    else:
        if nbefore == 0:
            if nblanks > 0:
                leadzero = True
                nblanks = nblanks - 1
            else:
                leadzero = False
            out = ''
            if nblanks > 0:
                if not PROC_NO_LEADING_BLANK:
                    out = out + ' ' * nblanks
            out = out + sign
            if leadzero:
                out = out + '0'
            if nbefore > 0:
                if nbefore > ndigits:
                    out = out + digits[:ndigits] + ' ' * (nbefore - ndigits)
                    digits = digits[ndigits:]
                    ndigits = 0
                else:
                    i = nbefore
                    out = out + digits[:i]
                    digits = digits[i:]
                    ndigits = ndigits - i
            out = out + PROC_DECIMAL_CHAR
            if nzero > 0:
                out = out + '0' * nzero
        else:
            if nafter > 0:
                if nafter > ndigits:
                    i = ndigits
                else:
                    i = nafter
                zeros = '0' * (nafter - i)
                out = out + digits[:i] + zeros
                digits = digits[nafter:]
                ndigits = ndigits - nafter
            if expchar is not None:
                if expchar != ' ':
                    out = out + expchar
                    edigits = edigits - 1
                fmt = '%+0' + str(edigits) + 'd'
                tmp_buff = fmt % ex
                if PROC_NO_LEADING_BLANK:
                    tmp_buf = tmp_buff + nblanks * ' '
                out = out + tmp_buff
        return out


def _calculate_sign(state, negative_flag):
    s = ''
    if negative_flag:
        s = '-'
    else:
        if state['incl_plus']:
            s = '+'
        else:
            s = ''
    return s


def _swapchar(s, ind, newch):
    """
    Helper function to make chars in a string mutableish
    """
    if 0 < ind >= len(s):
        raise IndexError('index out of range')
    return s[:ind] + newch + s[ind + 1:]


def _compose_a_string(w, state, val):
    val = str(val)
    if w is None:
        output = val
    else:
        if w >= len(val):
            output = val.rjust(w)
        else:
            output = val[:w]
    return output


def _compose_l_string(w, state, val):
    try:
        val = bool(val)
    except ValueError:
        raise ValueError("cannot convert '%s' to a boolean" % str(val))

    if val == True:
        sub_string = 'T'
    else:
        sub_string = 'F'
    sub_string = sub_string.rjust(w)
    return sub_string


def _compose_i_string(w, m, state, val):
    null_field = False
    try:
        val = int(val)
    except ValueError:
        raise ValueError("cannot convert '%s' to a integer" % str(val))

    int_string = '%d' % int(round(math.fabs(val)))
    if m is not None:
        int_string = left_pad(int_string, m, '0')
        if val == 0:
            if m == 0:
                int_string = ''
    else:
        if int_string != '':
            int_string = _get_sign(val, state['incl_plus']) + int_string
        if len(int_string) > w:
            int_string = '*' * w
        else:
            int_string = int_string.rjust(w)
    return int_string


def _get_sign(val, incl_plus):
    if val >= 0:
        if incl_plus == True:
            return '+'
        else:
            return ''
    else:
        return '-'


def _compose_boz_string(w, m, state, val, ftype):
    try:
        val = int(val)
    except ValueError:
        raise ValueError('Cannot convert %s to an integer' % str(val))

    if val == 0:
        if m is None:
            return '0'.rjust(w)
        if w == m == 0:
            return ' '
    else:
        if m == 0:
            return w * ' '
        else:
            s = left_pad('0', m, '0').rjust(w)
            if len(s) > w:
                return w * '*'
            s = ''
            if ftype == 'B':
                if val < 0:
                    return '*' * w
                while val > 0:
                    s = str(val % 2) + s
                    val = val >> 1

            else:
                if ftype == 'O':
                    if val < 0:
                        return '*' * w
                    s = '%o' % val
                elif ftype == 'Z':
                    if abs(val) > config.PROC_MAXINT:
                        return '*' * w
                    if val < 0:
                        s = '%X' % (config.PROC_MAXINT * 2 + 2 + val)
                    else:
                        s = '%X' % val
        if m is None:
            s = s.rjust(w)
        else:
            s = left_pad(s, m, '0').rjust(w)
    if len(s) > w:
        return w * '*'
    else:
        return s


def _write_string(record, sub_string, pos):
    """Function that actually writes the generated strings to a 'stream"""
    new_pos = pos + len(sub_string)
    if pos > len(record):
        record = record.ljust(pos)
        out = record + sub_string
    else:
        if pos == len(record):
            out = record + sub_string
        else:
            if pos < len(record):
                out = record[:pos] + sub_string + record[new_pos:]
    return (
     new_pos, out)


def left_pad(sub_string, width, pad_char):
    padding = pad_char * (width - len(sub_string))
    return padding + sub_string