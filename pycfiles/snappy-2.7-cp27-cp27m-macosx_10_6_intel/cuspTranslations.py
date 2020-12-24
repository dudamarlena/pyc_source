# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dunfield/snappy/build/lib.macosx-10.6-intel-2.7/snappy/verify/cuspTranslations.py
# Compiled at: 2018-08-17 21:53:27
from ..sage_helper import _within_sage
from .cuspCrossSection import ComplexCuspCrossSection

def cusp_translations_for_manifold(manifold, areas=None, check_std_form=True, verified=False, bits_prec=None):
    shapes = manifold.tetrahedra_shapes('rect', intervals=verified, bits_prec=bits_prec)
    c = ComplexCuspCrossSection.fromManifoldAndShapes(manifold, shapes)
    if verified:
        CIF = shapes[0].parent()
        c.check_logarithmic_edge_equations_and_positivity(CIF)
    else:
        sol_type = manifold.solution_type()
        if not sol_type == 'all tetrahedra positively oriented':
            raise RuntimeError("Manifold has non-geometric solution type '%s'." % sol_type)
    if areas:
        RF = shapes[0].real().parent()
        c.normalize_cusps([ RF(area) for area in areas ])
        if check_std_form:
            c.ensure_std_form()
    else:
        c.ensure_std_form(allow_scaling_up=True)
    c.ensure_disjoint_on_edges()
    return c.all_normalized_translations()


def cusp_translations_for_neighborhood(neighborhood, verified=False, bits_prec=None):
    manifold = neighborhood.manifold()
    areas = [ neighborhood.volume(i) * 2 for i in range(manifold.num_cusps()) ]
    return cusp_translations_for_manifold(manifold, areas=areas, check_std_form=verified, verified=verified, bits_prec=bits_prec)