# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: utf8config/core.py
# Compiled at: 2017-10-14 20:07:45
from __future__ import unicode_literals
import string
from collections import OrderedDict
import attr
try:
    from .io import load_value, dump_value
except:
    from utf8config.io import load_value, dump_value

bad_charset = set(b'`~!@#$%^&*()-+={[}]|\\:;<,>.?/\t\r\n ')

def validate_key(key):
    """
    Check the namespace.

    Valid namespace: a-zA-Z0-9, underscore. Not startswith numbers.
    """
    if len(bad_charset.intersection(key)):
        raise ValueError(b'%r is invalid key' % key)
    if key[0] in string.digits:
        raise ValueError(b'%r is invalid key' % key)


def extract_comment(line):
    u"""
    Extract comment string from `# This is comment`。
    """
    if not line.startswith(b'#'):
        raise ValueError
    index = 0
    for char in line:
        if char == b'#':
            index += 1
        else:
            return line[index:].strip()


def remove_post_comment(lines):
    u"""

    **中文文档**

    由于一段section的文本最后可能会带有一些注释, 但这些注释是属于下一个section的
    upper_comment, 而不属于这一个section。所以需要移除。
    """
    counter = 0
    reversed_lines = lines[::-1]
    for line in reversed_lines:
        counter += 1
        if not line.startswith(b'#'):
            break

    new_lines = reversed_lines[counter - 1:]
    lines = new_lines[::-1]
    return lines


@attr.s
class Field(object):
    key = attr.ib()
    value = attr.ib()
    upper_comment = attr.ib(default=b'')
    side_comment = attr.ib(default=b'')

    @staticmethod
    def load(text):
        lines = [ line.strip() for line in text.split(b'\n') if line.strip() ]
        counter = 0
        upper_comment_lines = list()
        side_comment = b''
        for line in lines:
            counter += 1
            if line.startswith(b'#'):
                comment = extract_comment(line)
                upper_comment_lines.append(comment)
            if not line.startswith(b'#'):
                if b' # ' in line:
                    side_comment = line.split(b' # ')[(-1)].strip()
                    key_value = line.split(b' # ')[0]
                else:
                    key_value = line
                key, value = key_value.split(b'=')
                key = key.strip()
                value = load_value(value.strip())

        upper_comment = (b'\n').join(upper_comment_lines)
        return Field(key, value, upper_comment, side_comment)

    def dump(self, ignore_comment=False):
        """

        :param no_comment: ignore comment.
        """
        lines = list()
        if ignore_comment:
            lines.append(b'%s = %s' % (self.key, dump_value(self.value)))
        else:
            if self.upper_comment:
                lines.append((b'\n').join([ b'# ' + l.strip() for l in self.upper_comment.split(b'\n')
                                          ]))
            if self.side_comment:
                lines.append(b'%s = %s # %s' % (
                 self.key, dump_value(self.value), self.side_comment))
            else:
                lines.append(b'%s = %s' % (self.key, dump_value(self.value)))
        lines.append(b'')
        return (b'\n').join(lines)


@attr.s
class ContainerStyled(object):

    def __getitem__(self, key):
        return self.data[key]

    def keys(self):
        return list(self.data.keys())

    def values(self):
        return list(self.data.values())

    def items(self):
        return list(self.data.items())

    def _add(self, key, value):
        if key in self.data:
            raise KeyError(b'Key(%s) already exists!' % key)
        else:
            self.data[key] = value

    def _remove(self, key):
        if key in self.data:
            del self.data[key]
        else:
            raise KeyError(b'Key(%s) not exists!' % key)

    def _construct_list(self, item_or_list):
        if isinstance(item_or_list, (tuple, list)):
            return item_or_list
        else:
            return (
             item_or_list,)


@attr.s
class Section(ContainerStyled):
    """
    Section **没有side_comment**!
    """
    name = attr.ib()
    upper_comment = attr.ib(default=b'')
    data = attr.ib(default=attr.Factory(OrderedDict))

    @property
    def fields(self):
        """
        field dict.
        """
        return self.data

    def add_field(self, field_or_field_list):
        """

        :param field_or_field_list: :class:`Field` or list of it.
        """
        field_or_field_list = self._construct_list(field_or_field_list)
        for field in field_or_field_list:
            self._add(field.key, field)

    def remove_field(self, key_or_key_list):
        """

        :param key_or_key_list: field name or list of it.
        """
        key_or_key_list = self._construct_list(key_or_key_list)
        for key in key_or_key_list:
            self._remove(key)

    @staticmethod
    def load(text):
        """
        load section from text.
        """
        lines = [ line.strip() for line in text.split(b'\n') if line.strip() ]
        counter = 0
        upper_comment_lines = list()
        for line in lines:
            counter += 1
            if line.startswith(b'#'):
                comment = extract_comment(line)
                upper_comment_lines.append(comment)
            elif line.startswith(b'[') and line.endswith(b']'):
                name = line[1:-1]
                validate_key(name)
                section = Section(name, (b'\n').join(upper_comment_lines))
                break

        lines = lines[counter:]
        field_text_list = list()
        field_lines = list()
        for line in lines:
            field_lines.append(line)
            if line.startswith(b'#'):
                pass
            else:
                field_text_list.append((b'\n').join(field_lines))
                field_lines = list()

        for field_text in field_text_list:
            field = Field.load(field_text)
            section.add_field(field)

        return section

    def dump(self, ignore_comment=False):
        """
        dump section to text.

        :param no_comment: ignore comment.
        """
        lines = list()
        if ignore_comment:
            pass
        else:
            if self.upper_comment:
                lines.append((b'\n').join([ b'# ' + l.strip() for l in self.upper_comment.split(b'\n')
                                          ]))
            lines.append(b'[%s]\n' % self.name)
            for field in self.fields.values():
                lines.append(field.dump(ignore_comment=ignore_comment))

        return (b'\n').join(lines)


@attr.s
class Config(ContainerStyled):
    """
    """
    data = attr.ib(default=attr.Factory(OrderedDict))

    @property
    def sections(self):
        return self.data

    def add_section(self, section_or_section_list):
        """

        :param section_or_section_list: :class:`Section` or list of it.
        """
        section_or_section_list = self._construct_list(section_or_section_list)
        for section in section_or_section_list:
            self._add(section.name, section)

    def remove_section(self, name_or_name_list):
        """

        :param name_or_name_list: section name or list of it.
        """
        name_or_name_list = self._construct_list(name_or_name_list)
        for name in name_or_name_list:
            self._remove(name)

    @staticmethod
    def load(text):
        """
        load config from text.
        """
        section_text_list = list()
        section_text_lines = list()
        for line in [b'# Empty section', b'[empty_section]', b'empty = empty'] + [ line.strip() for line in text.split(b'\n') if line.strip() ]:
            if line.startswith(b'[') and line.endswith(b']'):
                old_section_text_list = section_text_lines[:]
                section_text_lines = remove_post_comment(section_text_lines)
                section_text_list.append((b'\n').join(section_text_lines))
                section_text_lines = list()
                for line_ in old_section_text_list[::-1]:
                    if line_.startswith(b'#'):
                        section_text_lines.append(line_)
                    else:
                        break

                section_text_lines.append(line)
            else:
                section_text_lines.append(line)

        section_text_lines = remove_post_comment(section_text_lines)
        section_text_list.append((b'\n').join(section_text_lines))
        config = Config()
        for text in section_text_list[2:]:
            section = Section.load(text)
            config.add_section(section)

        return config

    def dump(self, ignore_comment=False):
        """
        dump config to text.

        :param no_comment: ignore comment.
        """
        lines = list()
        for section in self.sections.values():
            lines.append(section.dump(ignore_comment=ignore_comment))

        return (b'\n').join(lines)