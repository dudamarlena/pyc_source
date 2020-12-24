# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tyrs/utils.py
# Compiled at: 2011-12-19 14:12:42
import re, os, sys, string
from htmlentitydefs import entitydefs

def set_console_title():
    try:
        sys.stdout.write('\x1b]2;Tyrs\x07')
    except:
        pass


def cut_attag(name):
    if name[0] == '@':
        name = name[1:]
    return name


def get_exact_nick(word):
    if word[0] == '@':
        word = word[1:]
    alphanum = string.letters + string.digits
    try:
        while word[(-1)] not in alphanum:
            word = word[:-1]

    except IndexError:
        pass

    return word


def encode(string):
    try:
        return string.encode(sys.stdout.encoding, 'replace')
    except AttributeError:
        return string


def html_unescape(str):
    """ Unescapes HTML entities """

    def entity_replacer(m):
        entity = m.group(1)
        if entity in entitydefs:
            return entitydefs[entity]
        else:
            return m.group(0)

    return re.sub('&([^;]+);', entity_replacer, str)


def get_source(source):
    if source != 'web':
        source = source.split('>')
        source = source[1:]
        source = (' ').join(source)
        source = source.split('<')[:1]
        source = source[:1]
        source = (' ').join(source)
    return source


def open_image(user):
    image = user.profile_image_url
    command = tyrs.container['conf'].params['open_image_command']
    os.system(command % image)


def get_urls(text):
    return re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', text)