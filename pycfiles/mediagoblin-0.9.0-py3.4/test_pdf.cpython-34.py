# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_pdf.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 1809 bytes
import collections, tempfile, shutil, os, pytest
from mediagoblin.media_types.pdf.processing import pdf_info, check_prerequisites, create_pdf_thumb
from .resources import GOOD_PDF

@pytest.mark.skipif('not os.path.exists(GOOD_PDF) or not check_prerequisites()')
def test_pdf():
    expected_dict = {'pdf_author': -1,  'pdf_creator': -1, 
     'pdf_keywords': -1, 
     'pdf_page_size_height': -1, 
     'pdf_page_size_width': -1, 
     'pdf_pages': -1, 
     'pdf_producer': -1, 
     'pdf_title': -1, 
     'pdf_version_major': 1, 
     'pdf_version_minor': -1}
    good_info = pdf_info(GOOD_PDF)
    for k, v in expected_dict.items():
        assert k in good_info
        if not v == -1:
            if not v == good_info[k]:
                raise AssertionError

    temp_dir = tempfile.mkdtemp()
    create_pdf_thumb(GOOD_PDF, os.path.join(temp_dir, 'good_256_256.png'), 256, 256)
    shutil.rmtree(temp_dir)