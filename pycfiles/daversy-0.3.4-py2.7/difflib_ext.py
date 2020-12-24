# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\daversy\difflib_ext.py
# Compiled at: 2016-01-14 15:12:15
import re, difflib

def merge_group(list, func, start=True, end=True):
    l, r, s = list[0]
    first = ['', ' class="first"'][start]
    last = ['', ' class="last"'][end]
    if len(list) == 1:
        if start and end:
            return LINE_FORMAT % func(' class="first last"', l, r)
        else:
            return LINE_FORMAT % func(first + last, l, r)

    html = LINE_FORMAT % func(first, l, r)
    for i in range(1, len(list) - 1):
        l, r, s = list[i]
        html += LINE_FORMAT % func('', l, r)

    l, r, s = list[(-1)]
    html += LINE_FORMAT % func(last, l, r)
    return html


def make_table(table_id, header, fromlines, tolines, context=None, versions=['old', 'new']):
    diff = list(difflib._mdiff(fromlines, tolines, context))
    if not diff:
        return None
    else:
        same = lambda c, l, r: (
         c, l[0], r[0], 'l', format_line(l[1]))
        add = lambda c, l, r: (c, '', r[0], 'r', format_line(r[1]))
        sub = lambda c, l, r: (c, l[0], '', 'l', format_line(l[1]))
        html = TABLE_HEADER % tuple([table_id, header] + versions)
        for type, start, end in group_types(diff):
            if type == 'same':
                html += '<tbody>%s</tbody>\n' % merge_group(diff[start:end], same)
            elif type == 'add':
                html += '<tbody class="add">%s</tbody>\n' % merge_group(diff[start:end], add)
            elif type == 'del':
                html += '<tbody class="rem">%s</tbody>\n' % merge_group(diff[start:end], sub)
            elif type == 'mod':
                html += '<tbody class="mod">%s%s</tbody>\n' % (
                 merge_group(diff[start:end], sub, end=False),
                 merge_group(diff[start:end], add, start=False))
            elif type == 'skipped':
                html += '<tbody class="skipped"><tr><th>...</th><th>...</th><td>&nbsp;</td></tr></tbody>\n'

        html += TABLE_FOOTER
        return html


def get_type(left, right, status):
    if not status:
        if left or right:
            return 'same'
        return 'skipped'
    l_num, l_line = left
    r_num, r_line = right
    if l_num and not r_num:
        return 'del'
    else:
        if r_num and not l_num:
            return 'add'
        return 'mod'


def group_types(diff):
    items = [ get_type(l, r, s) for l, r, s in diff ]
    group = []
    if not items:
        print diff
    start, current = 0, items[0]
    for i in range(1, len(diff)):
        if items[i] != current:
            group.append((current, start, i))
            current = items[i]
            start = i

    group.append((current, start, len(diff)))
    return group


REPLACE_CHARS = [
 ('&', '&amp;'),
 ('<', '&lt;'),
 ('>', '&gt;'),
 (' ', '&nbsp;'),
 ('"', '&quot;'),
 ('\x00+', '<span class="ins">'),
 ('\x00-', '<span class="del">'),
 ('\x00^', '<span class="chg">'),
 ('\x01', '</span>')]
SINGLE_CHANGE = re.compile('^\x00[\\+\\-\\^]([^\x00]+)\x01\n?$')

def format_line(text):
    text = text.replace('\n', '')
    match = SINGLE_CHANGE.match(text)
    if match:
        text = match.group(1)
    for src, replace in REPLACE_CHARS:
        text = text.replace(src, replace)

    return text


TABLE_HEADER = '\n <li class=\'entry\' id=\'%s\'>\n   <h2>%s</h2>\n   <table class="inline" summary="Differences" cellspacing="0">\n     <colgroup><col class="lineno" /><col class="lineno" /><col class="content" /></colgroup>\n     <thead><th>%s</th><th>%s</th><th>&nbsp;</th></thead>\n'
TABLE_FOOTER = '\n   </table>\n </li>\n'
LINE_FORMAT = "<tr%s><th>%s</th><th>%s</th><td class='%s'><span>%s</span>&nbsp;</td></tr>"
HTML_HEADER = "\n<html><head><style type='text/css'>\n/* Diff preferences */\n#prefs fieldset { margin: 1em .5em .5em; padding: .5em 1em 0 }\n\n/* Diff/change overview */\n#overview {\n line-height: 130%;\n margin-top: 1em;\n padding: .5em;\n}\n#overview dt {\n font-weight: bold;\n padding-right: .25em;\n position: absolute;\n left: 0;\n text-align: right;\n width: 7.75em;\n}\n#overview dd { margin-left: 8em }\n\n/* Colors for change types */\n#chglist .edit, #overview .mod, .diff #legend .mod { background: #fd8 }\n#chglist .delete, #overview .rem, .diff #legend .rem { background: #f88 }\n#chglist .add, #overview .add, .diff #legend .add { background: #bfb }\n#chglist .copy, #overview .cp, .diff #legend .cp { background: #88f }\n#chglist .move, #overview .mv, .diff #legend .mv { background: #ccc }\n#chglist .unknown { background: #fff }\n\n/* Legend for diff colors */\n.diff #legend {\n float: left;\n font-size: 9px;\n line-height: 1em;\n margin: 1em 0;\n padding: .5em;\n}\n.diff #legend h3 { display: none; }\n.diff #legend dt {\n background: #fff;\n border: 1px solid #999;\n float: left;\n margin: .1em .5em .1em 2em;\n overflow: hidden;\n width: .8em; height: .8em;\n}\n.diff #legend dl, .diff #legend dd {\n display: inline;\n float: left;\n padding: 0;\n margin: 0;\n margin-right: .5em;\n}\n\n/* Styles for the list of diffs */\n.diff ul.entries { clear: both; margin: 0; padding: 0 }\n.diff li.entry {\n background: #f7f7f7;\n border: 1px solid #d7d7d7;\n list-style-type: none;\n margin: 0 0 2em;\n padding: 2px;\n position: relative;\n}\n.diff h2 {\n color: #333;\n font-size: 14px;\n letter-spacing: normal;\n margin: 0 auto;\n padding: .1em 0 .25em .5em;\n}\n\n/* Styles for the actual diff tables (side-by-side and inline) */\n.diff table {\n border: 1px solid #ddd;\n border-spacing: 0;\n border-top: 0;\n empty-cells: show;\n font-size: 12px;\n line-height: 130%;\n padding: 0;\n margin: 0 auto;\n width: 100%;\n}\n.diff table col.lineno { width: 4em }\n.diff table th {\n border-right: 1px solid #d7d7d7;\n border-bottom: 1px solid #998;\n font-size: 11px;\n}\n.diff table thead th {\n background: #eee;\n border-top: 1px solid #d7d7d7;\n color: #999;\n padding: 0 .25em;\n text-align: center;\n white-space: nowrap;\n}\n.diff table tbody th {\n background: #eed;\n color: #886;\n font-weight: normal;\n padding: 0 .5em;\n text-align: right;\n vertical-align: top;\n}\n.diff table tbody td {\n background: #fff;\n font: normal 11px monospace;\n overflow: hidden;\n padding: 1px 2px;\n vertical-align: top;\n}\n.diff table tbody.skipped td {\n background: #f7f7f7;\n border: 1px solid #d7d7d7;\n}\n.diff table td span.del, .diff table td span.ins { text-decoration: none }\n.diff table td span.del { color: #600 }\n.diff table td span.ins { color: #060 }\n\n/* Styles for the inline diff */\n.diff table.inline tbody.mod td.l, .diff table.inline tbody.rem td.l {\n background: #fdd;\n border-color: #c00;\n border-style: solid;\n border-width: 0 1px 0 1px;\n}\n.diff table.inline tbody.mod td.r, .diff table.inline tbody.add td.r {\n background: #dfd;\n border-color: #0a0;\n border-style: solid;\n border-width: 0 1px 0 1px;\n}\n.diff table.inline tbody.mod tr.first td.l,\n.diff table.inline tbody.rem tr.first td.l { border-top-width: 1px }\n.diff table.inline tbody.mod tr.last td.l,\n.diff table.inline tbody.rem tr.last td.l { border-bottom-width: 1px }\n.diff table.inline tbody.mod tr.first td.r,\n.diff table.inline tbody.add tr.first td.r { border-top-width: 1px }\n.diff table.inline tbody.mod tr.last td.r,\n.diff table.inline tbody.add tr.last td.r { border-bottom-width: 1px }\n.diff table.inline tbody.mod td span.del { background: #e99; color: #000 }\n.diff table.inline tbody.mod td span.ins { background: #9e9; color: #000 }\n.diff table.inline tbody.mod td span.chg { background: #ee9; color: #000 }\n\n/* Styles for the side-by-side diff */\n.diff table.sidebyside colgroup.content { width: 50% }\n.diff table.sidebyside tbody.mod td.l { background: #fe9 }\n.diff table.sidebyside tbody.mod td.r { background: #fd8 }\n.diff table.sidebyside tbody.add td.l { background: #dfd }\n.diff table.sidebyside tbody.add td.r { background: #cfc }\n.diff table.sidebyside tbody.rem td.l { background: #f88 }\n.diff table.sidebyside tbody.rem td.r { background: #faa }\n.diff table.sidebyside tbody.mod span.del, .diff table.sidebyside tbody.mod span.ins, .diff table.sidebyside tbody.mod span.chg {\n background: #fc0;\n}\n/* Changeset overview */\n#overview .files { padding-top: 2em }\n#overview .files ul { margin: 0; padding: 0 }\n#overview .files li { list-style-type: none }\n#overview .files li .comment { display: none }\n#overview .files li div {\n border: 1px solid #999;\n float: left;\n margin: .2em .5em 0 0;\n overflow: hidden;\n width: .8em; height: .8em;\n}\n#overview div.add div, #overview div.cp div, #overview div.mv div {\n border: 0;\n margin: 0;\n float: right;\n width: .35em;\n}\n\nspan.ver {font: normal 11px monospace;}\n</style></head><body>\n"
HTML_FOOTER = '\n </body>\n</html>\n'