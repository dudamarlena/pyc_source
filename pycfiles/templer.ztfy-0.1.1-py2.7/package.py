# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/templer/ztfy/package.py
# Compiled at: 2012-06-16 04:45:23
from templer.core import BasicNamespace

class ZTFYPackage(BasicNamespace):
    _template_dir = 'templates/ztfy_package'
    summary = 'A basic ZTFY project with a namespace package'
    help = 'This creates a basic ZTFY package'
    category = 'ZTFY'
    required_templates = []
    default_required_structures = []
    use_cheetah = True