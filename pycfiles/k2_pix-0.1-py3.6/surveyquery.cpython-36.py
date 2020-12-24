# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/k2-pix/surveyquery.py
# Compiled at: 2017-12-13 13:54:44
# Size of source mod 2**32: 1243 bytes
import numpy as np, astroquery
from astropy.io import fits
from astropy.wcs import WCS
from astroquery.skyview import SkyView
import matplotlib.pyplot as plt, urllib

def getSVImg(SC_ObjPos, SkyViewSurvey):
    """
    Input: a SkyCoord Position Vector and a Survey Type that is Compatable with NASA SkyView
    Output: A Numpy Pixel Array and Header Array
    """
    img_survey, pix_survey, hdr_survey = (None, None, None)
    try:
        img_survey = SkyView.get_images(position=SC_ObjPos, survey=[SkyViewSurvey], coordinates='J2000',
          pixels=30)
        if len(img_survey) > 0:
            pix_survey = img_survey[0][0].data
            hdr_survey = img_survey[0][0].header
    except (astroquery.exceptions.TimeoutError, urllib.HTTPError):
        pix_survey, hdr_survey = (None, None)

    return (
     pix_survey, hdr_survey)


if __name__ == '__main__':
    Survey = 'DSS'
    ObjPos = 'Dumbbell Nebula'
    pixels, header = getSVImg(ObjPos, Survey)
    plt.imshow(pixels)
    plt.show()