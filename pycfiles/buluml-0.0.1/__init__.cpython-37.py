# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/bulrush/__init__.py
# Compiled at: 2019-06-14 12:05:42
# Size of source mod 2**32: 695 bytes
from pathlib import Path
from .image_extractor import extract_images
from .license_generator import generate_license
from .schema_generator import generate_jsonld_schema
__all__ = [
 'ENVIRONMENT', 'FILTERS', 'PATH']
ENVIRONMENT = {'extensions': ['webassets.ext.jinja2.AssetsExtension', 'jinja2.ext.with_']}
FILTERS = dict(images=extract_images,
  license=generate_license,
  schema=generate_jsonld_schema)
PATH = str(Path(__file__).parent)