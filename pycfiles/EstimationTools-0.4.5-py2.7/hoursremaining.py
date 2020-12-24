# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/estimationtools/hoursremaining.py
# Compiled at: 2011-09-05 07:25:07
from estimationtools.utils import get_closed_states, execute_query, EstimationToolsBase
from trac.wiki.macros import WikiMacroBase
from trac.wiki.api import parse_args

class HoursRemaining(EstimationToolsBase, WikiMacroBase):
    """Calculates remaining estimated hours for the queried tickets.

    The macro accepts a comma-separated list of query parameters for the ticket selection, 
    in the form "key=value" as specified in TracQuery#QueryLanguage.
    
    Example:
    {{{
        [[HoursRemaining(milestone=Sprint 1)]]
    }}}
    """
    closed_states = get_closed_states()

    def expand_macro(self, formatter, name, content):
        req = formatter.req
        _ignore, options = parse_args(content, strict=False)
        options[self.estimation_field + '!'] = None
        options['status!'] = ('|').join(self.closed_states)
        tickets = execute_query(self.env, req, options)
        sum = 0.0
        for t in tickets:
            try:
                sum += float(t[self.estimation_field])
            except:
                pass

        return '%g' % round(sum, 2)