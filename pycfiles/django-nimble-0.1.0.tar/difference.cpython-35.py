# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: F:\Django\development\nimble\views\difference.py
# Compiled at: 2017-01-30 09:39:05
# Size of source mod 2**32: 4119 bytes
from django.http import HttpResponse
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from difflib import Differ
from collections import namedtuple
difference = namedtuple('Difference', ['line', 'tag'])
inline = namedtuple('Inline', ['line1', 'line2', 'tags1', 'tags2'])

class MyDiff(Differ):

    def _dump(self, tag, x, lo, hi):
        """Generate comparison results for a same-tagged range."""
        for i in range(lo, hi):
            yield difference(line=x[i], tag=tag)

    def _qformat(self, aline, bline, atags, btags):
        yield inline(line1=aline, line2=bline, tags1=[i for i, b in enumerate(atags) if b.strip()], tags2=[i for i, b in enumerate(btags) if b.strip()])


def strong_tag(text, highlights):
    html = format_html('')
    active = False
    for index, char in enumerate(text):
        if index in highlights and not active:
            html = format_html('{}{}', html, mark_safe('<strong>'))
            active = True
        if index not in highlights and active:
            html = format_html('{}{}', html, mark_safe('</strong>'))
            active = False
        html = format_html('{}{}', html, char)

    return html


def format_row(tag, row_class, text):
    return format_html('<tr class="{}" style="font-family:monospace;"><td>{}</td><td>{}</td></tr>', row_class, tag, text)


def bootstrap_diffs(first_lines, second_lines):
    table = format_html('<table class="table">')
    a = MyDiff()
    plus_tag = mark_safe('<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>')
    minus_tag = mark_safe('<span class="glyphicon glyphicon-minus" aria-hidden="true"></span>')
    for index, diff in enumerate(a.compare(first_lines, second_lines), start=1):
        if isinstance(diff, difference):
            if diff.tag == '+':
                row_class = 'success'
                tag = plus_tag
            else:
                if diff.tag == '-':
                    row_class = 'danger'
                    tag = minus_tag
                else:
                    row_class = 'blank'
                    tag = ''
            table = format_html('{}{}', table, format_row(tag, row_class, diff.line))
        else:
            line1 = strong_tag(diff.line1, diff.tags1)
            line2 = strong_tag(diff.line2, diff.tags2)
            row_class = 'warning'
            table = format_html('{}{}{}', table, format_row(minus_tag, row_class, line1), format_row(plus_tag, row_class, line2))

    return format_html('{}</table>', table)


def difference_view(*args, **kwargs):
    first_lines = [
     'start\n',
     'block\n',
     'one\n',
     'bye\n',
     'two\n',
     'some count of three\n',
     'end\n',
     'block\n']
    second_lines = [
     'start\n',
     'block\n',
     'one\n',
     'two\n',
     'some count of thwawe\n',
     'four\n',
     'end\n',
     'block\n']
    html = '<html><head><script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.1/jquery.min.js"></script>\n<link href="https://gitcdn.github.io/bootstrap-toggle/2.2.2/css/bootstrap-toggle.min.css" rel="stylesheet">\n<script src="https://gitcdn.github.io/bootstrap-toggle/2.2.2/js/bootstrap-toggle.min.js"></script>\n<link href="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet">\n<link rel="stylesheet" href="http://bootswatch.com/yeti/bootstrap.min.css" type="text/css">\n<script src="//maxcdn.bootstrapcdn.com/bootstrap/3.3.7/js/bootstrap.min.js"></script>\n</head><body>{}</body></html>'
    table = bootstrap_diffs(first_lines, second_lines)
    return HttpResponse(format_html(html, table))