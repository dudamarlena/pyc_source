# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/core/utils/normalization.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 2946 bytes
__authors__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '30/05/2018'
from tomwer.core.log import TomwerLogger
import fabio
_logger = TomwerLogger(__name__)

def flatFieldCorrection(imgs, dark, flat):
    """
    Simple normalization of a list of images.
    Normalization is made for X-Ray imaging:
    (img - dark) / (flat - dark)

    :param dict imgs: list of imgs to correct. key: index of the image,
                      value: the image path or numpy.ndarray
    :param numpy.ndarray dark: dark image
    :param numpy.ndarray flat: flat image
    :return: list of corrected images
    """
    res = {}
    conditionOK = True
    if dark.ndim != 2:
        _logger.error('cannot make flat field correction, dark should be of dimension 2')
        conditionOK = False
    if flat.ndim != 2:
        _logger.error('cannot make flat field correction, flat should be of dimension 2')
        conditionOK = False
    if dark.shape != flat.shape:
        _logger.error('Given dark and flat have incoherent dimension')
        conditionOK = False
    if conditionOK is False:
        return res
    for index, img in imgs.items():
        imgData = img
        if type(img) is str:
            assert img.endswith('.edf')
            imgData = fabio.open(img).data
        elif imgData.shape != dark.shape:
            _logger.error('Image has invalid. Cannot apply flat fieldcorrection it')
            corrrectedImage = imgData
        else:
            corrrectedImage = (imgData - dark) / (flat - dark)
        res[index] = corrrectedImage

    return res