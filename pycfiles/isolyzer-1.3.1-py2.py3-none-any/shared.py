# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/johan/isolyzer/isolyzer/shared.py
# Compiled at: 2018-01-25 09:32:36
"""Shared functions"""
import xml.etree.ElementTree as ET

def addProperty(element, tag, text):
    """Append childnode with text"""
    el = ET.SubElement(element, tag)
    el.text = text