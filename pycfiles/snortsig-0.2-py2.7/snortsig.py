# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snortsig.py
# Compiled at: 2014-06-28 21:48:17
from pyparsing import *
import collections, itertools

class SnortSig(object):
    _proto = Or([CaselessLiteral('tcp'), CaselessLiteral('udp'), CaselessLiteral('icmp'), CaselessLiteral('ip')])
    _direction = Or([Literal('<>'), Literal('->')])
    _action = Or([CaselessLiteral('pass'),
     CaselessLiteral('alert'),
     CaselessLiteral('reject'),
     CaselessLiteral('log'),
     CaselessLiteral('activate'),
     CaselessLiteral('dynamic'),
     CaselessLiteral('drop'),
     CaselessLiteral('sdrop')])
    dbl2 = Regex('"(?:[^"\\n\\r\\\\]|(?:\\\\")|(?:\\\\x[0-9a-fA-F]+)|(?:\\\\.))*"')
    dbl2.setParseAction(removeQuotes)
    _ipaddr = Combine(Word(nums) + ('.' + Word(nums)) * 3)
    _range = Combine(_ipaddr + '/' + Word(nums))
    _variable = Combine('$' + Word(alphanums + '_'))
    _ipaddr_list = Suppress('[') + delimitedList(Or([_ipaddr, _range, _variable])) + Suppress(']')
    _port_nums = Optional('!') + Or([
     Optional(':') + Word(nums) + Optional(':'),
     Word(nums) + ':' + Word(nums)])
    _port_list = Suppress('[') + delimitedList(Or([_port_nums, _variable])) + Suppress(']')
    _ports = Optional('!') + Or([_port_nums, _port_list, _variable, CaselessLiteral('any')])
    _key = Word(alphanums + '_') + Suppress(':')
    _noparam_element = Word(alphanums + '_') + Suppress(';')
    _delimited_pairs_element = _key + delimitedList(Or([Word(alphanums + '*_?%~+^<>()=#@&:!|./- '), Word(alphanums + '_') + Word(alphanums + '_-')])) + Suppress(';')
    _quoted_element = _key + dbl2 + Suppress(';')
    _number_element = _key + Optional('!') + Word(nums) + Suppress(';')
    _number_range = Optional('!') + Or([
     Word(nums) + '<>' + Word(nums),
     '>' + Optional('=') + Word(nums),
     '<' + Optional('=') + Word(nums),
     '=' + Word(nums),
     '-' + Word(nums),
     Word(nums) + '-',
     Word(nums) + '-' + Word(nums)])
    _urilen_element = CaselessLiteral('urilen') + Suppress(':') + _number_range + Optional(Literal(',') + Or([Literal('norm'), Literal('raw')])) + Suppress(';')
    _simple_range_element = _key + _number_range + Suppress(';')
    _word_element = _key + Word(alphas + '!<>+*-') + Suppress(';')
    _metadata_element = CaselessLiteral('metadata') + Suppress(':') + delimitedList(Group(Word(alphanums + '_') + Or([quotedString, OneOrMore(Word(alphanums + '_|-'))]))) + Suppress(';')
    _delilmited_element = Word(alphas) + Suppress(':') + delimitedList(Word(alphanums + '*?%~._+<>=&!|-')) + Suppress(';')
    _pcre_element = CaselessLiteral('pcre') + Suppress(':') + Optional('!') + dbl2 + Suppress(';')
    _content_modifier = Or([
     CaselessLiteral('nocase') + Suppress(';'),
     CaselessLiteral('rawbytes') + Suppress(';'),
     Group(CaselessLiteral('depth') + Suppress(':') + Word(alphanums + '_') + Suppress(';')),
     Group(CaselessLiteral('offset') + Suppress(':') + Word(alphanums + '_') + Suppress(';')),
     Group(CaselessLiteral('distance') + Suppress(':') + Word(alphanums + '_') + Suppress(';')),
     Group(CaselessLiteral('within') + Suppress(':') + Word(alphanums + '_') + Suppress(';')),
     CaselessLiteral('http_client_body') + Suppress(';'),
     CaselessLiteral('http_cookie') + Suppress(';'),
     CaselessLiteral('http_raw_cookie') + Suppress(';'),
     CaselessLiteral('http_header') + Suppress(';'),
     CaselessLiteral('http_raw_header') + Suppress(';'),
     CaselessLiteral('http_method') + Suppress(';'),
     CaselessLiteral('http_uri') + Suppress(';'),
     CaselessLiteral('http_raw_uri') + Suppress(';'),
     CaselessLiteral('http_stat_code') + Suppress(';'),
     CaselessLiteral('http_stat_msg') + Suppress(';'),
     Group(CaselessLiteral('fast_pattern') + Optional(Suppress(':') + Word(alphanums + '_')) + Suppress(';'))])
    _content_element = Or([CaselessLiteral('content'), CaselessLiteral('uricontent')]) + Suppress(':') + Optional('!') + dbl2 + Suppress(';') + ZeroOrMore(_content_modifier)
    _element = Or([
     _content_element,
     _pcre_element,
     _metadata_element,
     _urilen_element,
     _word_element,
     _delimited_pairs_element,
     _simple_range_element,
     _number_element,
     _quoted_element,
     _noparam_element])
    _src_dst = Optional('!') + Or([CaselessLiteral('any'), _variable, _ipaddr_list, _range, _ipaddr])
    _signature = Optional(OneOrMore('#'))('disabled') + _action('action') + _proto('protocol') + _src_dst('src') + _ports('src_port') + _direction('direction') + _src_dst('dst') + _ports('dst_port') + Suppress('(') + Dict(OneOrMore(Group(_element)))('payload') + Suppress(')')

    def __init__(self):
        self.sigs = []
        self.attribs = collections.Counter()
        self.unparsable = []
        self.comments = []

    def fromstring(self, sigs):
        for sigline in sigs.splitlines():
            try:
                sig = self._signature.parseString(sigline)
            except:
                sig_header = '#' + self._action
                try:
                    sig_header.parseString(sigline)
                except:
                    self.comments.append(sigline)
                else:
                    self.unparsable.append(sigline)

            else:
                payload = sig['payload']
                options = {}
                for e in payload:
                    self.attribs.update([e[0]])
                    if e[0] in options:
                        value = []
                        for i in e[1:]:
                            if isinstance(i, ParseResults):
                                value.append(i.asList())
                            else:
                                value.append(i)

                        options[e[0]].append(value)
                    else:
                        value = []
                        for i in e[1:]:
                            if isinstance(i, ParseResults):
                                value.append(i.asList())
                            else:
                                value.append(i)

                        options[e[0]] = [
                         value]

                for k, v in options.items():
                    if isinstance(v, list) and len(v) == 1:
                        chain = itertools.chain.from_iterable(v)
                        options[k] = list(chain)

                disabled = '1'
                try:
                    sig['disabled']
                except KeyError:
                    disabled = '0'

                self.sigs.append({'disabled': [
                              disabled], 
                   'action': [
                            sig['action']], 
                   'protocol': [
                              sig['protocol']], 
                   'src': sig['src'].asList(), 
                   'src_port': sig['src_port'].asList(), 
                   'direction': [
                               sig['direction']], 
                   'dst': sig['dst'].asList(), 
                   'dst_port': sig['dst_port'].asList(), 
                   'options': options, 
                   'comments': self.comments})
                self.comments = []

    def fromfile(self, sigfile):
        with open(sigfile, 'rb') as (f):
            sigs = f.read()
        self.fromstring(sigs)

    def getall(self):
        return self.sigs

    def search(self, term, attribute=None, exact=True):
        ret = []
        if attribute is not None:
            if attribute in self.attribs:
                for s in self.sigs:
                    if attribute in s['options'].keys() and self._list_search(s['options'][attribute], term, exact):
                        ret.append(s)

            else:
                for s in self.sigs:
                    if attribute in s and self._list_search(s[attribute], term, exact):
                        ret.append(s)

        else:
            for s in self.sigs:
                for k, v in s.items():
                    if k == 'comments':
                        continue
                    if self._list_search(v, term, exact):
                        ret.append(s)
                        break

        return ret

    def _list_search(self, search, term, exact):
        if isinstance(search, basestring):
            if exact and search == term or not exact and term in search:
                return True
        if isinstance(search, dict):
            for k, v in search.items():
                if self._list_search(v, term, exact):
                    return True

        for e in search:
            if isinstance(e, list):
                if self._list_search(e, term, exact):
                    return True
            elif exact and e == term or not exact and term in e:
                return True

    def unparsed(self):
        return self.unparsable