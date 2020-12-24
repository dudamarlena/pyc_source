# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\color\cam\colorappearancemodels.py
# Compiled at: 2019-10-24 08:27:52
# Size of source mod 2**32: 11684 bytes
"""

cam: sub-package with color appearance models
=============================================

 :_UNIQUE_HUE_DATA: database of unique hues with corresponding 
                             Hue quadratures and eccentricity factors 
                             for ciecam02, cam16, ciecam97s, cam15u, cam18sl)

 :_SURROUND_PARAMETERS: database of surround param. c, Nc, F and FLL 
                                 for ciecam02, cam16, ciecam97s and cam15u.

 :_NAKA_RUSHTON_PARAMETERS: | database with parameters 
                                       (n, sig, scaling and noise) 
                                       for the Naka-Rushton function: 
                            | NK(x) = sign(x) * scaling * ((abs(x)**n) / ((abs(x)**n) + (sig**n))) + noise

 :_CAM_02_X_UCS_PARAMETERS: | database with parameters specifying the conversion 
                              from ciecam02/cam16 to:
                            |    cam[x]ucs (uniform color space), 
                            |    cam[x]lcd (large color diff.), 
                            |    cam[x]scd (small color diff).
                            
 :_CAM15U_PARAMETERS: database with CAM15u model parameters.
 
 :_CAM_SWW16_PARAMETERS: cam_sww16 model parameters.
 
 :_CAM18SL_PARAMETERS: database with CAM18sl model parameters

 :_CAM_DEFAULT_WHITE_POINT: Default internal reference white point (xyz)

 :_CAM_DEFAULT_TYPE: Default CAM type str specifier.

 :_CAM_DEFAULT_MCAT: Default MCAT specifier.

 :_CAM_02_X_DEFAULT_CONDITIONS: Default CAM model parameters for model 
                                in cam._CAM_DEFAULT_TYPE

 :_CAM_AXES: dict with list[str,str,str] containing axis labels 
                  of defined cspaces.
                  
 :deltaH(): Compute a hue difference, dH = 2*C1*C2*sin(dh/2).

 :naka_rushton(): applies a Naka-Rushton function to the input
 
 :hue_angle(): calculates a positive hue angle

 :hue_quadrature(): calculates the Hue quadrature from the hue.

 :cam_structure_ciecam02_cam16(): | basic structure of ciecam02 and cam16 models.
                                  | Has 'forward' (xyz --> color attributes) 
                                    and 'inverse' (color attributes --> xyz) modes.

 :ciecam02(): | calculates ciecam02 output 
              | (wrapper for cam_structure_ciecam02_cam16 with specifics 
                of ciecam02): 
              | `N. Moroney, M. D. Fairchild, R. W. G. Hunt, C. Li, M. R. Luo, and T. Newman, 
                “The CIECAM02 color appearance model,” 
                IS&T/SID Tenth Color Imaging Conference. p. 23, 2002. <http://rit-mcsl.org/fairchild/PDFs/PRO19.pdf>`_

 :cam16(): | calculates cam16 output 
           | (wrapper for cam_structure_ciecam02_cam16 with specifics 
             of cam16):  
           | `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, 
             “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
             Color Res. Appl., p. n/a–n/a. <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract>`_

 :camucs_structure(): basic structure to go to ucs, lcd and scd color spaces 
                      (forward + inverse available)

 :cam02ucs(): | calculates ucs (or lcd, scd) output based on ciecam02 
                (forward + inverse available)
              |  `M. R. Luo, G. Cui, and C. Li, 
                 “Uniform colour spaces based on CIECAM02 colour appearance model,” 
                 Color Res. Appl., vol. 31, no. 4, pp. 320–330, 2006.
                 <http://onlinelibrary.wiley.com/doi/10.1002/col.20227/abstract>`_

 :cam16ucs(): | calculates ucs (or lcd, scd) output based on cam16 
                (forward + inverse available)
              | `C. Li, Z. Li, Z. Wang, Y. Xu, M. R. Luo, G. Cui, M. Melgosa, M. H. Brill, and M. Pointer, 
                “Comprehensive color solutions: CAM16, CAT16, and CAM16-UCS,” 
                Color Res. Appl., p. n/a–n/a. <http://onlinelibrary.wiley.com/doi/10.1002/col.22131/abstract>`_

 :cam15u(): | calculates the output for the CAM15u model for self-luminous unrelated stimuli. 
            | `M. Withouck, K. A. G. Smet, W. R. Ryckaert, and P. Hanselaer, 
              “Experimental driven modelling of the color appearance of 
              unrelated self-luminous stimuli: CAM15u,” 
              Opt. Express, vol. 23, no. 9, pp. 12045–12064, 2015.
              <https://www.osapublishing.org/oe/abstract.cfm?uri=oe-23-9-12045&origin=search>`_
            | `M. Withouck, K. A. G. Smet, and P. Hanselaer, (2015), 
            “Brightness prediction of different sized unrelated self-luminous stimuli,” 
            Opt. Express, vol. 23, no. 10, pp. 13455–13466. 
            <https://www.osapublishing.org/oe/abstract.cfm?uri=oe-23-10-13455&origin=search>`_
            
 :cam_sww16(): | A simple principled color appearance model based on a mapping 
                 of the Munsell color system.
               | `Smet, K. A. G., Webster, M. A., & Whitehead, L. A. (2016). 
                   A simple principled approach for modeling and understanding uniform color metrics. 
                   Journal of the Optical Society of America A, 33(3), A319–A331. 
                   <https://doi.org/10.1364/JOSAA.33.00A319>`_
               
 :cam18sl(): | calculates the output for the CAM18sl model for self-luminous related stimuli. 
             | `Hermans, S., Smet, K. A. G., & Hanselaer, P. (2018). 
               "Color appearance model for self-luminous stimuli."
               Journal of the Optical Society of America A, 35(12), 2000–2009. 
               <https://doi.org/10.1364/JOSAA.35.002000>`_           

 :specific_wrappers_in_the_'xyz_to_cspace()' and 'cpsace_to_xyz()' format:
      | 'xyz_to_jabM_ciecam02', 'jabM_ciecam02_to_xyz',
      | 'xyz_to_jabC_ciecam02', 'jabC_ciecam02_to_xyz',
      | 'xyz_to_jabM_cam16', 'jabM_cam16_to_xyz',
      | 'xyz_to_jabC_cam16', 'jabC_cam16_to_xyz',
      | 'xyz_to_jab_cam02ucs', 'jab_cam02ucs_to_xyz', 
      | 'xyz_to_jab_cam02lcd', 'jab_cam02lcd_to_xyz',
      | 'xyz_to_jab_cam02scd', 'jab_cam02scd_to_xyz', 
      | 'xyz_to_jab_cam16ucs', 'jab_cam16ucs_to_xyz',
      | 'xyz_to_jab_cam16lcd', 'jab_cam16lcd_to_xyz',
      | 'xyz_to_jab_cam16scd', 'jab_cam16scd_to_xyz',
      | 'xyz_to_qabW_cam15u', 'qabW_cam15u_to_xyz',
      | 'xyz_to_lab_cam_sww16', 'lab_cam_sww16_to_xyz',
      | 'xyz_to_qabW_cam18sl', 'qabW_cam18sl_to_xyz',
      | 'xyz_to_qabM_cam18sl', 'qabM_cam18sl_to_xyz',
      | 'xyz_to_qabS_cam18sl', 'qabS_cam18sl_to_xyz',

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from .cam_02_X import deltaH, naka_rushton, hue_angle, hue_quadrature, _CAM_02_X_AXES, _CAM_02_X_UNIQUE_HUE_DATA, _CAM_02_X_SURROUND_PARAMETERS, _CAM_02_X_NAKA_RUSHTON_PARAMETERS, _CAM_02_X_UCS_PARAMETERS, _CAM_02_X_DEFAULT_TYPE, _CAM_02_X_DEFAULT_WHITE_POINT, _CAM_02_X_DEFAULT_CONDITIONS, cam_structure_ciecam02_cam16, camucs_structure, ciecam02, cam16, cam02ucs, cam16ucs, xyz_to_jabM_ciecam02, jabM_ciecam02_to_xyz, xyz_to_jabC_ciecam02, jabC_ciecam02_to_xyz, xyz_to_jabM_cam16, jabM_cam16_to_xyz, xyz_to_jabC_cam16, jabC_cam16_to_xyz, xyz_to_jab_cam02ucs, jab_cam02ucs_to_xyz, xyz_to_jab_cam02lcd, jab_cam02lcd_to_xyz, xyz_to_jab_cam02scd, jab_cam02scd_to_xyz, xyz_to_jab_cam16ucs, jab_cam16ucs_to_xyz, xyz_to_jab_cam16lcd, jab_cam16lcd_to_xyz, xyz_to_jab_cam16scd, jab_cam16scd_to_xyz
from .cam15u import cam15u, _CAM15U_AXES, _CAM15U_UNIQUE_HUE_DATA, _CAM15U_PARAMETERS, _CAM15U_NAKA_RUSHTON_PARAMETERS, _CAM15U_SURROUND_PARAMETERS, xyz_to_qabW_cam15u, qabW_cam15u_to_xyz
from .sww2016 import cam_sww16, _CAM_SWW16_AXES, _CAM_SWW16_PARAMETERS, xyz_to_lab_cam_sww16, lab_cam_sww16_to_xyz
from .cam18sl import cam18sl, _CAM18SL_AXES, _CAM18SL_UNIQUE_HUE_DATA, _CAM18SL_PARAMETERS, _CAM18SL_NAKA_RUSHTON_PARAMETERS, xyz_to_qabW_cam18sl, qabW_cam18sl_to_xyz, xyz_to_qabM_cam18sl, qabM_cam18sl_to_xyz, xyz_to_qabS_cam18sl, qabS_cam18sl_to_xyz
__all__ = [
 '_CAM_AXES', '_UNIQUE_HUE_DATA', '_SURROUND_PARAMETERS',
 '_NAKA_RUSHTON_PARAMETERS', '_CAM_02_X_UCS_PARAMETERS']
__all__ += ['_CAM_DEFAULT_TYPE', '_CAM_DEFAULT_WHITE_POINT',
 '_CAM_DEFAULT_CONDITIONS']
__all__ += ['_CAM15U_PARAMETERS', '_CAM_SWW16_PARAMETERS', '_CAM18SL_PARAMETERS']
__all__ += ['deltaH', 'hue_angle', 'hue_quadrature', 'naka_rushton', 'ciecam02', 'cam16',
 'cam02ucs', 'cam16ucs', 'cam15u', 'cam_sww16', 'cam18sl']
__all__ += ['xyz_to_jabM_ciecam02', 'jabM_ciecam02_to_xyz',
 'xyz_to_jabC_ciecam02', 'jabC_ciecam02_to_xyz',
 'xyz_to_jabM_cam16', 'jabM_cam16_to_xyz',
 'xyz_to_jabC_cam16', 'jabC_cam16_to_xyz',
 'xyz_to_jab_cam02ucs', 'jab_cam02ucs_to_xyz',
 'xyz_to_jab_cam02lcd', 'jab_cam02lcd_to_xyz',
 'xyz_to_jab_cam02scd', 'jab_cam02scd_to_xyz',
 'xyz_to_jab_cam16ucs', 'jab_cam16ucs_to_xyz',
 'xyz_to_jab_cam16lcd', 'jab_cam16lcd_to_xyz',
 'xyz_to_jab_cam16scd', 'jab_cam16scd_to_xyz',
 'xyz_to_qabW_cam15u', 'qabW_cam15u_to_xyz',
 'xyz_to_lab_cam_sww16', 'lab_cam_sww16_to_xyz',
 'xyz_to_qabW_cam18sl', 'qabW_cam18sl_to_xyz',
 'xyz_to_qabM_cam18sl', 'qabM_cam18sl_to_xyz',
 'xyz_to_qabS_cam18sl', 'qabS_cam18sl_to_xyz']
_CAM_AXES = _CAM_02_X_AXES
_CAM_AXES['qabW_cam15u'] = _CAM15U_AXES
_CAM_AXES['lab_cam_sww16'] = _CAM_SWW16_AXES
_CAM_AXES['qabW_cam18sl'] = _CAM18SL_AXES
_UNIQUE_HUE_DATA = _CAM_02_X_UNIQUE_HUE_DATA
_UNIQUE_HUE_DATA['cam15u'] = _CAM15U_UNIQUE_HUE_DATA
_UNIQUE_HUE_DATA['models'].append('cam15u')
_UNIQUE_HUE_DATA['cam18sl'] = _CAM18SL_UNIQUE_HUE_DATA
_UNIQUE_HUE_DATA['models'].append('cam18sl')
_SURROUND_PARAMETERS = _CAM_02_X_SURROUND_PARAMETERS
_SURROUND_PARAMETERS['cam15u'] = _CAM15U_SURROUND_PARAMETERS
_SURROUND_PARAMETERS['cam_sww16'] = {}
_SURROUND_PARAMETERS['cam18sl'] = {}
_NAKA_RUSHTON_PARAMETERS = _CAM_02_X_NAKA_RUSHTON_PARAMETERS
_NAKA_RUSHTON_PARAMETERS['cam15u'] = _CAM15U_NAKA_RUSHTON_PARAMETERS
_NAKA_RUSHTON_PARAMETERS['cam18sl'] = _CAM18SL_NAKA_RUSHTON_PARAMETERS
_CAM_DEFAULT_TYPE = _CAM_02_X_DEFAULT_TYPE
_CAM_DEFAULT_WHITE_POINT = _CAM_02_X_DEFAULT_WHITE_POINT
_CAM_DEFAULT_CONDITIONS = _CAM_02_X_DEFAULT_CONDITIONS