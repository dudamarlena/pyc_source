# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dauptain/GITLAB/opentea/opentea/gui_forms/xor_widget.py
# Compiled at: 2019-02-03 15:40:26
# Size of source mod 2**32: 4221 bytes
"""Module for XOR widget"""
from tkinter import Menu as Tk_Menu
from tkinter import ttk
from opentea.gui_forms.constants import WIDTH_UNIT, GetException, SetException

class OTXorWidget:
    __doc__ = 'OT  Or-exclusive / oneOf widget.'

    def __init__(self, schema, root_frame, n_width=1):
        """Startup class.

        Inputs :
        --------
        schema : a schema as a nested object
        root_frame :  a Tk object were the widget will be grafted
        n_width : float
             relative size of the widget
        """
        self.tree = dict()
        self.current_child = None
        self._schema = schema
        title = self._schema['name']
        if 'title' in self._schema:
            title = self._schema['title']
        self._holder = ttk.LabelFrame(root_frame, text=title,
          name=(self._schema['name']),
          relief='sunken',
          width=(n_width * WIDTH_UNIT))
        self._forceps = ttk.Frame((self._holder), width=(n_width * WIDTH_UNIT),
          height=1)
        self._Menu_bt = ttk.Menubutton((self._holder), text='None')
        self._xor_holder = ttk.Frame(self._holder)
        self._holder.pack(side='top', fill='x', padx=2,
          pady=2,
          expand=False)
        self._forceps.pack(side='top')
        self._Menu_bt.pack(side='top')
        self._xor_holder.pack(side='top', fill='x', padx=2,
          pady=2,
          expand=False)
        self._Menu_bt.menu = Tk_Menu((self._Menu_bt), tearoff=False)
        self._Menu_bt['menu'] = self._Menu_bt.menu
        for oneof_item in self._schema['oneOf']:
            nam = oneof_item['required'][0]
            ch_s = oneof_item['properties'][nam]
            title = nam
            if 'title' in ch_s:
                title = ch_s['title']
            self._Menu_bt.menu.add_command(label=title,
              command=(lambda nam=nam: self._XorCallbck(nam)))

        self._XorCallbck(self._schema['default'])

    def _XorCallbck(self, name_child, data_in=None):
        """Reconfigure XOR button.

        Inputs :
        --------
        name_child : sting, naming the child object
        data_in : dictionary used to pre-fill the data
        """
        self.current_child = name_child
        child_schema = None
        for possible_childs in self._schema['oneOf']:
            if possible_childs['required'][0] == name_child:
                child_schema = possible_childs['properties'][name_child]

        for child_widget in self._xor_holder.winfo_children():
            child_widget.destroy()

        self.tree = dict()
        self.tree[name_child] = OTContainerWidget(child_schema, self._xor_holder)
        if data_in is None:
            self.tree[name_child].set(dict())
        else:
            self.tree[name_child].set(data_in)
        title = name_child
        if 'title' in child_schema:
            title = child_schema['title']
        self._Menu_bt.configure(text=title)

    def get(self):
        """Get the data of children widgets.

        Returns :
        ---------
        a dictionnary with the get result of current children
        """
        out = dict()
        try:
            found = self.tree[self.current_child].get()
            if found is not None:
                out[self.current_child] = found
        except GetException:
            pass

        if out == {}:
            out = None
        return out

    def set(self, dict_):
        """Get the data of children widgets.

        Input :
        -------
        a dictionnary with the value of the childrens
        """
        given_keys = dict_.keys()
        if len(given_keys) > 1:
            raise SetException('Multiple matching option, skipping...')
        for child in self._schema['oneOf']:
            if child in dict_:
                try:
                    self._XorCallbck(child, dict_[child])
                except SetException:
                    pass