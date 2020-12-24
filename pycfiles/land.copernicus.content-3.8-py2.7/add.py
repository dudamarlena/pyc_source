# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/land/copernicus/content/content/add.py
# Compiled at: 2017-09-19 09:07:49
from Products.Archetypes.interfaces import IObjectInitializedEvent
from pdftransformer import PDFTransformer

def fileHandler(obj):
    """Set the cover for the IATFile object
    """
    request = obj.REQUEST
    if obj.getContentType() != 'application/pdf':
        return
    cover_requested = obj.getField('auto_cover').getAccessor(obj)()
    if not cover_requested:
        return
    field = obj.getField('image')
    if field:
        pdfimageblob = field.getAccessor(obj)()
        if request.get('file_delete', 'nochange') == 'nochange' and pdfimageblob:
            return
    filedata = obj.getFile()
    with PDFTransformer(pdf=filedata.data, work_directory='/tmp') as (pdfTrans):
        with open(pdfTrans.generated_files[0], 'rb') as (cover):
            cover_blob = cover.read()
            field = obj.getField('image')
            field.getMutator(obj)(cover_blob)


def handler(obj, evt):
    if not IObjectInitializedEvent.providedBy(evt):
        return
    fileHandler(obj)