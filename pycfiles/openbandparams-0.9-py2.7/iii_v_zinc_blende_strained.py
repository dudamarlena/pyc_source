# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/openbandparams/iii_v_zinc_blende_strained.py
# Compiled at: 2015-04-09 02:47:55
from .iii_v_alloy import IIIVAlloy
from .parameter import method_parameter
from .references import arent_1989, vurgaftman_2001

class IIIVZincBlendeStrained001(IIIVAlloy):
    """
    The base class for biaxial-strained III-V zinc blende binary alloys
    grown on a (001) surface.
    """

    def __init__(self, unstrained, substrate=None, strain_out_of_plane=None):
        """
        Either ``substrate`` or ``strain_out_of_plane`` must be specified,
        but not both.
        
        Paramters
        ---------
        unstrained : IIIVZincBlendeAlloy
            Unstrained III-V zinc blende alloy

        substrate : Alloy with ``a`` parameter (default=None)
            Growth substrate, assumed to have a (001) surface

        strain_out_of_plane : float (default=None)
            Out-of-plane strain [dimensionless], which is negative for tensile
            strain and positive for compressive strain. This is the strain
            measured by X-ray diffraction (XRD) symmetric omega-2theta scans.
        """
        if substrate is not None and strain_out_of_plane is None:
            self.substrate = substrate
            self._strain_out_of_plane = None
            name = ('{}/{}(001)').format(unstrained.name, substrate.name)
        elif strain_out_of_plane is not None:
            self.substrate = None
            self._strain_out_of_plane = float(strain_out_of_plane)
            name = ('{} strained {:g}% along [001]').format(unstrained.name, float(strain_out_of_plane) * 100.0)
        else:
            raise ValueError('Either `substrate` or `strain_out_of_plane` must be specified, but not both.')
        self.unstrained = unstrained
        super(IIIVZincBlendeStrained001, self).__init__(name, unstrained.elements, parameters=None)
        return

    def latex(self):
        if self._strain_out_of_plane is not None:
            return ('{} strained {:g}% along [001]').format(self.unstrained.latex(), self._strain_out_of_plane * 100.0)
        else:
            return ('{}/{}(001)').format(self.unstrained.latex(), self.substrate.latex())
            return

    def element_fraction(self, element):
        """
        Returns the fractional concentration of ``element`` with respect
        to its sublattice. In a III-V binary, the fraction is either 1 if
        ``element`` is present, or 0 if it is not.
        """
        return self.unstrained.element_fraction(element)

    @method_parameter(dependencies=['a'], units='dimensionless', references=[arent_1989])
    def strain_in_plane(self, **kwargs):
        """
        Returns the in-plane strain assuming no lattice relaxation, which
        is positive for tensile strain and negative for compressive strain.
        """
        if self._strain_out_of_plane is not None:
            return self._strain_out_of_plane / -2.0 * (self.unstrained.c11(**kwargs) / self.unstrained.c12(**kwargs))
        else:
            return 1 - self.unstrained.a(**kwargs) / self.substrate.a(**kwargs)
            return

    @method_parameter(dependencies=['c12', 'c11', 'strain_in_plane'], units='dimensionless', references=[arent_1989])
    def strain_out_of_plane(self, **kwargs):
        """
        Returns the out-of-plane strain assuming no lattice relaxation, which
        is negative for tensile strain and positive for compressive strain.
        This is the strain measured by X-ray diffraction (XRD) symmetric
        omega-2theta scans.
        """
        if self._strain_out_of_plane is not None:
            return self._strain_out_of_plane
        else:
            return -2 * self.unstrained.c12(**kwargs) / self.unstrained.c11(**kwargs) * self.strain_in_plane(**kwargs)
            return

    @method_parameter(dependencies=['strain_in_plane', 'a'], units='angstrom', references=[arent_1989])
    def substrate_a(self, **kwargs):
        """
        Returns the substrate's lattice parameter.
        """
        if self.substrate is not None:
            return self.substrate.a(**kwargs)
        else:
            return self.unstrained.a(**kwargs) / (1.0 - self.strain_in_plane(**kwargs))
            return

    @method_parameter(dependencies=['a_c', 'strain_in_plane',
     'strain_out_of_plane'], units='eV', references=[arent_1989])
    def CBO_hydrostatic_strain_shift(self, **kwargs):
        return self.unstrained.a_c(**kwargs) * (2 * self.strain_in_plane(**kwargs) + self.strain_out_of_plane(**kwargs))

    @method_parameter(dependencies=['CBO_hydrostatic_strain_shift'], units='eV', references=[arent_1989])
    def CBO_strain_shift(self, **kwargs):
        return self.CBO_hydrostatic_strain_shift(**kwargs)

    @method_parameter(dependencies=['CBO', 'CBO_strain_shift'], units='eV')
    def CBO(self, **kwargs):
        """
        Returns the strain-shifted conduction band offset (CBO), assuming
        the strain affects all conduction band valleys equally.
        """
        return self.unstrained.CBO(**kwargs) + self.CBO_strain_shift(**kwargs)

    @method_parameter(dependencies=['CBO_Gamma', 'CBO_strain_shift'], units='eV')
    def CBO_Gamma(self, **kwargs):
        """
        Returns the strain-shifted Gamma-valley conduction band offset (CBO),
        assuming the strain affects all conduction band valleys equally.
        """
        return self.unstrained.CBO_Gamma(**kwargs) + self.CBO_strain_shift(**kwargs)

    @method_parameter(dependencies=['CBO_L', 'CBO_strain_shift'], units='eV')
    def CBO_L(self, **kwargs):
        """
        Returns the strain-shifted L-valley conduction band offset (CBO),
        assuming the strain affects all conduction band valleys equally.
        """
        return self.unstrained.CBO_L(**kwargs) + self.CBO_strain_shift(**kwargs)

    @method_parameter(dependencies=['CBO_X', 'CBO_strain_shift'], units='eV')
    def CBO_X(self, **kwargs):
        """
        Returns the strain-shifted X-valley conduction band offset (CBO),
        assuming the strain affects all conduction band valleys equally.
        """
        return self.unstrained.CBO_X(**kwargs) + self.CBO_strain_shift(**kwargs)

    @method_parameter(dependencies=['Eg', 'Eg_strain_shift'], units='eV')
    def Eg(self, **kwargs):
        """
        Returns the strain-shifted bandgap, ``Eg``.
        """
        return self.unstrained.Eg(**kwargs) + self.Eg_strain_shift(**kwargs)

    @method_parameter(dependencies=['VBO_hh', 'CBO'], units='eV')
    def Eg_hh(self, **kwargs):
        """
        Returns the strain-shifted heavy-hole bandgap, ``Eg_hh``.
        """
        return self.CBO(**kwargs) - self.VBO_hh(**kwargs)

    @method_parameter(dependencies=['VBO_lh', 'CBO'], units='eV')
    def Eg_lh(self, **kwargs):
        """
        Returns the strain-shifted light-hole bandgap, ``Eg_lh``.
        """
        return self.CBO(**kwargs) - self.VBO_lh(**kwargs)

    @method_parameter(dependencies=['CBO_strain_shift', 'VBO_strain_shift'], units='eV', references=[arent_1989])
    def Eg_strain_shift(self, **kwargs):
        return self.CBO_strain_shift(**kwargs) - self.VBO_strain_shift(**kwargs)

    @method_parameter(dependencies=['a_v', 'strain_in_plane',
     'strain_out_of_plane'], units='eV', references=[arent_1989])
    def VBO_hydrostatic_strain_shift(self, **kwargs):
        return self.unstrained.a_v(**kwargs) * (2 * self.strain_in_plane(**kwargs) + self.strain_out_of_plane(**kwargs))

    @method_parameter(dependencies=['b', 'strain_in_plane',
     'strain_out_of_plane'], units='eV', references=[arent_1989])
    def VBO_uniaxial_strain_shift(self, **kwargs):
        return self.unstrained.b(**kwargs) * (self.strain_out_of_plane(**kwargs) - self.strain_in_plane(**kwargs))

    @method_parameter(dependencies=['VBO_hydrostatic_strain_shift',
     'VBO_uniaxial_strain_shift'], units='eV', references=[arent_1989])
    def VBO_hh_strain_shift(self, **kwargs):
        return -(self.VBO_uniaxial_strain_shift(**kwargs) + self.VBO_hydrostatic_strain_shift(**kwargs))

    @method_parameter(dependencies=['VBO_hydrostatic_strain_shift',
     'VBO_uniaxial_strain_shift'], units='eV', references=[arent_1989])
    def VBO_lh_strain_shift(self, **kwargs):
        return self.VBO_uniaxial_strain_shift(**kwargs) - self.VBO_hydrostatic_strain_shift(**kwargs)

    @method_parameter(dependencies=['VBO', 'VBO_hh_strain_shift'], units='eV')
    def VBO_hh(self, **kwargs):
        return self.unstrained.VBO(**kwargs) + self.VBO_hh_strain_shift(**kwargs)

    @method_parameter(dependencies=['VBO', 'VBO_lh_strain_shift'], units='eV')
    def VBO_lh(self, **kwargs):
        return self.unstrained.VBO(**kwargs) + self.VBO_lh_strain_shift(**kwargs)

    @method_parameter(dependencies=['VBO_hh', 'VBO_lh'], units='eV')
    def VBO(self, **kwargs):
        return max(self.VBO_hh(**kwargs), self.VBO_lh(**kwargs))

    @method_parameter(dependencies=['VBO_hh_strain_shift',
     'VBO_lh_strain_shift'], units='eV')
    def VBO_strain_shift(self, **kwargs):
        return max(self.VBO_hh_strain_shift(**kwargs), self.VBO_lh_strain_shift(**kwargs))

    @method_parameter(dependencies=['Eg_Gamma', 'Delta_SO', 'Ep', 'F'], units='m_e', references=[vurgaftman_2001])
    def meff_e_Gamma(self, **kwargs):
        """
        Returns the electron effective mass in the Gamma-valley
        calculated from Eg_Gamma(T), CBO_strain_shift, Delta_SO, Ep and F,
        assuming the CBO_strain_shift causes warping of the Gamma-valley
        consistent with Kane's k.p model. Effects on the valance band
        are not included.
        
        TODO: verify that this is a reasonable assumption.
        """
        Eg = self.unstrained.Eg_Gamma(**kwargs) + self.CBO_strain_shift(**kwargs)
        Delta_SO = self.unstrained.Delta_SO(**kwargs)
        Ep = self.unstrained.Ep(**kwargs)
        F = self.unstrained.F(**kwargs)
        return 1.0 / (1.0 + 2.0 * F + Ep * (Eg + 2.0 * Delta_SO / 3.0) / (Eg * (Eg + Delta_SO)))