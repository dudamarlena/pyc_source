# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/fellowiki/util/xmlelement.py
# Compiled at: 2006-11-21 20:30:39
"""

TODO
    
"""
from copy import copy
import elementtree.ElementTree as ElementTree

class XMLElement(object):
    __module__ = __name__

    def __init__(self, tag=None, content=None, prepend_to=None, append_to=None, **attributes):
        self.tag = tag
        if content is None:
            self.content = []
        else:
            try:
                content.pop
                self.content = content
            except AttributeError:
                self.content = [
                 content]

        self.attributes = {}
        for (key, val) in attributes.items():
            if key[-1:] == '_':
                self.attributes[key[:-1]] = val
            else:
                self.attributes[key] = val

        self.callback = []
        self.translations = []
        if prepend_to is not None:
            prepend_to.prepend(self)
        if append_to is not None:
            append_to.append(self)
        return

    def clone(self, other):
        self.tag = other.tag
        self.content = other.content
        self.attributes = other.attributes
        self.callback = other.callback
        self.translations = other.translations

    def to_element_tree(self):
        xhtml = ElementTree.Element(self.tag)
        sub_xhtml = None
        current_textlist = []
        content = copy(self.content)
        translations = []
        for (key, val) in self.attributes.items():
            xhtml.set(key, str(val))

        while content:
            item = content.pop(0)
            try:
                current_textlist.extend(item)
            except TypeError:
                if item.tag is None:
                    content = item.content + content
                else:
                    current_text = ('').join(current_textlist)
                    current_textlist = []
                    if sub_xhtml is None:
                        xhtml.text = current_text
                    else:
                        sub_xhtml.tail = current_text
                    (sub_xhtml, sub_translations) = item.to_element_tree()
                    xhtml.append(sub_xhtml)
                    translations.extend(sub_translations)

        current_text = ('').join(current_textlist)
        if sub_xhtml is None:
            xhtml.text = current_text
        else:
            sub_xhtml.tail = current_text
        for translation in self.translations:
            if translation[1] is None:
                translations.append((xhtml, translation[0], translation[2]))
            else:
                translation[1](xhtml, translation[2])

        return (
         xhtml, translations)

    def is_empty(self):
        return not bool(self.content)

    def is_not_empty(self):
        return bool(self.content)

    def append(self, *appendee):
        self.content.extend(appendee)

    def prepend(self, *prependee):
        self.content = list(prependee) + self.content

    def set(self, key, val):
        self.attributes[key] = val

    def get(self, key):
        return self.attributes[key]


def SubElement(parent, *args, **kwargs):
    return XMLElement(append_to=parent, *args, **kwargs)