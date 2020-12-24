# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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