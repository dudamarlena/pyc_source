# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/imageaug/transforms.py
# Compiled at: 2020-01-05 21:07:03
# Size of source mod 2**32: 9356 bytes
"""imageaug.py - image augmentation for PyTorch"""
import random, torch, torchvision, PIL.Image
import PIL.ImageFilter as ImageFilter
import numpy as np
import imageaug.functional as F

class HorizontalFlip(object):
    __doc__ = 'Transform to horizontally flip tensor'

    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, tensor):
        if random.random() <= self.p:
            return tensor
        arr = np.flip(tensor.numpy(), 0).copy()
        tensor = torch.from_numpy(arr)
        if len(tensor.shape) == 3:
            return torch.flip(tensor, (0, 2))
        if len(tensor.shape) == 4:
            return torch.flip(tensor, (1, 3))
        raise NotImplemented


class VericalFlip(object):
    __doc__ = 'Transform to vertically flip tensor'

    def __init__(self, p=0.5):
        self.p = p

    def __call__(self, tensor):
        if random.random() <= self.p:
            return tensor
        arr = np.flip(tensor.numpy(), 0).copy()
        tensor = torch.from_numpy(arr)
        if len(tensor.shape) == 3:
            return torch.flip(tensor, (0, 1))
        if len(tensor.shape) == 4:
            return torch.flip(tensor, (1, 2))
        raise NotImplemented


class RandomGaussianBlur:

    def __init__(self, mu, sigma):
        self.mu = mu
        self.sigma = sigma

    def __call__(self, pil_image):
        return pil_image.filter(ImageFilter.GaussianBlur(radius=(max(0, random.normalvariate(self.mu, self.sigma)))))


class GaussianBlur:

    def __init__(self, radius):
        self.radius = radius

    def __call__(self, pil_image):
        return pil_image.filter(ImageFilter.GaussianBlur(radius=(self.radius)))


class MedianFilter:

    def __init__(self, channels, radius):
        self.radius = radius

    def __call__(self, pil_image):
        return pil_image.filter(PIL.ImageFilter.MedianFilter(self.size))


class MaxFilter:

    def __init__(self, channels, radius):
        self.radius = radius

    def __call__(self, pil_image):
        return pil_image.filter(PIL.ImageFilter.MaxFilter(self.size))


class MinFilter:

    def __init__(self, channels, radius):
        self.radius = radius

    def __call__(self, pil_image):
        return pil_image.filter(PIL.ImageFilter.MinFilter(self.size))


class RankFilter:
    __doc__ = 'Rank filter, sorts all pixels in a window of the given size, and\n    returns the rank-th value\n    \n    use 0 for a min filter\n    size * size / 2 for a median filter\n    size * size - 1 for a max filter, etc.\n    '

    def __init__(self, channels, radius, rank):
        self.radius = radius
        self.rank = rank

    def __call__(self, pil_image):
        return pil_image.filter(PIL.ImageFilter.RankFilter(self.radius, self.rank))


class GaussianNoise:
    __doc__ = 'Add Gaussian noise'

    def __init__(self, channels, std, mean=0.0):
        self.channels = channels
        self.std = std
        self.mean = mean

    def __call__(self, tensor):
        if len(tensor.shape) == 3:
            out = tensor.clone()
            out[self.channels, :, :] = F.gaussian_noise(tensor[self.channels, :, :], self.std, self.mean)
            return out
        if len(tensor.shape) == 4:
            out = tensor.clone()
            out[:, self.channels, :, :] = F.gaussian_noise(tensor[:, self.channels, :, :], self.std, self.mean)
            return out
        raise NotImplemented

    def __repr__(self):
        format_string = self.__class__.__name__ + '(std={0}'.format(self.std)
        format_string += ', mean={0}'.format(self.mean)
        format_string += ')'
        return format_string


class UniformNoise(object):
    __doc__ = 'Add uniform noise'

    def __init__(self, low, high):
        self.low = low
        self.high = high

    def __call__(self, tensor):
        if len(tensor.shape) == 3:
            out = tensor.clone()
            out[self.channels] = F.uniform_noise(tensor[self.channels], self.low, self.high)
            return out
        if len(tensor.shape) == 4:
            out = tensor.clone()
            out[:, self.channels] = F.uniform_noise(tensor[:, self.channels], self.low, self.high)
            return out
        raise NotImplemented

    def __repr__(self):
        format_string = self.__class__.__name__ + '(low={0}'.format(self.low)
        format_string += ', high={0}'.format(self.high)
        format_string += ')'
        return format_string


class RandomAdjustment(object):
    __doc__ = "Adjust brightness/contrast of a tensor's channels\n    \n    Parameters:\n        channels : int or tuple\n            channels to adjust\n        brightness: float\n            brightness standard deviation\n        contrast: float\n            contrast standard deviation\n        rgb: bool\n            tensored processed are in RGB colorspace\n    "

    def __init__(self, channels, brightness, contrast, rgb=True):
        self.channels = channels
        self.brightness = brightness
        self.contrast = contrast
        self.rgb = rgb

    def __call__(self, tensor):
        if len(tensor.shape) == 3:
            tensor = tensor.unsqueeze(0)
            unsqueezed = True
        else:
            unsqueezed = False
        if self.contrast > 0:
            tensor = F.adjust_channel_contrast(tensor, self.channels, random.lognormvariate(0, self.contrast), self.rgb)
        if self.brightness > 0:
            tensor = F.adjust_channel_brightness(tensor, self.channels, random.normalvariate(0, self.brightness))
        if unsqueezed:
            tensor = tensor.squeeze(0)
        return tensor

    def __repr__(self):
        format_string = self.__class__.__name__ + '(channels={0}'.format(self.channels)
        format_string += ', brightness={0}'.format(self.brightness)
        format_string += ', contrast={0}'.format(self.contrast)
        format_string += ')'
        return format_string


class Colorspace(object):
    __doc__ = 'Convert from one colorspace to another\n    \n    Available colorspaces:\n        RGB, RGBA\n        YUV, YUVA\n        YCH, YCHA\n        \n    Parameters:\n        input_colorspace: string\n            colorspace of input image tensor\n        output_colorspace: string\n            colorspace of output image tensor\n        clip: bool\n            clip RGB and RGBA outputs within 0-1\n    '

    def __init__(self, input_colorspace, output_colorspace, clip=True):
        self.input_colorspace = input_colorspace
        self.output_colorspace = output_colorspace
        self.clip = clip

    def __call__(self, tensor):
        if self.input_colorspace == self.output_colorspace:
            return tensor
        if len(tensor.shape) == 3:
            tensor = tensor.unsqueeze(0)
            return F.convert(tensor, self.input_colorspace, self.output_colorspace, self.clip).squeeze(0)
        return F.convert(tensor, self.input_colorspace, self.output_colorspace, self.clip)

    def __repr__(self):
        format_string = self.__class__.__name__ + '(input_colorspace={0}'.format(self.input_colorspace)
        format_string += ', output_colorspace={0}'.format(self.output_colorspace)
        format_string += ')'
        return format_string


class RandomRotatedCrop(object):
    __doc__ = 'Rotate image by angle and crop within the original unrotated image\n\n    Parameters:\n        crop_size : ( int, int )\n            size of crop area\n        mean : float\n            mean angle\n        std : float\n            standard deviation of normal distribution\n        downscale: float (from 0.0 to 1.0, default: 0)\n            controls the scaling before cropping a image\n            \n            when downscale is 1 or more, the image will be downscaled to fit as\n            much of the image into the rotated crop as possible\n            \n            otherwise, downscale controls how much downscaling to apply\n            0.5 will crop a quarter of the image (half the height and width)\n            \n            set to 0 to always crop the original image without downscaling\n        resample : int\n            nearest neighbour sampling (PIL.Image.NEAREST)\n            bilinear sampling (PIL.Image.BILINEAR)\n            bicubic sampling (PIL.Image.BICUBIC)\n        fillcolor : tuple\n            an optional color for area outside the rotated image\n    '

    def __init__(self, crop_size, mean=0.0, std=1.0, downscale=0, resample=PIL.Image.BILINEAR, fillcolor=None):
        self.crop_size = crop_size
        self.mean = mean
        self.std = std
        self.downscale = downscale
        self.resample = resample
        self.fillcolor = fillcolor

    def __call__(self, img):
        """RandomRotatedCrop transform function
        
        Parameters:
            img : PIL.Image
                image to be rotated
            
        Returns:
            rotated image (PIL.Image)
        """
        return F.random_rotated_crop(img, self.crop_size, self.mean, self.std, self.downscale, self.resample, self.fillcolor)

    def __repr__(self):
        format_string = self.__class__.__name__ + '(mean={0}'.format(self.mean)
        format_string += ', std={0}'.format(self.std)
        format_string += ', resample={0}'.format(self.resample)
        format_string += ')'
        return format_string