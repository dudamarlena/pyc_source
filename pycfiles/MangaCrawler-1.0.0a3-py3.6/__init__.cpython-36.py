# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/MangaCrawler/__init__.py
# Compiled at: 2017-04-24 15:13:47
# Size of source mod 2**32: 330 bytes
from .MAL import MAL
from .Manga import Manga
from .MangaCrawler import MangaCrawler
from .MangaFox import MangaFox
from .MangaSite import MangaSite
from .Settings import Settings
from .XML import XML

def main():
    settings = Settings()
    settings.from_sys_parameters()
    crawler = MangaCrawler()
    crawler.run(settings)