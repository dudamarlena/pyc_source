# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\mappyfile\transformer.py
# Compiled at: 2020-01-11 08:01:06
"""
Module to transform an AST (Abstract Syntax Tree) to a
Python dict structure
"""
from __future__ import unicode_literals
import sys, logging
from collections import OrderedDict
from lark import Tree
from lark.visitors import Transformer_InPlace, Transformer, v_args
from lark.lexer import Token
from mappyfile.tokens import SINGLETON_COMPOSITE_NAMES, REPEATED_KEYS
from mappyfile.ordereddict import CaseInsensitiveOrderedDict
from mappyfile.pprint import Quoter
PY2 = sys.version_info[0] < 3
if PY2:
    str = unicode
log = logging.getLogger(b'mappyfile')

class MapfileTransformer(Transformer, object):

    def __init__(self, include_position=False, include_comments=False):
        self.quoter = Quoter()
        self.include_position = include_position
        self.include_comments = include_comments

    def key_name(self, token):
        return token.value.lower()

    def start(self, children):
        """
        Parses a MapServer Mapfile
        Parsing of partial Mapfiles or lists of composites is also possible
        """
        composites = []
        for composite_dict in children:
            if False and self.include_position:
                key_token = composite_dict[1]
                key_name = key_token.value.lower()
                composites_position = self.get_position_dict(composite_dict)
                composites_position[key_name] = self.create_position_dict(key_token, None)
            composites.append(composite_dict)

        if len(composites) == 1:
            return composites[0]
        else:
            return composites
            return

    def get_position_dict(self, d):
        if b'__position__' in d:
            position_dict = d[b'__position__']
        else:
            position_dict = d[b'__position__'] = OrderedDict()
        return position_dict

    def flatten(self, values):
        flat_list = []
        for v in values:
            if isinstance(v, Token):
                flat_list.append(v)
            elif isinstance(v, list):
                flat_list += v
            elif isinstance(v, tuple):
                flat_list += v
            elif isinstance(v, dict):
                assert b'__tokens__' in v
                flat_list += v[b'__tokens__']
            else:
                raise ValueError(b'Attribute value type not supported', v)

        return flat_list

    def plural(self, s):
        if s.endswith(b's'):
            return s + b'es'
        else:
            return s + b's'

    def create_position_dict(self, key_token, values):
        line, column = key_token.line, key_token.column
        d = OrderedDict()
        d[b'line'] = line
        d[b'column'] = column
        if values:
            flat_list = self.flatten(values)
            value_positions = [ (v.line, v.column) for v in flat_list ]
            d[b'values'] = value_positions
        return d

    def get_single_key(self, d):
        keys = list(d.keys())
        assert len(keys) == 1
        return keys[0]

    def composite_body(self, t):
        return t

    def composite_type(self, t):
        return t

    def composite(self, t):
        """
        Handle the composite types e.g. CLASS..END
        t is a list in the form [[Token(__LAYER36, 'LAYER')], [OrderedDict([...])]]

        """
        if len(t) == 1:
            return t[0]
        else:
            key_token = t[0][0]
            attribute_dicts = t[1]
            if not isinstance(attribute_dicts, list):
                attribute_dicts = [attribute_dicts]
            key_name = self.key_name(key_token)
            composite_dict = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)
            composite_dict[b'__type__'] = key_name
            if self.include_position:
                pd = self.create_position_dict(key_token, None)
                composite_dict[b'__position__'] = pd
            if self.include_comments:
                comments_dict = composite_dict[b'__comments__'] = OrderedDict()
            for d in attribute_dicts:
                keys = d.keys()
                if b'__type__' in keys:
                    k = d[b'__type__']
                    if k in SINGLETON_COMPOSITE_NAMES:
                        composite_dict[k] = d
                    else:
                        plural_key = self.plural(k)
                        if plural_key not in composite_dict:
                            composite_dict[plural_key] = []
                        composite_dict[plural_key].append(d)
                else:
                    pos = d.pop(b'__position__')
                    d.pop(b'__tokens__', None)
                    comments = d.pop(b'__comments__', None)
                    key_name = self.get_single_key(d)
                    if key_name == b'config':
                        if key_name not in composite_dict:
                            composite_dict[key_name] = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)
                        cfg_dict = composite_dict[key_name]
                        cfg_dict.update(d[key_name])
                        if self.include_position:
                            if key_name not in pd:
                                pd[key_name] = OrderedDict()
                            subkey_name = self.get_single_key(d[key_name])
                            pd[key_name][subkey_name] = pos
                    elif key_name == b'points':
                        if key_name not in composite_dict:
                            composite_dict[key_name] = d[key_name]
                        else:
                            existing_points = composite_dict[key_name]

                            def depth(L):
                                return isinstance(L, (tuple, list)) and max(map(depth, L)) + 1

                            if depth(existing_points) == 2:
                                composite_dict[key_name] = [
                                 existing_points]
                            if key_name not in composite_dict:
                                composite_dict[key_name] = []
                            composite_dict[key_name].append(d[key_name])
                        if self.include_position:
                            if key_name not in pd:
                                pd[key_name] = pos
                            else:
                                existing_pos = pd[key_name]
                                if isinstance(existing_pos, dict):
                                    pd[key_name] = [
                                     existing_pos]
                                pd[key_name].append(pos)
                    elif key_name in REPEATED_KEYS:
                        if key_name not in composite_dict:
                            composite_dict[key_name] = []
                        composite_dict[key_name].append(d[key_name])
                        if self.include_position:
                            if key_name not in pd:
                                pd[key_name] = []
                            pd[key_name].append(pos)
                    else:
                        assert len(d.items()) == 1
                        if self.include_position:
                            pd[key_name] = pos
                        if self.include_comments and comments:
                            comments_dict[key_name] = comments
                        composite_dict[key_name] = d[key_name]

            return composite_dict

    def clean_string(self, val):
        return self.quoter.remove_quotes(val)

    def attr_name(self, tokens):
        t = tokens[0]
        t = isinstance(t, Token) or t[0]
        assert t.value.lower() in ('symbol', 'style')
        return t

    def attr(self, tokens):
        key_token = tokens[0]
        if isinstance(key_token, (list, tuple)):
            key_token = key_token[0]
            assert self.key_name(key_token) in ('style', 'symbol')
        key_name = self.key_name(key_token)
        value_tokens = tokens[1:]
        if isinstance(value_tokens[0], (list, tuple)):
            assert len(value_tokens) == 1
            value_tokens = value_tokens[0]
        pd = self.create_position_dict(key_token, value_tokens)
        d = OrderedDict()
        d[b'__position__'] = pd
        if len(value_tokens) > 1:
            if key_name == b'config':
                assert len(value_tokens) == 2
                values = {value_tokens[0].value: value_tokens[1].value}
            else:
                values = [ v.value for v in value_tokens ]
                d[b'__tokens__'] = [
                 key_token] + [ t for t in value_tokens ]
        else:
            value_token = value_tokens[0]
            d[b'__tokens__'] = [
             key_token, value_token]
            values = value_token.value
            if self.quoter.is_string(values):
                values = self.clean_string(values)
        d[key_name] = values
        return d

    def check_composite_tokens(self, name, tokens):
        """
        Return the key and contents of a KEY..END block
        for PATTERN, POINTS, and PROJECTION
        """
        assert len(tokens) >= 2
        key = tokens[0]
        assert key.value.lower() == name
        assert tokens[(-1)].value.lower() == b'end'
        if len(tokens) == 2:
            body = []
        else:
            body = tokens[1:-1]
        body_tokens = []
        for t in body:
            if isinstance(t, dict):
                body_tokens.append(t[b'__tokens__'])
            else:
                body_tokens.append(t)

        return (
         key, body_tokens)

    def process_value_pairs(self, tokens, type_):
        """
        Metadata, Values, and Validation blocks can either
        have string pairs or attributes
        Attributes will already be processed
        """
        key, body = self.check_composite_tokens(type_, tokens)
        key_name = self.key_name(key)
        d = CaseInsensitiveOrderedDict(CaseInsensitiveOrderedDict)
        for t in body:
            k = self.clean_string(t[0].value).lower()
            v = self.clean_string(t[1].value)
            if k in d.keys():
                log.warning((b'A duplicate key ({}) was found in {}. Only the last value ({}) will be used. ').format(k, type_, v))
            d[k] = v

        if self.include_position:
            pd = self.create_position_dict(key, body)
            d[b'__position__'] = pd
        d[b'__type__'] = key_name
        return d

    def connectionoptions(self, tokens):
        """
        Create a dict for the connectionoptions items
        """
        return self.process_value_pairs(tokens, b'connectionoptions')

    def metadata(self, tokens):
        """
        Create a dict for the metadata items
        """
        return self.process_value_pairs(tokens, b'metadata')

    def values(self, tokens):
        """
        Create a dict for the values items
        """
        return self.process_value_pairs(tokens, b'values')

    def config(self, t):
        assert len(t) == 3
        key = t[1].value.lower()
        value = t[2].value
        t[1].value = self.clean_string(key)
        t[2].value = self.clean_string(value)
        return self.attr(t)

    def validation(self, tokens):
        """
        Create a dict for the validation items
        """
        return self.process_value_pairs(tokens, b'validation')

    def projection(self, tokens):
        key, body = self.check_composite_tokens(b'projection', tokens)
        projection_strings = [ self.clean_string(v.value) for v in body ]
        key_token = tokens[0]
        value_token = tokens[1]
        value_token.value = projection_strings
        tokens = (key_token, value_token)
        return self.attr(tokens)

    def process_pair_lists(self, key_name, tokens):
        key, body = self.check_composite_tokens(key_name, tokens)
        pairs = [ (v[0].value, v[1].value) for v in body ]
        key_token = tokens[0]
        value_token = tokens[1][0]
        value_token.value = pairs
        tokens = (key_token, value_token)
        return self.attr(tokens)

    def points(self, tokens):
        return self.process_pair_lists(b'points', tokens)

    def pattern(self, tokens):
        return self.process_pair_lists(b'pattern', tokens)

    def comparison(self, t):
        assert len(t) == 3
        parts = [ str(p.value) for p in t ]
        v = (b' ').join(parts)
        v = (b'( {} )').format(v)
        t[0].value = v
        return t[0]

    def and_test(self, t):
        assert len(t) == 2
        t[0].value = (b'( {} AND {} )').format(t[0].value, t[1].value)
        return t[0]

    def or_test(self, t):
        assert len(t) == 2
        t[0].value = (b'( {} OR {} )').format(t[0].value, t[1].value)
        return t[0]

    def compare_op(self, t):
        v = t[0]
        return v

    def not_expression(self, t):
        v = t[0]
        v.value = (b'NOT {}').format(v.value)
        return v

    def expression(self, t):
        exp = (b' ').join([ str(v.value) for v in t ])
        if not self.quoter.in_parenthesis(exp):
            t[0].value = (b'({})').format(exp)
        return t[0]

    def add(self, t):
        assert len(t) == 2
        t[0].value = (b'{} + {}').format(t[0].value, t[1].value)
        return t[0]

    def sub(self, t):
        assert len(t) == 2
        t[0].value = (b'{} - {}').format(t[0].value, t[1].value)
        return t[0]

    def div(self, t):
        assert len(t) == 2
        t[0].value = (b'{} / {}').format(t[0].value, t[1].value)
        return t[0]

    def mul(self, t):
        assert len(t) == 2
        t[0].value = (b'{} * {}').format(t[0].value, t[1].value)
        return t[0]

    def power(self, t):
        assert len(t) == 2
        t[0].value = (b'{} ^ {}').format(t[0].value, t[1].value)
        return t[0]

    def runtime_var(self, t):
        v = t[0]
        return v

    def regexp(self, t):
        """
        E.g. regexp(u'/^[0-9]*$/')
        """
        v = t[0]
        return v

    def func_call(self, t):
        """
        For function calls e.g. TEXT (tostring([area],"%.2f"))
        """
        func, params = t
        func_name = func.value
        func.value = (b'({}({}))').format(func_name, params)
        return func

    def func_params(self, t):
        params = (b',').join(str(v.value) for v in t)
        return params

    def attr_bind(self, t):
        assert len(t) == 1
        t = t[0]
        t.value = (b'[{}]').format(t.value)
        return t

    def extent(self, t):
        assert len(t) == 4
        return t

    def color(self, t):
        pass

    def value(self, t):
        return t

    def true(self, t):
        v = t[0]
        v.value = True
        return v

    def false(self, t):
        v = t[0]
        v.value = False
        return v

    def int(self, t):
        v = t[0]
        v.value = int(v.value)
        return v

    def float(self, t):
        v = t[0]
        v.value = float(v.value)
        return v

    def bare_string(self, t):
        return t[0]

    def name(self, t):
        v = t[0]
        return v

    def string(self, t):
        v = t[0]
        return v

    def path(self, t):
        return t[0]

    def string_pair(self, t):
        a, b = t
        return [a, b]

    def rgb(self, t):
        r, g, b = t
        return (r, g, b)

    def attr_bind_pair(self, t):
        assert len(t) == 2
        return t

    def colorrange(self, t):
        assert len(t) == 6
        return t

    def hexcolorrange(self, t):
        assert len(t) == 2
        return t

    def hexcolor(self, t):
        t[0].value = self.clean_string(t[0].value).lower()
        return t[0]

    def num_pair(self, t):
        a, b = t
        return (a, b)

    def int_pair(self, t):
        a, b = t
        return (a, b)

    def list(self, t):
        v = t[0]
        list_values = (b',').join([ str(s) for s in t ])
        v.value = b'{%s}' % list_values
        return v


class CommentsTransformer(Transformer_InPlace):

    def __init__(self, mapfile_todict):
        self._mapfile_todict = mapfile_todict

    def get_comments(self, meta):
        all_comments = []
        if hasattr(meta, b'inline_comments'):
            all_comments += meta.inline_comments
        if hasattr(meta, b'header_comments'):
            all_comments += meta.header_comments
        return all_comments

    def add_metadata_comments(self, d, metadata):
        """
        Any duplicate keys will be replaced with the last duplicate along with comments
        """
        if len(metadata) > 2:
            string_pairs = metadata[1:-1]
            for sp in string_pairs:
                if isinstance(sp.children[0], Token):
                    token = sp.children[0]
                    assert token.type == b'UNQUOTED_STRING'
                    key = token.value
                else:
                    token = sp.children[0].children[0]
                    key = token.value
                key = self._mapfile_todict.clean_string(key).lower()
                assert key in d.keys()
                key_comments = self.get_comments(sp.meta)
                d[b'__comments__'][key] = key_comments

        return d

    @v_args(tree=True)
    def _save_attr_comments(self, tree):
        d = self._mapfile_todict.transform(tree)
        d[b'__comments__'] = self.get_comments(tree.meta)
        return d

    @v_args(tree=True)
    def _save_composite_comments(self, tree):
        d = self._mapfile_todict.transform(tree)
        if b'__comments__' not in d:
            d[b'__comments__'] = OrderedDict()
        comments = self.get_comments(tree.meta)
        if comments:
            d[b'__comments__'][b'__type__'] = comments
        if d[b'__type__'] == b'metadata':
            md = tree.children[0].children
            self.add_metadata_comments(d, md)
        return d

    attr = _save_attr_comments
    composite = _save_composite_comments


class MapfileToDict(object):

    def __init__(self, include_position=False, include_comments=False, transformerClass=MapfileTransformer, **kwargs):
        self.include_position = include_position
        self.include_comments = include_comments
        self.transformerClass = transformerClass
        self.kwargs = kwargs

    def transform(self, tree):
        tree = Canonize().transform(tree)
        self.mapfile_transformer = self.transformerClass(include_position=self.include_position, include_comments=self.include_comments, **self.kwargs)
        if self.include_comments:
            comments_transformer = CommentsTransformer(self.mapfile_transformer)
            tree = comments_transformer.transform(tree)
        return self.mapfile_transformer.transform(tree)


class Canonize(Transformer_InPlace):

    @v_args(tree=True)
    def symbolset(self, tree):
        composite_type = Tree(b'composite_type', [Token(b'symbolset', b'symbolset')])
        tree.data = b'composite'
        tree.children.insert(0, composite_type)
        return tree