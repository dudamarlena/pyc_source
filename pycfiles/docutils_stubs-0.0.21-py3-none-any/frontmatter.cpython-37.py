# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/transforms/frontmatter.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 19552 bytes
"""
Transforms related to the front matter of a document or a section
(information found before the main text):

- `DocTitle`: Used to transform a lone top level section's title to
  the document title, promote a remaining lone top-level section's
  title to the document subtitle, and determine the document's title
  metadata (document['title']) based on the document title and/or the
  "title" setting.

- `SectionSubTitle`: Used to transform a lone subsection into a
  subtitle.

- `DocInfo`: Used to transform a bibliographic field list into docinfo
  elements.
"""
__docformat__ = 'reStructuredText'
import re
from docutils import nodes, utils
from docutils.transforms import TransformError, Transform

class TitlePromoter(Transform):
    __doc__ = '\n    Abstract base class for DocTitle and SectionSubTitle transforms.\n    '

    def promote_title(self, node):
        """
        Transform the following tree::

            <node>
                <section>
                    <title>
                    ...

        into ::

            <node>
                <title>
                ...

        `node` is normally a document.
        """
        if not isinstance(node, nodes.Element):
            raise TypeError('node must be of Element-derived type.')
        if len(node):
            assert not isinstance(node[0], nodes.title)
        section, index = self.candidate_index(node)
        if index is None:
            return
        node.update_all_atts_concatenating(section, True, True)
        node[:] = section[:1] + node[:index] + section[1:]
        assert isinstance(node[0], nodes.title)
        return 1

    def promote_subtitle(self, node):
        """
        Transform the following node tree::

            <node>
                <title>
                <section>
                    <title>
                    ...

        into ::

            <node>
                <title>
                <subtitle>
                ...
        """
        if not isinstance(node, nodes.Element):
            raise TypeError('node must be of Element-derived type.')
        subsection, index = self.candidate_index(node)
        if index is None:
            return
        subtitle = nodes.subtitle()
        subtitle.update_all_atts_concatenating(subsection, True, True)
        subtitle[:] = subsection[0][:]
        node[:] = node[:1] + [subtitle] + node[1:index] + subsection[1:]
        return 1

    def candidate_index--- This code section failed: ---

 L. 129         0  LOAD_FAST                'node'
                2  LOAD_METHOD              first_child_not_matching_class

 L. 130         4  LOAD_GLOBAL              nodes
                6  LOAD_ATTR                PreBibliographic
                8  CALL_METHOD_1         1  '1 positional argument'
               10  STORE_FAST               'index'

 L. 131        12  LOAD_FAST                'index'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     52  'to 52'
               20  LOAD_GLOBAL              len
               22  LOAD_FAST                'node'
               24  CALL_FUNCTION_1       1  '1 positional argument'
               26  LOAD_FAST                'index'
               28  LOAD_CONST               1
               30  BINARY_ADD       
               32  COMPARE_OP               >
               34  POP_JUMP_IF_TRUE     52  'to 52'

 L. 132        36  LOAD_GLOBAL              isinstance
               38  LOAD_FAST                'node'
               40  LOAD_FAST                'index'
               42  BINARY_SUBSCR    
               44  LOAD_GLOBAL              nodes
               46  LOAD_ATTR                section
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  POP_JUMP_IF_TRUE     56  'to 56'
             52_0  COME_FROM            34  '34'
             52_1  COME_FROM            18  '18'

 L. 133        52  LOAD_CONST               (None, None)
               54  RETURN_VALUE     
             56_0  COME_FROM            50  '50'

 L. 135        56  LOAD_FAST                'node'
               58  LOAD_FAST                'index'
               60  BINARY_SUBSCR    
               62  LOAD_FAST                'index'
               64  BUILD_TUPLE_2         2 
               66  RETURN_VALUE     

Parse error at or near `BUILD_TUPLE_2' instruction at offset 64


class DocTitle(TitlePromoter):
    __doc__ = '\n    In reStructuredText_, there is no way to specify a document title\n    and subtitle explicitly. Instead, we can supply the document title\n    (and possibly the subtitle as well) implicitly, and use this\n    two-step transform to "raise" or "promote" the title(s) (and their\n    corresponding section contents) to the document level.\n\n    1. If the document contains a single top-level section as its\n       first non-comment element, the top-level section\'s title\n       becomes the document\'s title, and the top-level section\'s\n       contents become the document\'s immediate contents. The lone\n       top-level section header must be the first non-comment element\n       in the document.\n\n       For example, take this input text::\n\n           =================\n            Top-Level Title\n           =================\n\n           A paragraph.\n\n       Once parsed, it looks like this::\n\n           <document>\n               <section names="top-level title">\n                   <title>\n                       Top-Level Title\n                   <paragraph>\n                       A paragraph.\n\n       After running the DocTitle transform, we have::\n\n           <document names="top-level title">\n               <title>\n                   Top-Level Title\n               <paragraph>\n                   A paragraph.\n\n    2. If step 1 successfully determines the document title, we\n       continue by checking for a subtitle.\n\n       If the lone top-level section itself contains a single\n       second-level section as its first non-comment element, that\n       section\'s title is promoted to the document\'s subtitle, and\n       that section\'s contents become the document\'s immediate\n       contents. Given this input text::\n\n           =================\n            Top-Level Title\n           =================\n\n           Second-Level Title\n           ~~~~~~~~~~~~~~~~~~\n\n           A paragraph.\n\n       After parsing and running the Section Promotion transform, the\n       result is::\n\n           <document names="top-level title">\n               <title>\n                   Top-Level Title\n               <subtitle names="second-level title">\n                   Second-Level Title\n               <paragraph>\n                   A paragraph.\n\n       (Note that the implicit hyperlink target generated by the\n       "Second-Level Title" is preserved on the "subtitle" element\n       itself.)\n\n    Any comment elements occurring before the document title or\n    subtitle are accumulated and inserted as the first body elements\n    after the title(s).\n\n    This transform also sets the document\'s metadata title\n    (document[\'title\']).\n\n    .. _reStructuredText: http://docutils.sf.net/rst.html\n    '
    default_priority = 320

    def set_metadata(self):
        """
        Set document['title'] metadata title from the following
        sources, listed in order of priority:

        * Existing document['title'] attribute.
        * "title" setting.
        * Document title node (as promoted by promote_title).
        """
        if not self.document.hasattr('title'):
            if self.document.settings.title is not None:
                self.document['title'] = self.document.settings.title
            else:
                if len(self.document):
                    if isinstance(self.document[0], nodes.title):
                        self.document['title'] = self.document[0].astext()

    def apply(self):
        if getattr(self.document.settings, 'doctitle_xform', 1):
            if self.promote_title(self.document):
                self.promote_subtitle(self.document)
        self.set_metadata()


class SectionSubTitle(TitlePromoter):
    __doc__ = '\n    This works like document subtitles, but for sections.  For example, ::\n\n        <section>\n            <title>\n                Title\n            <section>\n                <title>\n                    Subtitle\n                ...\n\n    is transformed into ::\n\n        <section>\n            <title>\n                Title\n            <subtitle>\n                Subtitle\n            ...\n\n    For details refer to the docstring of DocTitle.\n    '
    default_priority = 350

    def apply(self):
        if not getattr(self.document.settings, 'sectsubtitle_xform', 1):
            return
        for section in self.document.traverse(nodes.section):
            self.promote_subtitle(section)


class DocInfo(Transform):
    __doc__ = '\n    This transform is specific to the reStructuredText_ markup syntax;\n    see "Bibliographic Fields" in the `reStructuredText Markup\n    Specification`_ for a high-level description. This transform\n    should be run *after* the `DocTitle` transform.\n\n    Given a field list as the first non-comment element after the\n    document title and subtitle (if present), registered bibliographic\n    field names are transformed to the corresponding DTD elements,\n    becoming child elements of the "docinfo" element (except for a\n    dedication and/or an abstract, which become "topic" elements after\n    "docinfo").\n\n    For example, given this document fragment after parsing::\n\n        <document>\n            <title>\n                Document Title\n            <field_list>\n                <field>\n                    <field_name>\n                        Author\n                    <field_body>\n                        <paragraph>\n                            A. Name\n                <field>\n                    <field_name>\n                        Status\n                    <field_body>\n                        <paragraph>\n                            $RCSfile$\n            ...\n\n    After running the bibliographic field list transform, the\n    resulting document tree would look like this::\n\n        <document>\n            <title>\n                Document Title\n            <docinfo>\n                <author>\n                    A. Name\n                <status>\n                    frontmatter.py\n            ...\n\n    The "Status" field contained an expanded RCS keyword, which is\n    normally (but optionally) cleaned up by the transform. The sole\n    contents of the field body must be a paragraph containing an\n    expanded RCS keyword of the form "$keyword: expansion text $". Any\n    RCS keyword can be processed in any bibliographic field. The\n    dollar signs and leading RCS keyword name are removed. Extra\n    processing is done for the following RCS keywords:\n\n    - "RCSfile" expands to the name of the file in the RCS or CVS\n      repository, which is the name of the source file with a ",v"\n      suffix appended. The transform will remove the ",v" suffix.\n\n    - "Date" expands to the format "YYYY/MM/DD hh:mm:ss" (in the UTC\n      time zone). The RCS Keywords transform will extract just the\n      date itself and transform it to an ISO 8601 format date, as in\n      "2000-12-31".\n\n      (Since the source file for this text is itself stored under CVS,\n      we can\'t show an example of the "Date" RCS keyword because we\n      can\'t prevent any RCS keywords used in this explanation from\n      being expanded. Only the "RCSfile" keyword is stable; its\n      expansion text changes only if the file name changes.)\n\n    .. _reStructuredText: http://docutils.sf.net/rst.html\n    .. _reStructuredText Markup Specification:\n       http://docutils.sf.net/docs/ref/rst/restructuredtext.html\n    '
    default_priority = 340
    biblio_nodes = {'author':nodes.author, 
     'authors':nodes.authors, 
     'organization':nodes.organization, 
     'address':nodes.address, 
     'contact':nodes.contact, 
     'version':nodes.version, 
     'revision':nodes.revision, 
     'status':nodes.status, 
     'date':nodes.date, 
     'copyright':nodes.copyright, 
     'dedication':nodes.topic, 
     'abstract':nodes.topic}

    def apply(self):
        if not getattr(self.document.settings, 'docinfo_xform', 1):
            return
        document = self.document
        index = document.first_child_not_matching_class(nodes.PreBibliographic)
        if index is None:
            return
        candidate = document[index]
        if isinstance(candidate, nodes.field_list):
            biblioindex = document.first_child_not_matching_class((
             nodes.Titular, nodes.Decorative))
            nodelist = self.extract_bibliographic(candidate)
            del document[index]
            document[biblioindex:biblioindex] = nodelist

    def extract_bibliographic(self, field_list):
        docinfo = nodes.docinfo()
        bibliofields = self.language.bibliographic_fields
        labels = self.language.labels
        topics = {'dedication':None,  'abstract':None}
        for field in field_list:
            try:
                name = field[0][0].astext()
                normedname = nodes.fully_normalize_name(name)
                if len(field) == 2:
                    if not (normedname in bibliofields and self.check_empty_biblio_field(field, name)):
                        raise TransformError
                else:
                    canonical = bibliofields[normedname]
                    biblioclass = self.biblio_nodes[canonical]
                    if issubclass(biblioclass, nodes.TextElement):
                        if not self.check_compound_biblio_field(field, name):
                            raise TransformError
                        utils.clean_rcs_keywords(field[1][0], self.rcs_keyword_substitutions)
                        docinfo.append(biblioclass(*('', ''), *field[1][0]))
                    else:
                        if issubclass(biblioclass, nodes.authors):
                            self.extract_authors(field, name, docinfo)
                        else:
                            if issubclass(biblioclass, nodes.topic):
                                if topics[canonical]:
                                    field[(-1)] += self.document.reporter.warning(('There can only be one "%s" field.' % name),
                                      base_node=field)
                                    raise TransformError
                                title = nodes.title(name, labels[canonical])
                                topics[canonical] = biblioclass(
 '', title, *(field[1].children), **{'classes': [canonical]})
                            else:
                                docinfo.append(biblioclass(*('', ), *field[1].children))
            except TransformError:
                if len(field[(-1)]) == 1:
                    if isinstance(field[(-1)][0], nodes.paragraph):
                        utils.clean_rcs_keywords(field[(-1)][0], self.rcs_keyword_substitutions)
                if normedname not in bibliofields:
                    classvalue = nodes.make_id(normedname)
                    if classvalue:
                        field['classes'].append(classvalue)
                docinfo.append(field)

        nodelist = []
        if len(docinfo) != 0:
            nodelist.append(docinfo)
        for name in ('dedication', 'abstract'):
            if topics[name]:
                nodelist.append(topics[name])

        return nodelist

    def check_empty_biblio_field(self, field, name):
        if len(field[(-1)]) < 1:
            field[(-1)] += self.document.reporter.warning(('Cannot extract empty bibliographic field "%s".' % name),
              base_node=field)
            return
        return 1

    def check_compound_biblio_field(self, field, name):
        if len(field[(-1)]) > 1:
            field[(-1)] += self.document.reporter.warning(('Cannot extract compound bibliographic field "%s".' % name),
              base_node=field)
            return
        else:
            isinstance(field[(-1)][0], nodes.paragraph) or field[(-1)] += self.document.reporter.warning(('Cannot extract bibliographic field "%s" containing anything other than a single paragraph.' % name),
              base_node=field)
            return
        return 1

    rcs_keyword_substitutions = [
     (
      re.compile('\\$Date: (\\d\\d\\d\\d)[-/](\\d\\d)[-/](\\d\\d)[ T][\\d:]+[^$]* \\$', re.IGNORECASE), '\\1-\\2-\\3'),
     (
      re.compile('\\$RCSfile: (.+),v \\$', re.IGNORECASE), '\\1'),
     (
      re.compile('\\$[a-zA-Z]+: (.+) \\$'), '\\1')]

    def extract_authors(self, field, name, docinfo):
        try:
            if len(field[1]) == 1:
                if isinstance(field[1][0], nodes.paragraph):
                    authors = self.authors_from_one_paragraph(field)
                elif isinstance(field[1][0], nodes.bullet_list):
                    authors = self.authors_from_bullet_list(field)
                else:
                    raise TransformError
            else:
                authors = self.authors_from_paragraphs(field)
            authornodes = [(nodes.author)(*('', ''), *author) for author in authors if author]
            if len(authornodes) >= 1:
                docinfo.append((nodes.authors)(*('', ), *authornodes))
            else:
                raise TransformError
        except TransformError:
            field[(-1)] += self.document.reporter.warning(('Bibliographic field "%s" incompatible with extraction: it must contain either a single paragraph (with authors separated by one of "%s"), multiple paragraphs (one per author), or a bullet list with one paragraph (one author) per item.' % (
             name, ''.join(self.language.author_separators))),
              base_node=field)
            raise

    def authors_from_one_paragraph(self, field):
        text = field[1][0].astext().strip()
        if not text:
            raise TransformError
        for authorsep in self.language.author_separators:
            authornames = text.split(authorsep)
            if len(authornames) > 1:
                break

        authornames = [author.strip() for author in authornames]
        authors = [[nodes.Text(author)] for author in authornames if author]
        return authors

    def authors_from_bullet_list(self, field):
        authors = []
        for item in field[1][0]:
            if not len(item) != 1:
                if not isinstance(item[0], nodes.paragraph):
                    raise TransformError
                authors.append(item[0].children)

        if not authors:
            raise TransformError
        return authors

    def authors_from_paragraphs(self, field):
        for item in field[1]:
            if not isinstance(item, nodes.paragraph):
                raise TransformError

        authors = [item.children for item in field[1]]
        return authors