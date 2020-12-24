# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/dotinspect.py
# Compiled at: 2010-10-14 14:04:22
"""
dotinspect

by Geoff Howland  <geoff AT ge01f DOT com>

dotinspect is a method of working with containers (dicts and sequences).

Format:  "var1.-1.(var2a.var2b).var3"

Explanation: Each dot represents an inspection of the current data.  The
first inspection would inspect the keyword "var1" in a dict.  The second
inspection would inspect the last item of a sequence.  The third inspection
is a sub-inspection.  It will first look into the value of it's sub-inspection
by evaluating all the terms in the parenthesis as if they were a new request.
These would then return a value, which would be used as the term to look into
the current container.  The final inspection is yet another term specified
for a dictionary lookup after the sub-inspection created a dynamic lookup.

This is useful for allowing user-specified content, and expanding data-oriented
development methods by making the processing of data generic, and leaving
the specifics to a data-based specification that will be processed or
interpretted into the specific result desired.

The attempt is to push more towards "real code" being very general in nature.
It processes a formatted statement.  Then the statements contain the actual
goal the user is aiming for.  This allows the "real code" to be hardended
significantly from when it is implementing the goals directly, as human goals
change frequently, and often require numerous levels of special cases to meet
our demanding needs.  By creating generalized processors at higher and higher
levels we can use hardened and battle-tested "real code", which can validate
and specify to greater precision the problems with the "goal directions",
because the rules of processing are known and operating at a directed level,
instead of "real code"'s totally general level, which could create anything.

This also allows for pipelining in other important processes, like regressive
testing, monitoring and request authentication, which are all universal issues
and have to be solved in every "real code" goal solution.  With generalized
processors, these issues only have to be solved once, for the generalized
processor, and then all "goal directions" (chunks of information), will
be processed by the general processors and get all the common functionality
for "free".

TODO(g): Test with sets.

TODO(g): Move out of unidist package.  It doesnt belong here.  Does it?
"""
import logging
from log import log

class NoValue(Exception):
    """No value was found."""
    pass


class EmptyContainer(Exception):
    """The container was empty."""
    pass


class NoValueMissingParents(Exception):
    """No value was found, because parents of the desired inspection pount were missing."""
    pass


def GetInspectTerms(inspect):
    """Returns a list of inspection terms.
  
  A term is typically a string or a number, but could also be a sub-inspection
  term: "var.(subvar)".  In this case the sub-inspection term is returned
  between the parenthesis.
  """
    terms = []
    subterms_rough = str(inspect).split('(')
    for item in subterms_rough:
        if ')' in item:
            (subterm, item) = item.split(')', 1)
            subinspect = '(%s)' % subterm
            terms.append(subinspect)
        if not item:
            continue
        parts = item.split('.')
        for part in parts:
            if part != '':
                terms.append(part)

    return terms


def CreateInspect(terms):
    """Create a term sequence.  Returns string:  var1.-1.var2"""
    for count in range(0, len(terms)):
        terms[count] = str(terms[count])

    inspect = ('.').join(terms)
    return inspect


def CreateSubInspect(terms):
    subinspect = '(%s)' % CreateInspect(terms)
    return subinspect


def IsSubInspect(term):
    """If this term is actually a sub-insection phrase."""
    if term.startswith('('):
        return True
    else:
        return False


def SubInspect(subinspect, data):
    """Perform a sub-inspection of the data."""
    inspect = subinspect[1:-1]
    return Inspect(inspect, data)


def Inspect(inspect, data, subinspect_data=None, _current_data=None):
    """Process the dotinspect notation from inspect, using the data as the target.
  
  Args:
    inspect: string, the formatted dotted inspection string
    data: container, dict or sequence
    subinspect_data: container [optional], if there is a sub-inspection, use
        this other data for that.  Allows some flexibility for crossing
        data sources, but rigid in only allowing one.  That is enough for this
        solution set, more would complicate things too much to keep it easy.
    _current_data: [internal use, private], container of current place in
        processing the inspection.
  """
    inspect = str(inspect)
    if inspect.startswith('"') and inspect.endswith('"'):
        return inspect[1:-1]
    else:
        if _current_data == None:
            _current_data = data
        terms = GetInspectTerms(inspect)
        term = terms[0]
        if IsSubInspect(term):
            if subinspect_data:
                term_value = SubInspect(term, subinspect_data)
            else:
                term_value = SubInspect(term, data)
        else:
            term_value = term
        try:
            term_value = int(term_value)
        except ValueError, e:
            try:
                term_value = float(term_value)
            except ValueError, e:
                term_value = str(term_value)

        try:
            value = _current_data[term_value]
        except Exception, e:
            log('Inspection data not found: %s' % str(e), logging.DEBUG)
            if len(terms) == 1:
                return NoValue
            return NoValueMissingParents

        if len(terms) > 1:
            recursive_inspect = CreateInspect(terms[1:])
            result = Inspect(recursive_inspect, data, _current_data=_current_data[term_value])
            return result
        result = _current_data[term_value]
        return result
        return


def Get(inspect, data):
    """Calls Inspect().  This function is sugar."""
    return Inspect(inspect, data)


def __Pop(inspect, data, subinspect_data=None):
    """TODO(g): Pop an entry off the list specified by the inspect phrase."""
    pass


def __Pull(inspect, data, subinspect_data=None):
    """TODO(g): Pop an entry off the list specified by the inspect phrase."""
    pass


def __Push(inspect, data, subinspect_data=None):
    """TODO(g): Pop an entry off the list specified by the inspect phrase."""
    pass


def __Dequeue(inspect, data, subinspect_data=None):
    """TODO(g): Pop an entry off the list specified by the inspect phrase."""
    __Pull(inspect, data, subinspect_data=subinspect_data)


def __Set(inspect, data, subinspect_data=None):
    """TODO(g): Pop an entry off the list specified by the inspect phrase."""
    pass


def __Exists(inspect, data, subinspect_data=None):
    """TODO(g): NoValue, not allowed, specifically."""
    pass


def __ExistsAll(inspect, data, subinspect_data=None):
    """TODO(g): NoValueMissingParents, not allowed, specifically."""
    pass


if __name__ == '__main__':
    terms1 = [
     'tennis', -1]
    subinspect = CreateSubInspect(terms1)
    print subinspect
    terms2 = ['bagau', subinspect, 0]
    inspect = CreateInspect(terms2)
    print inspect
    get_terms = GetInspectTerms(inspect)
    print get_terms
    data = {}
    data['bagau'] = [
     [
      888, 111], [999, '000']]
    data['tennis'] = [0, 3, 2, 1]
    result = Inspect(inspect, data)
    print result
    print Inspect(0, [500, 400, 300])
    print Inspect('0', [500, 400, 300])
    print Inspect('"0"', [500, 400, 300])