# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/champ/test_champ.py
# Compiled at: 2018-05-23 14:58:31
# Size of source mod 2**32: 2640 bytes
import logging, pdb, sys, traceback, matplotlib.pyplot as plt, numpy as np, champ
DESCRIPTION = ''
LOG_LEVEL = logging.INFO
LOG_FORMAT = '%(asctime)s:%(levelname)s:%(message)s'

def main():
    logging.basicConfig(format=LOG_FORMAT, level=LOG_LEVEL)
    logging.info('Command: %s', ' '.join(sys.argv))
    logging.info('Multilayer Test')
    test_hs_array = champ.get_random_halfspaces(50)
    logging.info('Coefficent array: ' + str(test_hs_array.shape))
    test_hs = champ.create_halfspaces_from_array(test_hs_array)
    logging.info('Number of Initial Partitions: %d' % len(test_hs))
    ind_2_doms = champ.get_intersection(test_hs_array)
    logging.info('Number of Admissible Partitions: %d' % len(ind_2_doms.keys()))
    plt.close()
    ax = champ.plot_2d_domains(ind_2_doms)
    plt.show()
    logging.info('Single-layer Test')
    test_hs_arry = champ.get_random_halfspaces(100, dim=2)
    test_hs = champ.create_halfspaces_from_array(test_hs_arry)
    logging.info('Number of Initial Partitions: %d' % len(test_hs))
    ind_2_doms = champ.get_intersection(test_hs_arry, max_pt=10)
    logging.info('Number of Admissible Partitions: %d' % len(ind_2_doms.keys()))
    plt.close()
    f, (a1, a2) = plt.subplots(1, 2, figsize=(8, 4))
    a1 = champ.plot_domains.plot_line_halfspaces(test_hs, ax=a1)
    a1.set_title('Visualization of All Partition Lines')
    a2 = champ.plot_single_layer_modularity_domains(ind_2_doms, ax=a2)
    plt.show()
    return 1


def pydebug(type, value, tb):
    logging.error('Error type:' + str(type) + ': ' + str(value))
    traceback.print_tb(tb)
    pdb.pm()


if __name__ == '__main__':
    sys.excepthook = pydebug
    sys.exit(main())