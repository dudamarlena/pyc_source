# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/will/projects/moya/moya/settings.py
# Compiled at: 2017-01-15 13:25:40
from __future__ import unicode_literals
from __future__ import print_function
from __future__ import absolute_import
from .containers import OrderedDict
from . import iniparse
from .compat import text_type, string_types, PY2, implements_to_string, implements_bool
from . import errors
from .tools import textual_list
from fs.path import dirname, join, normpath, relpath
import io, os

def read_settings(fs, path):
    with fs.safeopen(path, b'rb') as (settings_file):
        cfg = iniparse.parse(settings_file)
    return cfg


@implements_to_string
class SettingsKeyError(KeyError):

    def __init__(self, message):
        self.message = message

    def __str__(self):
        return self.message


class SettingsContainer(OrderedDict):

    @classmethod
    def apply_master(self, master, settings):
        for section_name, section in master.items():
            if section_name == b'service':
                continue
            if section_name in settings:
                settings[section_name].update(section)
            else:
                settings[section_name] = section

    @classmethod
    def read(cls, fs, path, master=None):
        visited = []
        if not isinstance(path, string_types):
            for p in path:
                if fs.isfile(p):
                    path = p
                    break
            else:
                raise errors.SettingsError((b'settings file not found (looked for {} in {})').format(textual_list(path, join_word=b'and'), fs))

        settings_stack = []
        while 1:
            path = relpath(normpath(path))
            if path in visited:
                raise errors.SettingsError((b'recursive extends detected, "{}" has already been extended').format(path))
            with fs.open(path, b'rt') as (settings_file):
                s = iniparse.parse(settings_file, SettingsContainer(), section_class=SettingsSectionContainer)
            visited.append(path)
            settings_stack.append(s)
            if b'extends' in s[b'']:
                path = join(dirname(path), s[b''][b'extends'])
            else:
                break

        settings_stack = settings_stack[::-1]
        settings = settings_stack[0]
        s = cls.__class__(settings_stack[0])
        for s in settings_stack[1:]:
            for section_name, section in s.items():
                if section_name in settings:
                    settings[section_name].update(section)
                else:
                    settings[section_name] = section

        if master is not None:
            cls.apply_master(master, settings)
        return settings

    @classmethod
    def read_os(cls, path):
        visited = []
        settings_stack = []
        while 1:
            path = os.path.abspath(os.path.normpath(path))
            if path in visited:
                raise errors.SettingsError((b'recursive extends detected, "{}" has already been extended').format(path))
            with io.open(path, b'rt') as (settings_file):
                s = iniparse.parse(settings_file, SettingsContainer(), section_class=SettingsSectionContainer)
            visited.append(path)
            settings_stack.append(s)
            if b'extends' in s[b'']:
                path = s[b''][b'extends']
            else:
                break

        settings_stack = settings_stack[::-1]
        settings = settings_stack[0]
        s = cls.__class__(settings_stack[0])
        for s in settings_stack[1:]:
            for section_name, section in s.items():
                if section_name in settings:
                    settings[section_name].update(section)
                else:
                    settings[section_name] = section

        return settings

    @classmethod
    def read_from_file(self, settings_file):
        """Reads settings, but doesn't do any extends processing"""
        settings = iniparse.parse(settings_file, SettingsContainer(), section_class=SettingsSectionContainer)
        return settings

    @classmethod
    def from_dict(self, d):
        return SettingsSectionContainer((k, SettingContainer(v)) for k, v in d.items())

    @classmethod
    def create(cls, **kwargs):
        return cls.from_dict(kwargs)

    def export(self, output_file, comments=None):
        """Write the settings to an open file"""
        ini = iniparse.write(self, comments=comments)
        output_file.write(ini)

    def copy(self):
        return SettingsContainer(self)

    def __getitem__(self, key):
        try:
            return super(SettingsContainer, self).__getitem__(key)
        except KeyError:
            return EmptySettings()

    def get(self, section_name, key, default=Ellipsis):
        if section_name not in self:
            if default is Ellipsis:
                raise SettingsKeyError(b'required section [%s] not found in settings' % section_name)
            else:
                return default
        section = self[section_name]
        if key not in section:
            if default is Ellipsis:
                raise SettingsKeyError(b"key '%s' not found in section [%s]" % (key, section_name))
            else:
                return default
        return section[key]

    def set(self, section_name, key, value):
        if section_name not in self:
            self[section_name] = SettingsSectionContainer()
        self[section_name][key] = value

    def get_bool(self, section_name, key, default=False):
        value = self.get(section_name, key, b'yes' if default else b'no')
        return value.strip().lower() in ('yes', 'true')

    def get_list(self, section_name, key, default=b''):
        value = self.get(section_name, key, default=default)
        return [ line.strip() for line in value.splitlines() if line.strip() ]

    def get_int(self, section_name, key, default=None):
        value_text = self.get(section_name, key, None)
        if value_text is None or not value_text.strip():
            return
        try:
            value = int(value_text)
        except:
            raise SettingsKeyError((b"key [{}]/{} should be empty or an integer value (not '{}')").format(section_name, key, value_text))
        else:
            return value

        return

    def __moyaconsole__(self, console):
        from console import Cell
        table = [
         (
          Cell(b'key', bold=True), Cell(b'value', bold=True))]
        table += sorted(self.items())
        console.table(table)


class SettingsSectionContainer(OrderedDict):

    def get_int(self, key, default=None):
        if key not in self:
            return default
        value = int(self[key])
        return value

    def get_bool(self, key, default=False):
        value = self.get(key, b'yes' if default else b'no')
        return value.strip().lower() in ('yes', 'true')

    def get_list(self, key, default=b''):
        value = self.get(key, default)
        return [ line.strip() for line in value.splitlines() if line.strip() ]

    def __moyaconsole__(self, console):
        from console import Cell
        table = [
         (
          Cell(b'key', bold=True), Cell(b'value', bold=True))]
        table += sorted(self.items())
        console.table(table)

    def __setitem__(self, key, value):
        value = SettingContainer(text_type(value))
        super(SettingsSectionContainer, self).__setitem__(key, value)


@implements_bool
class EmptySettings(object):

    def __getitem__(self, key):
        if key == b'list':
            return []
        if key == b'bool':
            return False
        if key == b'int':
            return 0
        return b''

    def __repr__(self):
        return b'<emptysettings>'

    def get_int(self, key, default=None):
        return default

    def get_bool(self, key, default=False):
        return default

    def get_list(self, key, default=b''):
        return default

    def get(self, key, default=None):
        return default

    def __bool__(self):
        return False

    def __unicode__(self):
        return b''

    def __iter__(self):
        return iter([])

    def items(self):
        return []

    def __moyaconsole__(self, console):
        from console import Cell
        table = [
         (
          Cell(b'key', bold=True), Cell(b'value', bold=True))]
        console.table(table)


@implements_to_string
class SettingContainer(text_type):

    def __init__(self, setting_text):
        if PY2:
            super(SettingContainer, self).__init__(setting_text)
        else:
            super().__init__()
        self.setting_text = setting_text.strip()
        self.lines = [ line.strip() for line in setting_text.splitlines() ] or []
        self.first = self.lines[0] if self.lines else b''
        self.bool = self.setting_text.lower() in ('yes', 'true')
        try:
            self.int = int(self.setting_text)
        except ValueError:
            self.int = None

        try:
            self.float = float(self.setting_text)
        except ValueError:
            self.float = None

        return

    def __str__(self):
        return self.setting_text

    def __getitem__(self, index):
        if isinstance(index, string_types):
            if index == b'list':
                return self.lines
            if index == b'bool':
                return self.bool
            if index == b'int':
                return self.int
            if index == b'float':
                return self.float
        return self.lines[index]

    def __eq__(self, other):
        return self.first == other

    def __ne__(self, other):
        return self.first != other

    if not PY2:

        def __hash__(self):
            return super().__hash__()


if __name__ == b'__main__':
    settings = SettingsContainer()
    print(settings[b'nothere'])
    s = SettingContainer(b'foo\nbar')
    print(s == b'foo')
    print(s[b'list'])