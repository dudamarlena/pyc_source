# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/readers/doctree.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1607 bytes
"""Reader for existing document trees."""
from docutils import readers, utils, transforms

class Reader(readers.ReReader):
    __doc__ = '\n    Adapt the Reader API for an existing document tree.\n\n    The existing document tree must be passed as the ``source`` parameter to\n    the `docutils.core.Publisher` initializer, wrapped in a\n    `docutils.io.DocTreeInput` object::\n\n        pub = docutils.core.Publisher(\n            ..., source=docutils.io.DocTreeInput(document), ...)\n\n    The original document settings are overridden; if you want to use the\n    settings of the original document, pass ``settings=document.settings`` to\n    the Publisher call above.\n    '
    supported = ('doctree', )
    config_section = 'doctree reader'
    config_section_dependencies = ('readers', )

    def parse(self):
        """
        No parsing to do; refurbish the document tree instead.
        Overrides the inherited method.
        """
        self.document = self.input
        self.document.transformer = transforms.Transformer(self.document)
        self.document.settings = self.settings
        self.document.reporter = utils.new_reporter(self.document.get('source', ''), self.document.settings)