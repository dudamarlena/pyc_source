# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ramusus/workspace/manufacture/env/src/django-odnoklassniki-photos/odnoklassniki_photos/factories.py
# Compiled at: 2015-01-25 03:14:07
import factory
from datetime import datetime
from odnoklassniki_groups.factories import GroupFactory
from .models import Photo, Album

class AlbumFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Album
    id = factory.Sequence(lambda n: n)
    created = datetime.now()
    owner = factory.SubFactory(GroupFactory)


class PhotoFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Photo
    id = factory.Sequence(lambda n: n)
    created = datetime.now()
    last_like_date = datetime.now()
    owner = factory.SubFactory(GroupFactory)
    album = factory.SubFactory(AlbumFactory)