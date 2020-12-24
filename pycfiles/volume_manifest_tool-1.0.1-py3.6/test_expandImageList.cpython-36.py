# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/v_m_t/test_expandImageList.py
# Compiled at: 2019-10-02 14:44:05
# Size of source mod 2**32: 386 bytes
from v_m_t.VolumeInfoBuda import expand_image_list

def test_expand():
    imageListString = 'I2PD44320001.tif:2|I2PD44320003.jpg|I2PD44320305.jpg:3'
    expected = ['I2PD44320001.tif', 'I2PD44320002.tif', 'I2PD44320003.jpg', 'I2PD44320305.jpg', 'I2PD44320306.jpg',
     'I2PD44320307.jpg']
    expanded = expand_image_list(imageListString)
    assert expanded == expected