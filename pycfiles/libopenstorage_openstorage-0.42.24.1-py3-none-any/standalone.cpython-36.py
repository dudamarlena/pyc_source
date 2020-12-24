# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/docutils/docutils/readers/standalone.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 2340 bytes
"""
Standalone file Reader for the reStructuredText markup syntax.
"""
__docformat__ = 'reStructuredText'
import sys
from docutils import frontend, readers
from docutils.transforms import frontmatter, references, misc

class Reader(readers.Reader):
    supported = ('standalone', )
    document = None
    settings_spec = (
     'Standalone Reader',
     None,
     (
      (
       'Disable the promotion of a lone top-level section title to document title (and subsequent section title to document subtitle promotion; enabled by default).',
       [
        '--no-doc-title'],
       {'dest':'doctitle_xform', 
        'action':'store_false',  'default':1,  'validator':frontend.validate_boolean}),
      (
       'Disable the bibliographic field list transform (enabled by default).',
       [
        '--no-doc-info'],
       {'dest':'docinfo_xform', 
        'action':'store_false',  'default':1,  'validator':frontend.validate_boolean}),
      (
       'Activate the promotion of lone subsection titles to section subtitles (disabled by default).',
       [
        '--section-subtitles'],
       {'dest':'sectsubtitle_xform', 
        'action':'store_true',  'default':0,  'validator':frontend.validate_boolean}),
      (
       'Deactivate the promotion of lone subsection titles.',
       [
        '--no-section-subtitles'],
       {'dest':'sectsubtitle_xform', 
        'action':'store_false'})))
    config_section = 'standalone reader'
    config_section_dependencies = ('readers', )

    def get_transforms(self):
        return readers.Reader.get_transforms(self) + [
         references.Substitutions,
         references.PropagateTargets,
         frontmatter.DocTitle,
         frontmatter.SectionSubTitle,
         frontmatter.DocInfo,
         references.AnonymousHyperlinks,
         references.IndirectHyperlinks,
         references.Footnotes,
         references.ExternalTargets,
         references.InternalTargets,
         references.DanglingReferences,
         misc.Transitions]