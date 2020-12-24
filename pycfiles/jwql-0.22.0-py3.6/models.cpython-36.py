# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/website/apps/jwql/models.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 2324 bytes
"""Defines the models for the ``jwql`` app.

** CURRENTLY NOT IN USE **

In Django, "a model is the single, definitive source of information
about your data. It contains the essential fields and behaviors of the
data you’re storing. Generally, each model maps to a single database
table" (from Django documentation). Each model contains fields, such
as character fields or date/time fields, that function like columns in
a data table. This module defines models that might be used to store
data related to the JWQL webpage. Interacts with the database located
at jwql/website/db.sqlite3.

Authors
-------
    - Lauren Chambers

Use
---
    This module is used as such:

    ::
        from models import MyModel
        data = MyModel.objects.filter(name="JWQL")

References
----------
    For more information please see:
        ```https://docs.djangoproject.com/en/2.0/topics/db/models/```
"""
import os
from django.db import models
INSTRUMENT_LIST = (('FGS', 'FGS'), ('MIRI', 'MIRI'), ('NIRCam', 'NIRCam'), ('NIRISS', 'NIRISS'),
                   ('NIRSpec', 'NIRSpec'))

class BaseModel(models.Model):
    __doc__ = 'A base model that other classes will inherit. Created to avoid\n    an obscure error about a missing ``app_label``.\n    '

    class Meta:
        abstract = True
        app_label = 'jwql'


class ImageData(BaseModel):
    __doc__ = 'A model that collects image filepaths, instrument labels, and\n    publishing date/time. Just an example used for learning django.\n\n    Attributes\n    ----------\n    filepath : FilePathField object\n        The full filepath of the datum\n    inst : CharField object\n        Name of the corresponding JWST instrument\n    pub_date : FilePathField object\n        Date and time when datum was added to the database.\n    '
    inst = models.CharField('instrument', max_length=6, choices=INSTRUMENT_LIST, default=None)
    pub_date = models.DateTimeField('date published')
    filepath = models.FilePathField(path='/user/lchambers/jwql/')

    def filename(self):
        return os.path.basename(self.filepath)

    def __str__(self):
        return self.filename()

    class Meta:
        verbose_name_plural = 'image data'
        db_table = 'imagedata'