# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notework/youzan/pdf2html.py
# Compiled at: 2019-11-27 01:29:05
# Size of source mod 2**32: 1399 bytes
from notetool.html.pyhtml import html, body, img, table, li, a, td, tr

class pd2html:

    def __init__(self, data):
        self.data = data
        self.columns = data.columns.values
        self.data_dict = data.to_dict(orient='records')
        self.pass_words = [
         'url']

    def get_title(self):
        tds = []
        for col in self.columns:
            if col in self.pass_words:
                continue
            tds.append(td(col))

        return tr(tds)

    def get_td(self, col, data_dict: dict):
        data = data_dict[col]
        if col in self.pass_words:
            return
        if col == 'id':
            url = data_dict['url']
            res = td(li(a(href=url, target='_blank')(data)))
        else:
            if 'img' in col or 'image' in col:
                res = td(img(src=(data + '?w=250&h=250&cp=1')))
            else:
                res = td(data)
        return res

    def get_tr(self, data: dict):
        l1 = len(self.columns)
        tds = []
        for i in range(0, l1):
            temp_td = self.get_td(self.columns[i], data)
            if temp_td is not None:
                tds.append(temp_td)

        return tr(tds)

    def html(self):
        trs = [
         self.get_title()]
        for d in self.data_dict:
            trs.append(self.get_tr(d))

        return html(body(table(trs)))

    def html_str(self):
        return self.html().render(user='Cenk')