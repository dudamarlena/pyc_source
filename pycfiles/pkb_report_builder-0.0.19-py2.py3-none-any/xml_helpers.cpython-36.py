# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Projects\Github\PKBReportBuilder\PKBReportBuilder\modules\xml_parser\xml_helpers.py
# Compiled at: 2019-01-15 04:55:18
# Size of source mod 2**32: 288 bytes
import xml.etree.ElementTree as ET

def find_block(current_block, element_name):
    try:
        results = []
        for result in current_block.findall(element_name):
            results.append(result)

        return results
    except Exception as e:
        pass