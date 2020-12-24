# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/guicocoa.py
# Compiled at: 2008-06-07 18:22:46
import sys, objc
from Foundation import *
from AppKit import *
from PyObjCTools import AppHelper
ascImg = NSImage.imageNamed_('NSAscendingSortIndicator')
descImg = NSImage.imageNamed_('NSDescendingSortIndicator')
altCols = NSColor.controlAlternatingRowBackgroundColors()

class AppDelegate(NSObject):
    __module__ = __name__

    def applicationDidFinishLaunching_(self, aNotification):
        self.sortColumn = None
        self.sortOrder = 'Ascending'
        self.indexes = []
        return

    def setTable(self, HEADER, TABLE, FOOTER):
        self.HEADER = HEADER
        self.TABLE = TABLE
        self.FOOTER = FOOTER

    def sayHello_(self, sender):
        print 'Hello again, World!'

    def doubleClick_(self, sender):
        print 'doubleClick!', sender.clickedColumn(), sender.clickedRow()

    def numberOfRowsInTableView_(self, aTableView):
        return len(self.TABLE) + len(self.FOOTER)

    def tableView_objectValueForTableColumn_row_(self, aTableView, aTableColumn, rowIndex):
        col = int(aTableColumn.identifier())
        return (self.TABLE + self.FOOTER)[rowIndex][col]

    def tableView_setObjectValue_forTableColumn_row_(self, aTableView, anObject, aTableColumn, rowIndex):
        col = int(aTableColumn.identifier())
        (self.TABLE + self.FOOTER)[rowIndex][col] = anObject

    def tableView_willDisplayCell_forTableColumn_row_(self, aTableView, aCell, aTableColumn, rowIndex):
        if rowIndex >= len(self.TABLE):
            aCell.setBackgroundColor_(NSColor.headerColor())
        else:
            aCell.setBackgroundColor_(altCols[(rowIndex % 2)])

    def tableView_didClickTableColumn_(self, aTableView, aTableColumn):
        col = int(aTableColumn.identifier())
        if self.sortColumn == None:
            self.sortColumn = col
            sortColumChanged = True
        elif self.sortColumn == col:
            sortColumChanged = False
        elif self.sortColumn != col:
            sortColumChanged = True
            self.sortColumn = col
        if not sortColumChanged:
            self.sortOrder = {'Ascending': 'Descending', 'Descending': 'Ascending'}[self.sortOrder]
        if len(self.FOOTER) == 2:
            SELECTED = self.FOOTER[1]
        tab = []
        for (i, row) in enumerate(self.TABLE):
            tab.append([row[col]] + row + [i in self.indexes])

        tab.sort()
        for tc in aTableView.tableColumns():
            aTableView.setIndicatorImage_inTableColumn_(None, tc)

        if self.sortOrder == 'Descending':
            tab.reverse()
            aTableView.setIndicatorImage_inTableColumn_(descImg, aTableColumn)
        elif self.sortOrder == 'Ascending':
            aTableView.setIndicatorImage_inTableColumn_(ascImg, aTableColumn)
        aTableView.selectAll_(self)
        selectedIndexes = [ row[(-1)] for row in tab ]
        for (j, idx) in enumerate(selectedIndexes):
            if not selectedIndexes[j]:
                aTableView.deselectRow_(j)

        self.TABLE = [ row[1:-1] for row in tab ]
        if len(self.FOOTER) == 2:
            self.FOOTER[1] = SELECTED
        aTableView.reloadData()
        aTableView.setNeedsDisplay_(True)
        return

    def tableView_shouldSelectRow_(self, aTableView, rowIndex):
        if rowIndex >= len(self.TABLE):
            return False
        return True

    def tableView_shouldEditTableColumn_row_(self, aTableView, aTableColumn, rowIndex):
        return False

    def tableViewSelectionDidChange_(self, notification):
        tableView = notification.object()
        indexSet = tableView.selectedRowIndexes()
        newIndexes = []
        for i in range(indexSet.count()):
            if i == 0:
                idx = indexSet.firstIndex()
            else:
                idx = indexSet.indexGreaterThanIndex_(idx)
            newIndexes.append(idx)

        if newIndexes == []:
            self.FOOTER = self.FOOTER[:1]
        elif [] == self.indexes != newIndexes:
            SELECTED = []
            for (colNum, col) in enumerate(tableView.tableColumns()):
                if col.headerCell().stringValue() != 'file':
                    val = sum([ self.TABLE[i][colNum] for i in newIndexes ])
                else:
                    val = 'selected'
                SELECTED.append(val)

            self.FOOTER += [SELECTED]
        elif [] != self.indexes != newIndexes:
            SELECTED = []
            for (colNum, col) in enumerate(tableView.tableColumns()):
                if col.headerCell().stringValue() != 'file':
                    val = sum([ self.TABLE[i][colNum] for i in newIndexes ])
                else:
                    val = 'selected'
                SELECTED.append(val)

            del self.FOOTER[-1]
            self.FOOTER += [SELECTED]
        if newIndexes != self.indexes:
            tableView.reloadData()
        self.indexes = newIndexes

    def windowShouldClose_(self, sender):
        app = NSApplication.sharedApplication().terminate_(sender)


def main(HEADER, TABLE, FOOTER):
    app = NSApplication.sharedApplication()
    delegate = AppDelegate.alloc().init()
    delegate.setTable(HEADER, TABLE, FOOTER)
    NSApp().setDelegate_(delegate)
    win = NSWindow.alloc()
    wframe = ((200.0, 300.0), (500.0, 300.0))
    mask = NSTitledWindowMask | NSClosableWindowMask | NSMiniaturizableWindowMask | NSResizableWindowMask
    win.initWithContentRect_styleMask_backing_defer_(wframe, mask, NSBackingStoreBuffered, False)
    win.setTitle_('Table results')
    win.setMinSize_((200, 150))
    win.setLevel_(NSNormalWindowLevel)
    frame = (
     (0, 0), wframe[1])
    tview = NSTableView.alloc().initWithFrame_(frame)
    win.contentView().addSubview_(tview)
    tview.setDelegate_(delegate)
    tview.setTarget_(delegate)
    tview.setAutosaveTableColumns_(True)
    tview.setDataSource_(delegate)
    tview.setAllowsMultipleSelection_(True)
    tview.setAllowsEmptySelection_(True)
    tview.setGridStyleMask_(NSTableViewSolidVerticalGridLineMask)
    tview.setUsesAlternatingRowBackgroundColors_(True)
    for col in range(len(HEADER)):
        tcol = NSTableColumn.alloc().initWithIdentifier_(col)
        tcol.setWidth_(100)
        tcol.headerCell().setStringValue_(HEADER[col])
        tcol.headerCell().setDrawsBackground_(True)
        tcol.headerCell().setBackgroundColor_(NSColor.headerColor())
        tcol.headerCell().setTarget_(delegate)
        tview.addTableColumn_(tcol)

    sview = NSScrollView.alloc().initWithFrame_(frame)
    win.contentView().addSubview_(sview)
    sview.window().setDelegate_(delegate)
    sview.setHasVerticalScroller_(True)
    sview.setHasHorizontalScroller_(True)
    sview.setAutohidesScrollers_(True)
    sview.setBorderType_(NSNoBorder)
    sview.setAutoresizingMask_(NSViewWidthSizable | NSViewHeightSizable)
    sview.setDocumentView_(tview)
    win.makeFirstResponder_(sview)
    if False:
        print tview.numberOfColumns(), tview.numberOfRows()
        print tview.tableColumns()
        print tview.tableColumnWithIdentifier_('size')
        print tview.subviews()
    if False:
        bye = NSButton.alloc().initWithFrame_(((10, 10), (80.0, 30.0)))
        win.contentView().addSubview_(bye)
        bye.setBezelStyle_(NSThickerSquareBezelStyle)
        bye.setTarget_(app)
        bye.setAction_('stop:')
        bye.setEnabled_(True)
        bye.setTitle_('Quit')
    win.display()
    win.orderFrontRegardless()
    AppHelper.runEventLoop()


def test():
    TABLE = '    size;file(fake)\n    608;crons\n    8;ex.csv\n    0;fonts\n    123;imm.dat\n    593;imm.license\n    8417;profile1.xml.odt\n    4240;UserDefaults.txt\n    9999;total'
    TABLE = [ line.split(';') for line in TABLE.split('\n') ]
    HEADER = TABLE[0]
    FOOTER = [TABLE[(-1)]]
    TABLE = TABLE[1:-1]
    main(HEADER, TABLE, FOOTER)


if __name__ == '__main__':
    try:
        TABLE = open(sys.argv[1]).read().strip()
    except IndexError:
        TABLE = '    size;file(fake)\n    608;crons\n    8;ex.csv\n    0;fonts\n    123;imm.dat\n    593;imm.license\n    8417;profile1.xml.odt\n    4240;UserDefaults.txt\n    9999;total'
    else:
        TABLE = [ line.split(';') for line in TABLE.split('\n') ]
        HEADER = TABLE[0]
        FOOTER = [TABLE[(-1)]]
        TABLE = TABLE[1:-1]
        main(HEADER, TABLE, FOOTER)