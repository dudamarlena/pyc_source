# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /tmp/pip-install-ncu5lfw4/arelle/arelle/UiUtil.py
# Compiled at: 2018-08-09 04:11:41
# Size of source mod 2**32: 34295 bytes
__doc__ = '\nCreated on Jan 25, 2011\n\n@author: Mark V Systems Limited\n(c) Copyright 2011 Mark V Systems Limited, All rights reserved.\n'
from tkinter import *
try:
    from tkinter.ttk import *
    _Combobox = ttk.Combobox
except ImportError:
    from ttk import *
    _Combobox = Combobox

TOPBORDER = 1
LEFTBORDER = 2
RIGHTBORDER = 3
BOTTOMBORDER = 4
CENTERCELL = 5
borderImage = None

class gridBorder(Separator):

    def __init__(self, master, x, y, border, columnspan=None, rowspan=None):
        Separator.__init__(self, master=master)
        if border in (TOPBORDER, BOTTOMBORDER):
            x = x * 2 - 1
            if columnspan:
                columnspan = columnspan * 2 + 1
            else:
                columnspan = 3
            self.config(orient='horizontal')
            sticky = (E, W)
        if border in (LEFTBORDER, RIGHTBORDER):
            y = y * 2 - 1
            if rowspan:
                rowspan = rowspan * 2 + 1
            else:
                rowspan = 3
            self.config(orient='vertical')
            sticky = (N, S)
        if border == TOPBORDER:
            rowspan = None
            y = y * 2 - 1
            master.rowconfigure(y, weight=0, uniform='noStretch')
        else:
            if border == BOTTOMBORDER:
                if rowspan:
                    y = (y + rowspan - 1) * 2 + 1
                    rowspan = None
                else:
                    y = y * 2 + 1
                master.rowconfigure(y, weight=0, uniform='noStretch')
            else:
                if border == LEFTBORDER:
                    columnspan = None
                    x = x * 2 - 1
                    master.columnconfigure(x, weight=0, uniform='noStretch')
                else:
                    if border == RIGHTBORDER:
                        if columnspan:
                            x = (x + columnspan - 1) * 2 + 1
                            columnspan = None
                        else:
                            x = x * 2 + 1
                        master.columnconfigure(x, weight=0, uniform='noStretch')
                    if columnspan and columnspan > 1 and rowspan and rowspan > 1:
                        self.grid(column=x, row=y, sticky=sticky, columnspan=columnspan, rowspan=rowspan)
                    else:
                        if columnspan and columnspan > 1:
                            self.grid(column=x, row=y, sticky=sticky, columnspan=columnspan)
                        else:
                            if rowspan and rowspan > 1:
                                self.grid(column=x, row=y, sticky=sticky, rowspan=rowspan)
                            else:
                                self.grid(column=x, row=y, sticky=sticky)
        self.x = x
        self.y = y
        self.columnspan = columnspan
        self.rowspan = rowspan
        try:
            contextMenuBinding = master.bind(master.contextMenuClick)
            if contextMenuBinding:
                self.bind(master.contextMenuClick, contextMenuBinding)
        except AttributeError:
            pass


class gridSpacer(Frame):

    def __init__(self, master, x, y, where):
        Frame.__init__(self, master=master)
        if where == CENTERCELL:
            offset = 0
        else:
            if where in (TOPBORDER, LEFTBORDER):
                offset = -1
            else:
                offset = 1
            x = x * 2 + offset
            y = y * 2 + offset
            self.grid(column=x, row=y)
            self.x = x
            self.y = y
            self.config(width=2, height=2)
            if where in (TOPBORDER, BOTTOMBORDER):
                master.rowconfigure(y, weight=0, uniform='noStretch')
            elif where in (LEFTBORDER, RIGHTBORDER):
                master.columnconfigure(x, weight=0, uniform='noStretch')
        try:
            contextMenuBinding = master.bind(master.contextMenuClick)
            if contextMenuBinding:
                self.bind(master.contextMenuClick, contextMenuBinding)
        except AttributeError:
            pass


class gridHdr(Label):

    def __init__(self, master, x, y, text, columnspan=None, rowspan=None, anchor='center', padding=None, wraplength=None, width=None, minwidth=None, stretchCols=True, stretchRows=True, objectId=None, onClick=None):
        Label.__init__(self, master=master)
        if isinstance(master.master.master, scrolledHeaderedFrame):
            x = x * 2
            y = y * 2
            if columnspan:
                columnspan = columnspan * 2 - 1
            if rowspan:
                rowspan = rowspan * 2 - 1
        self.config(text=text if text is not None else '', width=width, anchor=anchor)
        if padding:
            self.config(padding=padding)
        if wraplength:
            self.config(wraplength=wraplength)
        if columnspan and columnspan > 1 and rowspan and rowspan > 1:
            self.grid(column=x, row=y, sticky=(E, W, N, S), columnspan=columnspan, rowspan=rowspan)
        else:
            if columnspan and columnspan > 1:
                self.grid(column=x, row=y, sticky=(E, W, N, S), columnspan=columnspan)
            else:
                if rowspan and rowspan > 1:
                    self.grid(column=x, row=y, sticky=(E, W, N, S), rowspan=rowspan)
                else:
                    self.grid(column=x, row=y, sticky=(E, W, N, S))
                self.x = x
                self.y = y
                self.columnspan = columnspan
                self.rowspan = rowspan
                self.objectId = objectId
                if minwidth:
                    master.columnconfigure(x, minsize=minwidth)
                if stretchCols:
                    master.columnconfigure(x, weight=1)
                else:
                    master.columnconfigure(x, weight=0, uniform='noStretch')
            if stretchRows:
                master.rowconfigure(y, weight=1)
            else:
                master.rowconfigure(y, weight=0, uniform='noStretch')
        try:
            contextMenuBinding = master.bind(master.contextMenuClick)
            if contextMenuBinding:
                self.bind(master.contextMenuClick, contextMenuBinding)
        except AttributeError:
            pass

        if isinstance(master.master.master, scrolledHeaderedFrame):
            self.bind('<Configure>', master.master.master._configure_cell)
        if onClick:
            self.bind('<1>', onClick)


class gridCell(Entry):

    def __init__(self, master, x, y, value='', width=None, justify=None, objectId=None, onClick=None):
        Entry.__init__(self, master=master)
        self.valueVar = StringVar()
        self.valueVar.trace('w', self.valueChanged)
        self.config(textvariable=self.valueVar, justify=justify, width=width)
        if isinstance(master.master.master, scrolledHeaderedFrame):
            x = x * 2
            y = y * 2
        self.grid(column=x, row=y, sticky=(N, S, E, W))
        self.x = x
        self.y = y
        if value is not None:
            self.valueVar.set(value)
        self.objectId = objectId
        try:
            contextMenuBinding = master.bind(master.contextMenuClick)
            if contextMenuBinding:
                self.bind(master.contextMenuClick, contextMenuBinding)
        except AttributeError:
            pass

        if isinstance(master.master.master, scrolledHeaderedFrame):
            self.bind('<Configure>', master.master.master._configure_cell)
        if onClick:
            self.bind('<1>', onClick)
        self.isChanged = False

    @property
    def value(self):
        return self.valueVar.get()

    def setValue(self, value):
        return self.valueVar.set(value)

    def valueChanged(self, *args):
        self.isChanged = True


class gridCombobox(_Combobox):

    def __init__(self, master, x, y, value='', values=(), width=None, objectId=None, columnspan=None, selectindex=None, comboboxselected=None, state=None):
        _Combobox.__init__(self, master=master)
        self.valueVar = StringVar()
        self.valueVar.trace('w', self.valueChanged)
        self.config(textvariable=self.valueVar, background='#ff8ff8ff8', foreground='#000000000', width=width, state=state)
        self['values'] = values
        if isinstance(master.master.master, scrolledHeaderedFrame):
            x = x * 2
            y = y * 2
            if columnspan:
                columnspan = columnspan * 2 - 1
            if columnspan and columnspan > 1:
                self.grid(column=x, row=y, sticky=(E, W), columnspan=columnspan)
            else:
                self.grid(column=x, row=y, sticky=(E, W))
            if selectindex is not None:
                self.valueVar.set(values[selectindex])
        elif value:
            self.valueVar.set(value)
        self.objectId = objectId
        try:
            contextMenuBinding = master.bind(master.contextMenuClick)
            if contextMenuBinding:
                self.bind(master.contextMenuClick, contextMenuBinding)
        except AttributeError:
            pass

        if comboboxselected:
            self.bind('<<ComboboxSelected>>', comboboxselected)
        self.isChanged = False

    @property
    def value(self):
        return self.valueVar.get()

    @property
    def valueIndex(self):
        value = self.valueVar.get()
        values = self['values']
        if value in values:
            return values.index(value)
        return -1

    def valueChanged(self, *args):
        self.isChanged = True


class label(Label):

    def __init__(self, master, x, y, text):
        Label.__init__(self, master=master, text=text)
        self.grid(column=x, row=y, sticky=W, padx=8)


class checkbox(Checkbutton):

    def __init__(self, master, x, y, text, attr=None, columnspan=None, onclick=None):
        self.attr = attr
        self.onclick = onclick
        self.valueVar = StringVar()
        self.valueVar.trace('w', self.valueChanged)
        Checkbutton.__init__(self, master=master, text=text, variable=self.valueVar)
        self.grid(column=x, row=y, sticky=W, padx=24)
        if columnspan:
            self.grid(columnspan=columnspan)
        try:
            options = master.master.options
            if attr in options:
                self.valueVar.set(options[attr])
        except AttributeError:
            pass

        self.isChanged = False

    @property
    def value(self):
        if self.valueVar.get() == '1':
            return True
        else:
            return False

    def valueChanged(self, *args):
        self.isChanged = True
        if self.onclick is not None:
            self.onclick(self)


class radiobutton(Radiobutton):

    def __init__(self, master, x, y, text, value, attr=None, valueVar=None):
        self.attr = attr
        self.valueVar = valueVar if valueVar else StringVar()
        Radiobutton.__init__(self, master=master, text=text, variable=self.valueVar, value=value)
        self.grid(column=x, row=y, sticky=W, padx=24)
        try:
            options = master.master.options
            if attr in options:
                self.valueVar.set(options[attr])
        except AttributeError:
            pass

    @property
    def value(self):
        return self.valueVar.get()


class scrolledFrame(Frame):

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        hscrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.canvas = canvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set, xscrollcommand=hscrollbar.set)
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        canvas.grid(row=0, column=0, sticky=(N, S, E, W))
        vscrollbar.grid(row=0, column=1, sticky=(N, S))
        hscrollbar.grid(row=1, column=0, sticky=(E, W))
        vscrollbar.config(command=canvas.yview)
        hscrollbar.config(command=canvas.xview)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        canvas.columnconfigure(0, weight=1)
        canvas.rowconfigure(0, weight=1)
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)
        self.interior = interior = Frame(canvas)
        self.interior_id = canvas.create_window(0, 0, window=interior, anchor=NW)
        interior.bind('<Configure>', self._configure_interior)
        canvas.bind('<Configure>', self._configure_canvas)

    def _configure_interior(self, event):
        interiorW = self.interior.winfo_reqwidth()
        interiorH = self.interior.winfo_reqheight()
        self.canvas.config(scrollregion=(0, 0, interiorW, interiorH))

    def _configure_canvas(self, event):
        """ needed if only scrolling in one direction
        canvasW = self.canvas.winfo_width()
        if self.interior.winfo_reqwidth() != canvasW:
            # update the inner frame's width to fill the canvas
            self.canvas.itemconfigure(self.interior_id, width=canvasW)
        canvasH = self.canvas.winfo_height()
        if self.interior.winfo_reqheight() != canvasH:
            self.canvas.itemconfigure(self.interior_id, height=canvasH)
        """
        pass

    def clearGrid(self):
        x, y = self.size()
        for widget in self.winfo_children():
            widget.destroy()

        if x > 1 and y > 1:
            for x in range(x):
                self.tk.call(('grid', 'columnconfigure', self._w, x, '-minsize', 0))

            for y in range(y):
                self.tk.call(('grid', 'rowconfigure', self._w, y, '-minsize', 0))

            self.config(width=1, height=1)
        self.update()
        self.colsConfigured = False


class scrolledHeaderedFrame(Frame):

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)
        self.colsConfigured = False
        self.bodyCellsConfigured = False
        self.blockConfigureCell = False
        self.hdrVscrollbar = Scrollbar(self, orient=VERTICAL)
        self.hdrHscrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.bodyVscrollbar = Scrollbar(self, orient=VERTICAL)
        self.bodyHscrollbar = Scrollbar(self, orient=HORIZONTAL)
        self.colHdrCanvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.hdrVscrollbar.set)
        self.rowHdrCanvas = Canvas(self, bd=0, highlightthickness=0, xscrollcommand=self.hdrHscrollbar.set)
        self.bodyCanvas = Canvas(self, bd=0, highlightthickness=0, yscrollcommand=self.bodyVscrollbar.set, xscrollcommand=self.bodyHscrollbar.set)
        self.grid(row=0, column=0, sticky=(N, S, E, W))
        self.tblHdrInterior = Frame(self)
        self.tblHdrInterior.grid(row=1, column=0, sticky=(N, S, E, W))
        self.colHdrCanvas.grid(row=1, column=1, sticky=(N, W, E))
        self.rowHdrCanvas.grid(row=2, column=0, sticky=(N, W, S))
        self.bodyCanvas.grid(row=2, column=1, sticky=(N, S, E, W))
        self.hdrVscrollbar.grid(row=1, column=2, sticky=(N, S))
        self.hdrHscrollbar.grid(row=3, column=0, sticky=(E, W))
        self.bodyVscrollbar.grid(row=2, column=2, sticky=(N, S))
        self.bodyHscrollbar.grid(row=3, column=1, sticky=(E, W))
        self.hdrVscrollbar.config(command=self.colHdrCanvas.yview)
        self.hdrHscrollbar.config(command=self.rowHdrCanvas.xview)
        self.bodyVscrollbar.config(command=self._vscroll_body)
        self.bodyHscrollbar.config(command=self._hscroll_body)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.colHdrCanvas.xview_moveto(0)
        self.colHdrCanvas.yview_moveto(0)
        self.rowHdrCanvas.xview_moveto(0)
        self.rowHdrCanvas.yview_moveto(0)
        self.bodyCanvas.xview_moveto(0)
        self.bodyCanvas.yview_moveto(0)
        self.colHdrInterior = Frame(self.colHdrCanvas)
        self.rowHdrInterior = Frame(self.rowHdrCanvas)
        self.bodyInterior = Frame(self.bodyCanvas)
        self.colHdrInterior_id = self.colHdrCanvas.create_window(0, 0, window=self.colHdrInterior, anchor=NW)
        self.rowHdrInterior_id = self.rowHdrCanvas.create_window(0, 0, window=self.rowHdrInterior, anchor=NW)
        self.bodyInterior_id = self.bodyCanvas.create_window(0, 0, window=self.bodyInterior, anchor=NW)
        self.colHdrInterior.bind('<Configure>', self._configure_colHdrInterior)
        self.rowHdrInterior.bind('<Configure>', self._configure_rowHdrInterior)
        self.bodyInterior.bind('<Configure>', self._configure_bodyInterior)
        self.colHdrCanvas.bind('<Configure>', self._configure_colHdrCanvas)
        self.rowHdrCanvas.bind('<Configure>', self._configure_rowHdrCanvas)
        self.bodyCanvas.bind('<Configure>', self._configure_bodyCanvas)

    def _vscroll_body(self, *args):
        self.rowHdrCanvas.yview(*args)
        self.bodyCanvas.yview(*args)

    def _hscroll_body(self, *args):
        self.colHdrCanvas.xview(*args)
        self.bodyCanvas.xview(*args)

    def _mousewheel(self, event):
        self.rowHdrCanvas.yview('scroll', event.delta, 'units')
        self.bodyCanvas.yview('scroll', event.delta, 'units')
        return 'break'

    def clearGrid(self):
        self.colHdrCanvas.xview_moveto(0)
        self.colHdrCanvas.yview_moveto(0)
        self.rowHdrCanvas.xview_moveto(0)
        self.rowHdrCanvas.yview_moveto(0)
        self.bodyCanvas.xview_moveto(0)
        self.bodyCanvas.yview_moveto(0)
        for grid in (self.tblHdrInterior, self.colHdrInterior, self.rowHdrInterior, self.bodyInterior):
            x, y = grid.size()
            for widget in grid.winfo_children():
                widget.destroy()

            if x > 1 and y > 1:
                for x in range(x):
                    grid.tk.call(('grid', 'columnconfigure', grid._w, x, '-minsize', 0))

                for y in range(y):
                    grid.tk.call(('grid', 'rowconfigure', grid._w, y, '-minsize', 0))

                grid.config(width=1, height=1)
                grid.master.config(width=1, height=1, scrollregion=(0, 0, 1, 1))

        self.update()
        self.colsConfigured = False

    def _configure_colHdrInterior(self, event):
        interiorW = self.colHdrInterior.winfo_reqwidth()
        interiorH = self.colHdrInterior.winfo_reqheight()
        raiseHeight = interiorH != self.colHdrCanvas.winfo_height()
        self.colHdrCanvas.config(height=interiorH, scrollregion=(0, 0, interiorW, interiorH))
        if raiseHeight:
            self.colHdrCanvas.config(height=interiorH + 1)

    def _configure_rowHdrInterior(self, event):
        interiorW = self.rowHdrInterior.winfo_reqwidth()
        interiorH = self.rowHdrInterior.winfo_reqheight()
        widenWidth = interiorW != self.rowHdrCanvas.winfo_width() and interiorW != 1
        self.rowHdrCanvas.config(width=interiorW, scrollregion=(0, 0, interiorW, interiorH))
        if widenWidth:
            self.rowHdrCanvas.config(width=interiorW + 1)

    def _configure_bodyInterior(self, event):
        interiorW = self.bodyInterior.winfo_reqwidth()
        interiorH = self.bodyInterior.winfo_reqheight()
        self.bodyCanvas.config(scrollregion=(0, 0, interiorW, interiorH))

    def _configure_colHdrCanvas(self, event):
        canvasH = self.colHdrCanvas.winfo_height()
        if self.colHdrInterior.winfo_reqheight() != canvasH:
            self.colHdrCanvas.itemconfigure(self.colHdrInterior_id, height=canvasH)

    def _configure_rowHdrCanvas(self, event):
        canvasW = self.rowHdrCanvas.winfo_width()
        if self.rowHdrInterior.winfo_reqwidth() != canvasW:
            self.rowHdrCanvas.itemconfigure(self.rowHdrInterior_id, width=canvasW)
        if hasattr(self.tblHdrInterior, 'tblHdrLabel') and canvasW > self.tblHdrInterior.tblHdrWraplength:
            self.tblHdrInterior.tblHdrWraplength = canvasW - 4
            self.tblHdrInterior.tblHdrLabel.config(wraplength=canvasW - 4)

    def _configure_bodyCanvas(self, event):
        pass

    def _configure_interiors(self, event):
        bodyW = self.bodyInterior.winfo_reqwidth()
        bodyH = self.bodyInterior.winfo_reqheight()
        colHdrW = self.colHdrInterior.winfo_reqwidth()
        colHdrH = self.colHdrInterior.winfo_reqheight()
        rowHdrW = self.rowHdrInterior.winfo_reqwidth()
        rowHdrH = self.rowHdrInterior.winfo_reqheight()
        bodyW = max(bodyW, colHdrW)
        bodyH = max(bodyH, rowHdrH)
        self.bodyCanvas.config(scrollregion=(0, 0, bodyW, bodyH))
        self.colHdrCanvas.config(scrollregion=(0, 0, bodyW, colHdrH))
        self.rowHdrCanvas.config(scrollregion=(0, 0, rowHdrW, bodyH))

    def _configure_canvases(self, event):
        canvasH = self.colHdrCanvas.winfo_height()
        if self.colHdrInterior.winfo_reqheight() != canvasH:
            self.colHdrCanvas.itemconfigure(self.colHdrInterior_id, height=canvasH)
        canvasW = self.rowHdrCanvas.winfo_width()
        if self.rowHdrInterior.winfo_reqwidth() != canvasW:
            self.rowHdrCanvas.itemconfigure(self.rowHdrInterior_id, width=canvasW)

    def _configure_cell(self, event):
        self.blockConfigureCell = True
        cell = event.widget
        x = cell.x
        y = cell.y
        cellW = cell.winfo_reqwidth()
        cellH = cell.winfo_reqheight()
        isColHdrCell = event.widget.master == self.colHdrInterior
        isRowHdrCell = event.widget.master == self.rowHdrInterior
        isBodyCell = event.widget.master == self.bodyInterior
        if isColHdrCell:
            if hasattr(cell, 'columnspan') and cell.columnspan:
                columnspan = cell.columnspan
            else:
                columnspan = 1
            cellspan = (columnspan + 1) // 2
            w = int((cellW - (columnspan - 1) / 2) / cellspan)
            wWiderAlloced = 0
            wNumWider = 0
            for X in range(x, x + columnspan, 2):
                bodyColW = self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, X, '-minsize'))
                if bodyColW > w:
                    wWiderAlloced += bodyColW
                    wNumWider += 1

            if cellspan - wNumWider > 0 and cellW > wWiderAlloced:
                W = int((cellW - wWiderAlloced) / (cellspan - wNumWider))
                for X in range(x, x + columnspan, 2):
                    bodyColW = self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, X, '-minsize'))
                    if W > bodyColW:
                        self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, X, '-minsize', W))

            if isRowHdrCell:
                rowspan = getattr(cell, 'rowspan', None) or 1
                bodyRowH = self.bodyInterior.tk.call(('grid', 'rowconfigure', self.bodyInterior._w, y, '-minsize'))
                cellHperRow = (cellH - rowspan // 2 * 3) / ((rowspan + 1) // 2)
                if cellHperRow > bodyRowH:
                    for ySpanned in range(y + rowspan - 1, y - 1, -2):
                        self.bodyInterior.tk.call(('grid', 'rowconfigure', self.bodyInterior._w, ySpanned, '-minsize', cellHperRow))

                if isBodyCell:
                    rowHdrH = self.rowHdrInterior.tk.call(('grid', 'rowconfigure', self.rowHdrInterior._w, y, '-minsize'))
                    if cellH > rowHdrH:
                        self.rowHdrInterior.tk.call(('grid', 'rowconfigure', self.rowHdrInterior._w, y, '-minsize', cellH))
                    colHdrW = self.colHdrInterior.tk.call(('grid', 'columnconfigure', self.colHdrInterior._w, x, '-minsize'))
                    if cellW > colHdrW:
                        self.colHdrInterior.tk.call(('grid', 'columnconfigure', self.colHdrInterior._w, x, '-minsize', cellW))
        elif colHdrW > cellW:
            self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, x, '-minsize', colHdrW))
        self.blockConfigureCell = False

    def conformHdrsToBody(self):
        self.colsConfigured = True
        hdrCells = self.colHdrInterior.children
        hdrCellSortKeys = []
        for hdrCellId, hdrCell in hdrCells.items():
            if not hdrCell.x & 1:
                colspan = hdrCell.columnspan if hasattr(hdrCell, 'columnspan') and hdrCell.columnspan else 1
                hdrCellSortKeys.append((colspan, hdrCell.x, -hdrCell.y, hdrCellId))

        hdrCellSortKeys.sort()
        for columnspan, x, y, hdrCellId in hdrCellSortKeys:
            hdrCell = hdrCells[hdrCellId]
            hdrCellW = hdrCell.winfo_reqwidth()
            w = int(hdrCellW / columnspan)
            wWiderAlloced = 0
            wNumWider = 0
            for X in range(x, x + columnspan * 2, 2):
                bodyColW = self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, X, '-minsize'))
                if bodyColW > w:
                    wWiderAlloced += bodyColW
                    wNumWider += 1

            if columnspan - wNumWider > 0 and hdrCellW > wWiderAlloced:
                W = int((hdrCellW - wWiderAlloced) / (columnspan - wNumWider))
                for X in range(x, x + columnspan * 2, 2):
                    bodyColW = self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, X, '-minsize'))
                    if W > bodyColW:
                        self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, X, '-minsize', W))

    def conformBodyCellsToHeader(self):
        self.bodyCellsConfigured = True
        for bodyCell in self.bodyInterior.children.values():
            if isinstance(bodyCell, gridSpacer):
                pass
            else:
                bodyCellW = bodyCell.winfo_reqwidth()
                bodyCellH = bodyCell.winfo_reqheight()
                x = bodyCell.x
                hdrColW = self.colHdrInterior.tk.call(('grid', 'columnconfigure', self.colHdrInterior._w, x, '-minsize'))
                if bodyCellW < hdrColW:
                    self.bodyInterior.tk.call(('grid', 'columnconfigure', self.bodyInterior._w, x, '-minsize', hdrColW))
                y = bodyCell.y
                rowColH = self.colHdrInterior.tk.call(('grid', 'rowconfigure', self.rowHdrInterior._w, y, '-minsize'))
                if bodyCellH < rowColH:
                    self.bodyInterior.tk.call(('grid', 'rowconfigure', self.bodyInterior._w, y, '-minsize', rowColH))