# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tomas/git/euroix/django-cms-qe/cms_qe/staticfiles.py
# Compiled at: 2019-02-04 04:18:45
# Size of source mod 2**32: 1363 bytes
from django.contrib.staticfiles.storage import ManifestStaticFilesStorage as DjangoManifestStaticFilesStorage

class ManifestStaticFilesStorage(DjangoManifestStaticFilesStorage):
    __doc__ = "\n    Custom handle of ``django.contrib.staticfiles.storage.ManifestStaticFilesStorage``\n    to create different URLs for every version of static file. Means when you change\n    static file, Django's ``collectstatic`` detects that and creates ``staticfiles.json``\n    with all hashes and adds them to URLs when tag ``static`` is used.\n\n    It's good to use this when you don't want to have problems with caches--when you\n    change static but cache still serves the old one with new generated HTML. Thanks\n    to this storage you can be sure that every client will use new resources needed\n    by new page.\n\n    This custom version takes care of compatiblity of Django CMS which brings custom\n    static tag to add owns version and then Django's storage has problem to cooperate\n    with it. In Django 1.10 it has to override ``stored_name`` to ignore this problem\n    and in Django 1.11 is brought new attribute ``manifest_strict`` which has to be\n    set to ``False`` to work as in Django 1.10.\n    "
    manifest_strict = False

    def stored_name(self, name):
        try:
            return super().stored_name(name)
        except ValueError:
            return name