# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/ramjet/app.py
# Compiled at: 2017-11-07 02:38:41
# Size of source mod 2**32: 749 bytes
"""
Ramjet
"""
import logging, hashlib, jinja2
from aiohttp import web
import aiohttp_jinja2
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from aiohttp_session import setup
from ramjet.settings import LOG_NAME, SECRET_KEY
from ramjet.utils import logger

class PageNotFound(web.View):

    async def get(self):
        return web.Response(status=404, text='404: not found!😢')


def setup_web_handlers(app):
    key = hashlib.md5(SECRET_KEY.encode('utf8')).hexdigest().encode('utf8')
    setup(app, EncryptedCookieStorage(key))
    app.router.add_route('*', '/404.html', PageNotFound)


def setup_templates(app):
    aiohttp_jinja2.setup(app, loader=(jinja2.FileSystemLoader('./tasks')))