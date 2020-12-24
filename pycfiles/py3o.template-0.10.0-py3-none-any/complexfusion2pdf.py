# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/static/examples/complexfusion2pdf.py
# Compiled at: 2015-06-26 11:45:58
import requests, json
url = 'http://localhost:8765/form'
targetformats = [
 'odt', 'pdf', 'doc', 'docx']

class MyEncoder1(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Item):
            obj = obj._asdict()
        else:
            obj = super(MyEncoder1, self).default(obj)
        return obj


class Item(object):

    def _asdict(self):
        return self.__dict__


items = list()
item1 = Item()
item1.val1 = 'Item1 Value1'
item1.val2 = 'Item1 Value2'
item1.val3 = 'Item1 Value3'
item1.Currency = 'EUR'
item1.Amount = '12345.35'
item1.InvoiceRef = '#1234'
items.append(item1)
for i in xrange(1000):
    item = Item()
    item.val1 = 'Item%s Value1' % i
    item.val2 = 'Item%s Value2' % i
    item.val3 = 'Item%s Value3' % i
    item.Currency = 'EUR'
    item.Amount = '6666.77'
    item.InvoiceRef = 'Reference #%04d' % i
    items.append(item)

document = Item()
document.total = '9999999999999.999'
data = dict(items=items, document=document)
data_s = json.dumps(data, cls=MyEncoder1)
for targetformat in targetformats:
    files = {'tmpl_file': open('templates/py3o_example_template.odt', 'rb'), 
       'staticimage.img_logo': open('images/new_logo.png', 'rb')}
    fields = {'targetformat': targetformat, 
       'datadict': data_s, 
       'image_mapping': json.dumps({'staticimage.img_logo': 'logo'})}
    r = requests.post(url, data=fields, files=files)
    if r.status_code == 400:
        print r.json()
    else:
        chunk_size = 1024
        ext = targetformat.lower()
        with open('request_out.%s' % ext, 'wb') as (fd):
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)

    files['tmpl_file'].close()
    files['staticimage.img_logo'].close()