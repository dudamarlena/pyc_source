# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/herbert/dev/python/sctdev/simpleproject/simpleproject/../../communitytools/sphenecoll/sphene/contrib/libs/markdown/mdx_toc.py
# Compiled at: 2012-03-17 12:42:14
"""
Chris Clark - clach04@sf.net

My markdown extensions for adding:
    HTML Title 
    Table of Contents (aka toc)
"""
import os, sys, re, markdown
DEFAULT_TITLE = None

def extract_alphanumeric(in_str=None):
    """take alpha-numeric (7bit ascii) and return as a string
    """
    out_str = []
    for x in in_str.title():
        if x.isalnum():
            out_str.append(x)

    return ('').join(out_str)


class TitleExtension:
    """ Markdown extension: extract first header from doc and use it as
        the xhtml document title
    """

    def extendMarkdown(self, md):
        md.postprocessors.append(TitlePostprocessor(self))

    def createTitle(self, doc):
        """
           Locates first H1 heading and uses that as the title.

           @returns: the title as a dom element
        """

        def findHeaderOneFn(element=None):
            if element.type == 'element':
                if element.nodeName == 'h1':
                    return True

        headerone_doc_list = doc.find(findHeaderOneFn)
        if headerone_doc_list != []:
            child = headerone_doc_list[0]
            doc_title = child.childNodes[0].value
        else:
            doc_title = DEFAULT_TITLE
        if doc_title is not None:
            title_doc_tag = doc.createElement('title')
            title_doc_text = doc.createTextNode(doc_title)
            title_doc_tag.appendChild(title_doc_text)
            return title_doc_tag
        else:
            return


class TitlePostprocessor:

    def __init__(self, extension):
        self.extension = extension

    def run(self, doc):
        titleElement = self.extension.createTitle(doc)
        if titleElement:
            doc.documentElement.insertChild(0, titleElement)


class TocExtension:
    """Markdown extension: generate a Table Of Contents (aka toc)
    toc is returned in a div tag with class='toc'
    toc is either:
        appended to end of document
      OR 
        replaces first string occurence of "///Table of Contents Goes Here///"
    """

    def __init__(self, configs):
        self.TOC_INCLUDE_MARKER = '///Table of Contents Goes Here///'
        self.TOC_TITLE = 'Table Of Contents'
        self.include_header_one_in_toc = True
        self.include_header_one_in_toc = False
        self.toc_heading_type = 2
        if 'include_header_one_in_toc' in configs:
            self.include_header_one_in_toc = configs['include_header_one_in_toc']

    def extendMarkdown(self, md, md_globals):
        md.postprocessors.append(TocPostprocessor(self, md))

    def findTocPlaceholder(self, doc):

        def findTocPlaceholderFn(node=None, indent=0):
            if node.type == 'text':
                if node.value.find(self.TOC_INCLUDE_MARKER) > -1:
                    return True

        toc_div_list = doc.find(findTocPlaceholderFn)
        if toc_div_list:
            return toc_div_list[0]
        else:
            return

    def createTocDiv(self, doc):
        """
           Creates Table Of Contents based on headers.

           @returns: toc as a single as a dom element 
                     in a <div> tag with class='toc'
        """
        headers_compiled_re = compile_obj = re.compile('h[123456]', re.IGNORECASE)

        def findHeadersFn(element=None):
            if element.type == 'element':
                if headers_compiled_re.match(element.nodeName):
                    return True

        headers_doc_list = doc.find(findHeadersFn)
        generated_anchor_id = 0
        headers_list = []
        min_header_size_found = 6
        for element in headers_doc_list:
            heading_title = element.childNodes[0].value
            if heading_title.strip() != '':
                heading_type = int(element.nodeName[-1:])
                if heading_type != 1:
                    min_header_size_found = min(min_header_size_found, heading_type)
                elif self.include_header_one_in_toc:
                    min_header_size_found = min(min_header_size_found, heading_type)
                html_anchor_name = extract_alphanumeric(heading_title) + '__MD_autoTOC_%d' % generated_anchor_id
                html_anchor = doc.createElement('a', ' ')
                html_anchor.setAttribute('name', html_anchor_name)
                element.appendChild(html_anchor)
                headers_list.append((heading_type, heading_title,
                 html_anchor_name))
                generated_anchor_id = generated_anchor_id + 1

        if headers_list != []:
            toc_doc_list = doc.createElement('ul')
            for (heading_type, heading_title, html_anchor_name) in headers_list:
                if self.include_header_one_in_toc or heading_type != 1:
                    toc_doc_entry = doc.createElement('li')
                    toc_doc_link = doc.createElement('a')
                    toc_doc_link.setAttribute('href', '#' + html_anchor_name)
                    toc_doc_text = doc.createTextNode(heading_title)
                    toc_doc_link.appendChild(toc_doc_text)
                    toc_doc_entry.appendChild(toc_doc_link)
                    lowest_toc_doc_indent = doc.createElement('ul')
                    previous_toc_doc_indent = None
                    toc_doc_indent = None
                    indent_amt = heading_type - min_header_size_found
                    indent_list = range(0, indent_amt)
                    for x in indent_list:
                        toc_doc_indent = doc.createElement('ul')
                        if previous_toc_doc_indent is None:
                            toc_doc_indent.appendChild(lowest_toc_doc_indent)
                        else:
                            toc_doc_indent.appendChild(previous_toc_doc_indent)
                        previous_toc_doc_indent = toc_doc_indent

                    if toc_doc_indent is None:
                        toc_doc_indent = lowest_toc_doc_indent
                    lowest_toc_doc_indent.appendChild(toc_doc_entry)
                    toc_doc_list.appendChild(toc_doc_indent)

            div = doc.createElement('div')
            div.setAttribute('class', 'toc')
            if self.TOC_TITLE:
                toc_header = doc.createElement('h%d' % self.toc_heading_type)
                toc_header_text = doc.createTextNode(self.TOC_TITLE)
                toc_header.appendChild(toc_header_text)
                div.appendChild(toc_header)
            div.appendChild(toc_doc_list)
            return div
        else:
            return


class TocPostprocessor:

    def __init__(self, toc, md):
        self.toc = toc
        self.md = md

    def run(self, doc):
        tocPlaceholder = self.toc.findTocPlaceholder(doc)
        tocDiv = self.toc.createTocDiv(doc)
        if tocDiv:
            if tocPlaceholder:
                tocPlaceholder.parent.replaceChild(tocPlaceholder, tocDiv)
            else:
                self.md.tocDiv = tocDiv


def markdownWithTitle(text):
    md = markdown.Markdown()
    markdown.FootnoteExtension().extendMarkdown(md)
    footnoteExtension.extendMarkdown(md)
    titleExtension = TitleExtension()
    titleExtension.extendMarkdown(md)
    md.source = text
    return str(md)


def markdownWithManyExtensions(text):
    """converts input text string into xhtml using markdown with all known extensions
    """
    md = markdown.Markdown()
    extension_list = [markdown.FootnoteExtension, TitleExtension, TocExtension]
    for md_extension in extension_list:
        tempExtension = md_extension()
        tempExtension.extendMarkdown(md)

    md.source = text
    return str(md)


def makeExtension(configs=None):
    return TocExtension(configs)


if __name__ == '__main__':
    in_filename = sys.argv[1]
    out_filename = os.path.splitext(in_filename)[0] + '.html'
    if os.path.exists(out_filename):
        print '\nWARNING', out_filename, 'already exists, overwritting.\n'
    out_file = file(out_filename, 'w')
    out_file.write(markdownWithManyExtensions(file(in_filename).read()))