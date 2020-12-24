# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\expatriate\xpath\Function.py
# Compiled at: 2018-01-18 12:33:44
# Size of source mod 2**32: 15099 bytes
import logging, math, re
from .exceptions import *
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class Function(object):

    def f_last(args, context_node, context_position, context_size, variables):
        if len(args) != 0:
            raise XPathSyntaxException('last() expects 0 arguments')
        return context_size

    def f_position(args, context_node, context_position, context_size, variables):
        if len(args) != 0:
            raise XPathSyntaxException('position() expects 0 arguments')
        return context_position

    def f_count(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('count() expects 1 argument')
        return len(args[0])

    def f_id(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('id() expects 1 argument')
        else:
            from ..Node import Node
            ids = []
            if isinstance(args[0], list):
                for n in args[0]:
                    if not isinstance(n, Node):
                        raise XPathSyntaxException('Cannot determine the string value of ' + str(n))
                    s = n.get_string_value()
                    logger.debug('Using ' + str(s) + ' as string-value of ' + str(n))
                    ids.extend(re.split('[\\x20\\x09\\x0D\\x0A]+', s))

            else:
                ids = re.split('[\\x20\\x09\\x0D\\x0A]+', Function.f_string((args[0],), context_node, context_position, context_size, variables))
        doc = context_node.get_document()
        ns = []
        for i in ids:
            try:
                ns.append(doc.find_by_id(i))
            except KeyError:
                logger.debug('Could not find element with id: ' + str(i))

        if len(ns) == 1:
            return ns[0]
        else:
            return ns

    def f_local_name(args, context_node, context_position, context_size, variables):
        if len(args) == 0:
            a = [
             context_node]
        else:
            if len(args) == 1:
                a = args[0]
            else:
                raise XPathSyntaxException('local-name() expects 1 argument or none')
        if len(a) <= 0:
            return ''
        else:
            from ..Document import Document
            first_node = Document.ordered_first(a)
            if not hasattr(first_node, 'get_expanded_name'):
                return ''
            return first_node.get_expanded_name()[1]

    def f_namespace_uri(args, context_node, context_position, context_size, variables):
        if len(args) == 0:
            a = [
             context_node]
        else:
            if len(args) == 1:
                a = args[0]
            else:
                raise XPathSyntaxException('namespace-uri() expects 1 argument or none')
        if len(a) <= 0:
            return ''
        else:
            from ..Document import Document
            first_node = Document.ordered_first(a)
            if not hasattr(first_node, 'namespace'):
                return ''
            return first_node.namespace

    def f_name(args, context_node, context_position, context_size, variables):
        if len(args) == 0:
            a = [
             context_node]
        else:
            if len(args) == 1:
                a = args[0]
            else:
                raise XPathSyntaxException('name() expects 1 argument or none')
        if len(a) <= 0:
            return ''
        else:
            from ..Document import Document
            first_node = Document.ordered_first(a)
            if not hasattr(first_node, 'name'):
                return ''
            return first_node.name

    def f_string(args, context_node, context_position, context_size, variables):
        from ..Node import Node
        if len(args) == 0:
            a = [
             context_node]
        else:
            if len(args) == 1:
                a = args[0]
            else:
                raise XPathSyntaxException('string() expects 1 argument or none')
            if isinstance(a, list):
                if len(a) == 0:
                    return ''
                else:
                    from ..Document import Document
                    first_node = Document.ordered_first(a)
                    return first_node.get_string_value()
            if isinstance(a, Node):
                if hasattr(a, 'get_string_value'):
                    return a.get_string_value()
            if isinstance(a, float):
                if math.isnan(a):
                    return 'NaN'
                else:
                    if a == -math.inf:
                        return '-Infinity'
                    if a == math.inf:
                        return 'Infinity'
                    return str(a)
            elif a == True:
                return 'true'
        if a == False:
            return 'false'
        else:
            return str(a)

    def f_concat(args, context_node, context_position, context_size, variables):
        if len(args) < 2:
            raise XPathSyntaxException('concat() expects at least 2 arguments')
        r = ''
        for a in args:
            r += a

        return r

    def f_starts_with(args, context_node, context_position, context_size, variables):
        if len(args) != 2:
            raise XPathSyntaxException('starts-with() expects 2 arguments')
        return args[0].startswith(args[1])

    def f_contains(args, context_node, context_position, context_size, variables):
        if len(args) != 2:
            raise XPathSyntaxException('contains() expects 2 arguments')
        return args[1] in args[0]

    def f_substring_before(args, context_node, context_position, context_size, variables):
        if len(args) != 2:
            raise XPathSyntaxException('substring-before() expects 2 arguments')
        return args[0].partition(args[1])[0]

    def f_substring_after(args, context_node, context_position, context_size, variables):
        if len(args) != 2:
            raise XPathSyntaxException('substring-after() expects 2 arguments')
        return args[0].partition(args[1])[2]

    def f_substring(args, context_node, context_position, context_size, variables):
        if len(args) not in (2, 3):
            raise XPathSyntaxException('substring() expects 2 or 3 arguments')
        if args[1] == -math.inf:
            return ''
        else:
            arg_1 = Function.f_round((args[1],), context_node, context_position, context_size, variables)
            start = arg_1 - 1
            if start < 0:
                start = 0
            logger.debug('Substring start: ' + str(start))
            if len(args) > 2:
                if args[2] == -math.inf:
                    return ''
                else:
                    if args[2] == math.inf:
                        return args[0][start:]
                    end = arg_1 - 1 + Function.f_round((args[2],), context_node, context_position, context_size, variables)
                    logger.debug('Substring end: ' + str(end))
                    return args[0][start:end]
            return args[0][start:]

    def f_string_length(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('string-length() expects 1 argument')
        if not isinstance(args[0], str):
            raise XPathSyntaxException('string-length() expects a string argument')
        return len(args[0])

    def f_normalize_space(args, context_node, context_position, context_size, variables):
        if len(args) == 0:
            a = context_node.get_string_value()
        else:
            if len(args) == 1:
                a = args[0]
            else:
                raise XPathSyntaxException('normalize-space() expects 1 argument or none')
        a = a.strip(' \t\r\n')
        return re.sub('[\\x20\\x09\\x0D\\x0A]+', ' ', a)

    def f_translate(args, context_node, context_position, context_size, variables):
        if len(args) != 3:
            raise XPathSyntaxException('translate() expects 3 arguments')
        s = args[0]
        from_ = args[1]
        to = args[2]
        if len(to) > len(from_):
            to = to[:len(from_)]
        delete = from_[len(to):]
        from_ = from_[:len(to)]
        return s.translate(str.maketrans(from_, to, delete))

    def f_boolean(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('boolean() expects 1 argument')
        else:
            if isinstance(args[0], int) or isinstance(args[0], float):
                if args[0] != 0:
                    if not math.isnan(args[0]):
                        return True
                return False
            else:
                if isinstance(args[0], list):
                    return len(args[0]) > 0
                else:
                    if isinstance(args[0], str):
                        return len(args[0]) > 0
                    return bool(args[0])

    def f_not(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('not() expects 1 argument')
        return not args[0]

    def f_true(args, context_node, context_position, context_size, variables):
        if len(args) != 0:
            raise XPathSyntaxException('true() accepts no arguments')
        return True

    def f_false(args, context_node, context_position, context_size, variables):
        if len(args) != 0:
            raise XPathSyntaxException('false() accepts no arguments')
        return False

    def f_lang(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('lang() expects 1 argument')
        a = args[0].lower()
        n = context_node
        while not hasattr(n, 'attributes') or 'xml:lang' not in n.attributes:
            if n._parent is None:
                return False
            n = n._parent

        attr = n.attributes['xml:lang'].lower()
        if attr.startswith(a):
            return True
        else:
            return False

    def f_number(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('number() expects 1 argument')
        try:
            if isinstance(args[0], str):
                if args[0] == 'NaN':
                    return math.nan
                else:
                    if args[0] == 'Infinity':
                        return math.inf
                    if '.' in args[0]:
                        return float(args[0])
                    return int(args[0])
            else:
                if args[0] == True:
                    return 1
                else:
                    if args[0] == False:
                        return 0
                    else:
                        if isinstance(args[0], list):
                            s = f_string((args[0],), context_node, context_position, context_size, variables)
                            return f_number(s, context_node, context_position, context_size, variables)
                        if isinstance(args[0], int) or isinstance(args[0], float):
                            return args[0]
                    return int(args[0])
        except ValueError:
            raise XPathSyntaxException('Invalid syntax for a number')

    def f_sum(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('sum() expects 1 argument')
        r = 0
        for n in args[0]:
            s = Function.f_string((n,), context_node, context_position, context_size, variables)
            i = Function.f_number((s,), context_node, context_position, context_size, variables)
            r += i

        return r

    def f_floor(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('floor() expects 1 argument')
        return math.floor(args[0])

    def f_ceiling(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('ceiling() expects 1 argument')
        return math.ceil(args[0])

    def f_round(args, context_node, context_position, context_size, variables):
        if len(args) != 1:
            raise XPathSyntaxException('round() expects 1 argument')
        if math.isnan(args[0]):
            return math.nan
        if args[0] == math.inf:
            return math.inf
        else:
            if args[0] == -math.inf:
                return -math.inf
            return round(args[0])

    FUNCTIONS = {'last':f_last, 
     'position':f_position, 
     'count':f_count, 
     'id':f_id, 
     'local-name':f_local_name, 
     'namespace-uri':f_namespace_uri, 
     'name':f_name, 
     'string':f_string, 
     'concat':f_concat, 
     'starts-with':f_starts_with, 
     'contains':f_contains, 
     'substring-before':f_substring_before, 
     'substring-after':f_substring_after, 
     'substring':f_substring, 
     'string-length':f_string_length, 
     'normalize-space':f_normalize_space, 
     'translate':f_translate, 
     'boolean':f_boolean, 
     'not':f_not, 
     'true':f_true, 
     'false':f_false, 
     'lang':f_lang, 
     'number':f_number, 
     'sum':f_sum, 
     'floor':f_floor, 
     'ceiling':f_ceiling, 
     'round':f_round}

    def __init__(self, name, function):
        self.name = name
        self.function = function
        self.children = []

    def evaluate(self, context_node, context_position, context_size, variables):
        arg_evals = []
        for c in self.children:
            v = c.evaluate(context_node, context_position, context_size, variables)
            logger.debug('Evaluated child of ' + str(self) + ' to ' + str(v))
            arg_evals.append(v)

        return self.function(arg_evals, context_node, context_position, context_size, variables)

    def __str__(self):
        return 'Function ' + self.name + ': [' + ','.join([str(x) for x in self.children]) + ']'