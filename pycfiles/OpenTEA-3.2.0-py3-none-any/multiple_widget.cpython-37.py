# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/opentea/gui_forms/multiple_widget.py
# Compiled at: 2019-02-03 15:24:03
# Size of source mod 2**32: 5615 bytes
"""Module for Multiple widget"""
from tkinter import ttk
from opentea.gui_forms.constants import WIDTH_UNIT, GetException
from opentea.gui_forms.node_widgets import OTContainerWidget

class OTMultipleWidget:
    __doc__ = 'OT multiple widget.'

    def __init__(self, schema, root_frame):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        n_width : float
             relative size of the widget
        """
        self.tree = list()
        self.item_schema = schema['items']
        title = ''
        if 'title' in schema:
            title = schema['title']
        holder = ttk.LabelFrame(root_frame, text=title,
          name=(schema['name']),
          relief='sunken',
          width=(2 * WIDTH_UNIT))
        holder.pack(side='top', fill='x', padx=2, pady=2, expand=False)
        forceps = ttk.Frame(holder, width=(2 * WIDTH_UNIT), height=1)
        self.tv = ttk.Treeview(holder, selectmode='browse',
          height=15)
        scroll_vert = ttk.Scrollbar(holder, orient='vertical',
          command=(self.tv.yview))
        self.tv.configure(yscrollcommand=(scroll_vert.set))
        self.switchform = SwitchForm(holder, width=WIDTH_UNIT,
          name='tab_holder')
        forceps.grid(column=0, row=1, columnspan=3)
        scroll_vert.grid(column=1, row=1, sticky='news')
        self.tv.grid(column=0, row=1, sticky='news')
        self.switchform.grid(column=2, row=1, rowspan=2, sticky='news')
        self.switchform.grid_propagate(0)
        item_props = self.item_schema['properties']
        self.tv['columns'] = tuple(item_props.keys())
        col_width = int(WIDTH_UNIT / (len(self.tv['columns']) + 1))
        self.tv.column('#0', width=col_width)
        for key in item_props:
            title = key
            if 'title' in item_props[key]:
                title = item_props[key]['title']
            self.tv.column(key, width=col_width)
            self.tv.heading(key, text=title)

        dummy = []
        for i in range(2):
            lbl = 'line_' + str(i)
            dummy.append({'name': lbl})

        self.set(dummy)

        def tv_simple_click(event):
            row = self.tv.identify_row(event.y)
            self.switchform.sf_raise(row)

        self.tv.bind('<Button-1>', tv_simple_click)

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of childrens
        """
        out = list()
        for child in self.tree:
            try:
                found = child.get()
                if found is not None:
                    out.append(found)
            except GetException:
                pass

        if not out:
            out = None
        return out

    def set(self, list_):
        """Get the data of children widgets.

        Input :
        -------
        a list with the value of the childrens"""
        ingoing_childs = [item['name'] for item in list_]
        remaining_childs = ingoing_childs.copy()
        itemids_to_delete = []
        for item_id in self.tree:
            item_name = self.tree[item_id]['name']
            if item_name not in ingoing_childs:
                itemids_to_delete.append(item_id)
            else:
                data_in = list_[ingoing_childs.index(item_name)]
                self.tree[item_id].set(data_in)
                remaining_childs.remove(item_name)

        for item_id in itemids_to_delete:
            del self.tree[item_id]

        for item_name in remaining_childs:
            data_in = list_[ingoing_childs.index(item_name)]
            self.tree.insert(-1, OTMultipleItem(self, item_name))
            self.tree[(-1)].set(data_in)

    def _reorder_items(self, ingoing_childs):
        """Reorder the items upon a list.

        Must chanque the order in self.tree,
        and show it on the self.tv"""
        pass


class OTMultipleItem(OTContainerWidget):
    __doc__ = 'OT  multiple widget'

    def __init__(self, mutiple, name):
        self.tab = mutiple.switchform.add(name, title=name)
        super().__init__(mutiple.item_schema, self.tab)
        mutiple.tv.insert('', 'end',
          iid=name,
          text=name)


class SwitchForm(ttk.Frame):
    __doc__ = 'Overriden Frame class to mimick notebooks woithout tabs.'

    def add(self, name, title=None):
        """Add a tab-like Frame."""
        tab_id = ttk.LabelFrame(self, name=name, text=title, relief='sunken')
        tab_id.shortname = name
        self.sf_raise(tab_id)
        return tab_id

    def sf_del(self, tab_id):
        """Destroy tab_id tab."""
        tab_id.destroy()

    def sf_raise(self, tab_name):
        """Forget current view and repack tab_name tab."""
        for child_widget in self.winfo_children():
            if child_widget.shortname == tab_name:
                child_widget.pack(fill='both')
            else:
                child_widget.pack_forget()