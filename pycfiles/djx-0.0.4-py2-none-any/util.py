# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-zr3xXj/pytest/_pytest/assertion/util.py
# Compiled at: 2019-02-14 00:35:47
"""Utilities for assertion debugging"""
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import pprint, six, _pytest._code
from ..compat import Sequence
from _pytest._io.saferepr import saferepr
_reprcompare = None

def ecu(s):
    if isinstance(s, bytes):
        return s.decode('UTF-8', 'replace')
    else:
        return s


def format_explanation(explanation):
    """This formats an explanation

    Normally all embedded newlines are escaped, however there are
    three exceptions: 
{, 
} and 
~.  The first two are intended
    cover nested explanations, see function and attribute explanations
    for examples (.visit_Call(), visit_Attribute()).  The last one is
    for when one explanation needs to span multiple lines, e.g. when
    displaying diffs.
    """
    explanation = ecu(explanation)
    lines = _split_explanation(explanation)
    result = _format_lines(lines)
    return ('\n').join(result)


def _split_explanation(explanation):
    """Return a list of individual lines in the explanation

    This will return a list of lines split on '
{', '
}' and '
~'.
    Any other newlines will be escaped and appear in the line as the
    literal '
' characters.
    """
    raw_lines = (explanation or '').split('\n')
    lines = [raw_lines[0]]
    for values in raw_lines[1:]:
        if values and values[0] in ('{', '}', '~', '>'):
            lines.append(values)
        else:
            lines[(-1)] += '\\n' + values

    return lines


def _format_lines(lines):
    """Format the individual lines

    This will replace the '{', '}' and '~' characters of our mini
    formatting language with the proper 'where ...', 'and ...' and ' +
    ...' text, taking care of indentation along the way.

    Return a list of formatted lines.
    """
    result = lines[:1]
    stack = [0]
    stackcnt = [0]
    for line in lines[1:]:
        if line.startswith('{'):
            if stackcnt[(-1)]:
                s = 'and   '
            else:
                s = 'where '
            stack.append(len(result))
            stackcnt[(-1)] += 1
            stackcnt.append(0)
            result.append(' +' + '  ' * (len(stack) - 1) + s + line[1:])
        elif line.startswith('}'):
            stack.pop()
            stackcnt.pop()
            result[stack[(-1)]] += line[1:]
        else:
            assert line[0] in ('~', '>')
            stack[(-1)] += 1
            indent = len(stack) if line.startswith('~') else len(stack) - 1
            result.append('  ' * indent + line[1:])

    assert len(stack) == 1
    return result


try:
    basestring = basestring
except NameError:
    basestring = str

def assertrepr_compare(config, op, left, right):
    """Return specialised explanations for some operators/operands"""
    width = 65 - len(op) - 2
    left_repr = saferepr(left, maxsize=int(width // 2))
    right_repr = saferepr(right, maxsize=width - len(left_repr))
    summary = '%s %s %s' % (ecu(left_repr), op, ecu(right_repr))

    def issequence(x):
        return isinstance(x, Sequence) and not isinstance(x, basestring)

    def istext(x):
        return isinstance(x, basestring)

    def isdict(x):
        return isinstance(x, dict)

    def isset(x):
        return isinstance(x, (set, frozenset))

    def isdatacls(obj):
        return getattr(obj, '__dataclass_fields__', None) is not None

    def isattrs(obj):
        return getattr(obj, '__attrs_attrs__', None) is not None

    def isiterable(obj):
        try:
            iter(obj)
            return not istext(obj)
        except TypeError:
            return False

    verbose = config.getoption('verbose')
    explanation = None
    try:
        if op == '==':
            if istext(left) and istext(right):
                explanation = _diff_text(left, right, verbose)
            else:
                if issequence(left) and issequence(right):
                    explanation = _compare_eq_sequence(left, right, verbose)
                elif isset(left) and isset(right):
                    explanation = _compare_eq_set(left, right, verbose)
                elif isdict(left) and isdict(right):
                    explanation = _compare_eq_dict(left, right, verbose)
                elif type(left) == type(right) and (isdatacls(left) or isattrs(left)):
                    type_fn = (
                     isdatacls, isattrs)
                    explanation = _compare_eq_cls(left, right, verbose, type_fn)
                elif verbose:
                    explanation = _compare_eq_verbose(left, right)
                if isiterable(left) and isiterable(right):
                    expl = _compare_eq_iterable(left, right, verbose)
                    if explanation is not None:
                        explanation.extend(expl)
                    else:
                        explanation = expl
        elif op == 'not in':
            if istext(left) and istext(right):
                explanation = _notin_text(left, right, verbose)
    except Exception:
        explanation = [
         '(pytest_assertion plugin: representation of details failed.  Probably an object has a faulty __repr__.)',
         six.text_type(_pytest._code.ExceptionInfo.from_current())]

    if not explanation:
        return
    else:
        return [
         summary] + explanation


def _diff_text(left, right, verbose=False):
    """Return the explanation for the diff between text or bytes

    Unless --verbose is used this will skip leading and trailing
    characters which are identical to keep the diff minimal.

    If the input are bytes they will be safely converted to text.
    """
    from difflib import ndiff
    explanation = []

    def escape_for_readable_diff(binary_text):
        """
        Ensures that the internal string is always valid unicode, converting any bytes safely to valid unicode.
        This is done using repr() which then needs post-processing to fix the encompassing quotes and un-escape
        newlines and carriage returns (#429).
        """
        r = six.text_type(repr(binary_text)[1:-1])
        r = r.replace('\\n', '\n')
        r = r.replace('\\r', '\r')
        return r

    if isinstance(left, bytes):
        left = escape_for_readable_diff(left)
    if isinstance(right, bytes):
        right = escape_for_readable_diff(right)
    if not verbose:
        i = 0
        for i in range(min(len(left), len(right))):
            if left[i] != right[i]:
                break

        if i > 42:
            i -= 10
            explanation = [
             'Skipping %s identical leading characters in diff, use -v to show' % i]
            left = left[i:]
            right = right[i:]
        if len(left) == len(right):
            for i in range(len(left)):
                if left[(-i)] != right[(-i)]:
                    break

            if i > 42:
                i -= 10
                explanation += [
                 ('Skipping {} identical trailing characters in diff, use -v to show').format(i)]
                left = left[:-i]
                right = right[:-i]
    keepends = True
    if left.isspace() or right.isspace():
        left = repr(str(left))
        right = repr(str(right))
        explanation += ['Strings contain only whitespace, escaping them using repr()']
    explanation += [ line.strip('\n') for line in ndiff(left.splitlines(keepends), right.splitlines(keepends))
                   ]
    return explanation


def _compare_eq_verbose(left, right):
    keepends = True
    left_lines = repr(left).splitlines(keepends)
    right_lines = repr(right).splitlines(keepends)
    explanation = []
    explanation += [ '-' + line for line in left_lines ]
    explanation += [ '+' + line for line in right_lines ]
    return explanation


def _compare_eq_iterable(left, right, verbose=False):
    if not verbose:
        return ['Use -v to get the full diff']
    import difflib
    try:
        left_formatting = pprint.pformat(left).splitlines()
        right_formatting = pprint.pformat(right).splitlines()
        explanation = ['Full diff:']
    except Exception:
        left_formatting = sorted(repr(x) for x in left)
        right_formatting = sorted(repr(x) for x in right)
        explanation = ['Full diff (fallback to calling repr on each item):']

    explanation.extend(line.strip() for line in difflib.ndiff(left_formatting, right_formatting))
    return explanation


def _compare_eq_sequence(left, right, verbose=False):
    explanation = []
    for i in range(min(len(left), len(right))):
        if left[i] != right[i]:
            explanation += ['At index %s diff: %r != %r' % (i, left[i], right[i])]
            break

    if len(left) > len(right):
        explanation += [
         'Left contains more items, first extra item: %s' % saferepr(left[len(right)])]
    elif len(left) < len(right):
        explanation += [
         'Right contains more items, first extra item: %s' % saferepr(right[len(left)])]
    return explanation


def _compare_eq_set(left, right, verbose=False):
    explanation = []
    diff_left = left - right
    diff_right = right - left
    if diff_left:
        explanation.append('Extra items in the left set:')
        for item in diff_left:
            explanation.append(saferepr(item))

    if diff_right:
        explanation.append('Extra items in the right set:')
        for item in diff_right:
            explanation.append(saferepr(item))

    return explanation


def _compare_eq_dict(left, right, verbose=False):
    explanation = []
    common = set(left).intersection(set(right))
    same = {k:left[k] for k in common if left[k] == right[k]}
    if same and verbose < 2:
        explanation += ['Omitting %s identical items, use -vv to show' % len(same)]
    elif same:
        explanation += ['Common items:']
        explanation += pprint.pformat(same).splitlines()
    diff = {k for k in common if left[k] != right[k]}
    if diff:
        explanation += ['Differing items:']
        for k in diff:
            explanation += [saferepr({k: left[k]}) + ' != ' + saferepr({k: right[k]})]

    extra_left = set(left) - set(right)
    if extra_left:
        explanation.append('Left contains more items:')
        explanation.extend(pprint.pformat({k:left[k] for k in extra_left}).splitlines())
    extra_right = set(right) - set(left)
    if extra_right:
        explanation.append('Right contains more items:')
        explanation.extend(pprint.pformat({k:right[k] for k in extra_right}).splitlines())
    return explanation


def _compare_eq_cls(left, right, verbose, type_fns):
    isdatacls, isattrs = type_fns
    if isdatacls(left):
        all_fields = left.__dataclass_fields__
        fields_to_check = [ field for field, info in all_fields.items() if info.compare ]
    else:
        if isattrs(left):
            all_fields = left.__attrs_attrs__
            fields_to_check = [ field.name for field in all_fields if field.cmp ]
        same = []
        diff = []
        for field in fields_to_check:
            if getattr(left, field) == getattr(right, field):
                same.append(field)
            else:
                diff.append(field)

    explanation = []
    if same and verbose < 2:
        explanation.append('Omitting %s identical items, use -vv to show' % len(same))
    elif same:
        explanation += ['Matching attributes:']
        explanation += pprint.pformat(same).splitlines()
    if diff:
        explanation += ['Differing attributes:']
        for field in diff:
            explanation += [
             '%s: %r != %r' % (field, getattr(left, field), getattr(right, field))]

    return explanation


def _notin_text(term, text, verbose=False):
    index = text.find(term)
    head = text[:index]
    tail = text[index + len(term):]
    correct_text = head + tail
    diff = _diff_text(correct_text, text, verbose)
    newdiff = ['%s is contained here:' % saferepr(term, maxsize=42)]
    for line in diff:
        if line.startswith('Skipping'):
            continue
        if line.startswith('- '):
            continue
        if line.startswith('+ '):
            newdiff.append('  ' + line[2:])
        else:
            newdiff.append(line)

    return newdiff