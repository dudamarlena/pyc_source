# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\fragmap\web_ui.py
# Compiled at: 2019-09-05 14:04:56
# Size of source mod 2**32: 13251 bytes
from yattag import Doc
from .generate_matrix import Cell, BriefFragmap, ConnectedFragmap, ConnectedCell, ConnectionStatus
from .http import start_server
from .common_ui import first_line
import os, re, io

def nop():
    pass


def render_cell_graphics(tag, connected_cell, inner):
    kind = connected_cell.base.kind
    changes = connected_cell.changes

    def etag(*args, **kwargs):
        with tag(*args, **kwargs):
            pass

    def hideempty(status):
        if status == ConnectionStatus.EMPTY:
            return 'invisible'
        else:
            return ''

    def passinfill(status):
        if status == ConnectionStatus.INFILL:
            return 'visibility:hidden'
        else:
            return ''

    def activitymarker(status):
        if status == ConnectionStatus.CONNECTION:
            return 'active'
        else:
            return ''

    if kind != Cell.NO_CHANGE:
        inner()
        with tag('div', klass=('cell ' + activitymarker(changes.center))):
            etag('div', klass=('top ' + hideempty(changes.up)))
            etag('div', klass=('left ' + hideempty(changes.left)), style=(passinfill(changes.left)))
            with tag('div', klass='inner', style=(passinfill(changes.center))):
                etag('div', klass='dot')
            etag('div', klass=('right ' + hideempty(changes.right)), style=(passinfill(changes.right)))
            etag('div', klass=('bottom ' + hideempty(changes.down)))


def make_fragmap_page(fragmap):
    is_brief = isinstance(fragmap, BriefFragmap)
    matrix = ConnectedFragmap(fragmap).generate_matrix()
    doc, tag, text = Doc().tagtext()

    def colorized_line(line_object):
        origin = line_object.origin
        line = origin + line_object.content
        if line == '':
            return
        if origin == '-':
            with tag('pre', klass='codeline codeline_removed'):
                text(line)
        if origin == '+':
            with tag('pre', klass='codeline codeline_added'):
                text(line)
        if origin == '':
            with tag('pre', klass='codeline'):
                text(line)

    def etag(*args, **kwargs):
        with tag(*args, **kwargs):
            pass

    def render_cell(cell, r, c):

        def inner():
            with tag('div', klass='code'):
                if cell.base.node:
                    text(str(cell.base.node))
                    for line in cell.base.node._fragment.lines:
                        colorized_line(line)

        render_cell_graphics(tag, cell, inner)

    def get_first_filename(matrix, c):
        for r in range(len(matrix)):
            cell = matrix[r][c]
            if cell.base.kind != Cell.NO_CHANGE:
                return cell.base.node._filename

    def generate_first_filename_spans(matrix):
        filenames = []
        if len(matrix) == 0:
            return filenames
        else:
            for c in range(len(matrix[0])):
                fn = get_first_filename(matrix, c)
                if len(filenames) == 0:
                    filenames.append({'filename':fn,  'span':1,  'start':c})
                elif filenames[(-1)]['filename'] == fn or fn is None:
                    filenames[(-1)]['span'] += 1
                else:
                    if fn is not None:
                        filenames.append({'filename':fn,  'span':1,  'start':c})

            return filenames

    def render_filename_start_row(filenames):
        for fn in filenames:
            with tag('th', klass='filename_start', colspan=(fn['span']), style='vertical-align: top; overflow: hidden'):
                with tag('div', style='position: relative; width: inherit'):
                    with tag('div', style='overflow: hidden; position: absolute; right: 10px; width: 10000px; text-align: right'):
                        if fn['filename'] is not None:
                            text(fn['filename'])

    def filename_header_td_class(filenames, c):
        for fn in filenames:
            if c == fn['start']:
                return 'filename_start '

        return ''

    def get_html():
        doc.asis('<!DOCTYPE html>')
        with tag('html'):
            with tag('head'):
                with tag('meta', charset='utf-8'):
                    pass
                with tag('title'):
                    text('Fragmap - ' + os.getcwd())
                with tag('style', type='text/css'):
                    doc.asis(css())
            with tag('body'):
                with tag('div', id='map_window'):
                    with tag('table'):
                        start_filenames = generate_first_filename_spans(matrix)
                        with tag('tr'):
                            with tag('th', style='font-weight: bold'):
                                text('Hash')
                            with tag('th', style='font-weight: bold'):
                                text('Message')
                            if len(matrix) > 0:
                                render_filename_start_row(start_filenames)
                        for r in range(len(matrix)):
                            cur_patch = fragmap.patches[r].header
                            commit_msg = first_line(cur_patch.message)
                            hash = cur_patch.hex
                            with tag('tr'):
                                with tag('th'):
                                    with tag('span', klass='commit_hash'):
                                        text(hash[0:8])
                                with tag('th', klass='message_cell'):
                                    with tag('span', klass='commit_message'):
                                        text(commit_msg)
                                for c in range(len(matrix[r])):
                                    with tag('td', klass=(filename_header_td_class(start_filenames, c)), onclick='javascript:show(this)'):
                                        render_cell(matrix[r][c], r, c)

                with tag('div', id='code_window'):
                    text('')
                with tag('script'):
                    doc.asis(javascript())
        return doc.getvalue()

    return get_html()


def start_fragmap_server(fragmap_callback):

    def html_callback():
        return make_fragmap_page(fragmap_callback())

    server = start_server(html_callback)
    address = 'http://%s:%s' % server.server_address
    os.startfile(address)
    print('Serving fragmap at', address)
    print("Press 'r' to re-launch the page")
    print('Press any other key to terminate')
    from getch.getch import getch
    while ord(getch()) == ord('r'):
        os.startfile(address)

    server.shutdown()


def open_fragmap_page(fragmap, live):
    with open('fragmap.html', 'wb') as (f):
        f.write(make_fragmap_page(fragmap).encode())
        os.startfile(f.name)


def javascript():
    return '\n    prev_source = null;\n    function show(source) {\n      if (prev_source) {\n        prev_source.id = "";\n        prev_source.parentElement.id = "";\n      }\n      prev_source = source;\n      source.id = "selected_cell";\n      source.parentElement.id = "selected_row";\n      source.scrollIntoView();\n      document.getElementById(\'code_window\').innerHTML = source.childNodes[0].innerHTML;\n    }\n    function within(lower, x, upper) {\n      return lower <= x && x <= upper;\n    }\n    function inside(table, row, col) {\n      var nRows = table.getElementsByTagName(\'tr\').length;\n      var nCols = table.getElementsByTagName(\'tr\')[1].getElementsByTagName(\'td\').length || 0;\n      // Note: row minimum is 1 since the first row is the header\n      return within(1, row, nRows - 1) && within(0, col, nCols - 1);\n    }\n    function indexByTagName(haystack, tagName, needleChild) {\n      var children = haystack.getElementsByTagName(tagName);\n      for (var i = 0;; i++) {\n        if (children[i] == needleChild) {\n          return i;\n        }\n      }\n      return -1;\n    }\n    function neighbor(source, rowOffset, colOffset) {\n      var row = source.parentElement;\n      var colNumber = indexByTagName(row, \'td\', source);\n      var table = row.parentElement;\n      var rowNumber = indexByTagName(table, \'tr\', row);\n      if (!inside(table, rowNumber + rowOffset, colNumber + colOffset)) {\n        return null;\n      }\n      return table\n        .getElementsByTagName(\'tr\')[rowNumber + rowOffset]\n        .getElementsByTagName(\'td\')[colNumber + colOffset];\n    }\n    function neighborWhere(source, rowDirection, colDirection, pred) {\n      var cell = source;\n      var i = 0;\n      for (cell = neighbor(cell, rowDirection, colDirection);\n           cell !== null && !pred(cell);\n           i++, cell = neighbor(cell, rowDirection, colDirection)) {\n        // Empty\n      }\n      return [cell, i];\n    }\n    function active_cell(cell) {\n      return cell !== null && cell.getElementsByClassName(\'active\').length > 0;\n    }\n    function handleKeyDown(e) {\n      e = e || window.event;\n      var rowOffset = 0;\n      var colOffset = 0;\n      if (e.key == \'ArrowUp\') {\n        // up arrow\n        rowOffset = -1;\n      }\n      else if (e.key == \'ArrowDown\') {\n        // down arrow\n        rowOffset = 1;\n      }\n      else if (e.key == \'ArrowLeft\') {\n        // left arrow\n        colOffset = -1;\n      }\n      else if (e.key == \'ArrowRight\') {\n        // right arrow\n        colOffset = 1;\n      }\n      else {\n        return true;\n      }\n      var divertable = !e.ctrlKey;\n      var source = prev_source;\n      var next = source;\n      if (!divertable) {\n        [next, _] = neighborWhere(source, rowOffset, colOffset, active_cell);\n      }\n      else {\n        neigh = next;\n        while(neigh !== null) {\n          // Take one step in the desired direction\n          neigh = neighbor(neigh, rowOffset, colOffset);\n          if (neigh === null) {\n            break;\n          }\n          if (active_cell(neigh)) {\n            next = neigh;\n            break;\n          }\n          // Look to both sides\n          [nextPos, distPos] = neighborWhere(neigh, colOffset, rowOffset, active_cell);\n          [nextNeg, distNeg] = neighborWhere(neigh, -colOffset, -rowOffset, active_cell);\n          // Pick whichever was closest and valid\n          if (nextPos !== null) {\n            next = nextPos;\n            if (nextNeg !== null) {\n              next = distNeg < distPos ? nextNeg : nextPos;\n            }\n          }\n          else {\n            next = nextNeg;\n          }\n          if (next !== null) {\n            break;\n          }\n        }\n      }\n      if (next === null) {\n        next = source;\n      }\n      show(next);\n      return false;\n    }\n    document.body.onkeydown = handleKeyDown;\n    '


def css():
    cellwidth = 25
    scale = cellwidth / 360.0

    def scale_number(m):
        return str(int(m.group(1)) * scale)

    return re.sub('{{(\\d+)}}', scale_number, raw_css())


def raw_css():
    return '\n    body {\n      background: black;\n      color: #e5e5e5;\n    }\n    table {\n      border-collapse: collapse;\n    }\n    tr:nth-child(even), tr:nth-child(even) th:nth-child(1), tr:nth-child(even) th:nth-child(2) {\n      background-color: rgba(28, 28, 28);\n    }\n    tr:nth-child(odd), tr:nth-child(odd) th:nth-child(1), tr:nth-child(odd) th:nth-child(2){\n      background-color: rgba(36, 36, 36);\n    }\n    tr th:nth-child(1), tr th:nth-child(2) {\n      z-index: 2;\n    }\n    th {\n      font-family: sans-serif;\n      font-weight: normal;\n    }\n    td, .message_cell {\n      text-align: left;\n      vertical-align: bottom;\n      padding: 0;\n    }\n    .message_cell {\n      box-shadow: 10px 0px 10px 0px rgba(0,0,0,0.5);\n    }\n    th:first-child, th:nth-child(2) {\n      position: -webkit-sticky;\n      position: sticky;\n      left: 0;\n    }\n    .message_cell {\n      white-space: nowrap;\n      font-family: sans-serif;\n    }\n    .commit_hash {\n      font-family: monospace;\n      margin-right: 10pt;\n    }\n    .commit_message {\n      margin-right: 10pt;\n    }\n    .cell_change {\n      background-color: white;\n    }\n    .cell_between_changes {\n      background-color: red;\n    }\n    #selected_cell .dot {\n      background: white;\n      box-shadow: 0px 0px 5px 5px;\n    }\n    tr#selected_row {\n      background-color: rgba(160, 160, 160, 0.4);\n    }\n    .code {\n      display: none;\n    }\n    #map_window {\n      overflow-x: auto;\n    }\n    #code_window {\n      font-family: monospace;\n    }\n    .codeline {\n      margin: 0 auto;\n    }\n    .codeline_added {\n      color: green;\n    }\n    .codeline_removed {\n      color: red;\n    }\n    th.filename_start, td.filename_start {\n      border-left: 4px solid black;\n    }\n    .invisible, .invisible::before {\n        background: inherit;\n    }\n    .cell {\n        position: relative;\n        width: {{360}}px;\n        height: {{360}}px;\n        float: left;\n        z-index: 1;\n    }\n    .inner {\n        border-radius: {{20}}px;\n        height: {{140}}px;\n        width: {{140}}px;\n        padding: {{30}}px;\n        position: absolute;\n        left: {{80}}px;\n        top: {{80}}px;\n    }\n    .dot {\n        background: #0d76c2;\n        border-radius: {{60}}px; /* dot.border_radius = inner.border_radius - inner.padding */\n        box-shadow: {{15}}px {{15}}px {{3}}px {{3}}px rgba(0,0,0,0.8) inset;\n        display: block;\n        position: relative;\n        z-index: 2;\n        width: 100%;\n        height: 100%;\n    }\n    .left:not(.invisible), .right:not(.invisible), .inner {\n        background: #35aaff;\n    }\n    .left, .right {\n        border-radius: 0;\n        height: {{200}}px;\n        width: {{100}}px;\n        z-index: 1;\n        position: absolute;\n        top: {{80}}px;\n    }\n    .right {\n        right: 0px;\n    }\n    .left {\n        left: 0px;\n    }\n    .left.invisible, .right.invisible {\n       visibility: hidden;\n    }\n    .top:not(.invisible), .bottom:not(.invisible) {\n        background: #642bff;\n    }\n    .top, .bottom {\n        display: block;\n        position: absolute;\n        width: {{60}}px;\n        height: {{180}}px;\n        left: {{150}}px; /* top.left = cell.width/2 - top.width/2  */\n        z-index: -1;\n    }\n    .top {\n        top: 0px;\n    }\n    .bottom {\n        bottom: 0px;\n    }\n    '