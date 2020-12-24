# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /anaconda/lib/python2.7/site-packages/landlab/tests/speed_test_model_grid.py
# Compiled at: 2014-09-23 12:37:24
"""
simple script to run speed tests of various functions in model grid
"""
import landlab as ll, time

def main():
    mg = ll.RasterModelGrid(20, 30, 1.0)
    nt = 1000
    s = mg.zeros(centering='node')
    g = mg.zeros(centering='active_link')
    divg = mg.zeros(centering='node')
    start_time = time.time()
    for i in range(nt):
        g = mg.calculate_gradients_at_active_links(s, g)

    time1 = time.time()
    for i in range(nt):
        g = mg._calculate_gradients_at_active_links_slow(s, g)

    time2 = time.time()
    for i in range(nt):
        divg = mg.calculate_flux_divergence_at_nodes(g, divg)

    time3 = time.time()
    for i in range(nt):
        divg = mg.calculate_flux_divergence_at_nodes_slow(g, divg)

    time4 = time.time()
    for i in range(nt):
        divg = mg.calculate_flux_divergence_at_active_cells(g)

    time5 = time.time()
    for i in range(nt):
        divg = mg.calculate_flux_divergence_at_active_cells_slow(g)

    time6 = time.time()
    print 'Elapsed time with fast gradient algo: ' + str(time1 - start_time)
    print 'Elapsed time with slow gradient algo: ' + str(time2 - time1)
    print 'Elapsed time with fast node-divergence algo: ' + str(time3 - time2)
    print 'Elapsed time with slow node-divergence algo: ' + str(time4 - time3)
    print 'Elapsed time with fast activecell-divergence algo: ' + str(time5 - time4)
    print 'Elapsed time with slow activecell-divergence algo: ' + str(time6 - time5)


if __name__ == '__main__':
    main()