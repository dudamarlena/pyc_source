# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: D:\Documents\GitHub\luxpy\luxpy\spectrum\basics\spectral.py
# Compiled at: 2020-02-12 02:06:37
# Size of source mod 2**32: 59342 bytes
"""
Module supporting basic spectral calculations.
==============================================

 :_WL3: Default wavelength specification in vector-3 format: 
        ndarray([start, end, spacing])

 :_BB: Dict with constants for blackbody radiator calculation 
       constant are (c1, c2, n, na, c, h, k). 

 :_S012_DAYLIGHTPHASE: ndarray with CIE S0,S1, S2 curves for daylight 
        phase calculation.

 :_INTERP_TYPES: Dict with interpolation types associated with various types of
                 spectral data according to CIE recommendation:  

 :_S_INTERP_TYPE: Interpolation type for light source spectral data

 :_R_INTERP_TYPE: Interpolation type for reflective/transmissive spectral data

 :_CRI_REF_TYPE: Dict with blackbody to daylight transition (mixing) ranges for
                 various types of reference illuminants used in color rendering
                 index calculations.

 :getwlr(): Get/construct a wavelength range from a (start, stop, spacing) 
            3-vector.

 :getwld(): Get wavelength spacing of ndarray with wavelengths.

 :spd_normalize(): Spectrum normalization (supports: area, max, lambda, 
                   radiometric, photometric and quantal energy units).

 :cie_interp(): Interpolate / extrapolate spectral data following standard 
                [`CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_]

 :spd(): | All-in-one function that can:
         |  1. Read spectral data from data file or take input directly as 
            pandas.dataframe or ndarray.
         |  2. Convert spd-like data from ndarray to pandas.dataframe and back.
         |  3. Interpolate spectral data.
         |  4. Normalize spectral data.

 :xyzbar(): Get color matching functions.
        
 :vlbar(): Get Vlambda function.

 :spd_to_xyz(): Calculates xyz tristimulus values from spectral data. 
            
 :spd_to_ler():  Calculates Luminous efficacy of radiation (LER) 
                 from spectral data.

 :spd_to_power(): Calculate power of spectral data in radiometric, photometric
                  or quantal energy units.
         
 :blackbody(): Calculate blackbody radiator spectrum.
             
 :daylightlocus(): Calculates daylight chromaticity from cct. 

 :daylightphase(): Calculate daylight phase spectrum         
         
 :cri_ref(): Calculates a reference illuminant spectrum based on cct for color 
             rendering index calculations.
            (`CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_, 
             `cie224:2017, CIE 2017 Colour Fidelity Index for accurate scientific use. (2017), ISBN 978-3-902842-61-9. <http://www.cie.co.at/index.php?i_ca_id=1027>`_,
             `IES-TM-30-15: Method for Evaluating Light Source Color Rendition. New York, NY: The Illuminating Engineering Society of North America. <https://www.ies.org/store/technical-memoranda/ies-method-for-evaluating-light-source-color-rendition/>`_
 
    
References
----------

    1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    
    2. `cie224:2017, CIE 2017 Colour Fidelity Index for accurate scientific use. (2017),
    ISBN 978-3-902842-61-9. 
    <http://www.cie.co.at/index.php?i_ca_id=1027>`_
    
    3. `IES-TM-30-15: Method for Evaluating Light Source Color Rendition. 
    New York, NY: The Illuminating Engineering Society of North America. 
    <https://www.ies.org/store/technical-memoranda/ies-method-for-evaluating-light-source-color-rendition/>`_

.. codeauthor:: Kevin A.G. Smet (ksmet1977 at gmail.com)
"""
from luxpy import np, pd, interpolate, _PKG_PATH, _SEP, _EPS, _CIEOBS, np2d, getdata, math
from .cmf import _CMF
__all__ = [
 '_WL3', '_BB', '_S012_DAYLIGHTPHASE', '_INTERP_TYPES', '_S_INTERP_TYPE', '_R_INTERP_TYPE', '_CRI_REF_TYPE',
 '_CRI_REF_TYPES', 'getwlr', 'getwld', 'spd_normalize', 'cie_interp', 'spd', 'xyzbar', 'vlbar',
 'spd_to_xyz', 'spd_to_ler', 'spd_to_power',
 'blackbody', 'daylightlocus', 'daylightphase', 'cri_ref']
_WL3 = [
 360.0, 830.0, 1.0]
_BB = {'c1':3.74183e-16, 
 'c2':1.4388 * 0.01,  'n':1.0,  'na':1.00028,  'c':299792458,  'h':6.62607004e-34,  'k':1.38064852e-23}
_S012_DAYLIGHTPHASE = np.array([[360.0, 361.0, 362.0, 363.0, 364.0, 365.0, 366.0, 367.0, 368.0, 369.0, 370.0, 371.0, 372.0, 373.0, 374.0, 375.0, 376.0, 377.0, 378.0, 379.0, 380.0, 381.0, 382.0, 383.0, 384.0, 385.0, 386.0, 387.0, 388.0, 389.0, 390.0, 391.0, 392.0, 393.0, 394.0, 395.0, 396.0, 397.0, 398.0, 399.0, 400.0, 401.0, 402.0, 403.0, 404.0, 405.0, 406.0, 407.0, 408.0, 409.0, 410.0, 411.0, 412.0, 413.0, 414.0, 415.0, 416.0, 417.0, 418.0, 419.0, 420.0, 421.0, 422.0, 423.0, 424.0, 425.0, 426.0, 427.0, 428.0, 429.0, 430.0, 431.0, 432.0, 433.0, 434.0, 435.0, 436.0, 437.0, 438.0, 439.0, 440.0, 441.0, 442.0, 443.0, 444.0, 445.0, 446.0, 447.0, 448.0, 449.0, 450.0, 451.0, 452.0, 453.0, 454.0, 455.0, 456.0, 457.0, 458.0, 459.0, 460.0, 461.0, 462.0, 463.0, 464.0, 465.0, 466.0, 467.0, 468.0, 469.0, 470.0, 471.0, 472.0, 473.0, 474.0, 475.0, 476.0, 477.0, 478.0, 479.0, 480.0, 481.0, 482.0, 483.0, 484.0, 485.0, 486.0, 487.0, 488.0, 489.0, 490.0, 491.0, 492.0, 493.0, 494.0, 495.0, 496.0, 497.0, 498.0, 499.0, 500.0, 501.0, 502.0, 503.0, 504.0, 505.0, 506.0, 507.0, 508.0, 509.0, 510.0, 511.0, 512.0, 513.0, 514.0, 515.0, 516.0, 517.0, 518.0, 519.0, 520.0, 521.0, 522.0, 523.0, 524.0, 525.0, 526.0, 527.0, 528.0, 529.0, 530.0, 531.0, 532.0, 533.0, 534.0, 535.0, 536.0, 537.0, 538.0, 539.0, 540.0, 541.0, 542.0, 543.0, 544.0, 545.0, 546.0, 547.0, 548.0, 549.0, 550.0, 551.0, 552.0, 553.0, 554.0, 555.0, 556.0, 557.0, 558.0, 559.0, 560.0, 561.0, 562.0, 563.0, 564.0, 565.0, 566.0, 567.0, 568.0, 569.0, 570.0, 571.0, 572.0, 573.0, 574.0, 575.0, 576.0, 577.0, 578.0, 579.0, 580.0, 581.0, 582.0, 583.0, 584.0, 585.0, 586.0, 587.0, 588.0, 589.0, 590.0, 591.0, 592.0, 593.0, 594.0, 595.0, 596.0, 597.0, 598.0, 599.0, 600.0, 601.0, 602.0, 603.0, 604.0, 605.0, 606.0, 607.0, 608.0, 609.0, 610.0, 611.0, 612.0, 613.0, 614.0, 615.0, 616.0, 617.0, 618.0, 619.0, 620.0, 621.0, 622.0, 623.0, 624.0, 625.0, 626.0, 627.0, 628.0, 629.0, 630.0, 631.0, 632.0, 633.0, 634.0, 635.0, 636.0, 637.0, 638.0, 639.0, 640.0, 641.0, 642.0, 643.0, 644.0, 645.0, 646.0, 647.0, 648.0, 649.0, 650.0, 651.0, 652.0, 653.0, 654.0, 655.0, 656.0, 657.0, 658.0, 659.0, 660.0, 661.0, 662.0, 663.0, 664.0, 665.0, 666.0, 667.0, 668.0, 669.0, 670.0, 671.0, 672.0, 673.0, 674.0, 675.0, 676.0, 677.0, 678.0, 679.0, 680.0, 681.0, 682.0, 683.0, 684.0, 685.0, 686.0, 687.0, 688.0, 689.0, 690.0, 691.0, 692.0, 693.0, 694.0, 695.0, 696.0, 697.0, 698.0, 699.0, 700.0, 701.0, 702.0, 703.0, 704.0, 705.0, 706.0, 707.0, 708.0, 709.0, 710.0, 711.0, 712.0, 713.0, 714.0, 715.0, 716.0, 717.0, 718.0, 719.0, 720.0, 721.0, 722.0, 723.0, 724.0, 725.0, 726.0, 727.0, 728.0, 729.0, 730.0, 731.0, 732.0, 733.0, 734.0, 735.0, 736.0, 737.0, 738.0, 739.0, 740.0, 741.0, 742.0, 743.0, 744.0, 745.0, 746.0, 747.0, 748.0, 749.0, 750.0, 751.0, 752.0, 753.0, 754.0, 755.0, 756.0, 757.0, 758.0, 759.0, 760.0, 761.0, 762.0, 763.0, 764.0, 765.0, 766.0, 767.0, 768.0, 769.0, 770.0, 771.0, 772.0, 773.0, 774.0, 775.0, 776.0, 777.0, 778.0, 779.0, 780.0, 781.0, 782.0, 783.0, 784.0, 785.0, 786.0, 787.0, 788.0, 789.0, 790.0, 791.0, 792.0, 793.0, 794.0, 795.0, 796.0, 797.0, 798.0, 799.0, 800.0, 801.0, 802.0, 803.0, 804.0, 805.0, 806.0, 807.0, 808.0, 809.0, 810.0, 811.0, 812.0, 813.0, 814.0, 815.0, 816.0, 817.0, 818.0, 819.0, 820.0, 821.0, 822.0, 823.0, 824.0, 825.0, 826.0, 827.0, 828.0, 829.0, 830.0],
 [
  61.5, 62.23, 62.96, 63.69, 64.42, 65.15, 65.88, 66.61, 67.34, 68.07, 68.8, 68.26, 67.72, 67.18, 66.64, 66.1, 65.56, 65.02, 64.48, 63.94, 63.4, 63.64, 63.88, 64.12, 64.36, 64.6, 64.84, 65.08, 65.32, 65.56, 65.8, 68.7, 71.6, 74.5, 77.4, 80.3, 83.2, 86.1, 89.0, 91.9, 94.8, 95.8, 96.8, 97.8, 98.8, 99.8, 100.8, 101.8, 102.8, 103.8, 104.8, 104.91, 105.02, 105.13, 105.24, 105.35, 105.46, 105.57, 105.68, 105.79, 105.9, 104.99, 104.08, 103.17, 102.26, 101.35, 100.44, 99.53, 98.62, 97.71, 96.8, 98.51, 100.22, 101.93, 103.64, 105.35, 107.06, 108.77, 110.48, 112.19, 113.9, 115.07, 116.24, 117.41, 118.58, 119.75, 120.92, 122.09, 123.26, 124.43, 125.6, 125.59, 125.58, 125.57, 125.56, 125.55, 125.54, 125.53, 125.52, 125.51, 125.5, 125.08, 124.66, 124.24, 123.82, 123.4, 122.98, 122.56, 122.14, 121.72, 121.3, 121.3, 121.3, 121.3, 121.3, 121.3, 121.3, 121.3, 121.3, 121.3, 121.3, 120.52, 119.74, 118.96, 118.18, 117.4, 116.62, 115.84, 115.06, 114.28, 113.5, 113.46, 113.42, 113.38, 113.34, 113.3, 113.26, 113.22, 113.18, 113.14, 113.1, 112.87, 112.64, 112.41, 112.18, 111.95, 111.72, 111.49, 111.26, 111.03, 110.8, 110.37, 109.94, 109.51, 109.08, 108.65, 108.22, 107.79, 107.36, 106.93, 106.5, 106.73, 106.96, 107.19, 107.42, 107.65, 107.88, 108.11, 108.34, 108.57, 108.8, 108.45, 108.1, 107.75, 107.4, 107.05, 106.7, 106.35, 106.0, 105.65, 105.3, 105.21, 105.12, 105.03, 104.94, 104.85, 104.76, 104.67, 104.58, 104.49, 104.4, 103.96, 103.52, 103.08, 102.64, 102.2, 101.76, 101.32, 100.88, 100.44, 100.0, 99.6, 99.2, 98.8, 98.4, 98.0, 97.6, 97.2, 96.8, 96.4, 96.0, 95.91, 95.82, 95.73, 95.64, 95.55, 95.46, 95.37, 95.28, 95.19, 95.1, 94.5, 93.9, 93.3, 92.7, 92.1, 91.5, 90.9, 90.3, 89.7, 89.1, 89.24, 89.38, 89.52, 89.66, 89.8, 89.94, 90.08, 90.22, 90.36, 90.5, 90.48, 90.46, 90.44, 90.42, 90.4, 90.38, 90.36, 90.34, 90.32, 90.3, 90.11, 89.92, 89.73, 89.54, 89.35, 89.16, 88.97, 88.78, 88.59, 88.4, 87.96, 87.52, 87.08, 86.64, 86.2, 85.76, 85.32, 84.88, 84.44, 84.0, 84.11, 84.22, 84.33, 84.44, 84.55, 84.66, 84.77, 84.88, 84.99, 85.1, 84.78, 84.46, 84.14, 83.82, 83.5, 83.18, 82.86, 82.54, 82.22, 81.9, 81.97, 82.04, 82.11, 82.18, 82.25, 82.32, 82.39, 82.46, 82.53, 82.6, 82.83, 83.06, 83.29, 83.52, 83.75, 83.98, 84.21, 84.44, 84.67, 84.9, 84.54, 84.18, 83.82, 83.46, 83.1, 82.74, 82.38, 82.02, 81.66, 81.3, 80.36, 79.42, 78.48, 77.54, 76.6, 75.66, 74.72, 73.78, 72.84, 71.9, 72.14, 72.38, 72.62, 72.86, 73.1, 73.34, 73.58, 73.82, 74.06, 74.3, 74.51, 74.72, 74.93, 75.14, 75.35, 75.56, 75.77, 75.98, 76.19, 76.4, 75.09, 73.78, 72.47, 71.16, 69.85, 68.54, 67.23, 65.92, 64.61, 63.3, 64.14, 64.98, 65.82, 66.66, 67.5, 68.34, 69.18, 70.02, 70.86, 71.7, 72.23, 72.76, 73.29, 73.82, 74.35, 74.88, 75.41, 75.94, 76.47, 77.0, 75.82, 74.64, 73.46, 72.28, 71.1, 69.92, 68.74, 67.56, 66.38, 65.2, 63.45, 61.7, 59.95, 58.2, 56.45, 54.7, 52.95, 51.2, 49.45, 47.7, 49.79, 51.88, 53.97, 56.06, 58.15, 60.24, 62.33, 64.42, 66.51, 68.6, 68.24, 67.88, 67.52, 67.16, 66.8, 66.44, 66.08, 65.72, 65.36, 65.0, 65.1, 65.2, 65.3, 65.4, 65.5, 65.6, 65.7, 65.8, 65.9, 66.0, 65.5, 65.0, 64.5, 64.0, 63.5, 63.0, 62.5, 62.0, 61.5, 61.0, 60.23, 59.46, 58.69, 57.92, 57.15, 56.38, 55.61, 54.84, 54.07, 53.3, 53.86, 54.42, 54.98, 55.54, 56.1, 56.66, 57.22, 57.78, 58.34, 58.9, 59.2, 59.5, 59.8, 60.1, 60.4, 60.7, 61.0, 61.3, 61.6, 61.9],
 [
  38.0, 38.44, 38.88, 39.32, 39.76, 40.2, 40.64, 41.08, 41.52, 41.96, 42.4, 42.01, 41.62, 41.23, 40.84, 40.45, 40.06, 39.67, 39.28, 38.89, 38.5, 38.15, 37.8, 37.45, 37.1, 36.75, 36.4, 36.05, 35.7, 35.35, 35.0, 35.84, 36.68, 37.52, 38.36, 39.2, 40.04, 40.88, 41.72, 42.56, 43.4, 43.69, 43.98, 44.27, 44.56, 44.85, 45.14, 45.43, 45.72, 46.01, 46.3, 46.06, 45.82, 45.58, 45.34, 45.1, 44.86, 44.62, 44.38, 44.14, 43.9, 43.22, 42.54, 41.86, 41.18, 40.5, 39.82, 39.14, 38.46, 37.78, 37.1, 37.06, 37.02, 36.98, 36.94, 36.9, 36.86, 36.82, 36.78, 36.74, 36.7, 36.62, 36.54, 36.46, 36.38, 36.3, 36.22, 36.14, 36.06, 35.98, 35.9, 35.57, 35.24, 34.91, 34.58, 34.25, 33.92, 33.59, 33.26, 32.93, 32.6, 32.13, 31.66, 31.19, 30.72, 30.25, 29.78, 29.31, 28.84, 28.37, 27.9, 27.54, 27.18, 26.82, 26.46, 26.1, 25.74, 25.38, 25.02, 24.66, 24.3, 23.88, 23.46, 23.04, 22.62, 22.2, 21.78, 21.36, 20.94, 20.52, 20.1, 19.71, 19.32, 18.93, 18.54, 18.15, 17.76, 17.37, 16.98, 16.59, 16.2, 15.9, 15.6, 15.3, 15.0, 14.7, 14.4, 14.1, 13.8, 13.5, 13.2, 12.74, 12.28, 11.82, 11.36, 10.9, 10.44, 9.98, 9.52, 9.06, 8.6, 8.35, 8.1, 7.85, 7.6, 7.35, 7.1, 6.85, 6.6, 6.35, 6.1, 5.91, 5.72, 5.53, 5.34, 5.15, 4.96, 4.77, 4.58, 4.39, 4.2, 3.97, 3.74, 3.51, 3.28, 3.05, 2.82, 2.59, 2.36, 2.13, 1.9, 1.71, 1.52, 1.33, 1.14, 0.95, 0.76, 0.57, 0.38, 0.19, 0.0, -0.16, -0.32, -0.48, -0.64, -0.8, -0.96, -1.12, -1.28, -1.44, -1.6, -1.79, -1.98, -2.17, -2.36, -2.55, -2.74, -2.93, -3.12, -3.31, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.5, -3.73, -3.96, -4.19, -4.42, -4.65, -4.88, -5.11, -5.34, -5.57, -5.8, -5.94, -6.08, -6.22, -6.36, -6.5, -6.64, -6.78, -6.92, -7.06, -7.2, -7.34, -7.48, -7.62, -7.76, -7.9, -8.04, -8.18, -8.32, -8.46, -8.6, -8.69, -8.78, -8.87, -8.96, -9.05, -9.14, -9.23, -9.32, -9.41, -9.5, -9.64, -9.78, -9.92, -10.06, -10.2, -10.34, -10.48, -10.62, -10.76, -10.9, -10.88, -10.86, -10.84, -10.82, -10.8, -10.78, -10.76, -10.74, -10.72, -10.7, -10.83, -10.96, -11.09, -11.22, -11.35, -11.48, -11.61, -11.74, -11.87, -12.0, -12.2, -12.4, -12.6, -12.8, -13.0, -13.2, -13.4, -13.6, -13.8, -14.0, -13.96, -13.92, -13.88, -13.84, -13.8, -13.76, -13.72, -13.68, -13.64, -13.6, -13.44, -13.28, -13.12, -12.96, -12.8, -12.64, -12.48, -12.32, -12.16, -12.0, -12.13, -12.26, -12.39, -12.52, -12.65, -12.78, -12.91, -13.04, -13.17, -13.3, -13.26, -13.22, -13.18, -13.14, -13.1, -13.06, -13.02, -12.98, -12.94, -12.9, -12.67, -12.44, -12.21, -11.98, -11.75, -11.52, -11.29, -11.06, -10.83, -10.6, -10.7, -10.8, -10.9, -11.0, -11.1, -11.2, -11.3, -11.4, -11.5, -11.6, -11.66, -11.72, -11.78, -11.84, -11.9, -11.96, -12.02, -12.08, -12.14, -12.2, -12.0, -11.8, -11.6, -11.4, -11.2, -11.0, -10.8, -10.6, -10.4, -10.2, -9.96, -9.72, -9.48, -9.24, -9.0, -8.76, -8.52, -8.28, -8.04, -7.8, -8.14, -8.48, -8.82, -9.16, -9.5, -9.84, -10.18, -10.52, -10.86, -11.2, -11.12, -11.04, -10.96, -10.88, -10.8, -10.72, -10.64, -10.56, -10.48, -10.4, -10.42, -10.44, -10.46, -10.48, -10.5, -10.52, -10.54, -10.56, -10.58, -10.6, -10.51, -10.42, -10.33, -10.24, -10.15, -10.06, -9.97, -9.88, -9.79, -9.7, -9.56, -9.42, -9.28, -9.14, -9.0, -8.86, -8.72, -8.58, -8.44, -8.3, -8.4, -8.5, -8.6, -8.7, -8.8, -8.9, -9.0, -9.1, -9.2, -9.3, -9.35, -9.4, -9.45, -9.5, -9.55, -9.6, -9.65, -9.7, -9.75, -9.8],
 [
  5.3, 5.38, 5.46, 5.54, 5.62, 5.7, 5.78, 5.86, 5.94, 6.02, 6.1, 5.79, 5.48, 5.17, 4.86, 4.55, 4.24, 3.93, 3.62, 3.31, 3.0, 2.82, 2.64, 2.46, 2.28, 2.1, 1.92, 1.74, 1.56, 1.38, 1.2, 0.97, 0.74, 0.51, 0.28, 0.05, -0.18, -0.41, -0.64, -0.87, -1.1, -1.04, -0.98, -0.92, -0.86, -0.8, -0.74, -0.68, -0.62, -0.56, -0.5, -0.52, -0.54, -0.56, -0.58, -0.6, -0.62, -0.64, -0.66, -0.68, -0.7, -0.75, -0.8, -0.85, -0.9, -0.95, -1.0, -1.05, -1.1, -1.15, -1.2, -1.34, -1.48, -1.62, -1.76, -1.9, -2.04, -2.18, -2.32, -2.46, -2.6, -2.63, -2.66, -2.69, -2.72, -2.75, -2.78, -2.81, -2.84, -2.87, -2.9, -2.89, -2.88, -2.87, -2.86, -2.85, -2.84, -2.83, -2.82, -2.81, -2.8, -2.78, -2.76, -2.74, -2.72, -2.7, -2.68, -2.66, -2.64, -2.62, -2.6, -2.6, -2.6, -2.6, -2.6, -2.6, -2.6, -2.6, -2.6, -2.6, -2.6, -2.52, -2.44, -2.36, -2.28, -2.2, -2.12, -2.04, -1.96, -1.88, -1.8, -1.77, -1.74, -1.71, -1.68, -1.65, -1.62, -1.59, -1.56, -1.53, -1.5, -1.48, -1.46, -1.44, -1.42, -1.4, -1.38, -1.36, -1.34, -1.32, -1.3, -1.29, -1.28, -1.27, -1.26, -1.25, -1.24, -1.23, -1.22, -1.21, -1.2, -1.18, -1.16, -1.14, -1.12, -1.1, -1.08, -1.06, -1.04, -1.02, -1.0, -0.95, -0.9, -0.85, -0.8, -0.75, -0.7, -0.65, -0.6, -0.55, -0.5, -0.48, -0.46, -0.44, -0.42, -0.4, -0.38, -0.36, -0.34, -0.32, -0.3, -0.27, -0.24, -0.21, -0.18, -0.15, -0.12, -0.09, -0.06, -0.03, 0.0, 0.02, 0.04, 0.06, 0.08, 0.1, 0.12, 0.14, 0.16, 0.18, 0.2, 0.23, 0.26, 0.29, 0.32, 0.35, 0.38, 0.41, 0.44, 0.47, 0.5, 0.66, 0.82, 0.98, 1.14, 1.3, 1.46, 1.62, 1.78, 1.94, 2.1, 2.21, 2.32, 2.43, 2.54, 2.65, 2.76, 2.87, 2.98, 3.09, 3.2, 3.29, 3.38, 3.47, 3.56, 3.65, 3.74, 3.83, 3.92, 4.01, 4.1, 4.16, 4.22, 4.28, 4.34, 4.4, 4.46, 4.52, 4.58, 4.64, 4.7, 4.74, 4.78, 4.82, 4.86, 4.9, 4.94, 4.98, 5.02, 5.06, 5.1, 5.26, 5.42, 5.58, 5.74, 5.9, 6.06, 6.22, 6.38, 6.54, 6.7, 6.76, 6.82, 6.88, 6.94, 7.0, 7.06, 7.12, 7.18, 7.24, 7.3, 7.43, 7.56, 7.69, 7.82, 7.95, 8.08, 8.21, 8.34, 8.47, 8.6, 8.72, 8.84, 8.96, 9.08, 9.2, 9.32, 9.44, 9.56, 9.68, 9.8, 9.84, 9.88, 9.92, 9.96, 10.0, 10.04, 10.08, 10.12, 10.16, 10.2, 10.01, 9.82, 9.63, 9.44, 9.25, 9.06, 8.87, 8.68, 8.49, 8.3, 8.43, 8.56, 8.69, 8.82, 8.95, 9.08, 9.21, 9.34, 9.47, 9.6, 9.49, 9.38, 9.27, 9.16, 9.05, 8.94, 8.83, 8.72, 8.61, 8.5, 8.35, 8.2, 8.05, 7.9, 7.75, 7.6, 7.45, 7.3, 7.15, 7.0, 7.06, 7.12, 7.18, 7.24, 7.3, 7.36, 7.42, 7.48, 7.54, 7.6, 7.64, 7.68, 7.72, 7.76, 7.8, 7.84, 7.88, 7.92, 7.96, 8.0, 7.87, 7.74, 7.61, 7.48, 7.35, 7.22, 7.09, 6.96, 6.83, 6.7, 6.55, 6.4, 6.25, 6.1, 5.95, 5.8, 5.65, 5.5, 5.35, 5.2, 5.42, 5.64, 5.86, 6.08, 6.3, 6.52, 6.74, 6.96, 7.18, 7.4, 7.34, 7.28, 7.22, 7.16, 7.1, 7.04, 6.98, 6.92, 6.86, 6.8, 6.82, 6.84, 6.86, 6.88, 6.9, 6.92, 6.94, 6.96, 6.98, 7.0, 6.94, 6.88, 6.82, 6.76, 6.7, 6.64, 6.58, 6.52, 6.46, 6.4, 6.31, 6.22, 6.13, 6.04, 5.95, 5.86, 5.77, 5.68, 5.59, 5.5, 5.56, 5.62, 5.68, 5.74, 5.8, 5.86, 5.92, 5.98, 6.04, 6.1, 6.14, 6.18, 6.22, 6.26, 6.3, 6.34, 6.38, 6.42, 6.46, 6.5]])
_INTERP_TYPES = {'linear':[
  'rfl', 'RFL', 'r', 'R', 'xyzbar', 'cmf', 'lms', 'undefined'], 
 'cubic':['S', 'spd', 'SPD', 'Le'],  'none':None}
_S_INTERP_TYPE = 'cubic'
_R_INTERP_TYPE = 'linear'
_CRI_REF_TYPE = 'ciera'
_CRI_REF_TYPES = {'ciera':[5000.0, 5000.0],  'cierf':[4000.0, 5000.0],  'cierf-224-2017':[4000.0, 5000.0],  'iesrf':[
  4000.0, 5000.0], 
 'iesrf-tm30-15':[4500.0, 5500.0],  'iesrf-tm30-18':[4000.0, 5000.0],  'BB':[
  5000.0, 5000.0], 
 'DL':[5000.0, 5000.0]}

def getwlr(wl3=None):
    """
    Get/construct a wavelength range from a 3-vector (start, stop, spacing).
    
    Args:
        :wl3: 
            | list[start, stop, spacing], optional 
            | (defaults to luxpy._WL3)

    Returns:
        :returns: 
            | ndarray (.shape = (n,)) with n wavelengths ranging from
              start to stop, with wavelength interval equal to spacing.
    """
    if wl3 is None:
        wl3 = _WL3
    else:
        if len(wl3) == 3:
            wl = np.linspace(wl3[0], wl3[1], int(np.floor((wl3[1] - wl3[0] + wl3[2]) / wl3[2])))
        else:
            wl = wl3
    return wl


def getwld(wl):
    """
    Get wavelength spacing. 
    
    Args:
        :wl: 
            | ndarray with wavelengths
        
    Returns:
        :returns: 
            | - float:  for equal wavelength spacings
            | - ndarray (.shape = (n,)): for unequal wavelength spacings
    """
    d = np.diff(wl)
    dl = np.hstack((d[0], d[0:-1] / 2.0, d[(-1)])) + np.hstack((0.0, d[1:] / 2.0, 0.0))
    if np.array_equal(dl, dl.mean() * np.ones(dl.shape)):
        dl = dl[0]
    return dl


def spd_normalize(data, norm_type=None, norm_f=1, wl=True, cieobs=_CIEOBS):
    """
    Normalize a spectral power distribution (SPD).
    
    Args:
        :data: 
            | ndarray
        :norm_type: 
            | None, optional 
            |       - 'lambda': make lambda in norm_f equal to 1
            |       - 'area': area-normalization times norm_f
            |       - 'max': max-normalization times norm_f
            |       - 'ru': to :norm_f: radiometric units 
            |       - 'pu': to :norm_f: photometric units 
            |       - 'pusa': to :norm_f: photometric units (with Km corrected
            |                             to standard air, cfr. CIE TN003-2015)
            |       - 'qu': to :norm_f: quantal energy units
        :norm_f:
            | 1, optional
            | Normalization factor that determines the size of normalization 
              for 'max' and 'area' 
              or which wavelength is normalized to 1 for 'lambda' option.
        :wl: 
            | True or False, optional 
            | If True, the first column of data contains wavelengths.
        :cieobs:
            | _CIEOBS or str, optional
            | Type of cmf set to use for normalization using photometric units 
              (norm_type == 'pu')
    
    Returns:
        :returns: 
            | ndarray with normalized data.
    """
    if norm_type is not None:
        if not isinstance(norm_type, list):
            norm_type = [
             norm_type]
        else:
            if norm_f is not None:
                if not isinstance(norm_f, list):
                    norm_f = [
                     norm_f]
            else:
                if 'lambda' in norm_type:
                    wl = True
                    wlr = data[0]
                if 'qu' in norm_type:
                    wl = True
                    wlr = data[0]
            if (('area' in norm_type) | ('ru' in norm_type) | ('pu' in norm_type) | ('pusa' in norm_type)) & (wl == True):
                dl = getwld(data[0])
            else:
                dl = 1
        offset = int(wl)
        for i in range(data.shape[0] - offset):
            if len(norm_type) > 1:
                norm_type_ = norm_type[i]
            else:
                norm_type_ = norm_type[0]
            if norm_f is not None:
                if len(norm_f) > 1:
                    norm_f_ = norm_f[i]
                else:
                    norm_f_ = norm_f[0]
            else:
                if norm_type_ == 'lambda':
                    norm_f_ = 560.0
                else:
                    norm_f_ = 1.0
                if norm_type_ == 'max':
                    data[i + offset] = norm_f_ * data[(i + offset)] / np.max(data[(i + offset)])
                elif norm_type_ == 'area':
                    data[i + offset] = norm_f_ * data[(i + offset)] / (np.sum(data[(i + offset)]) * dl)
                else:
                    if norm_type_ == 'lambda':
                        wl_index = np.abs(wlr - norm_f_).argmin()
                        data[i + offset] = data[(i + offset)] / data[(i + offset)][wl_index]
                    else:
                        if (norm_type_ == 'ru') | (norm_type_ == 'pu') | (norm_type == 'pusa') | (norm_type_ == 'qu'):
                            rpq_power = spd_to_power((data[[0, i + offset], :]), cieobs=cieobs, ptype=norm_type_)
                            data[i + offset] = norm_f / rpq_power * data[(i + offset)]
                        else:
                            data[i + offset] = data[(i + offset)] / norm_f_

    return data


def cie_interp(data, wl_new, kind=None, negative_values_allowed=False, extrap_values=None):
    """
    Interpolate / extrapolate spectral data following standard CIE15-2018.
    
    | The kind of interpolation depends on the spectrum type defined in :kind:. 
    | Extrapolation is always done by replicate the closest known values.
    
    Args:
        :data: 
            | ndarray with spectral data 
            | (.shape = (number of spectra + 1, number of original wavelengths))
        :wl_new: 
            | ndarray with new wavelengths
        :kind: 
            | None, optional
            |   - If :kind: is None, return original data.
            |   - If :kind: is a spectrum type (see _INTERP_TYPES), the correct 
            |     interpolation type if automatically chosen.
            |   - Or :kind: can be any interpolation type supported by 
            |     luxpy.math.interp1
        :negative_values_allowed: 
            | False, optional
            | If False: negative values are clipped to zero.
        :extrap_values:
            | None, optional
            | If None: use CIE recommended 'closest value' approach when extrapolating.
            | If float or list or ndarray, use those values to fill extrapolated value(s).
            | If 'ext': use normal extrapolated values by math.interp1
    
    Returns:
        :returns: 
            | ndarray of interpolated spectral data.
              (.shape = (number of spectra + 1, number of wavelength in wl_new))
    """
    if kind is not None:
        wl_new = getwlr(wl_new)
        if (not np.array_equal(data[0], wl_new)) | np.isnan(data).any():
            extrap_values = np.atleast_1d(extrap_values)
            if kind in _INTERP_TYPES['linear']:
                kind = 'linear'
            else:
                if kind in _INTERP_TYPES['cubic']:
                    kind = 'cubic'
                wl = np.array(data[0])
                S = data[1:]
                wl_new = np.array(wl_new)
                N = S.shape[0]
                Si = np.ones([N, wl_new.shape[0]]) * np.nan
                for i in range(N):
                    nan_indices = np.isnan(S[i])
                    if nan_indices.any():
                        nonan_indices = np.logical_not(nan_indices)
                        wl_nonan = wl[nonan_indices]
                        S_i_nonan = S[i][nonan_indices]
                        Si_nonan = math.interp1(wl_nonan, S_i_nonan, wl_new, kind=kind, ext='extrapolate')
                        if extrap_values[0] is None:
                            Si_nonan[wl_new < wl_nonan[0]] = S_i_nonan[0]
                            Si_nonan[wl_new > wl_nonan[(-1)]] = S_i_nonan[(-1)]
                        elif (type(extrap_values[0]) == np.str_) | (type(extrap_values[0]) == str) and extrap_values[0][:3] == 'ext':
                            pass
                        else:
                            Si_nonan[wl_new < wl_nonan[0]] = extrap_values[0]
                            Si_nonan[wl_new > wl_nonan[(-1)]] = extrap_values[(-1)]
                        Si[i] = Si_nonan
                    else:
                        Si[i] = math.interp1(wl, (S[i]), wl_new, kind=kind, ext='extrapolate')
                        if extrap_values[0] is None:
                            Si[i][wl_new < wl[0]] = S[i][0]
                            Si[i][wl_new > wl[(-1)]] = S[i][(-1)]
                        else:
                            if (type(extrap_values[0]) == np.str_) | (type(extrap_values[0]) == str):
                                if extrap_values[0][:3] == 'ext':
                                    continue
                            Si[i][wl_new < wl[0]] = extrap_values[0]
                            Si[i][wl_new > wl[(-1)]] = extrap_values[(-1)]

                if negative_values_allowed == False:
                    if np.any(Si):
                        Si[Si < 0.0] = 0.0
                return np.vstack((wl_new, Si))
    return data


def spd(data=None, interpolation=None, kind='np', wl=None, columns=None, sep=',', header=None, datatype='S', norm_type=None, norm_f=None):
    """
    | All-in-one function that can:
    |    1. Read spectral data from data file or take input directly 
         as pandas.dataframe or ndarray.
    |    2. Convert spd-like data from ndarray to pandas.dataframe and back.
    |    3. Interpolate spectral data.
    |    4. Normalize spectral data.
            
    Args:
        :data: 
            | - str with path to file containing spectral data
            | - ndarray with spectral data
            | - pandas.dataframe with spectral data
            | (.shape = (number of spectra + 1, number of original wavelengths))
        :interpolation:
            | None, optional
            | - None: don't interpolate
            | - str with interpolation type or spectrum type
        :kind: 
            | str ['np','df'], optional 
            | Determines type(:returns:), np: ndarray, df: pandas.dataframe
        :wl: 
            | None, optional
            | New wavelength range for interpolation. 
            | Defaults to wavelengths specified by luxpy._WL3.
        :columns: 
            | -  None or list[str] of column names for dataframe, optional
        :header: 
            | None or 'infer', optional
            | - None: no header in file
            | - 'infer': infer headers from file
        :sep: 
            | ',' or '  ' or other char, optional
            | Column separator in case :data: specifies a data file. 
        :datatype': 
            | 'S' (light source) or 'R' (reflectance) or other, optional
            | Specifies a type of spectral data. 
            | Is used when creating column headers when :column: is None.
        :norm_type: 
            | None, optional 
            |       - 'lambda': make lambda in norm_f equal to 1
            |       - 'area': area-normalization times norm_f
            |       - 'max': max-normalization times norm_f
            |       - 'ru': to :norm_f: radiometric units 
            |       - 'pu': to :norm_f: photometric units 
            |       - 'pusa': to :norm_f: photometric units (with Km corrected
            |                             to standard air, cfr. CIE TN003-2015)
            |       - 'qu': to :norm_f: quantal energy units
        :norm_f:
            | 1, optional
            | Normalization factor that determines the size of normalization 
              for 'max' and 'area' 
              or which wavelength is normalized to 1 for 'lambda' option.
    
    Returns:
        :returns: 
            | ndarray or pandas.dataframe 
            | with interpolated and/or normalized spectral data.
    """
    if isinstance(data, str):
        transpose = True
    else:
        transpose = False
    wl = getwlr(wl)
    if data is not None:
        if (interpolation is None) & (norm_type is None):
            data = getdata(data=data, kind='np', columns=columns, sep=sep, header=header, datatype=datatype)
            if transpose == True:
                data = data.T
        else:
            data = getdata(data=data, kind='np', columns=columns, sep=sep, header=header, datatype=datatype)
            if transpose == True:
                data = data.T
            data = cie_interp(data=data, wl_new=wl, kind=interpolation)
            data = spd_normalize(data, norm_type=norm_type, norm_f=norm_f, wl=True)
        if isinstance(data, pd.DataFrame):
            columns = data.columns
    else:
        data = np2d(wl)
    if data.shape[0] - 1 == 0:
        columns = None
    if kind == 'df':
        data = data.T
    data = getdata(data=data, kind=kind, columns=columns, datatype=datatype)
    return data


def xyzbar(cieobs=_CIEOBS, scr='dict', wl_new=None, norm_type=None, norm_f=None, kind='np'):
    """
    Get color matching functions.  
    
    Args:
        :cieobs: 
            | luxpy._CIEOBS, optional
            | Sets the type of color matching functions to load.
        :scr: 
            | 'dict' or 'file', optional
            | Determines whether to load cmfs from file (./data/cmfs/) 
              or from dict defined in .cmf.py
        :wl: 
            | None, optional
            | New wavelength range for interpolation. 
            | Defaults to wavelengths specified by luxpy._WL3.
        :norm_type: 
            | None, optional 
            |       - 'lambda': make lambda in norm_f equal to 1
            |       - 'area': area-normalization times norm_f
            |       - 'max': max-normalization times norm_f
            |       - 'ru': to :norm_f: radiometric units 
            |       - 'pu': to :norm_f: photometric units 
            |       - 'pusa': to :norm_f: photometric units (with Km corrected
            |                             to standard air, cfr. CIE TN003-2015)
            |       - 'qu': to :norm_f: quantal energy units
        :norm_f:
            | 1, optional
            | Normalization factor that determines the size of normalization 
              for 'max' and 'area' 
              or which wavelength is normalized to 1 for 'lambda' option.
        :kind: 
            | str ['np','df'], optional 
            | Determines type(:returns:), np: ndarray, df: pandas.dataframe

    Returns:
        :returns: 
            | ndarray or pandas.dataframe with CMFs 
        
            
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    """
    if scr is 'file':
        dict_or_file = _PKG_PATH + _SEP + 'data' + _SEP + 'cmfs' + _SEP + 'ciexyz_' + cieobs + '.dat'
    else:
        if scr is 'dict':
            dict_or_file = _CMF[cieobs]['bar']
        else:
            if scr == 'cieobs':
                dict_or_file = cieobs
    return spd(data=dict_or_file, wl=wl_new, interpolation='linear', kind=kind, columns=['wl', 'xb', 'yb', 'zb'])


def vlbar(cieobs=_CIEOBS, scr='dict', wl_new=None, norm_type=None, norm_f=None, kind='np', out=1):
    """
    Get Vlambda functions.  
    
    Args:
        :cieobs: 
            | str, optional
            | Sets the type of Vlambda function to obtain.
        :scr: 
            | 'dict' or array, optional
            | - 'dict': get from ybar from _CMF
            | - 'array': ndarray in :cieobs:
            | Determines whether to load cmfs from file (./data/cmfs/) 
              or from dict defined in .cmf.py
            | Vlambda is obtained by collecting Ybar.
        :wl: 
            | None, optional
            | New wavelength range for interpolation. 
            | Defaults to wavelengths specified by luxpy._WL3.
        :norm_type: 
            | None, optional 
            |       - 'lambda': make lambda in norm_f equal to 1
            |       - 'area': area-normalization times norm_f
            |       - 'max': max-normalization times norm_f
            |       - 'ru': to :norm_f: radiometric units 
            |       - 'pu': to :norm_f: photometric units 
            |       - 'pusa': to :norm_f: photometric units (with Km corrected
            |                             to standard air, cfr. CIE TN003-2015)
            |       - 'qu': to :norm_f: quantal energy units
        :norm_f:
            | 1, optional
            | Normalization factor that determines the size of normalization 
              for 'max' and 'area' 
              or which wavelength is normalized to 1 for 'lambda' option.
        :kind: 
            | str ['np','df'], optional 
            | Determines type(:returns:), np: ndarray, df: pandas.dataframe
        :out: 
            | 1 or 2, optional
            |     1: returns Vlambda
            |     2: returns (Vlambda, Km)
    
    Returns:
        :returns: 
            | dataframe or ndarray with Vlambda of type :cieobs: 
        
            
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    """
    if scr == 'dict':
        dict_or_file = _CMF[cieobs]['bar'][[0, 2], :]
        K = _CMF[cieobs]['K']
    else:
        if scr is 'vltype':
            dict_or_file = cieobs
            K = 1
    Vl = spd(data=dict_or_file, wl=wl_new, interpolation='linear', kind=kind, columns=['wl', 'Vl'])
    if out == 2:
        return (Vl, K)
    else:
        return Vl


def spd_to_xyz(data, relative=True, rfl=None, cieobs=_CIEOBS, K=None, out=None, cie_std_dev_obs=None):
    """
    Calculates xyz tristimulus values from spectral data.
       
    Args: 
        :data: 
            | ndarray or pandas.dataframe with spectral data
            | (.shape = (number of spectra + 1, number of wavelengths))
            | Note that :data: is never interpolated, only CMFs and RFLs. 
            | This way interpolation errors due to peaky spectra are avoided. 
              Conform CIE15-2018.
        :relative: 
            | True or False, optional
            | Calculate relative XYZ (Yw = 100) or absolute XYZ (Y = Luminance)
        :rfl: 
            | ndarray with spectral reflectance functions.
            | Will be interpolated if wavelengths do not match those of :data:
        :cieobs:
            | luxpy._CIEOBS or str, optional
            | Determines the color matching functions to be used in the 
              calculation of XYZ.
        :K: 
            | None, optional
            |   e.g.  K  = 683 lm/W for '1931_2' (relative == False) 
            |   or K = 100/sum(spd*dl)        (relative == True)
        :out:
            | None or 1 or 2, optional
            | Determines number and shape of output. (see :returns:)
        :cie_std_dev_obs: 
            | None or str, optional
            | - None: don't use CIE Standard Deviate Observer function.
            | - 'f1': use F1 function.
    
    Returns:
        :returns:
            | If rfl is None:
            |    If out is None: ndarray of xyz values 
            |        (.shape = (data.shape[0],3))
            |    If out == 1: ndarray of xyz values 
            |        (.shape = (data.shape[0],3))
            |    If out == 2: (ndarray of xyz, ndarray of xyzw) values
            |        Note that xyz == xyzw, with (.shape = (data.shape[0],3))
            | If rfl is not None:
            |   If out is None: ndarray of xyz values 
            |         (.shape = (rfl.shape[0],data.shape[0],3))
            |   If out == 1: ndarray of xyz values 
            |       (.shape = (rfl.shape[0]+1,data.shape[0],3))
            |        The xyzw values of the light source spd are the first set 
            |        of values of the first dimension. The following values 
            |       along this dimension are the sample (rfl) xyz values.
            |    If out == 2: (ndarray of xyz, ndarray of xyzw) values
            |        with xyz.shape = (rfl.shape[0],data.shape[0],3)
            |        and with xyzw.shape = (data.shape[0],3)
             
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    """
    if isinstance(data, pd.DataFrame):
        data = getdata(data, kind='np')
    else:
        data = np2d(data)
    dl = getwld(data[0])
    if isinstance(cieobs, str):
        if K is None:
            K = _CMF[cieobs]['K']
        scr = 'dict'
    else:
        scr = 'cieobs'
        if (K is None) & (relative == False):
            K = 1
        cmf = xyzbar(cieobs=cieobs, scr=scr, wl_new=(data[0]), kind='np')
        if cie_std_dev_obs is not None:
            cmf_cie_std_dev_obs = xyzbar(cieobs=('cie_std_dev_obs_' + cie_std_dev_obs.lower()), scr=scr, wl_new=(data[0]), kind='np')
            cmf[1:] = cmf[1:] + cmf_cie_std_dev_obs[1:]
        if rfl is not None:
            rfl = cie_interp(data=(np2d(rfl)), wl_new=(data[0]), kind='rfl')
            rfl = np.concatenate((np.ones((1, data.shape[1])), rfl[1:]))
            rflwasnotnone = 1
        else:
            rfl = np.ones((1, data.shape[1]))
            rflwasnotnone = 0
        if rflwasnotnone == 1:
            if relative == True:
                K = 100.0 / np.dot(data[1:], cmf[2, :] * dl)
            xyz = K * np.array([np.dot(rfl, (data[1:] * cmf[i + 1, :] * dl).T) for i in range(3)])
        else:
            if relative == True:
                K = 100.0 / np.dot(data[1:], (cmf[2, :] * dl).T)
            xyz = K * np.dot(cmf[1:] * dl, data[1:].T)[:, None, :]
    xyz = np.transpose(xyz, [1, 2, 0])
    if out == 2:
        xyzw = np.atleast_2d(np.take(xyz, 0, axis=0))
        xyz = np.atleast_2d(np.take(xyz, [i + rflwasnotnone for i in range(rfl.shape[0] - rflwasnotnone)], axis=0))
        if rflwasnotnone == 0:
            xyz = np.squeeze(xyz, axis=0)
        return (xyz, xyzw)
    if out == 1:
        if rflwasnotnone == 0:
            xyz = np.squeeze(xyz, axis=0)
        return xyz
    else:
        xyz = np.atleast_2d(np.take(xyz, [i + rflwasnotnone for i in range(rfl.shape[0] - rflwasnotnone)], axis=0))
        if rflwasnotnone == 0:
            xyz = np.squeeze(xyz, axis=0)
        return xyz


def spd_to_ler(data, cieobs=_CIEOBS, K=None):
    """
    Calculates Luminous efficacy of radiation (LER) from spectral data.
       
    Args: 
        :data: 
            | ndarray or pandas.dataframe with spectral data
            | (.shape = (number of spectra + 1, number of wavelengths))
            | Note that :data: is never interpolated, only CMFs and RFLs. 
            | This way interpolation errors due to peaky spectra are avoided. 
            | Conform CIE15-2018.
        :cieobs: 
            | luxpy._CIEOBS, optional
            | Determines the color matching function set used in the 
            | calculation of LER. For cieobs = '1931_2' the ybar CMF curve equals
            | the CIE 1924 Vlambda curve.
        :K: 
            | None, optional
            |   e.g.  K  = 683 lm/W for '1931_2'
      
    Returns:
        :ler: 
            | ndarray of LER values. 
             
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    """
    if isinstance(cieobs, str):
        if K == None:
            K = _CMF[cieobs]['K']
        Vl = vlbar(cieobs=cieobs, scr='dict', wl_new=(data[0]), kind='np')[1:2]
    else:
        Vl = spd(wl=(data[0]), data=cieobs, interpolation='cmf', kind='np')[1:2]
    if K is None:
        raise Exception('spd_to_ler: User defined Vlambda, but no K scaling factor has been supplied.')
    dl = getwld(data[0])
    return (K * np.dot(Vl * dl, data[1:].T) / np.sum((data[1:] * dl), axis=(data.ndim - 1))).T


def spd_to_power(data, ptype='ru', cieobs=_CIEOBS):
    """
    Calculate power of spectral data in radiometric, photometric 
    or quantal energy units.
    
    Args:
        :data: 
            | ndarray with spectral data
        :ptype: 
            | 'ru' or str, optional
            | str: - 'ru': in radiometric units 
            |      - 'pu': in photometric units 
            |      - 'pusa': in photometric units with Km corrected 
            |                to standard air (cfr. CIE TN003-2015)
            |      - 'qu': in quantal energy units
        :cieobs: 
            | _CIEOBS or str, optional
            | Type of cmf set to use for photometric units.
    
    Returns:
        returns: 
            | ndarray with normalized spectral data (SI units)
    """
    dl = getwld(data[0])
    if ptype == 'ru':
        p = np2d(np.dot(data[1:], dl * np.ones(data.shape[1]))).T
    else:
        if ptype == 'pusa':
            na = _BB['na']
            c = _BB['c']
            lambdad = c / (na * 54 * 10000000000000.0) / 1e-09
            Km_correction_factor = 1 / (1 - 0.00014329999999995735 * (lambdad - 555))
            Vl, Km = vlbar(cieobs=cieobs, wl_new=(data[0]), out=2)
            Km = Km * Km_correction_factor
            p = Km * np2d(np.dot(data[1:], dl * Vl[1])).T
        else:
            if ptype == 'pu':
                Vl, Km = vlbar(cieobs=cieobs, wl_new=(data[0]), out=2)
                p = Km * np2d(np.dot(data[1:], dl * Vl[1])).T
            else:
                if ptype == 'qu':
                    fQ = 1e-09 / (_BB['h'] * _BB['c'])
                    p = np2d(fQ * np.dot(data[1:], dl * data[0])).T
    return p


def blackbody(cct, wl3=None):
    """
    Calculate blackbody radiator spectrum for correlated color temperature (cct).
    
    Args:
        :cct: 
            | int or float 
            | (for list of cct values, use cri_ref() with ref_type = 'BB')
        :wl3: 
            | None, optional
            | New wavelength range for interpolation. 
            | Defaults to wavelengths specified by luxpy._WL3.

    Returns:
        :returns:
            | ndarray with blackbody radiator spectrum
              (:returns:[0] contains wavelengths)
            
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    """
    cct = float(cct)
    if wl3 is None:
        wl3 = _WL3
    wl = getwlr(wl3)

    def fSr(x):
        return 1 / np.pi * _BB['c1'] * (x * 1e-09) ** (-5) * _BB['n'] ** (-2.0) * (np.exp(_BB['c2'] * (_BB['n'] * x * 1e-09 * (cct + _EPS)) ** (-1.0)) - 1.0) ** (-1.0)

    return np.vstack((wl, fSr(wl) / fSr(560.0)))


def daylightlocus(cct, force_daylight_below4000K=False):
    """ 
    Calculates daylight chromaticity from correlated color temperature (cct).
    
    Args:
        :cct: 
            | int or float or list of int/floats or ndarray
        :force_daylight_below4000K: 
            | False or True, optional
            | Daylight locus approximation is not defined below 4000 K, 
            | but by setting this to True, the calculation can be forced to 
            | calculate it anyway.
    
    Returns:
        :returns: 
            | (ndarray of x-coordinates, ndarray of y-coordinates)
        
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
    """
    cct = np2d(cct)
    if np.any((cct < 4000.0) & (force_daylight_below4000K == False)):
        raise Exception('spectral.daylightlocus(): Daylight locus approximation not defined below 4000 K')
    xD = -4.607 * (1000.0 / cct) ** 3.0 + 2.9678 * (1000.0 / cct) ** 2.0 + 0.09911 * (1000.0 / cct) + 0.244063
    p = cct >= 7000.0
    xD[p] = -2.0064 * (1000.0 / cct[p]) ** 3.0 + 1.9018 * (1000.0 / cct[p]) ** 2.0 + 0.24748 * (1000.0 / cct[p]) + 0.23704
    yD = -3.0 * xD ** 2.0 + 2.87 * xD - 0.275
    return (xD, yD)


def daylightphase(cct, wl3=None, force_daylight_below4000K=False, verbosity=None):
    """
    Calculate daylight phase spectrum for correlated color temperature (cct).
        
    Args:
        :cct: 
            | int or float 
            | (for list of cct values, use cri_ref() with ref_type = 'DL')
        :wl3: 
            | None, optional
            | New wavelength range for interpolation. 
            | Defaults to wavelengths specified by luxpy._WL3.
        :force_daylight_below4000K: 
            | False or True, optional
            | Daylight locus approximation is not defined below 4000 K, 
            | but by setting this to True, the calculation can be forced to 
            | calculate it anyway.
        :verbosity: 
            | None, optional
            |   If None: do not print warning when CCT < 4000 K.
            
    Returns:
        :returns: 
            | ndarray with daylight phase spectrum
              (:returns:[0] contains wavelengths)
            
    References:
        1. `CIE15:2018, “Colorimetry,” CIE, Vienna, Austria, 2018. <https://doi.org/10.25039/TR.015.2018>`_
     """
    cct = float(cct)
    if wl3 is None:
        wl3 = _WL3
    else:
        if (cct < 4000.0) & (force_daylight_below4000K == False):
            if verbosity is not None:
                print('Warning daylightphase spd not defined below 4000 K. Using blackbody radiator instead.')
            Sr = blackbody(cct, wl3)
        else:
            wl = getwlr(wl3)
            if not np.array_equal(_S012_DAYLIGHTPHASE[0], wl):
                S012_daylightphase = cie_interp(data=_S012_DAYLIGHTPHASE, wl_new=wl, kind='linear', negative_values_allowed=True)
            else:
                S012_daylightphase = _S012_DAYLIGHTPHASE
            xD, yD = daylightlocus(cct, force_daylight_below4000K=force_daylight_below4000K)
            M1 = (-1.3515 - 1.7703 * xD + 5.9114 * yD) / (0.0241 + 0.2562 * xD - 0.7341 * yD)
            M2 = (0.03 - 31.4424 * xD + 30.0717 * yD) / (0.0241 + 0.2562 * xD - 0.7341 * yD)
            Sr = S012_daylightphase[1, :] + M1 * S012_daylightphase[2, :] + M2 * S012_daylightphase[3, :]
            Sr560 = Sr[:, np.where(np.abs(S012_daylightphase[0, :] - 560.0) == np.min(np.abs(S012_daylightphase[0, :] - 560)))[0]]
            Sr = Sr / Sr560
            Sr[Sr == float('NaN')] = 0
            Sr = np.vstack((wl, Sr))
    return Sr


def cri_ref(ccts, wl3=None, ref_type=_CRI_REF_TYPE, mix_range=None, cieobs=_CIEOBS, norm_type=None, norm_f=None, force_daylight_below4000K=False):
    """
    Calculates a reference illuminant spectrum based on cct 
    for color rendering index calculations .
    
    Args:
        :ccts: 
            | list of int/floats or ndarray with ccts.
        :wl3: 
            | None, optional
            | New wavelength range for interpolation. 
            | Defaults to wavelengths specified by luxpy._WL3.
        :ref_type:
            | str or list[str], optional
            | Specifies the type of reference spectrum to be calculated.
            | Defaults to luxpy._CRI_REF_TYPE. 
            | If :ref_type: is list of strings, then for each cct in :ccts: 
              a different reference illuminant can be specified. 
            | If :ref_type: == 'spd', then :ccts: is assumed to be an ndarray
              of reference illuminant spectra.
        :mix_range: 
            | None or ndarray, optional
            | Determines the cct range between which the reference illuminant is
            | a weigthed mean of a Planckian and Daylight Phase spectrum. 
            | Weighthing is done as described in IES TM30:
            |    SPDreference = (Te-T)/(Te-Tb)*Planckian+(T-Tb)/(Te-Tb)*daylight
            |    with Tb and Te are resp. the starting and end CCTs of the 
            |    mixing range and whereby the Planckian and Daylight SPDs 
            |    have been normalized for equal luminous flux.
            | If None: use the default specified for :ref_type:.
            | Can be a ndarray with shape[0] > 1, in which different mixing
            | ranges will be used for cct in :ccts:.
        :cieobs: 
            | luxpy._CIEOBS, optional
            | Required for the normalization of the Planckian and Daylight SPDs 
              when calculating a 'mixed' reference illuminant.
        :norm_type: 
            | None, optional 
            |       - 'lambda': make lambda in norm_f equal to 1
            |       - 'area': area-normalization times norm_f
            |       - 'max': max-normalization times norm_f
            |       - 'ru': to :norm_f: radiometric units 
            |       - 'pu': to :norm_f: photometric units 
            |       - 'pusa': to :norm_f: photometric units (with Km corrected
            |                             to standard air, cfr. CIE TN003-2015)
            |       - 'qu': to :norm_f: quantal energy units
        :norm_f:
            | 1, optional
            | Normalization factor that determines the size of normalization 
              for 'max' and 'area' 
              or which wavelength is normalized to 1 for 'lambda' option.
        :force_daylight_below4000K: 
            | False or True, optional
            | Daylight locus approximation is not defined below 4000 K, 
            | but by setting this to True, the calculation can be forced to 
              calculate it anyway.
    
    Returns:
        :returns: 
            | ndarray with reference illuminant spectra.
              (:returns:[0] contains wavelengths)

    Note: 
        Future versions will have the ability to take a dict as input 
        for ref_type. This way other reference illuminants can be specified 
        than the ones in _CRI_REF_TYPES. 
    """
    if ref_type == 'spd':
        return spd(ccts, wl=wl3, norm_type=norm_type, norm_f=norm_f)
    else:
        if mix_range is not None:
            mix_range = np2d(mix_range)
        if not isinstance(ref_type, list) | isinstance(ref_type, dict):
            ref_type = [
             ref_type]
        for i in range(len(ccts)):
            cct = ccts[i]
            if isinstance(ref_type, dict):
                raise Exception('cri_ref(): dictionary ref_type: Not yet implemented')
            else:
                if len(ref_type) > 1:
                    ref_type_ = ref_type[i]
                else:
                    ref_type_ = ref_type[0]
                if mix_range is None:
                    mix_range_ = _CRI_REF_TYPES[ref_type_]
                else:
                    if mix_range.shape[0] > 1:
                        mix_range_ = mix_range[i]
                    else:
                        mix_range_ = mix_range[0]
                    if (mix_range_[0] == mix_range_[1]) | (ref_type_[0:2] == 'BB') | (ref_type_[0:2] == 'DL'):
                        if (cct < mix_range_[0]) & (not ref_type_[0:2] == 'DL') | (ref_type_[0:2] == 'BB'):
                            Sr = blackbody(cct, wl3)
                        else:
                            if (cct >= mix_range_[0]) & (not ref_type_[0:2] == 'BB') | (ref_type_[0:2] == 'DL'):
                                Sr = daylightphase(cct, wl3, force_daylight_below4000K=force_daylight_below4000K)
                    else:
                        SrBB = blackbody(cct, wl3)
                        SrDL = daylightphase(cct, wl3, verbosity=None, force_daylight_below4000K=force_daylight_below4000K)
                        cmf = xyzbar(cieobs=cieobs, scr='dict', wl_new=wl3)
                        wl = SrBB[0]
                        ld = getwld(wl)
                        SrBB = 100.0 * SrBB[1] / np.array(np.sum(SrBB[1] * cmf[2] * ld))
                        SrDL = 100.0 * SrDL[1] / np.array(np.sum(SrDL[1] * cmf[2] * ld))
                        Tb = float(mix_range_[0])
                        Te = float(mix_range_[1])
                        cBB = (Te - cct) / (Te - Tb)
                        cDL = (cct - Tb) / (Te - Tb)
                        if cBB < 0.0:
                            cBB = 0.0
                        elif cBB > 1:
                            cBB = 1.0
            if cDL < 0.0:
                cDL = 0.0
            else:
                if cDL > 1:
                    cDL = 1.0
                Sr = SrBB * cBB + SrDL * cDL
                Sr[Sr == float('NaN')] = 0.0
                Sr560 = Sr[np.where(np.abs(wl - 560.0) == np.min(np.abs(wl - 560.0)))[0]]
                Sr = np.vstack((wl, Sr / Sr560))
            if i == 0:
                Srs = Sr[1]
            else:
                Srs = np.vstack((Srs, Sr[1]))

        Srs = np.vstack((Sr[0], Srs))
        return spd(Srs, wl=None, norm_type=norm_type, norm_f=norm_f)