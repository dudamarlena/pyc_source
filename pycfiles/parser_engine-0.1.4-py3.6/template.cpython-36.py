# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parser_engine/template.py
# Compiled at: 2019-04-16 05:55:04
# Size of source mod 2**32: 5081 bytes
import json, copy, six
from scrapy.linkextractors import LinkExtractor
from .utils import is_string
from . import log

class PETemplate(object):

    def __init__(self, name, fields=None, **kwargs):
        self.name = name
        self.fields = fields
        for k, v in kwargs.items():
            self.__setattr__(k, v)

    def __getattr__(self, item):
        return self.get(item)

    @classmethod
    def from_json(cls, s):
        if not s:
            raise RuntimeError('init ' + cls.__name__ + ' from empty json/dict error, maybe the template not found by id?')
        else:
            s = copy.deepcopy(s)
            if not isinstance(s, dict):
                try:
                    s = json.loads(s)
                except json.decoder.JSONDecodeError as e:
                    raise e

            fields = s.pop('fields', tuple())
            if fields:
                fields = [PEField((field.pop('key')), **field) for field in fields if field.get('key')]
        return cls((s.pop('name')), fields, **s)

    def get(self, key):
        try:
            return self.__getattribute__(key)
        except AttributeError:
            pass

    def get_link_extractor(self):
        return LinkExtractor(allow=(self.get('allow')), deny=(self.get('deny')),
          allow_domains=(self.get('allow_domains')),
          deny_domains=(self.get('deny_domains')),
          restrict_css=(self.get('restrict_css')),
          restrict_xpaths=(self.get('restrict_xpaths')))


class PEField(dict):

    def __init__(self, key, **kwargs):
        kwargs['key'] = key
        (super().__init__)(**kwargs)
        if not self.xpath:
            if self.tags:
                self._compile_xpath()
        if not self.css:
            if self.attr_name:
                self._compile_css()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return '<PEField> ' + json.dumps(self, indent=2)

    def __getattr__(self, item):
        return self.get(item)

    def _compile_xpath(self):
        self._compile_xpath_tag_condition()
        self.xpath = './/{tag}{tag_condition}{attribute_to_extract}{suffix}'.format(tag=('/'.join(self.tags)),
          tag_condition=('[' + self.tag_condition + ']' if self.tag_condition else self.get_xpath_by_position(self.position)),
          attribute_to_extract=('/@' + self.attr_name if self.attr_name else ''),
          suffix=('/text()' if not self.attr_name else ''))
        log.debug('field [%s] xpath: "%s"' % (self.key, self.xpath))

    def _compile_css(self):
        pass

    def _compile_xpath_tag_condition(self):
        attr = self.attributes
        if is_string(attr):
            self.tag_condition = attr
        else:
            if isinstance(attr, dict):
                s = []
                for k, v in attr.items():
                    s.append('@' + k + '=' + self._cast_value(v))

                self.tag_condition = 'and'.join(s)
            elif isinstance(attr, list):
                s = []
                for i in attr:
                    s.append('@' + i[0] + self._cast_operator(i[1]) + self._cast_value(i[2]))

                self.tag_condition = 'and'.join(s)

    @staticmethod
    def _cast_operator(origin):
        return origin

    @staticmethod
    def _cast_value(origin):
        if is_string(origin):
            return '"' + origin + '"'
        else:
            return origin

    @staticmethod
    def get_xpath_by_position(position):
        if position is None or position == '':
            return ''
        else:
            if isinstance(position, six.string_types):
                if position.startswith('>') or position.startswith('<'):
                    return '[position()%s]' % position
            pos = int(position)
            if pos > 0:
                return '[%d]' % pos
            if pos < 0:
                return '[last()-%d]' % (abs(pos) - 1)