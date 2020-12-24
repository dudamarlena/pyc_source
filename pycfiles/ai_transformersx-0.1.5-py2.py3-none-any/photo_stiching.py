# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/ai_tools/photo_stiching.py
# Compiled at: 2018-08-14 06:21:23
__doc__ = '\nCreated on Tue Aug 14 11:47:59 2018\n\n@author: wuhongrui\n\n'
import cv2, numpy as np, pandas as pd

def photostitch(image_list):
    if len(image_list) % 2 == 1:
        img_list.pop(-1)
    img = []
    for image_name in image_list:
        img.append(cv2.imread(image_name))

    for i in range(0, len(img)):
        if i % 2 == 0:
            new_image = np.concatenate([img[i], img[(i + 1)]], axis=1)
            if i == 0:
                image = new_image
        elif i % 2 == 1 and i != 1:
            image = np.vstack((image, new_image))

    return image


def photostitch_col(image_matrix_list):
    tmp = np.zeros((320, 240, 3), dtype='uint8')
    for img in image_matrix_list:
        imgs = cv2.resize(img, (240, 320), interpolation=cv2.INTER_CUBIC)
        print (tmp.shape, imgs.shape)
        tmp = np.vstack((tmp, imgs))

    return tmp


def photostitch2(img_list1, img_list2):
    img1 = photostitch(img_list1)
    img2 = photostitch(img_list2)
    image = np.concatenate([img1, img2], axis=1)
    midImgDraw(image)
    cv2.imshow('image', image)
    cv2.waitKey(10000)
    cv2.imwrite('stitchResult.png', image)


def midImgDraw(img):
    rows, cols, channels = img.shape
    cv2.line(img, (cols / 2, 0), (cols / 2, rows), (255, 0, 0), 2)


if __name__ == '__main__':
    image_list = ['1.png', '2.png', '3.png', '4.png', '5.png', '6.png', '7.png', '8.png', '9.png', '10.png']
    photostitch2(image_list, image_list)