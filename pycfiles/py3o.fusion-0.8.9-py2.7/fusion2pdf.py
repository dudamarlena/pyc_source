# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/static/examples/fusion2pdf.py
# Compiled at: 2015-06-26 11:45:07
import requests, json
url = 'http://localhost:8765/form'
targetformats = [
 'pdf']

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


document = Item()
document.person_name = 'Aide'
document.person_surname = 'Florent'
document.person_company = 'XCG Consulting'
document.person_url = 'http://www.xcg-consulting.fr'
data = {'document': document}
data_s = json.dumps(data, cls=MyEncoder1)
for targetformat in targetformats:
    files = {'tmpl_file': open('templates/fusion2pdf.odt', 'rb')}
    fields = {'targetformat': targetformat, 
       'datadict': data_s, 
       'image_mapping': '{}'}
    r = requests.post(url, data=fields, files=files)
    files['tmpl_file'].close()
    if r.status_code == 400:
        print r.json()
    else:
        chunk_size = 1024
        ext = targetformat.lower()
        with open('fusion2pdf.%s' % ext, 'wb') as (fd):
            for chunk in r.iter_content(chunk_size):
                fd.write(chunk)