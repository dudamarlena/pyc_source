# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/scheduler/filters/json_filter.py
# Compiled at: 2016-06-13 14:11:03
import operator
from vsm.openstack.common import jsonutils
from vsm.openstack.common.scheduler import filters

class JsonFilter(filters.BaseHostFilter):
    """Host Filter to allow simple JSON-based grammar for
    selecting hosts.
    """

    def _op_compare(self, args, op):
        """Returns True if the specified operator can successfully
        compare the first item in the args with all the rest. Will
        return False if only one item is in the list.
        """
        if len(args) < 2:
            return False
        if op is operator.contains:
            bad = args[0] not in args[1:]
        else:
            bad = [ arg for arg in args[1:] if not op(args[0], arg)
                  ]
        return not bool(bad)

    def _equals(self, args):
        """First term is == all the other terms."""
        return self._op_compare(args, operator.eq)

    def _less_than(self, args):
        """First term is < all the other terms."""
        return self._op_compare(args, operator.lt)

    def _greater_than(self, args):
        """First term is > all the other terms."""
        return self._op_compare(args, operator.gt)

    def _in(self, args):
        """First term is in set of remaining terms"""
        return self._op_compare(args, operator.contains)

    def _less_than_equal(self, args):
        """First term is <= all the other terms."""
        return self._op_compare(args, operator.le)

    def _greater_than_equal(self, args):
        """First term is >= all the other terms."""
        return self._op_compare(args, operator.ge)

    def _not(self, args):
        """Flip each of the arguments."""
        return [ not arg for arg in args ]

    def _or(self, args):
        """True if any arg is True."""
        return any(args)

    def _and(self, args):
        """True if all args are True."""
        return all(args)

    commands = {'=': _equals, 
       '<': _less_than, 
       '>': _greater_than, 
       'in': _in, 
       '<=': _less_than_equal, 
       '>=': _greater_than_equal, 
       'not': _not, 
       'or': _or, 
       'and': _and}

    def _parse_string(self, string, host_state):
        """Strings prefixed with $ are capability lookups in the
        form '$variable' where 'variable' is an attribute in the
        HostState class.  If $variable is a dictionary, you may
        use: $variable.dictkey
        """
        if not string:
            return
        else:
            if not string.startswith('$'):
                return string
            path = string[1:].split('.')
            obj = getattr(host_state, path[0], None)
            if obj is None:
                return
            for item in path[1:]:
                obj = obj.get(item, None)
                if obj is None:
                    return

            return obj

    def _process_filter(self, query, host_state):
        """Recursively parse the query structure."""
        if not query:
            return True
        else:
            cmd = query[0]
            method = self.commands[cmd]
            cooked_args = []
            for arg in query[1:]:
                if isinstance(arg, list):
                    arg = self._process_filter(arg, host_state)
                elif isinstance(arg, basestring):
                    arg = self._parse_string(arg, host_state)
                if arg is not None:
                    cooked_args.append(arg)

            result = method(self, cooked_args)
            return result

    def host_passes(self, host_state, filter_properties):
        """Return a list of hosts that can fulfill the requirements
        specified in the query.
        """
        try:
            query = filter_properties['scheduler_hints']['query']
        except KeyError:
            query = None

        if not query:
            return True
        else:
            result = self._process_filter(jsonutils.loads(query), host_state)
            if isinstance(result, list):
                result = any(result)
            if result:
                return True
            return False