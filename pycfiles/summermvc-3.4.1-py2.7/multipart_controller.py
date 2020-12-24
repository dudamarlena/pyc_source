# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/summermvc/templates/project_demo/src/controller/multipart_controller.py
# Compiled at: 2018-05-30 09:33:07
from summermvc.decorator import *
from summermvc.mvc import *

@rest_controller
class MultipartController(object):

    @request_mapping('/upload', method=RequestMethod.GET, produce='text/html')
    def upload_files_get(self):
        html = ('\n            <html>\n                <head>\n                    <title>multipart test</title>\n                </head>\n\n                <body>\n                    <form action="/upload" enctype="multipart/form-data" method="post">\n                        <input type="file" name="upload_file_1" /><br />\n                        <input type="file" name="upload_file_2" /><br />\n                        <input type="submit" value="submit" /><br />\n                    </form>\n                <body>\n            </html>\n            ').strip()
        yield html

    @request_mapping('/upload', method=RequestMethod.POST)
    def upload_files_post(self, model, request, request_body):
        upload_files = MultipartParser(request_body, request.content_type_attributes['boundary'])
        print upload_files.files
        model.add_attribute('success', True)
        return 'json'