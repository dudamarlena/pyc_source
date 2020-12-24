# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/multiforloop/templatetags/multifor.py
# Compiled at: 2014-02-19 08:47:48
from itertools import izip_longest
from django.template.base import Library
from django.conf import settings
register = Library()
from django.template import Node, NodeList, Template, Context, Variable
from django.template import TemplateSyntaxError, VariableDoesNotExist

class ForNode(Node):
    child_nodelists = ('nodelist_loop', 'nodelist_empty')
    zip = zip
    get_overall_len = min

    def __init__(self, loopvars_list, sequence_list, is_reversed_list, nodelist_loop, nodelist_empty=None, zip_func=None):
        self.loopvars_list, self.sequence_list = loopvars_list, sequence_list
        self.is_reversed_list = is_reversed_list
        self.nodelist_loop = nodelist_loop
        if nodelist_empty is None:
            self.nodelist_empty = NodeList()
        else:
            self.nodelist_empty = nodelist_empty
        if zip_func is not None:
            self.zip = zip_func
        return

    def __repr__(self):

        def make_rev_txt(revd):
            return revd and ' reversed' or ''

        rev_text_list = [ make_rev_txt(revd) for revd in self.is_reversed_list ]
        zip_list = zip(self.loopvars_list, self.sequence_list, rev_text_list)
        sections = [ '%s in %s%s' % ((', ').join(l), s, r) for l, s, r in zip_list ]
        return '<For Node: for %s, tail_len: %d>' % (
         ('; ').join(sections), len(self.nodelist_loop))

    def __iter__(self):
        for node in self.nodelist_loop:
            yield node

        for node in self.nodelist_empty:
            yield node

    def render(self, context):
        if 'forloop' in context:
            parentloop = context['forloop']
        else:
            parentloop = {}
        context.push()
        vals_list = []
        len_values_list = []
        for s in self.sequence_list:
            try:
                values = s.resolve(context, True)
            except VariableDoesNotExist:
                values = []

            if values is None:
                values = []
            if not hasattr(values, '__len__'):
                values = list(values)
            vals_list.append(values)
            len_values_list.append(len(values))

        len_values = self.get_overall_len(len_values_list)
        if len_values < 1:
            context.pop()
            return self.nodelist_empty.render(context)
        else:
            nodelist = NodeList()

            def rev(revd, values):
                return revd and reversed(values) or values

            values_list = [ rev(*v) for v in zip(self.is_reversed_list, vals_list) ]
            unpack_list = [ len(l) > 1 for l in self.loopvars_list ]
            loop_dict = context['forloop'] = {'parentloop': parentloop}
            for i, items in enumerate(self.zip(*values_list)):
                loop_dict['counter0'] = i
                loop_dict['counter'] = i + 1
                loop_dict['revcounter'] = len_values - i
                loop_dict['revcounter0'] = len_values - i - 1
                loop_dict['first'] = i == 0
                loop_dict['last'] = i == len_values - 1
                uli_zip = zip(unpack_list, self.loopvars_list, items)
                for unpack, loopvars, item in uli_zip:
                    if unpack:
                        context.update(dict(zip(loopvars, item)))
                    else:
                        context[loopvars[0]] = item

                for node in self.nodelist_loop:
                    nodelist.append(node.render(context))

                for unpack in unpack_list:
                    if unpack:
                        context.pop()

            context.pop()
            return nodelist.render(context)


class ForLongestNode(ForNode):

    def zip(self, *args):
        return izip_longest(fillvalue=settings.TEMPLATE_STRING_IF_INVALID, *args)

    get_overall_len = max


def do_for(parser, token, ForNode=ForNode):
    all_bits = token.contents.split()[1:]
    sections = [ s.strip() for s in (' ').join(all_bits).split(';') ]
    loopvars_list = []
    sequence_list = []
    is_reversed_list = []
    for sec in sections:
        bits = sec.split()
        if len(bits) < 3:
            raise TemplateSyntaxError("'for' statements should have at least four words: %s" % token.contents)
        is_reversed = bits[(-1)] == 'reversed'
        in_index = is_reversed and -3 or -2
        is_reversed_list.append(is_reversed)
        if bits[in_index] != 'in':
            raise TemplateSyntaxError("'for' statements should use the format 'for x in y': %s" % token.contents)
        loopvars_list.append([ l.strip() for l in (' ').join(bits[:in_index]).split(',') ])
        for loopvars in loopvars_list:
            for var in loopvars:
                if not var or ' ' in var:
                    raise TemplateSyntaxError("'for' tag received an invalid argument: %s" % token.contents)

        sequence_list.append(parser.compile_filter(bits[(in_index + 1)]))

    nodelist_loop = parser.parse(('empty', 'endfor'))
    token = parser.next_token()
    if token.contents == 'empty':
        nodelist_empty = parser.parse(('endfor', ))
        parser.delete_first_token()
    else:
        nodelist_empty = None
    return ForNode(loopvars_list, sequence_list, is_reversed_list, nodelist_loop, nodelist_empty)


do_for = register.tag('for', do_for)

def do_for_longest(*args, **kwargs):
    return do_for(ForNode=ForLongestNode, *args, **kwargs)


do_for_longest = register.tag('for_longest', do_for_longest)