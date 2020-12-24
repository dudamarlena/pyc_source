# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/py3o/fusion/static/examples/odt2pdf.py
# Compiled at: 2015-06-02 10:25:30
import requests
url = 'http://localhost:8765/form'
files = {'tmpl_file': open('templates/simple.odt', 'rb')}
fields = {'targetformat': 'pdf', 
   'datadict': '{}', 
   'image_mapping': '{}'}
r = requests.post(url, data=fields, files=files)
files['tmpl_file'].close()
if r.status_code == 400:
    print r.json()
else:
    chunk_size = 1024
    outname = 'request_out.pdf'
    with open(outname, 'wb') as (fd):
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)

    print 'Your file: %s is ready' % outname