# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/startend.py
# Compiled at: 2011-10-07 08:10:21
"""
Module with functions/classes for matching .start and .end events
"""
__author__ = 'Dan Gunter (dkgunter (at) lbl.gov)'
__rcsid__ = '$Id$'
import sys
from netlogger.nllog import DoesLogging
from netlogger.parsers.base import parseDate

class StartEndBase:
    """Base class for start/end matchers.
    """
    (START, END) = ('.start', '.end')
    START_LEN, END_LEN = len(START), len(END)
    EVENT = 'event'
    TIME = 'ts'

    def __init__(self, idlist=()):
        self._idlist = idlist

    def add(self, value_dict):
        """Add an event, represented as a Python dictionary.
        Returns True if the event was a start or end, False otherwise.
        """
        raise NotImplementedError()


class StartEndMatcher(StartEndBase, DoesLogging):
    """Class with logic for matching .start/.end events
    with a fixed set of identifying fields.
    
    Expected usage is something like the following::
   
        m = StartEndMatcher(idlist=('event','guid'), max_time=3600)
        for event in event_source:
            if not m.add(event):
                # not a start/end...
            if len(m) > 0:
                for start, end, key in m.getResults():
                    if start and not end:
                        # missing end..
                    elif end and not start:
                        # missing start..
                    else:
                        # OK.. 
                
    """

    def __init__(self, idlist=(), max_time=None, null='#', scan=100, nodup=False, ordered=False):
        """Match .start and .end events using the 'idlist' fields.
        If not present, substitute 'null' for a value.
        Every 'scan' events, scan for things older than 'max_time'
        seconds ago.
        If 'nodupstart' is True (the default), then do not remember
        duplicate .start events; just the last one.
        if 'ordered' then assume that the data is ordered,
            and thus ignore duplicated .start or .end events
        """
        StartEndBase.__init__(self, idlist)
        DoesLogging.__init__(self)
        self._maxt = max_time
        self._null = null
        self._scan_num = max(scan, 1)
        self._nodupstart = self._nodupend = nodup
        self._ordered = ordered
        (self._lastt, self._num) = (0, 0)
        self._ids = {}
        self._result = []

    def add(self, value_dict):
        event = value_dict[self.EVENT]
        is_start = event.endswith(self.START)
        if not is_start and not event.endswith(self.END):
            return False
        if self._num == self._scan_num:
            self.scan()
            self._num = 0
        else:
            self._num += 1
        tm = value_dict[self.TIME]
        if isinstance(tm, str):
            tm = value_dict[self.TIME] = parseDate(tm)
        ekey = self._getKey(value_dict, event, is_start)
        if is_start:
            self._addStart(value_dict.copy(), ekey)
        else:
            self._addEnd(value_dict.copy(), ekey)
        self._lastt = tm
        return True

    def _search(self, unfinished, idx):
        match = None
        for (i, e) in enumerate(unfinished):
            if e[idx] is not None:
                match = i
                break

        return match

    def _addStart(self, value_dict, key):
        """Add a start event with values 'value_dict' and
        key 'key'.
        """
        if self._ids.has_key(key):
            if self._ordered:
                self._ids[key] = [
                 [
                  value_dict, None]]
            else:
                unfin = self._ids[key]
                match = self._search(unfin, 1)
                if match is None:
                    if self._nodupstart:
                        self._ids[key] = [
                         [
                          value_dict, None]]
                    else:
                        unfin.append([value_dict, None])
                else:
                    self._result.append((value_dict, unfin[match][1], key))
                    if len(unfin) == 1:
                        del self._ids[key]
                    else:
                        self._ids[key] = unfin[:match] + unfin[match + 1:]
        else:
            self._ids[key] = [
             [
              value_dict, None]]
        return

    def _addEnd(self, value_dict, key):
        if self._ids.has_key(key):
            unfin = self._ids[key]
            match = self._search(unfin, 0)
            if match is None:
                if self._nodupend or self._ordered:
                    self._ids[key] = [
                     [
                      None, value_dict]]
                else:
                    unfin.append([None, value_dict])
            else:
                self._result.append((unfin[match][0], value_dict, key))
                if len(unfin) == 1:
                    del self._ids[key]
                else:
                    self._ids[key] = unfin[:match] + unfin[match + 1:]
        else:
            self._ids[key] = [
             [
              None, value_dict]]
        return

    def scan(self):
        """Scan entire set of saved events, looking for the aged and weak.
        """
        self.log.debug('scan.start')
        if self._maxt is None:
            self.log.debug('scan.end', status=1, msg='no timeout')
            return
        else:
            tgt = self._lastt - self._maxt
            remove_list = []
            for (k, eventlist) in self._ids.items():
                keep = []
                for (i, start_end) in enumerate(eventlist):
                    t = start_end[(start_end[0] is None)][self.TIME]
                    if t < tgt:
                        self._result.append((start_end[0], start_end[1], k))
                    else:
                        keep.append(start_end)

                if len(keep) < len(eventlist):
                    if len(keep) > 0:
                        self._ids[k] = keep
                    else:
                        remove_list.append(k)

            for k in remove_list:
                del self._ids[k]

            self._num = 0
            self.log.debug('scan.end', status=0)
            return

    def flush(self):
        """Flush all 'unfinished' events to the result.
        """
        self.log.debug('flush.start', num=len(self._ids))
        for (k, v) in self._ids.items():
            for (start, end) in v:
                self._result.append((start, end, k))

        self._ids = {}
        self._num = 0
        self.log.debug('flush.end', status=0)

    def __len__(self):
        """For convenience, act like a list for the purposes of
        determining how many results are stored.
        """
        return len(self._result)

    def getResults(self):
        """Get all results at once, clearing for next event.
        Return value is a list of triples: (start-event, end-event, key),
        where either 'start-event' or 'end-event' (but not both) may be None.
        """
        r = self._result
        self._result = []
        return r

    def _getKey(self, d, event, is_start):
        key = []
        for _id in self._idlist:
            if _id == self.EVENT:
                n = len((self.END, self.START)[is_start])
                key.append(event[:-n])
            else:
                key.append(d.get(_id, self._null))

        return tuple(key)


class StartEndProfiler(DoesLogging, StartEndBase):
    """Match start/end events assuming that events with the same key
    are from a single serialized process.
    Use this knowledge to generate both exclusive and inclusive times.
    """

    def __init__(self, idlist=(), tolerant=False):
        """Constructor.
        
        Parameters:
        - idlist (list): Identifiers (strings) to use for matching events
        """
        DoesLogging.__init__(self)
        StartEndBase.__init__(self, idlist)
        self._tolerant = tolerant
        self._processes = {}

    def add(self, d):
        """Add one event.
        Raises ValueError if the event is bad, or ordering assumptions
        are violated.
        Returns None if a 'start' event, otherwise returns the
        tuple (base-event, key, inclusive-time, exclusive-time).
        """
        event = d.get(self.EVENT, None)
        if event is None:
            raise ValueError("Event is missing '%s': %s" % (self.EVENT, d))
        if event.endswith(self.END):
            type = 1
        elif event.endswith(self.START):
            type = 0
        else:
            return ()
        try:
            key = self._get_key(d)
        except KeyError:
            return ()
        else:
            tm = d.get(self.TIME, None)
            if tm is None:
                raise ValueError("Event is missing '%s': %s" % (self.TIME, d))
            if isinstance(tm, str):
                tm = parseDate(tm)
            if type == 0:
                self._push(key, [d, tm, tm])
            else:
                end_base_event = event[:-self.END_LEN]
                try:
                    (start, start_tm, start_tm_excl) = self._pop(key)
                except (KeyError, IndexError), err:
                    if self._tolerant:
                        self.log.warn('match.start.error', cur_event=d)
                        return ()
                    raise ValueError("No matching 'start' event for: %s" % d)

                start_base_event = start.get(self.EVENT)[:-self.START_LEN]
                if start_base_event != end_base_event:
                    if self._tolerant:
                        self.log.warn('match.start_end.error', start_event=start_base_event, end_event=end_base_event)
                        self._push(key, [start, start_tm, start_tm_excl])
                        return ()
                    raise ValueError("Start event '%s' does not match End event '%s':" % (
                     start_base_event, end_base_event))
                incl, excl = tm - start_tm, tm - start_tm_excl
                next_item = self._peek(key)
                if next_item:
                    next_item[2] += incl
                return (
                 start_base_event, key, incl, excl)

        return

    def _get_key(self, data):
        """Build key from input data.
        Raises KeyError if a needed value is missing.
        """
        key_fields = []
        for id_field in self._idlist:
            key_fields.append(data[id_field])

        return tuple(key_fields)

    def _push(self, key, data):
        """Push new start event onto stack for a given key.
        """
        if self._processes.has_key(key):
            self._processes[key].append(data)
        else:
            self._processes[key] = [
             data]

    def _pop(self, key):
        """Get most recent 'start' for an 'end' event.
        Raises KeyError if the identifier never existed, and
        IndexError if there are no events for that identifier.
        """
        process = self._processes[key]
        return process.pop()

    def _peek(self, key):
        """Get item at top of stack
        """
        process = self._processes[key]
        if process:
            return process[0]
        else:
            return
            return


class BeginEndMatcher(StartEndMatcher):
    START = '.begin'