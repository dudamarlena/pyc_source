# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/BasicAugmentation/basic_augmentation.py
# Compiled at: 2020-04-27 02:28:08
# Size of source mod 2**32: 3979 bytes
import numpy as np
from PIL import Image
from scipy.ndimage import rotate
import cv2

class Augmentation:

    def __init__(self, rotate_p=0.35, flip_p=0.35, cutout_p=0.35, add_noise_p=0.35):
        """
        Used to add variance to input layer of CNN to help models generalize better.

        :param rotate_p: Probability of image being rotated
        :param flip_p:  Probability of image being flipped
        :param cutout_p:  Probability of image having random squares cutout
        :param add_noise_p:  Probability of noise being added to image
        """
        self.rotate_p = rotate_p
        self.flip_p = flip_p
        self.cutout_p = cutout_p
        self.add_noise_p = add_noise_p

    def __call__(self, img):
        numpy = False
        if type(img) == np.ndarray:
            numpy == True
            img = Image.fromarray(img)
        img = self.rotate(self.rotate_p, img)
        img = self.flip(self.flip_p, img)
        img = self.cutout(self.cutout_p, img)
        img = self.noise(self.add_noise_p, img)
        if numpy:
            return np.array(img)
        return img

    def flip(self, p, img):
        img = np.array(img)
        hori = np.random.randint(0, 4)
        if np.random.randint(0, 101) / 100 < p:
            if hori == 0:
                img = img[:, ::-1, :]
            else:
                if hori == 1:
                    img = img[::-1, :, :]
                else:
                    img = img[::-1, ::-1, :]
        return Image.fromarray(img)

    def rotate(self, p, img):
        img = np.array(img)
        if np.random.randint(0, 101) / 100 < p:
            img = rotate(img, (np.random.randint(-15, 15)), reshape=False, mode='nearest')
        return Image.fromarray(img)

    def cutout(self, p, img):
        img = np.array(img)
        if np.random.randint(0, 101) / 100 < p:
            squareW = int(img.shape[1] * np.random.randint(3, 17) / 1000)
            squareH = int(squareW * (1 + np.random.randint(-50, 50) / 100))
            for x in range(np.random.randint(0, (50 - squareW) * 4.5)):
                colour = 0 if np.random.randint(0, 2) == 1 else 255
                rand_width_pos = np.random.randint(0, img.shape[1])
                rand_height_pos = np.random.randint(0, img.shape[0])
                channel = np.random.randint(0, 4)
                if channel == 3:
                    img[rand_height_pos:rand_height_pos + squareW, rand_width_pos:rand_width_pos + squareH, :] = colour
                else:
                    img[rand_height_pos:rand_height_pos + squareW, rand_width_pos:rand_width_pos + squareH, channel] = colour

        return Image.fromarray(img)

    def noise(self, p, img):
        img = np.array(img)
        img1 = img.copy()
        if np.random.randint(0, 101) / 100 < p:
            noise = np.random.randint(0, np.random.randint(10, 65), img.shape)
            img1 = cv2.add(img1, noise.astype(np.uint8))
            for x in range(np.random.randint(0, 30)):
                rand_width = np.random.randint(0, img.shape[1])
                rand_width_pos = np.random.randint(0, img.shape[1])
                rand_height = np.random.randint(0, img.shape[0])
                rand_height_pos = np.random.randint(0, img.shape[0])
                channel = np.random.randint(0, 3)
                if channel == 3:
                    img1[rand_height_pos:rand_height_pos + rand_height, rand_width_pos:rand_width_pos + rand_width, :] = img[rand_height_pos:rand_height_pos + rand_height, rand_width_pos:rand_width_pos + rand_width, :]
                else:
                    img1[rand_height_pos:rand_height_pos + rand_height, rand_width_pos:rand_width_pos + rand_width, channel] = img[rand_height_pos:rand_height_pos + rand_height,
                     rand_width_pos:rand_width_pos + rand_width, channel]

        return Image.fromarray(img1)