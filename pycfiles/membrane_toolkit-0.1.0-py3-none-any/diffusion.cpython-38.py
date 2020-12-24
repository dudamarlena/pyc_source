# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/d/UNC Drive/pymemsci/membrane_toolkit/core/diffusion.py
# Compiled at: 2020-04-19 22:19:49
# Size of source mod 2**32: 1600 bytes
"""
Diffusion coefficient methods

All should start with diffusion_coefficient_
"""

def diffusion_coefficient_mackie_meares(D_bulk: float, phi_w: float) -> float:
    r"""
    Calculate the membrane-phase diffusion coefficient according to the Mackie-Meares
    model.

    Args:
        D_bulk (float): Bulk diffusion coefficient, [L**2 / t]
        phi_w (float): Water volume fraction (0 < \( \phi_w \) < 1) in the membrane
            [dimensionless]

    Returns:
        float: Diffusion coefficient in the membrane, [L**2 / t]

    Notes:
        The Mackie-Meares model relates the bulk diffusion coefficient of a species
        to its diffusion coefficient inside a porous medium through the volume fraction
        of water (or porosity) of that medium. The equation is

        $$
            D_{mem} = D_{bulk} * ( \frac{\phi_w}{2-\phi_w} )^2
        $$

    References:
        Mackie, J. S.; Meares, P. The Diffusion of Electrolytes in a Cation-Exchange
        Resin Membrane. I. Theoretical. Proc. R. Soc. London A 1955, 232 (1191),
        498–509.
    """
    if phi_w < 0 or phi_w > 1:
        raise ValueError('Invalid phi_w = {}. phi_w must be between 0 and 1'.format(phi_w))
    return D_bulk * (phi_w / (2 - phi_w)) ** 2


def diffusion_coefficient_free_volume():
    """
    Calculate the membrane-phase diffusion coefficient according to the free-volume
    model.
    """
    pass