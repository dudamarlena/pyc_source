# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdftables/pdftables.py
# Compiled at: 2016-07-22 05:10:04
# Size of source mod 2**32: 20308 bytes
"""
Some experiments with pdfminer
http://www.unixuser.org/~euske/python/pdfminer/programming.html
Some help here:
http://denis.papathanasiou.org/2010/08/04/extracting-text-images-from-pdf-files
"""
import sys, codecs
from pdfminer.pdfparser import PDFParser
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfdevice import PDFDevice
from pdfminer.layout import LAParams, LTPage
from pdfminer.converter import PDFPageAggregator
import collections
from .tree import Leaf, LeafList
import requests
from io import StringIO
import math, numpy
from .counter import Counter

def fround(x):
    return float(round(x))


IS_TABLE_COLUMN_COUNT_THRESHOLD = 3
IS_TABLE_ROW_COUNT_THRESHOLD = 3

class TableDiagnosticData(object):

    def __init__(self, box_list=LeafList(), top_plot=dict(), left_plot=dict(), x_comb=[], y_comb=[]):
        self.box_list = box_list
        self.top_plot = top_plot
        self.left_plot = left_plot
        self.x_comb = x_comb
        self.y_comb = y_comb


class Table(list):

    def __init__(self, content, page, page_total, table_index, table_index_total):
        super(Table, self).__init__(content)
        self.page_number = page
        self.total_pages = page_total
        self.table_number_on_page = table_index
        self.total_tables_on_page = table_index_total


LEFT = 0
TOP = 3
RIGHT = 2
BOTTOM = 1

def get_tables(fh):
    """
    Return a list of 'tables' from the given file handle, where a table is a
    list of rows, and a row is a list of strings.
    """
    result = []
    interpreter, device = initialize_pdf_interpreter()
    pages = list(PDFPage.get_pages(fh))
    doc_length = len(pages)
    for i, pdf_page in enumerate(pages):
        if not page_contains_tables(pdf_page, interpreter, device):
            continue
        interpreter.process_page(pdf_page)
        processed_page = device.get_result()
        table, _ = page_to_tables(processed_page, extend_y=True, hints=[], atomise=True)
        crop_table(table)
        result.append(Table(table, i + 1, doc_length, 1, 1))

    return result


def crop_table(table):
    """
    Remove empty rows from the top and bottom of the table.
    """
    for row in list(table):
        if not any(cell.strip() for cell in row):
            table.remove(row)
        else:
            break

    for row in list(reversed(table)):
        if not any(cell.strip() for cell in row):
            table.remove(row)
        else:
            break


def initialize_pdf_interpreter():
    rsrcmgr = PDFResourceManager()
    device = PDFDevice(rsrcmgr)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    laparams = LAParams()
    laparams.word_margin = 0.0
    device = PDFPageAggregator(rsrcmgr, laparams=laparams)
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    return (interpreter, device)


def contains_tables(fh):
    """
    contains_tables(fh) takes a file handle and returns a boolean array of the
    length of the document which is true for pages which contains tables
    """
    interpreter, device = initialize_pdf_interpreter()
    pages = PDFPage.get_pages(fh)
    return [page_contains_tables(p, interpreter, device) for p in pages]


def page_contains_tables(pdf_page, interpreter, device):
    interpreter.process_page(pdf_page)
    layout = device.get_result()
    box_list = LeafList().populate(layout)
    for item in box_list:
        if not isinstance(item, Leaf):
            raise AssertionError('NOT LEAF')

    yhist = box_list.histogram(Leaf._top).rounder(1)
    test = [k for k, v in list(yhist.items()) if v > IS_TABLE_COLUMN_COUNT_THRESHOLD]
    return len(test) > IS_TABLE_ROW_COUNT_THRESHOLD


def threshold_above(hist, threshold_value):
    """
    >>> threshold_above(Counter({518: 10, 520: 20, 530: 20,                                              525: 17}), 15)
    [520, 530, 525]
    """
    if not isinstance(hist, Counter):
        raise ValueError('requires Counter')
    above = [k for k, v in list(hist.items()) if v > threshold_value]
    return above


def comb(combarray, value):
    """
    Takes a sorted array and returns the interval number of the value passed to
    the function
    """
    if combarray != sorted(combarray):
        if combarray != sorted(combarray, reverse=True):
            raise Exception('comb: combarray is not sorted')
    index = -1
    if combarray[0] > combarray[(-1)]:
        for i in range(1, len(combarray)):
            if combarray[(i - 1)] >= value >= combarray[i]:
                index = i - 1
                continue

    else:
        for i in range(1, len(combarray)):
            if combarray[(i - 1)] <= value <= combarray[i]:
                index = i - 1
                continue

    return index


def apply_combs(box_list, x_comb, y_comb):
    """Allocates text to table cells using the x and y combs"""
    ncolumns = len(x_comb) - 1
    nrows = len(y_comb) - 1
    table_array = [[''] * ncolumns for j in range(nrows)]
    for box in box_list:
        y = fround(box.midline)
        x = fround(box.centreline)
        rowindex = comb(y_comb, y)
        columnindex = comb(x_comb, x)
        if rowindex != -1 and columnindex != -1:
            table_array[rowindex][columnindex] += box.text.rstrip('\n\r')
            continue

    return table_array


def comb_from_projection(projection, threshold, orientation):
    """Calculates the boundaries between cells from the projection of the boxes
    onto either the y axis (for rows) or the x-axis (for columns). These
    boundaries are known as the comb
    """
    if orientation == 'row':
        tol = 1
    elif orientation == 'column':
        tol = 3
    projection_threshold = threshold_above(projection, threshold)
    projection_threshold = sorted(projection_threshold)
    uppers = []
    lowers = []
    lowers.append(projection_threshold[0])
    for i in range(1, len(projection_threshold)):
        if projection_threshold[i] > projection_threshold[(i - 1)] + 1:
            uppers.append(projection_threshold[(i - 1)])
            lowers.append(projection_threshold[i])
            continue

    uppers.append(projection_threshold[(-1)])
    comb = comb_from_uppers_and_lowers(uppers, lowers, tol=tol, projection=projection)
    comb.reverse()
    return comb


def comb_from_uppers_and_lowers(uppers, lowers, tol=1, projection=dict()):
    """Called by comb_from_projection to calculate the comb given a set of
    uppers and lowers, which are upper and lower edges of the thresholded
    projection"""
    assert len(uppers) == len(lowers)
    uppers.sort(reverse=True)
    lowers.sort(reverse=True)
    comb = []
    comb.append(uppers[0])
    for i in range(1, len(uppers)):
        if lowers[(i - 1)] - uppers[i] > tol:
            comb.append(find_minima(lowers[(i - 1)], uppers[i], projection))
            continue

    comb.append(lowers[(-1)])
    return comb


def find_minima(lower, upper, projection=dict()):
    if len(projection) == 0:
        idx = (lower + upper) / 2.0
    else:
        profile = []
        for i in range(upper, lower):
            profile.append(projection[i])

        val, idx = min((val, idx) for idx, val in enumerate(profile))
        idx = upper + idx
    return idx


def comb_extend(comb, minv, maxv):
    """Extend the comb to minv and maxv"""
    reversed = False
    if comb[0] > comb[(-1)]:
        comb.reverse()
        reversed = True
    minc = comb[0]
    maxc = comb[(-1)]
    rowSpacing = numpy.average(numpy.diff(comb))
    if minv < minc:
        comb.reverse()
        comb.extend(list(numpy.arange(minc, minv, -rowSpacing))[1:])
        comb.reverse()
    if maxv > maxc:
        comb.extend(list(numpy.arange(maxc, maxv, rowSpacing))[1:])
    if reversed:
        comb.reverse()
    return comb


def project_boxes(box_list, orientation, erosion=0):
    """
    Take a set of boxes and project their extent onto an axis
    """
    if orientation == 'column':
        upper = RIGHT
        lower = LEFT
    elif orientation == 'row':
        upper = TOP
        lower = BOTTOM
    projection = {}
    minv = fround(min([box.bbox[lower] for box in box_list])) - 2
    maxv = fround(max([box.bbox[upper] for box in box_list])) + 2
    coords = list(range(int(minv), int(maxv)))
    projection = coords
    for box in box_list:
        for i in range(int(fround(box.bbox[lower])) + erosion, int(fround(box.bbox[upper])) - erosion):
            projection.append(i)

    return Counter(projection)


def get_pdf_page(fh, pagenumber):
    interpreter, device = initialize_pdf_interpreter()
    pages = list(PDFPage.get_pages(fh))
    try:
        page = pages[(pagenumber - 1)]
    except IndexError:
        raise IndexError('Invalid page number')

    interpreter.process_page(page)
    processedPage = device.get_result()
    return processedPage


def get_min_and_max_y_from_hints(box_list, top_string, bottom_string):
    miny = None
    maxy = None
    if top_string:
        top_box = [box for box in box_list if top_string in box.text]
        if top_box:
            maxy = top_box[0].top
    if bottom_string:
        bottomBox = [box for box in box_list if bottom_string in box.text]
        if bottomBox:
            miny = bottomBox[0].bottom
    return (
     miny, maxy)


def rounder(val, tol):
    """
    Utility function to round numbers to arbitrary tolerance
    """
    return fround(1.0 * val / tol) * tol


def multi_column_detect(page):
    """
    Test for multiColumns from a box_list, returns an integer number of columns
    and a set of (left, right) pairs delineating any columns
    """
    box_list = LeafList().populate(page, ['LTPage', 'LTTextLineHorizontal']).purge_empty_text()
    box_list = filter_box_list_by_type(box_list, 'LTTextLineHorizontal')
    pile = {}
    vstep = 5
    minv = rounder(min([box.bottom for box in box_list]), 5)
    maxv = rounder(max([box.top for box in box_list]), 5)
    minx = fround(min([box.left for box in box_list]))
    maxx = fround(max([box.right for box in box_list]))
    coords = list(range(int(minv), int(maxv) + vstep, vstep))
    pile = collections.OrderedDict(list(zip(coords, [0] * len(coords))))
    for box in box_list:
        pile[int(rounder(box.midline, vstep))] += box.width

    for key, value in list(pile.items()):
        pile[key] = value // (maxx - minx)

    bstep = 10
    boxhist = {}
    boxwidthmin = rounder(min([box.width for box in box_list]), bstep)
    boxwidthmax = rounder(max([box.width for box in box_list]), bstep)
    coords = list(range(int(boxwidthmin), int(boxwidthmax) + bstep, bstep))
    boxhist = collections.OrderedDict(list(zip(coords, [0] * len(coords))))
    for box in box_list:
        boxhist[int(rounder(box.width, bstep))] += 1

    nboxes = len(box_list)
    for key, value in list(boxhist.items()):
        boxhist[key] = float(value) / float(nboxes)

    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.plot(list(map(float, list(boxhist.keys()))), list(map(float, list(boxhist.values()))), color='red')
    plt.show()
    projection = project_boxes(box_list, 'column')
    return (
     pile, projection)


def page_to_tables(page, extend_y=False, hints=[], atomise=False):
    """
    Get a rectangular list of list of strings from one page of a document
    """
    if not isinstance(page, LTPage):
        raise TypeError('Page must be LTPage, not {}'.format(page.__class__))
    table_array = []
    columnThreshold = 5
    rowThreshold = 3
    if atomise:
        flt = [
         'LTPage', 'LTTextLineHorizontal', 'LTChar']
    else:
        flt = [
         'LTPage', 'LTTextLineHorizontal']
    box_list = LeafList().populate(page, flt).purge_empty_text()
    minx, maxx, miny, maxy = find_table_bounding_box(box_list, hints=hints)
    if miny is None and maxy is None:
        print('found no tables')
        return (
         table_array, TableDiagnosticData())
    if atomise:
        box_list = box_list.filterByType(['LTPage', 'LTChar'])
    filtered_box_list = filter_box_list_by_position(box_list, miny, maxy, Leaf._midline)
    filtered_box_list = filter_box_list_by_position(filtered_box_list, minx, maxx, Leaf._centreline)
    column_projection = project_boxes(filtered_box_list, 'column')
    erodelevel = int(math.floor(calculate_modal_height(filtered_box_list) // 4))
    row_projection = project_boxes(filtered_box_list, 'row', erosion=erodelevel)
    y_comb = comb_from_projection(row_projection, rowThreshold, 'row')
    y_comb.reverse()
    x_comb = comb_from_projection(column_projection, columnThreshold, 'column')
    x_comb[0] = minx
    x_comb[-1] = maxx
    if extend_y:
        pageminy = min([box.bottom for box in box_list])
        pagemaxy = max([box.top for box in box_list])
        y_comb = comb_extend(y_comb, pageminy, pagemaxy)
        filtered_box_list = box_list
    table_array = apply_combs(box_list, x_comb, y_comb)
    if atomise:
        tmp_table = []
        for row in table_array:
            stripped_row = list(map(str.strip, row))
            tmp_table.append(stripped_row)

        table_array = tmp_table
    diagnostic_data = TableDiagnosticData(filtered_box_list, column_projection, row_projection, x_comb, y_comb)
    return (
     table_array, diagnostic_data)


def find_table_bounding_box(box_list, hints=[]):
    """ Returns one bounding box (minx, maxx, miny, maxy) for tables based
    on a boxlist
    """
    miny = min([box.bottom for box in box_list])
    maxy = max([box.top for box in box_list])
    minx = min([box.left for box in box_list])
    maxx = max([box.right for box in box_list])
    textLine_boxlist = box_list.filterByType('LTTextLineHorizontal')
    yhisttop = textLine_boxlist.histogram(Leaf._top).rounder(2)
    yhistbottom = textLine_boxlist.histogram(Leaf._bottom).rounder(2)
    try:
        miny = min(threshold_above(yhistbottom, IS_TABLE_COLUMN_COUNT_THRESHOLD))
        maxy = max(threshold_above(yhisttop, IS_TABLE_COLUMN_COUNT_THRESHOLD))
    except ValueError:
        miny = None
        maxy = None

    if hints:
        top_string = hints[0]
        bottom_string = hints[1]
        hintedminy, hintedmaxy = get_min_and_max_y_from_hints(textLine_boxlist, top_string, bottom_string)
        if hintedminy:
            miny = hintedminy
        if hintedmaxy:
            maxy = hintedmaxy
    return (minx, maxx, miny, maxy)


def filter_box_list_by_position(box_list, minv, maxv, dir_fun):
    filtered_box_list = LeafList()
    for box in box_list:
        if dir_fun(box) >= minv and dir_fun(box) <= maxv:
            filtered_box_list.append(box)
            continue

    return filtered_box_list


def calculate_modal_height(box_list):
    height_list = []
    for box in box_list:
        if box.classname in ('LTTextLineHorizontal', 'LTChar'):
            height_list.append(fround(box.bbox[TOP] - box.bbox[BOTTOM]))
            continue

    modal_height = Counter(height_list).most_common(1)
    return modal_height[0][0]


def file_handle_from_url(URL):
    response = requests.get(URL)
    fh = StringIO(response.content)
    return fh


if __name__ == '__main__':
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
    if len(sys.argv) > 1:
        from .display import to_string
        with open(sys.argv[1], 'rb') as (f):
            tables = get_tables(f)
            for i, table in enumerate(tables):
                print('---- TABLE {} ----'.format(i + 1))
                print(to_string(table))

    else:
        print('Usage: {} <file.pdf>'.format(sys.argv[0]))