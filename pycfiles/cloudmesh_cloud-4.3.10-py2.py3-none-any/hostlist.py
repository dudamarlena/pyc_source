# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/grey/.pyenv/versions/cm/lib/python2.7/site-packages/cloudmesh_client/common/hostlist.py
# Compiled at: 2017-04-23 10:30:41
__doc__ = 'Handle hostlist expressions.\nThis module provides operations to expand and collect hostlist\nexpressions.\nThe hostlist expression syntax is the same as in several programs\ndeveloped at LLNL (https://computing.llnl.gov/linux/). However in\ncorner cases the behaviour of this module have not been compared for\ncompatibility with pdsh/dshbak/SLURM et al.\n'
__version__ = '1.14'
import re, itertools

class BadHostlist(Exception):
    pass


MAX_SIZE = 100000

class Parameter(object):

    @classmethod
    def expand(cls, parameter, allow_duplicates=False, sort=False):
        return expand_hostlist(parameter, allow_duplicates=False, sort=False)


def expand_hostlist(hostlist, allow_duplicates=False, sort=False):
    """Expand a hostlist expression string to a Python list.
    Example: expand_hostlist("n[9-11],d[01-02]") ==>
             ['n9', 'n10', 'n11', 'd01', 'd02']
    Unless allow_duplicates is true, duplicates will be purged
    from the results. If sort is true, the output will be sorted.
    """
    results = []
    bracket_level = 0
    part = ''
    for c in hostlist + ',':
        if c == ',' and bracket_level == 0:
            if part:
                results.extend(expand_part(part))
            part = ''
            bad_part = False
        else:
            part += c
        if c == '[':
            bracket_level += 1
        elif c == ']':
            bracket_level -= 1
        if bracket_level > 1:
            raise BadHostlist('nested brackets')
        elif bracket_level < 0:
            raise BadHostlist('unbalanced brackets')

    if bracket_level > 0:
        raise BadHostlist('unbalanced brackets')
    if not allow_duplicates:
        results = remove_duplicates(results)
    if sort:
        results = numerically_sorted(results)
    return results


def expand_part(s):
    """Expand a part (e.g. "x[1-2]y[1-3][1-3]") (no outer level commas)."""
    if s == '':
        return ['']
    m = re.match('([^,\\[]*)(\\[[^\\]]*\\])?(.*)', s)
    prefix, rangelist, rest = m.group(1, 2, 3)
    rest_expanded = expand_part(rest)
    if not rangelist:
        us_expanded = [prefix]
    else:
        us_expanded = expand_rangelist(prefix, rangelist[1:-1])
    if len(us_expanded) * len(rest_expanded) > MAX_SIZE:
        raise BadHostlist('results too large')
    return [ us_part + rest_part for us_part in us_expanded for rest_part in rest_expanded
           ]


def expand_rangelist(prefix, rangelist):
    """ Expand a rangelist (e.g. "1-10,14"), putting a prefix before."""
    results = []
    for range_ in rangelist.split(','):
        results.extend(expand_range(prefix, range_))

    return results


def expand_range(prefix, range_):
    """ Expand a range (e.g. 1-10 or 14), putting a prefix before."""
    m = re.match('^[0-9]+$', range_)
    if m:
        return ['%s%s' % (prefix, range_)]
    m = re.match('^([0-9]+)-([0-9]+)$', range_)
    if not m:
        raise BadHostlist('bad range')
    s_low, s_high = m.group(1, 2)
    low = int(s_low)
    high = int(s_high)
    width = len(s_low)
    if high < low:
        raise BadHostlist('start > stop')
    else:
        if high - low > MAX_SIZE:
            raise BadHostlist('range too large')
        results = []
        for i in xrange(low, high + 1):
            results.append('%s%0*d' % (prefix, width, i))

    return results


def remove_duplicates(l):
    """Remove duplicates from a list (but keep the order)."""
    seen = set()
    results = []
    for e in l:
        if e not in seen:
            results.append(e)
            seen.add(e)

    return results


def collect_hostlist(hosts, silently_discard_bad=False):
    """Collect a hostlist string from a Python list of hosts.
    We start grouping from the rightmost numerical part.
    Duplicates are removed.
    A bad hostname raises an exception (unless silently_discard_bad
    is true causing the bad hostname to be silently discarded instead).
    """
    left_right = []
    for host in hosts:
        host = host.strip()
        if host == '':
            continue
        if re.search('[][,]', host):
            if silently_discard_bad:
                continue
            else:
                raise BadHostlist('forbidden character')
        left_right.append((host, ''))

    looping = True
    while looping:
        left_right, looping = collect_hostlist_1(left_right)

    return (',').join([ left + right for left, right in left_right ])


def collect_hostlist_1(left_right):
    """Collect a hostlist string from a list of hosts (left+right).
    The input is a list of tuples (left, right). The left part
    is analyzed, while the right part is just passed along
    (it can contain already collected range expressions).
    """
    sortlist = []
    remaining = set()
    for left, right in left_right:
        host = left + right
        remaining.add(host)
        m = re.match('^(.*?)([0-9]+)?([^0-9]*)$', left)
        prefix, num_str, suffix = m.group(1, 2, 3)
        suffix = suffix + right
        if num_str is None:
            assert prefix == ''
            sortlist.append(((host, None), None, None, host))
        else:
            num_int = int(num_str)
            num_width = len(num_str)
            sortlist.append(((prefix, suffix), num_int, num_width, host))

    sortlist.sort()
    results = []
    needs_another_loop = False
    for (prefix, suffix), group in itertools.groupby(sortlist, key=lambda x: x[0]):
        if suffix is None:
            results.append(('', prefix))
            remaining.remove(prefix)
        else:
            range_list = []
            for (prefix2, suffix2), num_int, num_width, host in group:
                if host not in remaining:
                    continue
                assert num_int is not None
                low = num_int
                while True:
                    host = '%s%0*d%s' % (prefix, num_width, num_int, suffix)
                    if host in remaining:
                        remaining.remove(host)
                        num_int += 1
                    else:
                        break

                high = num_int - 1
                assert high >= low
                range_list.append((low, high, num_width))

            needs_another_loop = True
            if len(range_list) == 1 and range_list[0][0] == range_list[0][1]:
                results.append((prefix,
                 '%0*d%s' % (
                  range_list[0][2], range_list[0][0], suffix)))
            else:
                results.append((prefix,
                 '[' + (',').join([ format_range(l, h, w) for l, h, w in range_list ]) + ']' + suffix))

    assert not remaining
    return (
     results, needs_another_loop)


def format_range(low, high, width):
    """Format a range from low to high inclusively, with a certain width."""
    if low == high:
        return '%0*d' % (width, low)
    else:
        return '%0*d-%0*d' % (width, low, width, high)


def numerically_sorted(l):
    """Sort a list of hosts numerically.
    E.g. sorted order should be n1, n2, n10; not n1, n10, n2.
    """
    return sorted(l, key=numeric_sort_key)


nsk_re = re.compile('([0-9]+)|([^0-9]+)')

def numeric_sort_key(x):
    return [ handle_int_nonint(i_ni) for i_ni in nsk_re.findall(x) ]


def handle_int_nonint(int_nonint_tuple):
    if int_nonint_tuple[0]:
        return int(int_nonint_tuple[0])
    else:
        return int_nonint_tuple[1]


def parse_slurm_tasks_per_node(s):
    res = []
    for part in s.split(','):
        m = re.match('^([0-9]+)(\\(x([0-9]+)\\))?$', part)
        if m:
            tasks = int(m.group(1))
            repetitions = m.group(3)
            if repetitions is None:
                repetitions = 1
            else:
                repetitions = int(repetitions)
            if repetitions > MAX_SIZE:
                raise BadHostlist('task list repetitions too large')
            for i in range(repetitions):
                res.append(tasks)

        else:
            raise BadHostlist('bad task list syntax')

    return res


if __name__ == '__main__':
    import os, sys
    sys.stderr.write("The command line utility has been moved to a separate 'hostlist' program.\n")
    sys.exit(os.EX_USAGE)