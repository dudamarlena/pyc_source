# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/limcv/aircv.py
# Compiled at: 2019-12-11 22:04:19
# Size of source mod 2**32: 4147 bytes
import os, sys, cv2, numpy as np
from .error import FileNotExistError
from six import PY2, PY3
from .utils import cv2_2_pil

def imread(filename):
    """根据图片路径，将图片读取为cv2的图片处理格式."""
    if not os.path.isfile(filename):
        raise FileNotExistError('File not exist: %s' % filename)
    elif PY3:
        img = cv2.imdecode(np.fromfile(filename, dtype=(np.uint8)), cv2.IMREAD_UNCHANGED)
    else:
        filename = filename.encode(sys.getfilesystemencoding())
        img = cv2.imread(filename, 1)
    return img


def imwrite(filename, img):
    """写出图片到本地路径，压缩"""
    if PY2:
        filename = filename.encode(sys.getfilesystemencoding())
    pil_img = cv2_2_pil(img)
    pil_img.save(filename, quality=10, optimize=True)


def show(img, title='show_img', test_flag=False):
    """在可缩放窗口里显示图片."""
    cv2.namedWindow(title, cv2.WINDOW_NORMAL)
    cv2.imshow(title, img)
    if not test_flag:
        cv2.waitKey(0)
    cv2.destroyAllWindows()


def show_origin_size(img, title='image', test_flag=False):
    """原始尺寸窗口中显示图片."""
    cv2.imshow(title, img)
    if not test_flag:
        cv2.waitKey(0)
    cv2.destroyAllWindows()


def rotate(img, angle=90, clockwise=True):
    """
        函数使图片可顺时针或逆时针旋转90、180、270度.
        默认clockwise=True：顺时针旋转
    """

    def count_clock_rotate(img):
        rows, cols = img.shape[:2]
        rotate_img = np.zeros((cols, rows))
        rotate_img = cv2.transpose(img)
        rotate_img = cv2.flip(rotate_img, 0)
        return rotate_img

    counter_rotate_time = (4 - angle / 90) % 4 if clockwise else angle / 90 % 4
    for i in range(int(counter_rotate_time)):
        img = count_clock_rotate(img)

    return img


def crop_image(img, rect):
    """
        区域截图，同时返回截取结果 和 截取偏移;
        Crop image , rect = [x_min, y_min, x_max ,y_max].
        (airtest中有用到)
    """
    if isinstance(rect, (list, tuple)):
        height, width = img.shape[:2]
        x_min, y_min, x_max, y_max = [int(i) for i in rect]
        x_min, y_min = max(0, x_min), max(0, y_min)
        x_min, y_min = min(width - 1, x_min), min(height - 1, y_min)
        x_max, y_max = max(0, x_max), max(0, y_max)
        x_max, y_max = min(width - 1, x_max), min(height - 1, y_max)
        img_crop = img[y_min:y_max, x_min:x_max]
        return img_crop
    raise Exception('to crop a image, rect should be a list like: [x_min, y_min, x_max, y_max].')


def mark_point(img, point, circle=False, color=100, radius=20):
    """ 调试用的: 标记一个点 """
    x, y = point
    if circle:
        cv2.circle(img, (x, y), radius, 255, thickness=2)
    cv2.line(img, (x - radius, y), (x + radius, y), color)
    cv2.line(img, (x, y - radius), (x, y + radius), color)
    return img


def mask_image(img, mask, color=(255, 255, 255), linewidth=-1):
    """
        将screen的mask矩形区域刷成白色gbr(255, 255, 255).
        其中mask区域为: [x_min, y_min, x_max, y_max].
        color: 顺序分别的blue-green-red通道.
        linewidth: 为-1时则完全填充填充，为正整数时为线框宽度.
    """
    offset = int(linewidth / 2)
    return cv2.rectangle(img, (mask[0] - offset, mask[1] - offset), (mask[2] + linewidth, mask[3] + linewidth), color, linewidth)


def get_resolution(img):
    h, w = img.shape[:2]
    return (w, h)


def resize(img, ratio):
    w = img.shape[1]
    h = img.shape[0]
    newW = int(w * ratio)
    newH = int(h * ratio)
    newImg = cv2.resize(img, (newW, newH), interpolation=(cv2.INTER_CUBIC))
    return newImg