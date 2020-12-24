# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/image.py
# Compiled at: 2019-11-26 03:01:36
# Size of source mod 2**32: 1413 bytes
import numpy as np
from io import BytesIO
from PIL import Image
import base64, cv2
from .itis import is_np_array

def base64_to_np(b64_code):
    image = Image.open(BytesIO(base64.b64decode(b64_code)))
    img = np.array(image)
    return img


def np_to_base64(image_np):
    assert is_np_array(image_np)
    output_buffer = BytesIO()
    img = Image.fromarray(image_np.astype('uint8')).convert('RGB')
    img.save(output_buffer, format='JPEG')
    binary_data = output_buffer.getvalue()
    base64_data = base64.b64encode(binary_data)
    return base64_data


def get_mean_std(image_files):
    """
    获取图片均值方差
    :param image_files:
    :return:
    """
    if len(image_files) <= 0:
        return ([0.0, 0.0, 0.0], [0.0, 0.0, 0.0])
    else:
        means, stds = list(zip(*[cv2.meanStdDev(np.array(cv2.imread(image_file))) for image_file in image_files]))
        means = np.squeeze(np.array(means))
        stds = np.squeeze(np.array(stds))
        return (np.mean(means, axis=0).tolist(), np.mean(stds, axis=0).tolist())


def list_images(img_root, recursive=True):
    import os
    from glob import iglob
    imgs = []
    for ext in ('*.gif', '*.png', '*.jpg', '*.tiff', '*.jpeg', '*.bmp'):
        imgs.extend(iglob((os.path.join(img_root, ext)), recursive=recursive))
        if recursive:
            imgs.extend(iglob((os.path.join(img_root, '**', ext)), recursive=recursive))

    return imgs