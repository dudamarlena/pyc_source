# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jeremyr/dev/perso/champollion/test/unit/conftest.py
# Compiled at: 2017-06-03 15:44:19
import os, shutil, tempfile, pytest

@pytest.fixture()
def temporary_directory(request):
    """Return a temporary directory path."""
    path = tempfile.mkdtemp()

    def cleanup():
        """Remove temporary directory."""
        shutil.rmtree(path)

    request.addfinalizer(cleanup)
    return path


@pytest.fixture()
def doc_folder(temporary_directory):
    path = os.path.join(temporary_directory, 'doc')
    os.makedirs(path)
    js_source = os.path.join(temporary_directory, 'doc', 'example')
    os.makedirs(js_source)
    conf_file = os.path.join(path, 'conf.py')
    with open(conf_file, 'w') as (f):
        f.write("# :coding: utf-8\nextensions=['champollion']\nsource_suffix = '.rst'\nmaster_doc = 'index'\nauthor = u'Jeremy Retailleau'\nexclude_patterns = ['Thumbs.db', '.DS_Store']\njs_source='./example'")
    return path