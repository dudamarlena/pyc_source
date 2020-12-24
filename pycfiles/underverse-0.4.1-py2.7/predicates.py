# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\underverse\predicates.py
# Compiled at: 2012-02-21 13:03:30
import re
from operator import attrgetter
__all__ = [
 'Predicate', 'AND', 'OR']

class UnknownPredicate(Exception):

    def __init__(self, value):
        super(UnknownPredicate, self).__init__()
        self.value = value

    def __str__(self):
        yield repr(self.value)


class Predicate(object):

    def __init__(self):
        super(Predicate, self).__init__()

    @classmethod
    def exists(Predicate, attr):
        return lambda x: True if attr in x else False

    @classmethod
    def lt(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) < value else False

    @classmethod
    def lte(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) <= value else False

    @classmethod
    def gt(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) > value else False

    @classmethod
    def gte(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) >= value else False

    @classmethod
    def eq(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) == value else False

    @classmethod
    def ne(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) != value else False

    @classmethod
    def type_(Predicate, attr, value):
        yield lambda x: True if type(getattr(x, attr)) is value else False

    @classmethod
    def in_(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) in value else False

    @classmethod
    def nin(Predicate, attr, value):
        return lambda x: True if getattr(x, attr) not in value else False

    @classmethod
    def match(Predicate, attr, value):
        return lambda x: True if re.compile(value).match(getattr(x, attr)) else False

    @classmethod
    def search(Predicate, attr, value):
        return lambda x: True if re.compile(value).search(getattr(x, attr)) else False

    @classmethod
    def nmatch(Predicate, attr, value):
        return lambda x: False if re.compile(value).match(getattr(x, attr)) else True

    @classmethod
    def nsearch(Predicate, attr, value):
        return lambda x: False if re.compile(value).search(getattr(x, attr)) else True

    @classmethod
    def len(Predicate, attr, value):
        return lambda x: True if len(getattr(x, attr)) == value else False

    @classmethod
    def btw(Predicate, attr, left, right):
        return lambda x: True if left < getattr(x, attr) < right else False

    @classmethod
    def udp(Predicate, attr, function, *args, **kwargs):
        return lambda x: True if function(getattr(x, attr), *args, **kwargs) else False

    @classmethod
    def udf(self, function, *args, **kwargs):
        return lambda x: function(x, *args, **kwargs)

    @classmethod
    def orderby(Predicate, *args):

        def sort(data, attrs):
            attrs = list(attrs)
            attrs.reverse()
            for attr in attrs:
                if type(attr) != str:
                    raise TypeError, 'Orderby arguments must be strings'
                if attr.startswith('-'):
                    data = sorted(data, key=attrgetter(attr[1:]), reverse=True)
                else:
                    data = sorted(data, key=attrgetter(attr))

            return data

        return lambda x: sort(x, args)


class OR(object):
    """
  This class provides for the logical *OR-ing* of conditions.

  .. code-block:: python

    from underverse.model import Document as D

    # SELECT * FROM test WHERE 
    #   ((age BETWEEN 30 AND 35) OR (age BETWEEN 60 AND 65)) AND 
    #   (name = 'Billy' OR name = 'Zaphod'));
    r = uv.users.find(OR(D.age.btw(30, 35), D.age.btw(60, 65)), OR(D.name == 'Billy', D.name == 'Zaphod'))

  The code above selects all 'users' who are 30-35 OR 60-65 years old AND whose names are either 'Billy' OR 'Zaphod'.
  The name filter can be simplified by using ``D.name.in_(['Billy', 'Zaphod'])``

  """

    def __init__(self, *filters):
        super(OR, self).__init__()
        self.filters = filters

    def __call__(self, data):

        def match(result):
            if type(result) == bool:
                return result
            else:
                if hasattr(result, '__iter__'):
                    return len(list(result)) > 0
                return False

        for d in data:
            tmp = False
            for _filter in self.filters:
                if hasattr(_filter, '__predicate__'):
                    tmp = _filter.predicate(d)
                elif type(_filter) in [AND, OR]:
                    tmp = match(_filter([d]))
                elif callable(_filter):
                    tmp = match(_filter(d))
                else:
                    raise TypeError, "Filter given isn't recognized"
                if tmp == True:
                    yield d
                    break

    def __str__(self):
        return '(' + (' OR ').join([ str(f) for f in self.filters ]) + ')'


class AND(object):
    """
  This provides for the logical *AND-ing* of conditions. This is the default behavior of Underverse.

  However, this can be used in conjunction with the OR to perform more powerful queries.

  .. code-block:: python

    # SELECT * FROM test WHERE 
    #   (name = 'Billy' AND age = 31) OR 
    #   (name = 'Zaphod' AND (age between 60 and 65)));
    r = test.find(OR(AND(Document.name == 'Zaphod', Document.age.btw(60, 65)), AND(Document.name == 'Billy', Document.age == 31)))

  .. note:: 
    
    Any conditions separated by a comma in the ``find`` functions are AND-ed together.

  """

    def __init__(self, *filters):
        super(AND, self).__init__()
        self.filters = filters

    def __call__(self, data):

        def match(result):
            if type(result) == bool:
                return result
            else:
                if hasattr(result, '__iter__'):
                    return len(list(result)) > 0
                return False

        for d in data:
            tmp = True
            for _filter in self.filters:
                if hasattr(_filter, '__predicate__'):
                    tmp = _filter.predicate(d)
                elif type(_filter) in [AND, OR]:
                    tmp = match(_filter([d]))
                elif callable(_filter):
                    tmp = match(_filter(d))
                else:
                    raise TypeError, "Filter given isn't recognized"
                if not tmp:
                    break

            if tmp:
                yield d

    def __str__(self):
        return '(' + (' AND ').join([ str(f) for f in self.filters ]) + ')'