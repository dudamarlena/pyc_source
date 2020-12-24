# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/igwtools/traverse.py
# Compiled at: 2007-10-24 14:04:23
""" 
Set of tools to work with the output files from the LabView program
that drives the conductivity probe.  Output file are typically called
trav?.dat
"""
import sys, getopt, csv, pylab, numpy
from scipy import stats

def load_trav_dat(filename):
    """Load trav.dat file and return a tuple of (z, rho)"""
    s = csv.Sniffer()
    sample = open(filename, 'r').read()
    d = s.sniff(sample)
    h = s.has_header(sample)
    z = []
    rho = []
    f = csv.reader(open(filename, 'rb'), dialect=d)
    for row in f:
        z.append(float(row[0]))
        rho.append(float(row[1]))

    return (numpy.array(z), numpy.array(rho))


def plot_fit(z, rho, zmin, zmax):
    if zmin == None:
        zmin = z[(-1)]
    if zmax == None:
        zmax = z[0]
    a = max(pylab.find(z >= zmin))
    b = min(pylab.find(z <= zmax))
    z = z[b:a]
    rho = rho[b:a]
    (slope, intercept, r) = stats.linregress(z, rho)[0:3]
    print 'drhodz = %.5e' % slope,
    print 'intercept = %.4f' % intercept,
    print 'R = %.2f' % r,
    rho_fit_min = intercept + slope * zmin
    rho_fit_max = intercept + slope * zmax
    pylab.plot([rho_fit_min, rho_fit_max], [zmin, zmax], 'k-', linewidth=2)
    g = -980
    rho0 = 1.0
    N2 = g / rho0 * slope
    print 'N2 = %.5f' % N2,
    print 'N = %.5f' % numpy.sqrt(N2)
    return


def plot_traverse(filenames, legend=False, fit=False, zmin=None, zmax=None):
    """
takes a list of trav.dat files and plots them on the same graph
"""
    if len(filenames) == 0:
        return
    pylab.figure()
    pylab.title('Density Profiles')
    pylab.xlabel('$\\rho\\ (g\\ cm^{-3})$')
    pylab.ylabel('$z\\ (cm)$')
    for i in range(len(filenames)):
        print 'Processing', filenames[i]
        (z, rho) = load_trav_dat(filenames[i])
        pylab.plot(rho, z)
        if fit:
            plot_fit(z, rho, zmin, zmax)

    if legend:
        leg = pylab.legend()
        for i in range(len(filenames)):
            leg.get_texts()[i].set_text(filenames[i])


def entry_plot_traverse():
    try:
        (opts, args) = getopt.getopt(sys.argv[1:], 'flp', ['zmin=', 'zmax='])
    except getopt.GetoptError:
        print 'Usage: plot_traverse [options] trav.dat ...'
        return 2

    legend = False
    fit = False
    pdf = False
    zmin = None
    zmax = None
    for (o, a) in opts:
        if o == '-f':
            fit = True
        if o == '-l':
            legend = True
        if o == '--zmin':
            zmin = float(a)
        if o == '--zmax':
            zmax = float(a)
        if o == '-p':
            pdf = True

    plot_traverse(args, fit=fit, legend=legend, zmin=zmin, zmax=zmax)
    if pdf:
        pylab.savefig('trav.pdf')
    else:
        pylab.show()
    return