# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gallery/admin_forms.py
# Compiled at: 2016-03-08 06:27:04
import os, zipfile
from StringIO import StringIO
from tempfile import mkdtemp
from django import forms
from django.core.files import File
from gallery.models import GalleryImage
from gallery.fields import FileMultiField

class BulkImageUploadForm(forms.Form):
    files_label = 'Your browser may allow you to select multiple files at\nonce. Try holding down the CTRL key when you select files.'
    files = FileMultiField(max_size=1000000, help_text=files_label, required=False)

    def __init__(self, *args, **kwargs):
        self.gallery = kwargs.pop('gallery')
        super(BulkImageUploadForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        images = []
        if self.cleaned_data['files']:
            for item in self.cleaned_data['files']:
                item.seek(0)
                to_add = []
                itemfp = StringIO(item.read())
                item.seek(0)
                try:
                    zfp = zipfile.ZipFile(itemfp, 'r')
                except:
                    to_add.append(item)

                if not zfp.testzip():
                    tmpdir = mkdtemp()
                    for filename in sorted(zfp.namelist()):
                        tmpfile = os.path.join(tmpdir, filename)
                        data = zfp.read(filename)
                        fp = open(tmpfile, 'wb')
                        fp.write(data)
                        fp.close()
                        afile = File(open(tmpfile), 'rb')
                        afile.name = filename
                        to_add.append(afile)

                else:
                    to_add.append(item)
                for afile in to_add:
                    obj = GalleryImage(title=afile.name, gallery=self.gallery)
                    obj.image = afile
                    obj.save()
                    obj.sites = list(self.gallery.sites.all())
                    obj.save()
                    images.append(obj)

        return images