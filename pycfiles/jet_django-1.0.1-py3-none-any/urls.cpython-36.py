# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_django/jet_django/urls.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 1426 bytes
from django.conf.urls import url
from jet_bridge_base.views.api import ApiView
from jet_bridge_base.views.file_upload import FileUploadView
from jet_bridge_base.views.image_resize import ImageResizeView
from jet_bridge_base.views.message import MessageView
from jet_bridge_base.views.model import ModelViewSet
from jet_bridge_base.views.model_description import ModelDescriptionView
from jet_bridge_base.views.register import RegisterView
from jet_bridge_base.views.sql import SqlView
from jet_django.route_view import route_view
from jet_django.router import Router
app_name = 'jet_django'

def init_urls():
    router = Router()
    router.register('models/(?P<model>[^/]+)/', route_view(ModelViewSet))
    extra_urls = [
     url('^$', (route_view(ApiView).as_view()), name='root'),
     url('^register/', (route_view(RegisterView).as_view()), name='register'),
     url('^model_descriptions/', (route_view(ModelDescriptionView).as_view()), name='model-descriptions'),
     url('^sql/', (route_view(SqlView).as_view()), name='sql'),
     url('^messages/', (route_view(MessageView).as_view()), name='message'),
     url('^file_upload/', (route_view(FileUploadView).as_view()), name='file-upload'),
     url('^image_resize/', (route_view(ImageResizeView).as_view()), name='image-resize')]
    api_urls = router.urls + extra_urls
    return api_urls


jet_urls = init_urls()
urlpatterns = jet_urls