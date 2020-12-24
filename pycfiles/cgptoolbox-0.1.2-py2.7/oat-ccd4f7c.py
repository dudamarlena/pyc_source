# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\cgp\utils\oat-ccd4f7c.py
# Compiled at: 2013-01-23 10:24:30
"""One-at-a-time sensitivity analysis. Naive, but robust."""
from collections import OrderedDict
import numpy as np
from joblib import Memory
from cgp.utils.rnumpy import r
from cgp.virtexp.elphys.examples import Fitz
from cgp.virtexp.elphys.paceable import ap_stats_array
from cgp.utils.splom import rlist2pydict
from cgp.utils.rec2dict import dict2rec
from cgp.phenotyping.attractor import AttractorMixin
from cgp.virtexp.elphys import ap_stats
from cgp.cvodeint.core import CvodeException
from cgp.utils.failwith import nans_like
r.library('reshape')
mem = Memory('oat')

class Cell(Fitz, AttractorMixin):
    pass


c = Cell()
x = np.linspace(0, 2, 3)

def makerec(L):
    par = OrderedDict(L)
    par = r.rename(r.melt(par), r.c(L1='parname', value='parvalue'))
    return dict2rec(rlist2pydict(par))


relpar = makerec([ (k, x) for k in c.pr.dtype.names ])
par = makerec([ (k, x * float(c.pr[k])) for k in c.pr.dtype.names ])

def pheno(par):
    """Action potential statistics for given parameters."""
    ph = []
    nanvalue = None
    for parvalue, parname in par:
        with c.autorestore():
            c.pr[parname] = parvalue
            try:
                t, y, period = c.cycle()
                stats = ap_stats_array(ap_stats(t, y.V))
                ph.append(stats)
                if nanvalue is None:
                    nanvalue = nans_like(stats)
            except CvodeException:
                ph.append(None)

    print nanvalue
    print ph
    ph = [ nanvalue if i is None else i for i in ph ]
    return np.concatenate(ph).view(nanvalue.dtype, np.recarray)


ph = pheno(par)
df = r.melt(r.cbind(relpar, ph), id_vars=['parvalue', 'parname'])
df = r.rename(df, r.c(variable='phname', value='phvalue'))
print r.head(df)
r['df'] = df
r.library('ggplot2')
r.par(ask=True)
r('\ndf <- within(df, {\n    parname <- as.factor(parname)\n    phname <- as.factor(phname)\n    group <- interaction(parname, phname)\n})\nprint(ggplot(df, aes(parvalue, phvalue, colour=parname, group=group)) + geom_path() + geom_point() + facet_wrap(~phname, scales="free_y"))\nggsave("c:/temp/temp.pdf")\nplot(1)\n')