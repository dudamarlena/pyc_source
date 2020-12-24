# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marple/marple.py
# Compiled at: 2018-07-01 03:00:38
# Size of source mod 2**32: 4542 bytes
import re, os, configparser, yaml
from configparser import MissingSectionHeaderError
from django.conf import settings
from django.core import management
from django.core.management.base import BaseCommand, CommandError
from marple.models import MarpleItem
from marple.apps import MarpleConfig

class MarpleBaseManager:

    def __init__(self, type, content, guess_line, *args, **kwargs):
        self.type = type
        self.content = content
        self.guess_line = guess_line

    def get_name(self):
        return self.re_name.search(self.guess_line).group(1)

    def get_data(self):
        data = {}
        try:
            data = yaml.load(self.content.replace('/// ', ''))
        except yaml.YAMLError as exc:
            print(exc)

        data['guess_line'] = self.guess_line
        return data

    def save(self):
        MarpleItem.objects.create(type=(self.type),
          name=(self.get_name()),
          data=(self.get_data()))


class MarpleVariableManager(MarpleBaseManager):

    def __init__(self, *args, **kwargs):
        self.re_name = re.compile('\\$(.*):')
        (super(MarpleVariableManager, self).__init__)(*args, **kwargs)


class MarpleMixinManager(MarpleBaseManager):

    def __init__(self, *args, **kwargs):
        self.re_name = re.compile('@mixin (.*){')
        (super(MarpleMixinManager, self).__init__)(*args, **kwargs)


class MarpleColorManager(MarpleBaseManager):

    def __init__(self, *args, **kwargs):
        self.re_name = re.compile('\\$(.*):')
        self.re_value = re.compile('\\$.+:(.+);')
        (super(MarpleColorManager, self).__init__)(*args, **kwargs)

    def get_data(self):
        data = super(MarpleColorManager, self).get_data()
        data['value'] = self.re_value.search(self.guess_line).group(1)
        return data


class Marple:
    r_comment = re.compile('(?m)(^/{3} .*(?:\n/{3} .*)*\n?)(^.*)$')
    r_guess_color = re.compile('^\\s*\\$\\S+:\\s*(#[a-fA-F0-9]{3}|#[a-fA-F0-9]{6}|rgba?\\(\\s*\\d+\\s*,\\s*\\d+\\s*,\\s*\\d+\\s*(,\\s*\\.?\\d+\\s*)?\\))\\s*;$')
    r_guess_mixin = re.compile('^\\s*@mixin .*$')
    r_guess_variable = re.compile('^\\s*\\$\\S+\\s*:\\s*(?!(?:#|rgba?))\\S*;$')

    def __init__(self, *args, **kwargs):
        self.root = getattr(settings, 'MARPLE_ROOT', 'sass')
        self.exclude = getattr(settings, 'MARPLE_EXCLUDE', ['.sass-cache'])
        self.managers = {'variable':MarpleVariableManager, 
         'mixin':MarpleMixinManager, 
         'color':MarpleColorManager}

    def guess_type(self, line):
        if self.r_guess_color.search(line) != None:
            return 'color'
        else:
            if self.r_guess_mixin.search(line) != None:
                return 'mixin'
            if self.r_guess_variable.search(line) != None:
                return 'variable'

    def get_files(self):
        out = []
        for dirname, dirnames, filenames in os.walk(self.root):
            for filename in filenames:
                relpath = os.path.join(dirname, filename)
                if relpath.endswith('.scss'):
                    out.append(relpath)

            [dirnames.remove(dir) for dir in self.exclude if dir in dirnames]

        return out

    def get_comments(self, content):
        comments = []
        for match in self.r_comment.finditer(content):
            comment_content = match.group(1)
            guess_line = match.group(2)
            comment_type = self.guess_type(guess_line)
            if not comment_type:
                pass
            else:
                comments.append((comment_type, comment_content, guess_line))

        return comments

    def digest(self, force_update=False):
        if not force_update:
            return
        else:
            MarpleItem.objects.all().delete()
            files = self.get_files()
            content = ''
            for file in files:
                with open(file, 'r') as (f):
                    content += f.read()

            comments = self.get_comments(content)
            for comment in comments:
                comment_type, comment_content, guess_line = comment
                manager_class = self.managers[comment_type]
                manager = manager_class(comment_type, comment_content, guess_line)
                manager.save()

            return 'Found %s comments in %s files.' % (len(comments), len(files))