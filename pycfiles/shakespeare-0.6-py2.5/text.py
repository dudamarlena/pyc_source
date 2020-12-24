# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/controllers/text.py
# Compiled at: 2008-10-29 17:02:16
import logging, genshi
from shakespeare.lib.base import *
import shakespeare, shakespeare.index, shakespeare.format, shakespeare.model as model
log = logging.getLogger(__name__)

class TextController(BaseController):

    def index(self):
        c.works_index = shakespeare.index.all
        return render('text/index')

    def view(self):
        name = request.params.get('name', '')
        format = request.params.get('format', 'plain')
        if format == 'annotate':
            return self.view_annotate(name)
        namelist = name.split()
        numtexts = len(namelist)
        textlist = [ model.Material.byName(tname) for tname in namelist ]
        if format == 'raw':
            result = textlist[0].get_text().read()
            status = '200 OK'
            response.headers['Content-Type'] = 'text/plain'
            return result
        texts = []
        for item in textlist:
            tfileobj = item.get_text()
            ttext = shakespeare.format.format_text(tfileobj, format)
            thtml = genshi.HTML(ttext)
            texts.append(thtml)

        c.frame_width = 100.0 / numtexts - 4.0
        c.texts = texts
        return render('text/view', strip_whitespace=False)