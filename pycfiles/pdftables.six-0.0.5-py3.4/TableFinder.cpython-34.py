# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pdftables/TableFinder.py
# Compiled at: 2016-07-21 11:30:30
# Size of source mod 2**32: 3823 bytes
"""
Code to find tables in PDF files
"""
import os, scraperwiki, lxml.html, glob, matplotlib.pyplot as plt, collections
from .counter import Counter

def pdftoxml(filename, options):
    ConverterPath = str('C:\\Users\\Ian\\BitBucketRepos\\0939-AgraInforma\\bin\\pdftohtml.exe')
    directory = os.path.split(filename)[0]
    tmpxml = os.path.join(directory, 'temph.xml')
    if tmpxml in os.listdir('.'):
        os.remove(tmpxml)
    cmd = '%s -xml %s "%s" %s' % (ConverterPath, options, filename, os.path.splitext(tmpxml)[0])
    os.system(cmd)
    f = open(tmpxml, 'rb')
    content = f.read()
    f.close()
    return content


def processpage(page):
    left = []
    width = []
    top = []
    right = []
    for textchunk in page is not None and page.xpath('text'):
        thisleft = int(textchunk.attrib.get('left'))
        thiswidth = int(textchunk.attrib.get('width'))
        left.append(thisleft)
        width.append(thiswidth)
        top.append(pageheight - int(textchunk.attrib.get('top')))
        right.append(thisleft + thiswidth)

    return (pageheight, pagewidth, left, top, right)


def plotpage(pageheight, pagewidth, pagenumber, SelectedPDF, left, top, right):
    fig = plt.figure()
    ax1 = fig.add_subplot(111)
    ax1.axis('equal')
    ax1.plot([0, pagewidth, pagewidth, 0, 0], [0, 0, pageheight, pageheight, 0])
    ax1.scatter(left, top, s=10, c='b', marker='s')
    ax1.scatter(right, top, s=10, c='r', marker='o')
    fig.suptitle('%s : Page %d' % (SelectedPDF, pagenumber), fontsize=15)
    plt.show()
    return fig


PDF_TEST_FILES = str('C:\\Users\\Ian\\BitBucketRepos\\0939-AgraInforma\\fixtures')
SelectedPDF = 'argentina_diputados_voting_record.pdf'
xmldata = pdftoxml(os.path.join(PDF_TEST_FILES, SelectedPDF), options)
root = lxml.etree.fromstring(xmldata)
pages = list(root)
for page in pages:
    pagenumber = int(page.attrib.get('number'))
    pagewidth = int(page.attrib.get('width'))
    pageheight = int(page.attrib.get('height'))
    pageheight, pagewidth, left, top, right = processpage(page)
    fig = plotpage(pageheight, pagewidth, pagenumber, SelectedPDF, left, top, right)