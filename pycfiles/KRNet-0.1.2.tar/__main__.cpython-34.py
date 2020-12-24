# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: krnet/__main__.py
# Compiled at: 2015-07-06 23:46:09
# Size of source mod 2**32: 810 bytes
import sys, networkx as nx
from krnetworkx import KRNetworkX
print('~~Welcome to KRNet~~')
print('  Author: Sanket Desai<desai.sanket12@gmail.com>')
print('  Web: https://pypi.python.org/pypi/KRNet')
print('  License: MIT')
if len(sys.argv) < 3:
    print('  USAGE: python3 krnet <KEGG_REACTION_FILE> <OUTFILE.gml>')
else:
    kn_ = KRNetworkX(sys.argv[1])
    if kn_ == None:
        print('  *****************************************************')
        print('  Reaction Graph not created! Check the input files...')
        sys.exit(0)
    else:
        print('  *************************************')
        print('  Reaction Graph successfully created!!')
        print('  Reactome has %d nodes and %d edges.' % (kn_.number_of_nodes(), kn_.number_of_edges()))
        kn_.write_to_file(sys.argv[2])
        print('  Thank you for using KRNet.')