# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/readers/pep.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 1555 bytes
"""
Python Enhancement Proposal (PEP) Reader.
"""
__docformat__ = 'reStructuredText'
from docutils.readers import standalone
from docutils.transforms import peps, references, misc, frontmatter
from docutils.parsers import rst

class Reader(standalone.Reader):
    supported = ('pep', )
    settings_spec = (
     'PEP Reader Option Defaults',
     'The --pep-references and --rfc-references options (for the reStructuredText parser) are on by default.', ())
    config_section = 'pep reader'
    config_section_dependencies = ('readers', 'standalone reader')

    def get_transforms(self):
        transforms = standalone.Reader.get_transforms(self)
        transforms.remove(frontmatter.DocTitle)
        transforms.remove(frontmatter.SectionSubTitle)
        transforms.remove(frontmatter.DocInfo)
        transforms.extend([peps.Headers, peps.Contents, peps.TargetNotes])
        return transforms

    settings_default_overrides = {'pep_references':1, 
     'rfc_references':1}
    inliner_class = rst.states.Inliner

    def __init__(self, parser=None, parser_name=None):
        """`parser` should be ``None``."""
        if parser is None:
            parser = rst.Parser(rfc2822=True, inliner=(self.inliner_class()))
        standalone.Reader.__init__(self, parser, '')