# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/shakespeare/controllers/site.py
# Compiled at: 2008-10-29 17:02:15
import logging, genshi
from shakespeare.lib.base import *
import shakespeare, shakespeare.index, shakespeare.format, shakespeare.model as model
log = logging.getLogger(__name__)

class SiteController(BaseController):

    def index(self):
        c.works_index = shakespeare.index.all
        return render('index')

    def guide(self):
        return render('guide')

    def marginalia(self):
        prefix = '/' + h.url_for('marginalia')
        media_app = annotater.marginalia.MarginaliaMedia(prefix)
        out = media_app(request.environ, self.start_response)
        return out

    def annotation(self):
        store = annotater.store.AnnotaterStore()
        return store(request.environ, self.start_response)

    def view_annotate(self):
        name = request.params.get('name')
        textobj = model.Material.byName(name)
        tfileobj = textobj.get_text()
        formatter = shakespeare.format.TextFormatterAnnotate()
        annotation_store_fqdn = wsgiref.util.application_uri(request.environ)
        page_url = wsgiref.util.request_uri(request.environ)
        ttext = formatter.format(tfileobj, page_uri=page_url)
        thtml = genshi.HTML(ttext)
        prefix = cfg.get('annotater', 'marginalia_prefix')
        marginalia_media = annotater.marginalia.get_media_header(prefix, annotation_store_fqdn, page_url)
        buttons = annotater.marginalia.get_buttons(page_url)
        marginalia_media = genshi.HTML(marginalia_media)
        buttons = genshi.HTML(buttons)
        c.text_with_annotation = thtml
        c.marginalia_media = marginalia_media
        c.annotation_buttons = buttons
        return render('view_annotate', strip_whitespace=False)