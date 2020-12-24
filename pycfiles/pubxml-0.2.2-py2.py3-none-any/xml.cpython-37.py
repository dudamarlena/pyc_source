# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sah/bg/pubxml/src/pubxml/xml.py
# Compiled at: 2019-11-16 22:37:18
# Size of source mod 2**32: 3776 bytes
from dataclasses import dataclass, field
from pathlib import Path
from lxml import etree

@dataclass
class XML:
    filename = None
    filename: str
    root = None
    root: str
    tree = None
    tree: str
    nsmap = field(default_factory=dict)
    nsmap: dict

    def __post_init__(self):
        if self.filename:
            if not self.tree:
                if not self.root:
                    self.tree = etree.parse(self.filename)
                    self.root = self.tree.getroot()
        if self.root:
            self.tree = self.root.getroottree()
        else:
            if self.tree:
                self.root = self.tree.getroot()
            elif not self.nsmap:
                if self.root is not None:
                    self.nsmap = {ns if ns is not None else '_':uri for ns, uri in self.root.nsmap.items()}

    def __repr__(self):
        return f'{self.__class__.__name__}(filename="{self.filename}", root="{self.root}")'

    def write(self, filename=None, method='c14n', **kwargs):
        """
        Write the XML document to a file (using the XML.tree.write() method).

        * filename=None: An optional filename to write to (default=self.filename).
        * method='c14n': Canonicalize output by default.
        """
        (self.tree.write)((filename or self.filename), **kwargs)

    @property
    def path(self):
        """
        return a pathlib.Path object containing the document filename, or None
        """
        if self.filename is not None:
            return Path(self.filename)

    def xpath(self, expr, element=None, nsmap=None, extensions=None, strings='plain', **params):
        """
        Return xpath results for the given context or document root.

        * expr: the xpath expression
        * element: the element context in which to evaluate the xpath expression
        * nsmap: the namespace map to use with the expression (default = Document nsmap)
        * extensions: additional xpath extension functions to make available
        * strings: default='plain' to return plain strings, 'smart' to use smart strings
          (smart strings have a `.getparent()` method). Smart strings are off by default
          for efficiency.
        * **params: additional parameters that are made available to xpath.
        """
        if not element:
            element = self.root
        xpath_args = {**{'namespaces':nsmap or self.nsmap,  'extensions':extensions, 
         'smart_strings':strings == 'smart'}, **params}
        return (element.xpath)(expr, **xpath_args)

    def first(self, path, context=None, nsmap=None, exts=None, strings='plain', **params):
        """
        Return first xpath result for the given context or document root, or None.
        """
        results = (self.xpath)(
 path, context=context, nsmap=nsmap, exts=exts, strings='plain', **params)
        return next(iter(results), None)

    def prefixed_tag(self, element, nsmap=None):
        nsmap = nsmap or self.nsmap
        tag = element.tag.split('}')[(-1)]
        if element.prefix:
            return f"{element.prefix}:{tag}"
        if '}' in element.tag:
            ns = element.tag.split('}')[0].strip('{}')
            if nsmap:
                if ns in nsmap.values():
                    keys, values = list(nsmap.keys()), list(nsmap.values())
                    prefix = keys[values.index(ns)]
                    return f"{prefix}:{tag}"
        return tag