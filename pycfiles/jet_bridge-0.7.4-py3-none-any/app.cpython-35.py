# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge/jet_bridge/app.py
# Compiled at: 2020-03-04 22:15:05
# Size of source mod 2**32: 2106 bytes
import os, tornado.ioloop, tornado.web
from jet_bridge.handlers.temporary_redirect import TemporaryRedirectHandler
from jet_bridge_base import settings as base_settings
from jet_bridge_base.views.api import ApiView
from jet_bridge_base.views.image_resize import ImageResizeView
from jet_bridge_base.views.file_upload import FileUploadView
from jet_bridge_base.views.message import MessageView
from jet_bridge_base.views.model import ModelViewSet
from jet_bridge_base.views.model_description import ModelDescriptionView
from jet_bridge_base.views.register import RegisterView
from jet_bridge_base.views.reload import ReloadView
from jet_bridge_base.views.sql import SqlView
from jet_bridge import settings, media
from jet_bridge.handlers.view import view_handler
from jet_bridge.handlers.not_found import NotFoundHandler
from jet_bridge.router import Router

def make_app():
    router = Router()
    router.register('/api/models/(?P<model>[^/]+)/', view_handler(ModelViewSet))
    urls = [
     (
      '/', TemporaryRedirectHandler, {'url': '/api/'}),
     (
      '/register/', view_handler(RegisterView)),
     (
      '/api/', view_handler(ApiView)),
     (
      '/api/register/', view_handler(RegisterView)),
     (
      '/api/model_descriptions/', view_handler(ModelDescriptionView)),
     (
      '/api/sql/', view_handler(SqlView)),
     (
      '/api/messages/', view_handler(MessageView)),
     (
      '/api/file_upload/', view_handler(FileUploadView)),
     (
      '/api/image_resize/', view_handler(ImageResizeView)),
     (
      '/api/reload/', view_handler(ReloadView)),
     (
      '/media/(.*)', tornado.web.StaticFileHandler, {'path': settings.MEDIA_ROOT})]
    urls += router.urls
    if settings.MEDIA_STORAGE == media.MEDIA_STORAGE_FILE:
        urls.append(('/media/(.*)', tornado.web.StaticFileHandler, {'path': settings.MEDIA_ROOT}))
    return tornado.web.Application(handlers=urls, debug=settings.DEBUG, default_handler_class=NotFoundHandler, template_path=os.path.join(base_settings.BASE_DIR, 'templates'), autoreload=settings.DEBUG)