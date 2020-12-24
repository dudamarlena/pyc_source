# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\test\_test_clampable.py
# Compiled at: 2012-02-03 05:34:19
"""Tests for :mod:`cgp.virtexp.elphys.clampable`."""
import numpy as np
from nose.plugins.attrib import attr
from cgp.virtexp.elphys.clampable import catrec, mmfits

@attr(slow=True)
def test_vargap():
    """Test fast vs slow variable-gap protocol."""
    from cgp.virtexp.elphys.examples import Bond
    b = Bond()
    protocol = [(100, -80), (50, 0),
     (
      np.arange(2, 78, 15), (-90, -80, -70)), (100, 0)]
    p1, gap, p2 = b.vargap(protocol)
    np.testing.assert_equal([ len(i) for i in (p1, gap, p2) ], [1, 3, 18])
    L = b.vecvclamp(protocol)
    np.testing.assert_equal([ len(i) for i in zip(*[ traj for _proto, traj in L ]) ], [18, 18, 18, 18])


@attr(slow=True)
def test_bond_protocols(plot=False):
    """Run all Bondarenko protocols."""
    from cgp.virtexp.elphys.examples import Bond
    b = Bond(chunksize=10000)

    def plotprot(i, varnames, limits, L):
        """Plot one protocol."""
        from pylab import figure, subplot, plot, savefig, legend, axis
        figure()
        proto0, _ = L[0]
        isclamped = len(proto0[0]) == 2
        for j, (n, lim) in enumerate(zip(varnames, limits)):
            subplot(len(varnames), 1, j + 1)
            leg = set()
            for k in n.split():
                if isclamped:
                    for _proto, traj in L:
                        t, y, _dy, a = catrec(*traj[1:])
                        plot(t, y[k] if k in y.dtype.names else a[k], label=k if k not in leg else None)
                        leg.add(k)

                else:
                    for _proto, paces in L:
                        t, y, _dy, a, _stats = catrec(*paces)
                        plot(t, y[k] if k in y.dtype.names else a[k], label=k if k not in leg else None)
                        leg.add(k)

                legend()

            if lim:
                axis(lim)

        savefig('fig%s%s.png' % (i, b.name))
        return

    bp = b.bond_protocols()
    for i, (varnames, protocol, limits, _url) in bp.items():
        if len(protocol[0]) == 2:
            L = b.vecvclamp(protocol)
        else:
            L = b.vecpace(protocol)
        if plot:
            plotprot(i, varnames, limits, L)


def test_mmfits():
    """
    Michaelis-Menten fit of peak i_CaL current vs gap duration.
    
    This uses a reduced version of the variable-gap protocol of Bondarenko's 
    figure 7. The full version is available as b.bond_protocols()[7].protocol.
    """
    from cgp.virtexp.elphys.examples import Bond
    b = Bond()
    protocol = ((1000, -80), (250, 0), (np.linspace(2, 202, 5), -80), (100, 0))
    with b.autorestore():
        L = b.vecvclamp(protocol)
    np.testing.assert_allclose(mmfits(L, k='i_CaL'), (6.44, 18.14), rtol=0.001)
    try:
        mmfits(L, 2, ['i_Na'])
    except AssertionError as exc:
        msg = "k must be a single field name of y or a, not <type 'list'>"
        assert msg in str(exc)