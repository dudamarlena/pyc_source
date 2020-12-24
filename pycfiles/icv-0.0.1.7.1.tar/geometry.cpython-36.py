# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/image/transforms/geometry.py
# Compiled at: 2019-07-27 10:14:01
# Size of source mod 2**32: 6711 bytes
from __future__ import division
import cv2, numpy as np
from ..io import imread
from .resize import imresize
from icv.utils.itis import is_np_array, is_seq, is_empty

def immerge--- This code section failed: ---

 L.  11         0  LOAD_GLOBAL              len
                2  LOAD_FAST                'img_list'
                4  CALL_FUNCTION_1       1  '1 positional argument'
                6  LOAD_CONST               0
                8  COMPARE_OP               >
               10  POP_JUMP_IF_TRUE     16  'to 16'
               12  LOAD_ASSERT              AssertionError
               14  RAISE_VARARGS_1       1  'exception'
             16_0  COME_FROM            10  '10'

 L.  12        16  LOAD_FAST                'origin'
               18  LOAD_CONST               ('x', 'y')
               20  COMPARE_OP               in
               22  POP_JUMP_IF_TRUE     32  'to 32'
               24  LOAD_ASSERT              AssertionError
               26  LOAD_STR                 "param origin should be 'x' or 'y'"
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  RAISE_VARARGS_1       1  'exception'
             32_0  COME_FROM            22  '22'

 L.  13        32  LOAD_GLOBAL              is_seq
               34  LOAD_FAST                'img_list'
               36  CALL_FUNCTION_1       1  '1 positional argument'
               38  POP_JUMP_IF_FALSE    50  'to 50'
               40  LOAD_GLOBAL              is_empty
               42  LOAD_FAST                'img_list'
               44  CALL_FUNCTION_1       1  '1 positional argument'
               46  UNARY_NOT        
             48_0  COME_FROM            38  '38'
               48  POP_JUMP_IF_TRUE     58  'to 58'
               50  LOAD_ASSERT              AssertionError
               52  LOAD_STR                 'param img_list should be a sequence'
               54  CALL_FUNCTION_1       1  '1 positional argument'
               56  RAISE_VARARGS_1       1  'exception'
             58_0  COME_FROM            48  '48'

 L.  14        58  LOAD_DEREF               'resize'
               60  LOAD_CONST               None
               62  COMPARE_OP               is
               64  POP_JUMP_IF_TRUE     90  'to 90'
               66  LOAD_GLOBAL              is_seq
               68  LOAD_DEREF               'resize'
               70  CALL_FUNCTION_1       1  '1 positional argument'
               72  POP_JUMP_IF_FALSE    86  'to 86'
               74  LOAD_GLOBAL              len
               76  LOAD_DEREF               'resize'
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  LOAD_CONST               2
               82  COMPARE_OP               ==
             84_0  COME_FROM            72  '72'
               84  POP_JUMP_IF_TRUE     90  'to 90'
               86  LOAD_ASSERT              AssertionError
               88  RAISE_VARARGS_1       1  'exception'
             90_0  COME_FROM            84  '84'
             90_1  COME_FROM            64  '64'

 L.  15        90  LOAD_LISTCOMP            '<code_object <listcomp>>'
               92  LOAD_STR                 'immerge.<locals>.<listcomp>'
               94  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               96  LOAD_FAST                'img_list'
               98  GET_ITER         
              100  CALL_FUNCTION_1       1  '1 positional argument'
              102  STORE_FAST               'img_list'

 L.  16       104  LOAD_GLOBAL              len
              106  LOAD_FAST                'img_list'
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  LOAD_CONST               1
              112  COMPARE_OP               ==
              114  POP_JUMP_IF_FALSE   124  'to 124'

 L.  17       116  LOAD_FAST                'img_list'
              118  LOAD_CONST               0
              120  BINARY_SUBSCR    
              122  RETURN_END_IF    
            124_0  COME_FROM           114  '114'

 L.  19       124  LOAD_DEREF               'resize'
              126  LOAD_CONST               None
              128  COMPARE_OP               is
              130  POP_JUMP_IF_FALSE   204  'to 204'

 L.  20       132  LOAD_FAST                'origin'
              134  LOAD_STR                 'x'
              136  COMPARE_OP               ==
              138  POP_JUMP_IF_FALSE   172  'to 172'

 L.  21       140  LOAD_GLOBAL              len
              142  LOAD_GLOBAL              set
              144  LOAD_LISTCOMP            '<code_object <listcomp>>'
              146  LOAD_STR                 'immerge.<locals>.<listcomp>'
              148  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              150  LOAD_FAST                'img_list'
              152  GET_ITER         
              154  CALL_FUNCTION_1       1  '1 positional argument'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  CALL_FUNCTION_1       1  '1 positional argument'
              160  LOAD_CONST               1
              162  COMPARE_OP               ==
              164  POP_JUMP_IF_TRUE    202  'to 202'
              166  LOAD_ASSERT              AssertionError
              168  RAISE_VARARGS_1       1  'exception'
              170  JUMP_ABSOLUTE       222  'to 222'
              172  ELSE                     '202'

 L.  23       172  LOAD_GLOBAL              len
              174  LOAD_GLOBAL              set
              176  LOAD_LISTCOMP            '<code_object <listcomp>>'
              178  LOAD_STR                 'immerge.<locals>.<listcomp>'
              180  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              182  LOAD_FAST                'img_list'
              184  GET_ITER         
              186  CALL_FUNCTION_1       1  '1 positional argument'
              188  CALL_FUNCTION_1       1  '1 positional argument'
              190  CALL_FUNCTION_1       1  '1 positional argument'
              192  LOAD_CONST               1
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_TRUE    222  'to 222'
              198  LOAD_GLOBAL              AssertionError
              200  RAISE_VARARGS_1       1  'exception'
            202_0  COME_FROM           164  '164'
              202  JUMP_FORWARD        222  'to 222'
              204  ELSE                     '222'

 L.  25       204  LOAD_CLOSURE             'resize'
              206  BUILD_TUPLE_1         1 
              208  LOAD_LISTCOMP            '<code_object <listcomp>>'
              210  LOAD_STR                 'immerge.<locals>.<listcomp>'
              212  MAKE_FUNCTION_8          'closure'
              214  LOAD_FAST                'img_list'
              216  GET_ITER         
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  STORE_FAST               'img_list'
            222_0  COME_FROM           202  '202'
            222_1  COME_FROM           196  '196'

 L.  27       222  LOAD_GLOBAL              np
              224  LOAD_ATTR                concatenate
              226  LOAD_FAST                'img_list'
              228  LOAD_FAST                'origin'
              230  LOAD_STR                 'x'
              232  COMPARE_OP               ==
              234  POP_JUMP_IF_FALSE   240  'to 240'
              236  LOAD_CONST               1
              238  JUMP_FORWARD        242  'to 242'
              240  ELSE                     '242'
              240  LOAD_CONST               0
            242_0  COME_FROM           238  '238'
              242  LOAD_CONST               ('axis',)
              244  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              246  STORE_FAST               'merged_img_np'

 L.  28       248  LOAD_FAST                'merged_img_np'
              250  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 250


def immix_up(img_list, resize=None, weight=None):
    assert lenimg_list > 0
    if not weight is None:
        if not (lenimg_list == lenweight and sumweight == 1.0):
            raise AssertionError
    img_list = [imreadimg for img in img_list]
    if lenimg_list == 1:
        return img_list[0]
    else:
        if resize is None:
            assert lenset[img.shape[:2] for img in img_list] == 1
        else:
            img_list = [imresize(img, resize) for img in img_list]
        img_mixup = np.sum[img_list[i] * weight[i] for i in rangelenimg_list]
        return img_mixup


def imflip_lr(img):
    """Flip an image horizontally

    Args:
        img (ndarray): Image to be flipped.
    Returns:
        ndarray: The flipped image.
    """
    return np.flip((imreadimg), axis=1)


def imflip_ud(img):
    """Flip an image vertically

    Args:
        img (ndarray): Image to be flipped.
    Returns:
        ndarray: The flipped image.
    """
    return np.flip((imreadimg), axis=0)


def imrotate(img, angle, center=None, scale=1.0, border_value=0, auto_bound=False):
    """Rotate an image.

    Args:
        img (ndarray): Image to be rotated.
        angle (float): Rotation angle in degrees, positive values mean
            clockwise rotation.
        center (tuple): Center of the rotation in the source image, by default
            it is the center of the image.
        scale (float): Isotropic scale factor.
        border_value (int): Border value.
        auto_bound (bool): Whether to adjust the image size to cover the whole
            rotated image.

    Returns:
        ndarray: The rotated image.
    """
    if center is not None:
        if auto_bound:
            raise ValueError'`auto_bound` conflicts with `center`'
    else:
        img = imreadimg
        h, w = img.shape[:2]
        if center is None:
            center = (
             (w - 1) * 0.5, (h - 1) * 0.5)
        assert isinstance(center, tuple)
        matrix = cv2.getRotationMatrix2D(center, -angle, scale)
        if auto_bound:
            cos = np.absmatrix[(0, 0)]
            sin = np.absmatrix[(0, 1)]
            new_w = h * sin + w * cos
            new_h = h * cos + w * sin
            matrix[(0, 2)] += (new_w - w) * 0.5
            matrix[(1, 2)] += (new_h - h) * 0.5
            w = intnp.roundnew_w
            h = intnp.roundnew_h
    rotated = cv2.warpAffine(img, matrix, (w, h), borderValue=border_value)
    return rotated


def imcrop(img, bboxes, scale=1.0, pad_fill=None):
    """Crop image patches.

    3 steps: scale the bboxes -> clip bboxes -> crop and pad.

    Args:
        img (ndarray): Image to be cropped.
        bboxes (ndarray): Shape (k, 4) or (4, ), location of cropped bboxes.
        scale (float, optional): Scale ratio of bboxes, the default value
            1.0 means no padding.
        pad_fill (number or list): Value to be filled for padding, None for
            no padding.

    Returns:
        list or ndarray: The cropped image patches.
    """
    from icv.data.shape.transforms import bbox_clip, bbox_scaling
    img = imreadimg
    chn = 1 if img.ndim == 2 else img.shape[2]
    if pad_fill is not None:
        if isinstance(pad_fill, (int, float)):
            pad_fill = [pad_fill for _ in rangechn]
        if not lenpad_fill == chn:
            raise AssertionError
    if not is_np_arraybboxes:
        bboxes = np.arraybboxes
    _bboxes = bboxes[(None, Ellipsis)] if bboxes.ndim == 1 else bboxes
    scaled_bboxes = bbox_scaling(_bboxes, scale).astypenp.int32
    clipped_bbox = bbox_clip(scaled_bboxes, img.shape)
    patches = []
    for i in rangeclipped_bbox.shape[0]:
        x1, y1, x2, y2 = tupleclipped_bbox[i, :]
        if pad_fill is None:
            patch = img[y1:y2 + 1, x1:x2 + 1, ...]
        else:
            _x1, _y1, _x2, _y2 = tuplescaled_bboxes[i, :]
            if chn == 2:
                patch_shape = (
                 _y2 - _y1 + 1, _x2 - _x1 + 1)
            else:
                patch_shape = (
                 _y2 - _y1 + 1, _x2 - _x1 + 1, chn)
            patch = np.array(pad_fill,
              dtype=(img.dtype)) * np.ones(patch_shape,
              dtype=(img.dtype))
            x_start = 0 if _x1 >= 0 else -_x1
            y_start = 0 if _y1 >= 0 else -_y1
            w = x2 - x1 + 1
            h = y2 - y1 + 1
            patch[y_start:y_start + h, x_start:x_start + w, ...] = img[y1:y1 + h, x1:x1 + w, ...]
        patches.appendpatch

    if bboxes.ndim == 1:
        return patches[0]
    else:
        return patches


def impad(img, shape, pad_val=0):
    """Pad an image to a certain shape.

    Args:
        img (ndarray): Image to be padded.
        shape (tuple): Expected padding shape.
        pad_val (number or sequence): Values to be filled in padding areas.

    Returns:
        ndarray: The padded image.
    """
    img = imreadimg
    if not isinstance(pad_val, (int, float)):
        if not lenpad_val == img.shape[(-1)]:
            raise AssertionError
    else:
        if lenshape < lenimg.shape:
            shape = shape + (img.shape[(-1)],)
        assert lenshape == lenimg.shape
    for i in rangelenshape - 1:
        assert shape[i] >= img.shape[i]

    pad = np.empty(shape, dtype=(img.dtype))
    pad[...] = pad_val
    pad[:img.shape[0], :img.shape[1], ...] = img
    return pad


def impad_to_multiple(img, divisor, pad_val=0):
    """Pad an image to ensure each edge to be multiple to some number.

    Args:
        img (ndarray): Image to be padded.
        divisor (int): Padded image edges will be multiple to divisor.
        pad_val (number or sequence): Same as :func:`impad`.

    Returns:
        ndarray: The padded image.
    """
    img = imreadimg
    pad_h = intnp.ceilimg.shape[0] / divisor * divisor
    pad_w = intnp.ceilimg.shape[1] / divisor * divisor
    return impad(img, (pad_h, pad_w), pad_val)