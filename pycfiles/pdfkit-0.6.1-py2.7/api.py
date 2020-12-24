# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/pdfkit/api.py
# Compiled at: 2016-12-19 08:41:12
from .pdfkit import PDFKit
from .pdfkit import Configuration

def from_url(url, output_path, options=None, toc=None, cover=None, configuration=None, cover_first=False):
    """
    Convert file of files from URLs to PDF document

    :param url: URL or list of URLs to be saved
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf global and page options, with or w/o '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()
    :param configuration_first: (optional) if True, cover always precedes TOC

    Returns: True on success
    """
    r = PDFKit(url, 'url', options=options, toc=toc, cover=cover, configuration=configuration, cover_first=cover_first)
    return r.to_pdf(output_path)


def from_file(input, output_path, options=None, toc=None, cover=None, css=None, configuration=None, cover_first=False):
    """
    Convert HTML file or files to PDF document

    :param input: path to HTML file or list with paths or file-like object
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf options, with or w/o '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param css: (optional) string with path to css file which will be added to a single input file
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()
    :param configuration_first: (optional) if True, cover always precedes TOC

    Returns: True on success
    """
    r = PDFKit(input, 'file', options=options, toc=toc, cover=cover, css=css, configuration=configuration, cover_first=cover_first)
    return r.to_pdf(output_path)


def from_string(input, output_path, options=None, toc=None, cover=None, css=None, configuration=None, cover_first=False):
    """
    Convert given string or strings to PDF document

    :param input: string with a desired text. Could be a raw text or a html file
    :param output_path: path to output PDF file. False means file will be returned as string.
    :param options: (optional) dict with wkhtmltopdf options, with or w/o '--'
    :param toc: (optional) dict with toc-specific wkhtmltopdf options, with or w/o '--'
    :param cover: (optional) string with url/filename with a cover html page
    :param css: (optional) string with path to css file which will be added to a input string
    :param configuration: (optional) instance of pdfkit.configuration.Configuration()
    :param configuration_first: (optional) if True, cover always precedes TOC

    Returns: True on success
    """
    r = PDFKit(input, 'string', options=options, toc=toc, cover=cover, css=css, configuration=configuration, cover_first=cover_first)
    return r.to_pdf(output_path)


def configuration(**kwargs):
    """
    Constructs and returns a :class:`Configuration` with given options

    :param wkhtmltopdf: path to binary
    :param meta_tag_prefix: the prefix for ``pdfkit`` specific meta tags
    """
    return Configuration(**kwargs)