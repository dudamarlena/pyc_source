# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdftables/pdftables_analysis.py
# Compiled at: 2016-07-21 18:27:49
# Size of source mod 2**32: 4578 bytes
import sys, codecs
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)
from . import pdftables as pt
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import make_axes_locatable
from .tree import Leaf, LeafList
from pdfminer.pdfpage import PDFPage
FilterOptions = [
 'LTPage', 'LTTextBoxHorizontal', 'LTFigure', 'LTLine', 'LTRect', 'LTImage', 'LTTextLineHorizontal', 'LTCurve', 'LTChar', 'LTAnon']
Colours = ['black', 'green', 'black', 'red', 'red', 'black', 'blue', 'red', 'red', 'White']
ColourTable = dict(list(zip(FilterOptions, Colours)))
LEFT = 0
TOP = 3
RIGHT = 2
BOTTOM = 1

def plotpage(d):
    """This is from pdftables"""
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.axis('equal')
    for boxstruct in d.box_list:
        box = boxstruct.bbox
        thiscolour = ColourTable[boxstruct.classname]
        ax1.plot([box[0], box[2], box[2], box[0], box[0]], [box[1], box[1], box[3], box[3], box[1]], color=thiscolour)

    divider = make_axes_locatable(ax1)
    ax1.yaxis.set_label_position('right')
    if d.top_plot:
        axHistx = divider.append_axes('top', 1.2, pad=0.1, sharex=ax1)
        axHistx.plot(list(map(float, list(d.top_plot.keys()))), list(map(float, list(d.top_plot.values()))), color='red')
    if d.left_plot:
        axHisty = divider.append_axes('left', 1.2, pad=0.1, sharey=ax1)
        axHisty.plot(list(map(float, list(d.left_plot.values()))), list(map(float, list(d.left_plot.keys()))), color='red')
    if d.y_comb:
        miny = min(d.y_comb)
        maxy = max(d.y_comb)
        for x in d.x_comb:
            ax1.plot([x, x], [miny, maxy], color='black')
            axHistx.scatter(x, 0, color='black')

    if d.x_comb:
        minx = min(d.x_comb)
        maxx = max(d.x_comb)
        for y in d.y_comb:
            ax1.plot([minx, maxx], [y, y], color='black')
            axHisty.scatter(1, y, color='black')

    plt.draw()
    plt.show(block=False)
    return (
     fig, ax1)


def plothistogram(hist):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.scatter(list(map(float, list(hist.keys()))), list(map(float, list(hist.values()))))
    plt.draw()
    return fig


def plotAllPages(fh):
    fig_list = []
    ax1_list = []
    interpreter, device = pt.initialize_pdf_interpreter()
    pages = PDFPage.get_pages(fh)
    flt = [
     'LTPage', 'LTChar']
    for i, page in enumerate(pages):
        interpreter.process_page(page)
        layout = device.get_result()
        box_list = LeafList().populate(layout, interested=flt)
        ModalHeight = pt.calculate_modal_height(box_list)
        diagnostic_data = pt.TableDiagnosticData(box_list, {}, {}, [], [])
        fig, ax1 = plotpage(diagnostic_data)
        fig_list.append(fig)
        ax1_list.append(ax1)
        title = 'page %d' % (i + 1)
        fig.suptitle(title)
        print(box_list.count())
        print('Modal character height: %d' % ModalHeight)

    return (fig_list, ax1_list)