# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mansmagnusson/Projects/genmod/genmod/annotations/__init__.py
# Compiled at: 2017-02-05 15:24:29
# Size of source mod 2**32: 288 bytes
import pkg_resources
ensembl_file_37 = 'annotations/ensembl_genes_37.txt.gz'
ensembl_file_38 = 'annotations/ensembl_genes_38.txt.gz'
ensembl_path_37 = pkg_resources.resource_filename('genmod', ensembl_file_37)
ensembl_path_38 = pkg_resources.resource_filename('genmod', ensembl_file_38)