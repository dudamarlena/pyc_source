# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/test/test_scan.py
# Compiled at: 2018-12-16 17:32:26
# Size of source mod 2**32: 880 bytes
import shutil
from ipecac.tools import extract, scan
from test import utils

def test_detect_expected_files():
    sandbox = utils.generate_files()
    base = sandbox['base']
    expected = ['incidents/controller.py', 'hotdogs/doc.py', 'users/fake.py']
    actual = scan.detect_comments(f"{base}/")
    for item in actual:
        if not expected[0] in item:
            assert expected[1] in item
            assert expected[2] not in item

    shutil.rmtree(base)


def test_find_and_parse():
    sandbox = utils.generate_files()
    base = sandbox['base']
    files = [
     f"{base}/incidents/controller.py",
     f"{base}/hotdogs/doc.py"]
    controller = open(files[0]).read()
    doc = open(files[1]).read()
    expected = [extract.parse_block(doc), extract.parse_block(controller)]
    actual = scan.find_and_parse(f"{base}/")
    assert expected == actual
    shutil.rmtree(base)