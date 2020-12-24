# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/epcy/argparser/get_kallisto_part.py
# Compiled at: 2020-03-24 10:22:05
# Size of source mod 2**32: 702 bytes
from .get_bootstrap_part import *

def get_argparser_kallisto_part(parser):
    parser.add_argument('--kal', dest='KAL',
      help='To work with kallisto quantification output. A collumn "kallisto" which contains the path of kallisto output folder for each sample, need to be added to the design file. By default EPCY will works on TPM unless --cpm is specified.',
      action='store_true')
    get_argparser_bootstrap_part(parser)
    parser.set_defaults(KAL=False)