# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ../../../scrapy/soupselect.py
# Compiled at: 2011-08-03 14:24:39
"""
soupselect.py

CSS selector support for BeautifulSoup.

soup = BeautifulSoup('<html>...')
select(soup, 'div')
- returns a list of div elements

select(soup, 'div#main ul a')
- returns a list of links inside a ul inside div#main

"""
import re
tag_re = re.compile('^[a-z0-9]+$')
attribselect_re = re.compile('^(?P<tag>\\w+)?\\[(?P<attribute>\\w+)(?P<operator>[=~\\|\\^\\$\\*]?)' + '=?"?(?P<value>[^\\]"]*)"?\\]$')

def attribute_checker(operator, attribute, value=''):
    """
    Takes an operator, attribute and optional value; returns a function that
    will return True for elements that match that combination.
    """
    return {'=': lambda el: el.get(attribute) == value, 
       '~': lambda el: value in el.get(attribute, '').split(), 
       '^': lambda el: el.get(attribute, '').startswith(value), 
       '$': lambda el: el.get(attribute, '').endswith(value), 
       '*': lambda el: value in el.get(attribute, ''), 
       '|': lambda el: el.get(attribute, '') == value or el.get(attribute, '').startswith('%s-' % value)}.get(operator, lambda el: el.has_key(attribute))


def select(soup, selector):
    """
    soup should be a BeautifulSoup instance; selector is a CSS selector 
    specifying the elements you want to retrieve.
    """
    tokens = selector.split()
    current_context = [soup]
    for token in tokens:
        m = attribselect_re.match(token)
        if m:
            tag, attribute, operator, value = m.groups()
            if not tag:
                tag = True
            checker = attribute_checker(operator, attribute, value)
            found = []
            for context in current_context:
                found.extend([ el for el in context.findAll(tag) if checker(el) ])

            current_context = found
            continue
        if '#' in token:
            tag, id = token.split('#', 1)
            if not tag:
                tag = True
            el = current_context[0].find(tag, {'id': id})
            if not el:
                return []
            current_context = [
             el]
            continue
        if '.' in token:
            tag, klass = token.split('.', 1)
            if not tag:
                tag = True
            found = []
            for context in current_context:
                found.extend(context.findAll(tag, {'class': lambda attr: attr and klass in attr.split()}))

            current_context = found
            continue
        if token == '*':
            found = []
            for context in current_context:
                found.extend(context.findAll(True))

            current_context = found
            continue
        if not tag_re.match(token):
            return []
        found = []
        for context in current_context:
            found.extend(context.findAll(token))

        current_context = found

    return current_context


def monkeypatch(BeautifulSoupClass=None):
    """
    If you don't explicitly state the class to patch, defaults to the most 
    common import location for BeautifulSoup.
    """
    if not BeautifulSoupClass:
        from BeautifulSoup import BeautifulSoup as BeautifulSoupClass
    BeautifulSoupClass.findSelect = select


def unmonkeypatch(BeautifulSoupClass=None):
    if not BeautifulSoupClass:
        from BeautifulSoup import BeautifulSoup as BeautifulSoupClass
    delattr(BeautifulSoupClass, 'findSelect')