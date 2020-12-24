# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ana/dev/dexy-filter-examples/dexy_filter_examples/__init__.py
# Compiled at: 2014-01-09 15:13:05
from dexy.template import Template

class Idio(Template):
    """
    Idio.
    """
    aliases = [
     'idio']


class Asciidoc(Template):
    """
    Asciidoc.
    """
    aliases = [
     'asciidoc']
    _settings = {'copy-output-dir': True}


class Asciidoctor(Template):
    """
    Asciidoctor.
    """
    aliases = [
     'asciidoctor']
    _settings = {'copy-output-dir': True}


class Slides(Template):
    """
    slides
    """
    aliases = [
     'slides']
    _settings = {'copy-output-dir': True}


class Ipynb(Template):
    """
    ipynb
    """
    aliases = [
     'ipynb']


class IpynbCasper(Template):
    """
    ipynb casper
    """
    aliases = [
     'ipynbcasper']


class Bash(Template):
    """
    Bash-related filter examples.
    """
    aliases = [
     'bash']


class Tidy(Template):
    """
    Runs various tidy templates.
    """
    aliases = [
     'tidy']


class Go(Template):
    """
    Runs the go filter.
    """
    aliases = [
     'go']


class Ditaa(Template):
    """
    Runs the ditaa filter.
    """
    aliases = [
     'ditaa']


class Julia(Template):
    """
    Run the julia filter.
    """
    aliases = [
     'julia']
    filters_used = ['julia']


class Matlab(Template):
    """
    Run the matlab filter.
    """
    aliases = [
     'matlab']
    filters_used = ['matlabint']


class Cowsay(Template):
    """
    Run the cowsay filter with various options.
    """
    aliases = [
     'cowsay']
    filters_used = ['cowsay', 'jinja']


class Pygments(Template):
    """
    Applies the pygments filter.
    """
    aliases = [
     'pygments']
    filters_used = ['pyg', 'shint', 'idio', 'l']


class PygmentsStylesheets(Template):
    """
    How to generate stylesheets for use with pygments.
    """
    aliases = [
     'pygments-stylesheets']
    filters_used = ['pyg', 'shint', 'idio']


class PygmentsImage(Template):
    """
    How to use the image output formats from pygments.
    """
    aliases = [
     'pygments-image']
    filters_used = ['pyg', 'gn', 'jn', 'pn']

    @classmethod
    def is_active(klass):
        try:
            import PIL
            return True
        except ImportError:
            return False


class Markdown(Template):
    """
    Convert markdown to HTML.
    """
    aliases = [
     'markdown']
    filters_used = ['markdown', 'jinja', 'pyg']


class Figlet(Template):
    """
    Makes a figlet out of text.
    """
    aliases = [
     'figlet']
    filters_used = ['figlet']


class Abc(Template):
    """
    Shows how to generate a .pdf from .abc music notation file.
    """
    aliases = [
     'abc']
    filters_used = ['abc', 'h']


class Regetron(Template):
    """
    Shows how to use regetron.
    """
    aliases = [
     'regetron']
    filters_used = ['regetron']


class ReStructuredText(Template):
    """
    Shows how to convert ReST using various filters.
    """
    aliases = [
     'rst']
    filters_used = ['rstdocparts', 'rst', 'rstbody', 'latex']


class HtmlSections(Template):
    """
    Split a HTML document up into sections based on comments.
    """
    aliases = [
     'htmlsections']
    filters_used = ['htmlsections', 'jinja']


class PhRender(Template):
    """
    Use phantom js to render HTML to an image
    """
    aliases = [
     'phrender']
    filters_used = ['phrender']