# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/Expression.py
# Compiled at: 2009-12-17 14:51:53
import inspect, types
from Error import error
from Record import Record

def get_current_vars(*locals):
    """Returns the locals and globals from ALL frames top to bottom. Variables
     in inner-most frames override the outermost frames.
     
     The locals is a list of local dictionaries, with the first ones listed
     overriding any variables in the latter ones listed.  These take precendence
     over any variables found in the frames.
  """
    g = {}
    l = {}
    stack = inspect.stack()
    stack.reverse()
    for frame in stack:
        f = frame[0]
        l.update(f.f_locals)
        g.update(f.f_globals)

    for local in locals:
        l.update(local)

    return (
     l, g)


class PicaloExpression:
    """A class that compiles an expression.  This is done so the expression
     and locals/globals are only compiled and determined one time rather
     than for each time the expression is run.  It's for efficiency."""

    def __init__(self, expression, *locals):
        """Constructor.  The initial_locals and initial_globals dicts override
       any local or global variables"""
        if not isinstance(expression, (types.StringType, types.UnicodeType, PicaloExpression)):
            expression = unicode(expression)
        (self.locals, self.globals) = get_current_vars(*locals)
        if isinstance(expression, PicaloExpression):
            self.expression = expression.expression
        else:
            self.expression = expression
        try:
            self.code = compile(self.expression, '<string>', 'eval')
        except Exception, e:
            self.code = compile("error('Expression is invalid: " + str(e).replace("'", "'") + "')", '<string>', 'eval')

    def evaluate(self, locals, expression_backtrack=[]):
        """Runs the expression given any additional locals and globals
    
       locals => A list of dictionaries containing mappings that override the values in locals
       expression_backtrack => A list of all the expression id's we've run so far, to catch circular logic.
    """
        try:
            assert id(self) not in expression_backtrack, 'Circular logic detected'
            new_expression_backtrack = [id(self)] + expression_backtrack
            l = self.locals
            if len(locals) > 0:
                l = dict(self.locals)
                for d in locals:
                    if isinstance(d, Record):
                        l.update([ (d._table.columns[j].name, d.__get_value__(j, new_expression_backtrack)) for j in range(len(d)) ])
                    else:
                        l.update(d)

            return eval(self.code, self.globals, l)
        except Exception, e:
            return error(e)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        """Returns a string representation of this expression"""
        return '<Expression: ' + self.expression + '>'

    def __eq__(self, other):
        if isinstance(other, PicaloExpression):
            return self.expression == other.expression
        return self.expression == other

    def __ne__(self, other):
        return not self.__eq__(other)