# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/bouma/gitprojects/provgroningen/buildout/src/djinn_i18n/djinn_i18n/__init__.py
# Compiled at: 2014-10-06 05:47:45
from django.templatetags import i18n
from django.template import Node
from urls import urlpatterns
DESCR = 'The i18n (internationalisation) tool enables you to override\ntranslations for the Djinn intranet application'

def get_urls():
    return urlpatterns


def get_js():
    return []


def get_css():
    return [
     'djinn_i18n.css']


def get_info():
    return {'name': 'i18n', 'url': 'djinn_i18n_index', 
       'description': DESCR, 
       'icon': 'flag'}


original_do_translate = i18n.do_translate

class TranslateNodeWrapper(Node):

    def __init__(self, node, attr=False):
        """ If attr is true-ish, we're within an attribute. If so, don't wrap
        with a span, but set the message id on the element itself. """
        self.node = node
        self.attr = attr

    def render(self, context):
        value = self.node.render(context)
        token = self.node.filter_expression.token.replace('"', '')
        return '%s' % value


def _do_translate(parser, token):
    attr = False
    close_tag = open_tag = -1
    i = 0
    while close_tag == -1 and open_tag == -1 and i < len(parser.tokens):
        close_tag = parser.tokens[i].contents.find('>')
        open_tag = parser.tokens[i].contents.find('<')
        i += 1

    if close_tag > -1 and (open_tag == -1 or close_tag < open_tag):
        attr = True
    return TranslateNodeWrapper(original_do_translate(parser, token), attr=attr)