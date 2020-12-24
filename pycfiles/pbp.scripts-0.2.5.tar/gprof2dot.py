# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Volumes/MacDev/perso/atomisator.ziade.org/packages/pbp.scripts/pbp/scripts/gprof2dot.py
# Compiled at: 2008-08-24 07:21:32
"""Generate a dot graph from the output of several profilers."""
__author__ = 'Jose Fonseca'
__version__ = '1.0'
import sys, os.path, re, textwrap, optparse
try:
    import debug
except ImportError:
    pass

def percentage(p):
    return '%.02f%%' % (p * 100.0,)


def add(a, b):
    return a + b


def equal(a, b):
    if a == b:
        return a
    else:
        return
    return


def fail(a, b):
    assert False


def ratio(numerator, denominator):
    numerator = float(numerator)
    denominator = float(denominator)
    assert 0.0 <= numerator
    assert numerator <= denominator
    try:
        return numerator / denominator
    except ZeroDivisionError:
        return 1.0


class UndefinedEvent(Exception):
    """Raised when attempting to get an event which is undefined."""
    __module__ = __name__

    def __init__(self, event):
        Exception.__init__(self)
        self.event = event

    def __str__(self):
        return 'unspecified event %s' % self.event.name


class Event(object):
    """Describe a kind of event, and its basic operations."""
    __module__ = __name__

    def __init__(self, name, null, aggregator, formatter=str):
        self.name = name
        self._null = null
        self._aggregator = aggregator
        self._formatter = formatter

    def __eq__(self, other):
        return self is other

    def __hash__(self):
        return id(self)

    def null(self):
        return self._null

    def aggregate(self, val1, val2):
        """Aggregate two event values."""
        assert val1 is not None
        assert val2 is not None
        return self._aggregator(val1, val2)

    def format(self, val):
        """Format an event value."""
        assert val is not None
        return self._formatter(val)


MODULE = Event('Module', None, equal)
PROCESS = Event('Process', None, equal)
CALLS = Event('Calls', 0, add)
SAMPLES = Event('Samples', 0, add)
TIME = Event('Time', 0.0, add, lambda x: '(' + str(x) + ')')
TIME_RATIO = Event('Time ratio', 0.0, add, lambda x: '(' + percentage(x) + ')')
TOTAL_TIME = Event('Total time', 0.0, fail)
TOTAL_TIME_RATIO = Event('Total time ratio', 0.0, fail, percentage)
CALL_RATIO = Event('Call ratio', 0.0, add, percentage)
PRUNE_RATIO = Event('Prune ratio', 0.0, add, percentage)

class Object(object):
    """Base class for all objects in profile which can store events."""
    __module__ = __name__

    def __init__(self, events=None):
        if events is None:
            self.events = {}
        else:
            self.events = events
        return

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self is other

    def __contains__(self, event):
        return event in self.events

    def __getitem__(self, event):
        try:
            return self.events[event]
        except KeyError:
            raise UndefinedEvent(event)

    def __setitem__(self, event, value):
        if value is None:
            if event in self.events:
                del self.events[event]
        else:
            self.events[event] = value
        return


class Call(Object):
    """A call between functions.
    
    There should be at most one call object for every pair of functions.
    """
    __module__ = __name__

    def __init__(self, callee_id):
        Object.__init__(self)
        self.callee_id = callee_id


class Function(Object):
    """A function."""
    __module__ = __name__

    def __init__(self, id, name):
        Object.__init__(self)
        self.id = id
        self.name = name
        self.calls = {}
        self.cycle = None
        return

    def add_call(self, call):
        if call.callee_id in self.calls:
            sys.stderr.write('warning: overwriting call from function %s to %s\n' % (str(self.id), str(call.callee_id)))
        self.calls[call.callee_id] = call

    def __repr__(self):
        return self.name


class Cycle(Object):
    """A cycle made from recursive function calls."""
    __module__ = __name__

    def __init__(self):
        Object.__init__(self)
        self.functions = set()

    def add_function(self, function):
        assert function not in self.functions
        self.functions.add(function)
        if function.cycle is not None:
            for other in function.cycle.functions:
                if function not in self.functions:
                    self.add_function(other)

        function.cycle = self
        return


class Profile(Object):
    """The whole profile."""
    __module__ = __name__

    def __init__(self):
        Object.__init__(self)
        self.functions = {}
        self.cycles = []

    def add_function(self, function):
        if function.id in self.functions:
            sys.stderr.write('warning: overwriting function %s (id %s)\n' % (function.name, str(function.id)))
        self.functions[function.id] = function

    def add_cycle(self, cycle):
        self.cycles.append(cycle)

    def validate(self):
        """Validate the edges."""
        for function in self.functions.itervalues():
            for callee_id in function.calls.keys():
                assert function.calls[callee_id].callee_id == callee_id
                if callee_id not in self.functions:
                    sys.stderr.write('warning: call to undefined function %s from function %s\n' % (str(callee_id), function.name))
                    del function.calls[callee_id]

    def find_cycles(self):
        """Find cycles using Tarjan's strongly connected components algorithm."""
        visited = set()
        for function in self.functions.itervalues():
            if function not in visited:
                self._tarjan(function, 0, [], {}, {}, visited)

        cycles = []
        for function in self.functions.itervalues():
            if function.cycle is not None and function.cycle not in cycles:
                cycles.append(function.cycle)

        self.cycles = cycles
        return

    def _tarjan(self, function, order, stack, orders, lowlinks, visited):
        """Tarjan's strongly connected components algorithm.

        See also:
        - http://en.wikipedia.org/wiki/Tarjan's_strongly_connected_components_algorithm
        """
        visited.add(function)
        orders[function] = order
        lowlinks[function] = order
        order += 1
        pos = len(stack)
        stack.append(function)
        for call in function.calls.itervalues():
            callee = self.functions[call.callee_id]
            if callee not in orders:
                order = self._tarjan(callee, order, stack, orders, lowlinks, visited)
                lowlinks[function] = min(lowlinks[function], lowlinks[callee])
            elif callee in stack:
                lowlinks[function] = min(lowlinks[function], orders[callee])

        if lowlinks[function] == orders[function]:
            members = stack[pos:]
            del stack[pos:]
            if len(members) > 1:
                cycle = Cycle()
                for member in members:
                    cycle.add_function(member)

        return order

    def call_ratios(self, event):
        cycle_totals = {}
        for cycle in self.cycles:
            cycle_totals[cycle] = 0.0

        function_totals = {}
        for function in self.functions.itervalues():
            function_totals[function] = 0.0

        for function in self.functions.itervalues():
            for call in function.calls.itervalues():
                if call.callee_id != function.id:
                    callee = self.functions[call.callee_id]
                    function_totals[callee] += call[event]
                    if callee.cycle is not None and callee.cycle is not function.cycle:
                        cycle_totals[callee.cycle] += call[event]

        for function in self.functions.itervalues():
            for call in function.calls.itervalues():
                assert CALL_RATIO not in call
                if call.callee_id != function.id:
                    callee = self.functions[call.callee_id]
                    if callee.cycle is not None and callee.cycle is not function.cycle:
                        total = cycle_totals[callee.cycle]
                    else:
                        total = function_totals[callee]
                    call[CALL_RATIO] = ratio(call[event], total)

        return

    def integrate(self, outevent, inevent):
        """Propagate function time ratio allong the function calls.

        Must be called after finding the cycles.

        See also:
        - http://citeseer.ist.psu.edu/graham82gprof.html
        """
        assert outevent not in self
        for function in self.functions.itervalues():
            assert outevent not in function
            assert inevent in function
            for call in function.calls.itervalues():
                assert outevent not in call
                if call.callee_id != function.id:
                    assert CALL_RATIO in call

        for cycle in self.cycles:
            total = inevent.null()
            for function in self.functions.itervalues():
                total = inevent.aggregate(total, function[inevent])

            self[inevent] = total

        total = inevent.null()
        for function in self.functions.itervalues():
            total = inevent.aggregate(total, function[inevent])
            self._integrate_function(function, outevent, inevent)

        self[outevent] = total

    def _integrate_function(self, function, outevent, inevent):
        if function.cycle is not None:
            return self._integrate_cycle(function.cycle, outevent, inevent)
        else:
            if outevent not in function:
                total = function[inevent]
                for call in function.calls.itervalues():
                    if call.callee_id != function.id:
                        total += self._integrate_call(call, outevent, inevent)

                function[outevent] = total
            return function[outevent]
        return

    def _integrate_call(self, call, outevent, inevent):
        assert outevent not in call
        assert CALL_RATIO in call
        callee = self.functions[call.callee_id]
        subtotal = call[CALL_RATIO] * self._integrate_function(callee, outevent, inevent)
        call[outevent] = subtotal
        return subtotal

    def _integrate_cycle(self, cycle, outevent, inevent):
        if outevent not in cycle:
            total = inevent.null()
            for member in cycle.functions:
                subtotal = member[inevent]
                for call in member.calls.itervalues():
                    callee = self.functions[call.callee_id]
                    if callee.cycle is not cycle:
                        subtotal += self._integrate_call(call, outevent, inevent)

                total += subtotal

            cycle[outevent] = total
            callees = {}
            for function in self.functions.itervalues():
                if function.cycle is not cycle:
                    for call in function.calls.itervalues():
                        callee = self.functions[call.callee_id]
                        if callee.cycle is cycle:
                            try:
                                callees[callee] += call[CALL_RATIO]
                            except KeyError:
                                callees[callee] = call[CALL_RATIO]

            for (callee, call_ratio) in callees.iteritems():
                ranks = {}
                call_ratios = {}
                partials = {}
                self._rank_cycle_function(cycle, callee, 0, ranks)
                self._call_ratios_cycle(cycle, callee, ranks, call_ratios, set())
                partial = self._integrate_cycle_function(cycle, callee, call_ratio, partials, ranks, call_ratios, outevent, inevent)
                assert partial == max(partials.values())
                assert not total or abs(1.0 - partial / (call_ratio * total)) <= 0.001

        return cycle[outevent]

    def _rank_cycle_function(self, cycle, function, rank, ranks):
        if function not in ranks or ranks[function] > rank:
            ranks[function] = rank
            for call in function.calls.itervalues():
                if call.callee_id != function.id:
                    callee = self.functions[call.callee_id]
                    if callee.cycle is cycle:
                        self._rank_cycle_function(cycle, callee, rank + 1, ranks)

    def _call_ratios_cycle(self, cycle, function, ranks, call_ratios, visited):
        if function not in visited:
            visited.add(function)
            for call in function.calls.itervalues():
                if call.callee_id != function.id:
                    callee = self.functions[call.callee_id]
                    if callee.cycle is cycle:
                        if ranks[callee] > ranks[function]:
                            call_ratios[callee] = call_ratios.get(callee, 0.0) + call[CALL_RATIO]
                            self._call_ratios_cycle(cycle, callee, ranks, call_ratios, visited)

    def _integrate_cycle_function(self, cycle, function, partial_ratio, partials, ranks, call_ratios, outevent, inevent):
        if function not in partials:
            partial = partial_ratio * function[inevent]
            for call in function.calls.itervalues():
                if call.callee_id != function.id:
                    callee = self.functions[call.callee_id]
                    if callee.cycle is not cycle:
                        assert outevent in call
                        partial += partial_ratio * call[outevent]
                    elif ranks[callee] > ranks[function]:
                        callee_partial = self._integrate_cycle_function(cycle, callee, partial_ratio, partials, ranks, call_ratios, outevent, inevent)
                        call_ratio = ratio(call[CALL_RATIO], call_ratios[callee])
                        call_partial = call_ratio * callee_partial
                        try:
                            call[outevent] += call_partial
                        except UndefinedEvent:
                            call[outevent] = call_partial
                        else:
                            partial += call_partial

            partials[function] = partial
            try:
                function[outevent] += partial
            except UndefinedEvent:
                function[outevent] = partial

        return partials[function]

    def aggregate(self, event):
        """Aggregate an event for the whole profile."""
        total = event.null()
        for function in self.functions.itervalues():
            try:
                total = event.aggregate(total, function[event])
            except UndefinedEvent:
                return

        self[event] = total

    def ratio(self, outevent, inevent):
        assert outevent not in self
        assert inevent in self
        for function in self.functions.itervalues():
            assert outevent not in function
            assert inevent in function
            function[outevent] = ratio(function[inevent], self[inevent])
            for call in function.calls.itervalues():
                assert outevent not in call
                if inevent in call:
                    call[outevent] = ratio(call[inevent], self[inevent])

        self[outevent] = 1.0

    def prune(self, node_thres, edge_thres):
        """Prune the profile"""
        for function in self.functions.itervalues():
            try:
                function[PRUNE_RATIO] = function[TOTAL_TIME_RATIO]
            except UndefinedEvent:
                pass

            for call in function.calls.itervalues():
                callee = self.functions[call.callee_id]
                if TOTAL_TIME_RATIO in call:
                    call[PRUNE_RATIO] = call[TOTAL_TIME_RATIO]
                else:
                    try:
                        call[PRUNE_RATIO] = min(function[TOTAL_TIME_RATIO], callee[TOTAL_TIME_RATIO])
                    except UndefinedEvent:
                        pass

        for function_id in self.functions.keys():
            function = self.functions[function_id]
            try:
                if function[PRUNE_RATIO] < node_thres:
                    del self.functions[function_id]
            except UndefinedEvent:
                pass

        for function in self.functions.itervalues():
            for callee_id in function.calls.keys():
                call = function.calls[callee_id]
                try:
                    if callee_id not in self.functions or call[PRUNE_RATIO] < edge_thres:
                        del function.calls[callee_id]
                except UndefinedEvent:
                    pass

    def dump(self):
        for function in self.functions.itervalues():
            sys.stderr.write('Function %s:\n' % (function.name,))
            self._dump_events(function.events)
            for call in function.calls.itervalues():
                callee = self.functions[call.callee_id]
                sys.stderr.write('  Call %s:\n' % (callee.name,))
                self._dump_events(call.events)

    def _dump_events(self, events):
        for (event, value) in events.iteritems():
            sys.stderr.write('    %s: %s\n' % (event.name, event.format(value)))


class Struct:
    """Masquerade a dictionary with a structure-like behavior."""
    __module__ = __name__

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        self.__dict__['_attrs'] = attrs
        return

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self._attrs[name] = value

    def __str__(self):
        return str(self._attrs)

    def __repr__(self):
        return repr(self._attrs)


class ParseError(Exception):
    """Raised when parsing to signal mismatches."""
    __module__ = __name__

    def __init__(self, msg, line):
        self.msg = msg
        self.line = line

    def __str__(self):
        return '%s: %r' % (self.msg, self.line)


class Parser:
    """Parser interface."""
    __module__ = __name__

    def __init__(self):
        pass

    def parse(self):
        raise NotImplementedError


class LineParser(Parser):
    """Base class for parsers that read line-based formats."""
    __module__ = __name__

    def __init__(self, file):
        Parser.__init__(self)
        self._file = file
        self.__line = None
        self.__eof = False
        return

    def readline(self):
        line = self._file.readline()
        if not line:
            self.__line = ''
            self.__eof = True
        self.__line = line.rstrip('\r\n')

    def lookahead(self):
        assert self.__line is not None
        return self.__line

    def consume(self):
        assert self.__line is not None
        line = self.__line
        self.readline()
        return line

    def eof(self):
        assert self.__line is not None
        return self.__eof


class GprofParser(Parser):
    """Parser for GNU gprof output.

    See also:
    - Chapter "Interpreting gprof's Output" from the GNU gprof manual
      http://sourceware.org/binutils/docs-2.18/gprof/Call-Graph.html#Call-Graph
    - File "cg_print.c" from the GNU gprof source code
      http://sourceware.org/cgi-bin/cvsweb.cgi/~checkout~/src/gprof/cg_print.c?rev=1.12&cvsroot=src
    """
    __module__ = __name__

    def __init__(self, fp):
        Parser.__init__(self)
        self.fp = fp
        self.functions = {}
        self.cycles = {}

    def readline(self):
        line = self.fp.readline()
        if not line:
            sys.stderr.write('error: unexpected end of file\n')
            sys.exit(1)
        line = line.rstrip('\r\n')
        return line

    _int_re = re.compile('^\\d+$')
    _float_re = re.compile('^\\d+\\.\\d+$')

    def translate(self, mo):
        """Extract a structure from a match object, while translating the types in the process."""
        attrs = {}
        groupdict = mo.groupdict()
        for (name, value) in groupdict.iteritems():
            if value is None:
                value = None
            elif self._int_re.match(value):
                value = int(value)
            elif self._float_re.match(value):
                value = float(value)
            attrs[name] = value

        return Struct(attrs)

    _cg_header_re = re.compile('^\\s+called/total\\s+parents\\s*$|' + '^index\\s+%time\\s+self\\s+descendents\\s+called\\+self\\s+name\\s+index\\s*$|' + '^\\s+called/total\\s+children\\s*$|' + '^index\\s+%\\s+time\\s+self\\s+children\\s+called\\s+name\\s*$')
    _cg_ignore_re = re.compile('^\\s+<spontaneous>\\s*$|^.*\\((\\d+)\\)$')
    _cg_primary_re = re.compile('^\\[(?P<index>\\d+)\\]' + '\\s+(?P<percentage_time>\\d+\\.\\d+)' + '\\s+(?P<self>\\d+\\.\\d+)' + '\\s+(?P<descendants>\\d+\\.\\d+)' + '\\s+(?:(?P<called>\\d+)(?:\\+(?P<called_self>\\d+))?)?' + '\\s+(?P<name>\\S.*?)' + '(?:\\s+<cycle\\s(?P<cycle>\\d+)>)?' + '\\s\\[(\\d+)\\]$')
    _cg_parent_re = re.compile('^\\s+(?P<self>\\d+\\.\\d+)?' + '\\s+(?P<descendants>\\d+\\.\\d+)?' + '\\s+(?P<called>\\d+)(?:/(?P<called_total>\\d+))?' + '\\s+(?P<name>\\S.*?)' + '(?:\\s+<cycle\\s(?P<cycle>\\d+)>)?' + '\\s\\[(?P<index>\\d+)\\]$')
    _cg_child_re = _cg_parent_re
    _cg_cycle_header_re = re.compile('^\\[(?P<index>\\d+)\\]' + '\\s+(?P<percentage_time>\\d+\\.\\d+)' + '\\s+(?P<self>\\d+\\.\\d+)' + '\\s+(?P<descendants>\\d+\\.\\d+)' + '\\s+(?:(?P<called>\\d+)(?:\\+(?P<called_self>\\d+))?)?' + '\\s+<cycle\\s(?P<cycle>\\d+)\\sas\\sa\\swhole>' + '\\s\\[(\\d+)\\]$')
    _cg_cycle_member_re = re.compile('^\\s+(?P<self>\\d+\\.\\d+)?' + '\\s+(?P<descendants>\\d+\\.\\d+)?' + '\\s+(?P<called>\\d+)(?:\\+(?P<called_self>\\d+))?' + '\\s+(?P<name>\\S.*?)' + '(?:\\s+<cycle\\s(?P<cycle>\\d+)>)?' + '\\s\\[(?P<index>\\d+)\\]$')
    _cg_sep_re = re.compile('^--+$')

    def parse_function_entry(self, lines):
        parents = []
        children = []
        while True:
            if not lines:
                sys.stderr.write('warning: unexpected end of entry\n')
            line = lines.pop(0)
            if line.startswith('['):
                break
            mo = self._cg_parent_re.match(line)
            if not mo:
                if self._cg_ignore_re.match(line):
                    continue
                sys.stderr.write('warning: unrecognized call graph entry: %r\n' % line)
            else:
                parent = self.translate(mo)
                parents.append(parent)

        mo = self._cg_primary_re.match(line)
        if not mo:
            sys.stderr.write('warning: unrecognized call graph entry: %r\n' % line)
            return
        else:
            function = self.translate(mo)
        while lines:
            line = lines.pop(0)
            mo = self._cg_child_re.match(line)
            if not mo:
                if self._cg_ignore_re.match(line):
                    continue
                sys.stderr.write('warning: unrecognized call graph entry: %r\n' % line)
            else:
                child = self.translate(mo)
                children.append(child)

        function.parents = parents
        function.children = children
        self.functions[function.index] = function

    def parse_cycle_entry(self, lines):
        line = lines[0]
        mo = self._cg_cycle_header_re.match(line)
        if not mo:
            sys.stderr.write('warning: unrecognized call graph entry: %r\n' % line)
            return
        cycle = self.translate(mo)
        cycle.functions = []
        for line in lines[1:]:
            mo = self._cg_cycle_member_re.match(line)
            if not mo:
                sys.stderr.write('warning: unrecognized call graph entry: %r\n' % line)
                continue
            call = self.translate(mo)
            cycle.functions.append(call)

        self.cycles[cycle.cycle] = cycle

    def parse_cg_entry(self, lines):
        if lines[0].startswith('['):
            self.parse_cycle_entry(lines)
        else:
            self.parse_function_entry(lines)

    def parse_cg(self):
        """Parse the call graph."""
        while not self._cg_header_re.match(self.readline()):
            pass

        line = self.readline()
        while self._cg_header_re.match(line):
            line = self.readline()

        entry_lines = []
        while line != '\x0c':
            if line and not line.isspace():
                if self._cg_sep_re.match(line):
                    self.parse_cg_entry(entry_lines)
                    entry_lines = []
                else:
                    entry_lines.append(line)
            line = self.readline()

    def parse(self):
        self.parse_cg()
        self.fp.close()
        profile = Profile()
        profile[TIME] = 0.0
        cycles = {}
        for index in self.cycles.iterkeys():
            cycles[index] = Cycle()

        for entry in self.functions.itervalues():
            function = Function(entry.index, entry.name)
            function[TIME] = entry.self
            if entry.called is not None:
                function[CALLS] = entry.called
            if entry.called_self is not None:
                call = Call(entry.index)
                call[CALLS] = entry.called_self
                function[CALLS] += entry.called_self
            for child in entry.children:
                call = Call(child.index)
                assert child.called is not None
                call[CALLS] = child.called
                if child.index not in self.functions:
                    missing = Function(child.index, child.name)
                    function[TIME] = 0.0
                    function[CALLS] = 0
                    profile.add_function(missing)
                function.add_call(call)

            profile.add_function(function)
            if entry.cycle is not None:
                cycles[entry.cycle].add_function(function)
            profile[TIME] = profile[TIME] + function[TIME]

        for cycle in cycles.itervalues():
            profile.add_cycle(cycle)

        profile.validate()
        profile.ratio(TIME_RATIO, TIME)
        profile.call_ratios(CALLS)
        profile.integrate(TOTAL_TIME, TIME)
        profile.ratio(TOTAL_TIME_RATIO, TOTAL_TIME)
        return profile


class OprofileParser(LineParser):
    """Parser for oprofile callgraph output.
    
    See also:
    - http://oprofile.sourceforge.net/doc/opreport.html#opreport-callgraph
    """
    __module__ = __name__
    _fields_re = {'samples': '(?P<samples>\\d+)', '%': '(?P<percentage>\\S+)', 'linenr info': '(?P<source>\\(no location information\\)|\\S+:\\d+)', 'image name': '(?P<image>\\S+(?:\\s\\(tgid:[^)]*\\))?)', 'app name': '(?P<application>\\S+)', 'symbol name': '(?P<symbol>\\(no symbols\\)|.+?)'}

    def __init__(self, infile):
        LineParser.__init__(self, infile)
        self.entries = {}
        self.entry_re = None
        return

    def add_entry(self, callers, function, callees):
        try:
            entry = self.entries[function.id]
        except KeyError:
            self.entries[function.id] = (
             callers, function, callees)
        else:
            (callers_total, function_total, callees_total) = entry
            self.update_subentries_dict(callers_total, callers)
            function_total.samples += function.samples
            self.update_subentries_dict(callees_total, callees)

    def update_subentries_dict(self, totals, partials):
        for partial in partials.itervalues():
            try:
                total = totals[partial.id]
            except KeyError:
                totals[partial.id] = partial
            else:
                total.samples += partial.samples

    def parse(self):
        self.readline()
        self.parse_header()
        while self.lookahead():
            self.parse_entry()

        profile = Profile()
        reverse_call_samples = {}
        profile[SAMPLES] = 0
        for (_callers, _function, _callees) in self.entries.itervalues():
            function = Function(_function.id, _function.name)
            function[SAMPLES] = _function.samples
            profile.add_function(function)
            profile[SAMPLES] += _function.samples
            if _function.application:
                function[PROCESS] = os.path.basename(_function.application)
            if _function.image:
                function[MODULE] = os.path.basename(_function.image)
            total_callee_samples = 0
            for _callee in _callees.itervalues():
                total_callee_samples += _callee.samples

            for _callee in _callees.itervalues():
                if not _callee.self:
                    call = Call(_callee.id)
                    call[SAMPLES] = _callee.samples
                    function.add_call(call)

        profile.validate()
        profile.find_cycles()
        profile.ratio(TIME_RATIO, SAMPLES)
        profile.call_ratios(SAMPLES)
        profile.integrate(TOTAL_TIME_RATIO, TIME_RATIO)
        return profile

    def parse_header(self):
        while not self.match_header():
            self.consume()

        line = self.lookahead()
        fields = re.split('\\s\\s+', line)
        entry_re = '^\\s*' + ('\\s+').join([ self._fields_re[field] for field in fields ]) + '(?P<self>\\s+\\[self\\])?$'
        self.entry_re = re.compile(entry_re)
        self.skip_separator()

    def parse_entry(self):
        callers = self.parse_subentries()
        if self.match_primary():
            function = self.parse_subentry()
            if function is not None:
                callees = self.parse_subentries()
                self.add_entry(callers, function, callees)
        self.skip_separator()
        return

    def parse_subentries(self):
        subentries = {}
        while self.match_secondary():
            subentry = self.parse_subentry()
            subentries[subentry.id] = subentry

        return subentries

    def parse_subentry(self):
        entry = Struct()
        line = self.consume()
        mo = self.entry_re.match(line)
        if not mo:
            raise ParseError('failed to parse', line)
        fields = mo.groupdict()
        entry.samples = int(fields.get('samples', 0))
        entry.percentage = float(fields.get('percentage', 0.0))
        if 'source' in fields and fields['source'] != '(no location information)':
            source = fields['source']
            (filename, lineno) = source.split(':')
            entry.filename = filename
            entry.lineno = int(lineno)
        else:
            source = ''
            entry.filename = None
            entry.lineno = None
        entry.image = fields.get('image', '')
        entry.application = fields.get('application', '')
        if 'symbol' in fields and fields['symbol'] != '(no symbols)':
            entry.symbol = fields['symbol']
        else:
            entry.symbol = ''
        if entry.symbol.startswith('"') and entry.symbol.endswith('"'):
            entry.symbol = entry.symbol[1:-1]
        entry.id = (':').join((entry.application, entry.image, source, entry.symbol))
        entry.self = fields.get('self', None) != None
        if entry.self:
            entry.id += ':self'
        if entry.symbol:
            entry.name = entry.symbol
        else:
            entry.name = entry.image
        return entry

    def skip_separator(self):
        while not self.match_separator():
            self.consume()

        self.consume()

    def match_header(self):
        line = self.lookahead()
        return line.startswith('samples')

    def match_separator(self):
        line = self.lookahead()
        return line == '-' * len(line)

    def match_primary(self):
        line = self.lookahead()
        return not line[:1].isspace()

    def match_secondary(self):
        line = self.lookahead()
        return line[:1].isspace()


class PstatsParser:
    """Parser python profiling statistics saved with te pstats module."""
    __module__ = __name__

    def __init__(self, *filename):
        import pstats
        self.stats = pstats.Stats(*filename)
        self.profile = Profile()
        self.function_ids = {}

    def get_function_name(self, (filename, line, name)):
        module = os.path.splitext(filename)[0]
        module = os.path.basename(module)
        return '%s:%d:%s' % (module, line, name)

    def get_function(self, key):
        try:
            id = self.function_ids[key]
        except KeyError:
            id = len(self.function_ids)
            name = self.get_function_name(key)
            function = Function(id, name)
            self.profile.functions[id] = function
            self.function_ids[key] = id
        else:
            function = self.profile.functions[id]

        return function

    def parse(self):
        self.profile[TIME] = 0.0
        self.profile[TOTAL_TIME] = self.stats.total_tt
        for (fn, (cc, nc, tt, ct, callers)) in self.stats.stats.iteritems():
            callee = self.get_function(fn)
            callee[CALLS] = nc
            callee[TOTAL_TIME] = ct
            callee[TIME] = tt
            self.profile[TIME] += tt
            self.profile[TOTAL_TIME] = max(self.profile[TOTAL_TIME], ct)
            for (fn, value) in callers.iteritems():
                caller = self.get_function(fn)
                call = Call(callee.id)
                if isinstance(value, tuple):
                    for i in xrange(0, len(value), 4):
                        (nc, cc, tt, ct) = value[i:i + 4]
                        if CALLS in call:
                            call[CALLS] += cc
                        else:
                            call[CALLS] = cc
                        if TOTAL_TIME in call:
                            call[TOTAL_TIME] += ct
                        else:
                            call[TOTAL_TIME] = ct

                else:
                    call[CALLS] = value
                    call[TOTAL_TIME] = ratio(value, nc) * ct
                caller.add_call(call)

        self.profile.validate()
        self.profile.ratio(TIME_RATIO, TIME)
        self.profile.ratio(TOTAL_TIME_RATIO, TOTAL_TIME)
        return self.profile


class DotWriter:
    """Writer for the DOT language.

    See also:
    - "The DOT Language" specification
      http://www.graphviz.org/doc/info/lang.html
    """
    __module__ = __name__

    def __init__(self, fp):
        self.fp = fp

    fontname = 'Arial'
    fontsize = '10'

    def graph(self, profile, colormap):
        self.begin_graph()
        self.attr('graph', fontname=self.fontname, fontsize=self.fontsize)
        self.attr('node', fontname=self.fontname, fontsize=self.fontsize, shape='box', style='filled', fontcolor='white')
        self.attr('edge', fontname=self.fontname, fontsize=self.fontsize)
        for function in profile.functions.itervalues():
            labels = []
            for event in (PROCESS, MODULE):
                if event in function.events:
                    label = event.format(function[event])
                    labels.append(label)

            labels.append(function.name)
            for event in (TOTAL_TIME_RATIO, TIME_RATIO, CALLS):
                if event in function.events:
                    label = event.format(function[event])
                    labels.append(label)

            try:
                color_ratio = function[PRUNE_RATIO]
            except UndefinedEvent:
                color_ratio = 0.0

            label = ('\n').join(labels)
            color = self.color(colormap(color_ratio))
            self.node(function.id, label=label, color=color)
            for call in function.calls.itervalues():
                callee = profile.functions[call.callee_id]
                labels = []
                for event in (TOTAL_TIME_RATIO, CALLS):
                    if event in call.events:
                        label = event.format(call[event])
                        labels.append(label)

                try:
                    color_ratio = call[PRUNE_RATIO]
                except UndefinedEvent:
                    try:
                        color_ratio = call[PRUNE_RATIO]
                    except UndefinedEvent:
                        color_ratio = 0.0

                label = ('\n').join(labels)
                color = self.color(colormap(color_ratio))
                self.edge(function.id, call.callee_id, label=label, color=color, fontcolor=color)

        self.end_graph()

    def begin_graph(self):
        self.write('digraph {\n')

    def end_graph(self):
        self.write('}\n')

    def attr(self, what, **attrs):
        self.write('\t')
        self.write(what)
        self.attr_list(attrs)
        self.write(';\n')

    def node(self, node, **attrs):
        self.write('\t')
        self.id(node)
        self.attr_list(attrs)
        self.write(';\n')

    def edge(self, src, dst, **attrs):
        self.write('\t')
        self.id(src)
        self.write(' -> ')
        self.id(dst)
        self.attr_list(attrs)
        self.write(';\n')

    def attr_list(self, attrs):
        if not attrs:
            return
        self.write(' [')
        first = True
        for (name, value) in attrs.iteritems():
            if first:
                first = False
            else:
                self.write(', ')
            self.id(name)
            self.write('=')
            self.id(value)

        self.write(']')

    def id(self, id):
        if isinstance(id, (int, float)):
            s = str(id)
        elif isinstance(id, str):
            if id.isalnum():
                s = id
            else:
                s = self.escape(id)
        else:
            raise TypeError
        self.write(s)

    def color(self, (r, g, b)):

        def float2int(f):
            if f <= 0.0:
                return 0
            if f >= 1.0:
                return 255
            return int(255.0 * f + 0.5)

        return '#' + ('').join([ '%02x' % float2int(c) for c in (r, g, b) ])

    def escape(self, s):
        s = s.replace('\\', '\\\\')
        s = s.replace('\n', '\\n')
        s = s.replace('\t', '\\t')
        s = s.replace('"', '\\"')
        return '"' + s + '"'

    def write(self, s):
        self.fp.write(s)


class ColorMap:
    """Color map."""
    __module__ = __name__

    def __init__(self, cmin, cmax, cpow=(1.0, 1.0, 1.0)):
        (self.hmin, self.smin, self.lmin) = cmin
        (self.hmax, self.smax, self.lmax) = cmax
        (self.hpow, self.spow, self.lpow) = cpow

    def __call__(self, ratio):
        """Map a ratio value into a RGB color."""
        ratio = min(max(ratio, 0.0), 1.0)
        h = self.hmin + ratio ** self.hpow * (self.hmax - self.hmin)
        s = self.smin + ratio ** self.spow * (self.smax - self.smin)
        l = self.lmin + ratio ** self.lpow * (self.lmax - self.lmin)
        return self.hsl_to_rgb(h, s, l)

    def hsl_to_rgb(self, h, s, l):
        """Convert a color from HSL color-model to RGB.

        See also:
        - http://www.w3.org/TR/css3-color/#hsl-color
        """
        h = h % 1.0
        s = min(max(s, 0.0), 1.0)
        l = min(max(l, 0.0), 1.0)
        if l <= 0.5:
            m2 = l * (s + 1.0)
        else:
            m2 = l + s - l * s
        m1 = l * 2.0 - m2
        r = self._hue_to_rgb(m1, m2, h + 1.0 / 3.0)
        g = self._hue_to_rgb(m1, m2, h)
        b = self._hue_to_rgb(m1, m2, h - 1.0 / 3.0)
        return (r, g, b)

    def _hue_to_rgb(self, m1, m2, h):
        if h < 0.0:
            h += 1.0
        elif h > 1.0:
            h -= 1.0
        if h * 6 < 1.0:
            return m1 + (m2 - m1) * h * 6.0
        elif h * 2 < 1.0:
            return m2
        elif h * 3 < 2.0:
            return m1 + (m2 - m1) * (2.0 / 3.0 - h) * 6.0
        else:
            return m1


TEMPERATURE_COLORMAP = ColorMap((2.0 / 3.0, 0.8, 0.25), (
 0.0, 1.0, 0.5), (
 0.5, 1.0, 1.0))
PINK_COLORMAP = ColorMap((0.0, 1.0, 0.9), (
 0.0, 1.0, 0.5), (
 1.0, 1.0, 1.0))
GRAY_COLORMAP = ColorMap((0.0, 0.0, 0.925), (
 0.0, 0.0, 0.0), (
 1.0, 1.0, 1.0))

class Main:
    """Main program."""
    __module__ = __name__
    colormaps = {'color': TEMPERATURE_COLORMAP, 'pink': PINK_COLORMAP, 'gray': GRAY_COLORMAP}

    def main(self):
        """Main program."""
        parser = optparse.OptionParser(usage='\n\t%prog [options] [file] ...', version='%%prog %s' % __version__)
        parser.add_option('-o', '--output', metavar='FILE', type='string', dest='output', help='output filename [stdout]')
        parser.add_option('-n', '--node-thres', metavar='PERCENTAGE', type='float', dest='node_thres', default=0.5, help='eliminate nodes below this threshold [default: %default]')
        parser.add_option('-e', '--edge-thres', metavar='PERCENTAGE', type='float', dest='edge_thres', default=0.1, help='eliminate edges below this threshold [default: %default]')
        parser.add_option('-f', '--format', type='choice', choices=('prof', 'oprofile',
                                                                    'pstats'), dest='format', default='prof', help='profile format: prof, oprofile, or pstats [default: %default]')
        parser.add_option('-c', '--colormap', type='choice', choices=('color', 'pink',
                                                                      'gray'), dest='colormap', default='color', help='color map: color, pink or gray [default: %default]')
        parser.add_option('-s', '--strip', action='store_true', dest='strip', default=False, help='strip function parameters, template parameters, and const modifiers from demangled C++ function names')
        parser.add_option('-w', '--wrap', action='store_true', dest='wrap', default=False, help='wrap function names')
        (self.options, self.args) = parser.parse_args(sys.argv[1:])
        if len(self.args) > 1:
            if self.options.format != 'pstats':
                parser.error('incorrect number of arguments')
            try:
                self.colormap = self.colormaps[self.options.colormap]
            except KeyError:
                parser.error("invalid colormap '%s'" % self.options.colormap)
            else:
                if self.options.format == 'prof':
                    fp = self.args or sys.stdin
                else:
                    fp = open(self.args[0], 'rt')
                parser = GprofParser(fp)
        elif self.options.format == 'oprofile':
            if not self.args:
                fp = sys.stdin
            else:
                fp = open(self.args[0], 'rt')
            parser = OprofileParser(fp)
        elif self.options.format == 'pstats':
            if not self.args:
                parser.error('at least a file must be specified for pstats input')
            parser = PstatsParser(*self.args)
        else:
            parser.error("invalid format '%s'" % self.options.format)
        self.profile = parser.parse()
        if self.options.output is None:
            self.output = sys.stdout
        else:
            self.output = open(self.options.output, 'wt')
        self.write_graph()
        return

    _parenthesis_re = re.compile('\\([^()]*\\)')
    _angles_re = re.compile('<[^<>]*>')
    _const_re = re.compile('\\s+const$')

    def strip_function_name(self, name):
        """Remove extraneous information from C++ demangled function names."""
        while True:
            (name, n) = self._parenthesis_re.subn('', name)
            if not n:
                break

        name = self._const_re.sub('', name)
        while True:
            (name, n) = self._angles_re.subn('', name)
            if not n:
                break

        return name

    def wrap_function_name(self, name):
        """Split the function name on multiple lines."""
        if len(name) > 32:
            ratio = 2.0 / 3.0
            height = max(int(len(name) / (1.0 - ratio) + 0.5), 1)
            width = max(len(name) / height, 32)
            name = textwrap.fill(name, width, break_long_words=False)
        name = name.replace(', ', ',')
        name = name.replace('> >', '>>')
        name = name.replace('> >', '>>')
        return name

    def compress_function_name(self, name):
        """Compress function name according to the user preferences."""
        if self.options.strip:
            name = self.strip_function_name(name)
        if self.options.wrap:
            name = self.wrap_function_name(name)
        return name

    def write_graph(self):
        dot = DotWriter(self.output)
        profile = self.profile
        profile.prune(self.options.node_thres / 100.0, self.options.edge_thres / 100.0)
        for function in profile.functions.itervalues():
            function.name = self.compress_function_name(function.name)

        dot.graph(profile, self.colormap)


def run_script():
    Main().main()


if __name__ == '__main__':
    run_script()