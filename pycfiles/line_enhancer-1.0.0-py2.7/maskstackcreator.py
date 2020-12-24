# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/line_enhancer/maskstackcreator.py
# Compiled at: 2018-08-02 09:09:23
import numpy as np, functools, scipy.ndimage

class MaskStackCreator:

    def __init__(self, filament_width, mask_size, mask_width, angle_step, interpolation_order=1, bright_background=False):
        self._filament_width = filament_width
        self._mask_size = mask_size
        self._mask_width = mask_width
        self._mask_stack = None
        self._mask_fft_stack = None
        self._angle_step = angle_step
        self._interpolation_order = interpolation_order
        self._bright_background = bright_background
        return

    def get_mask_stack(self):
        return self._mask_stack

    def get_mask_fft_stack(self):
        if self._mask_fft_stack is not None:
            return self._mask_fft_stack
        else:
            mask = self.calculate_mask(self._mask_size, self._filament_width, self._mask_width)
            self._mask_fft_stack = self.calculate_fourier_mask_stack_vectorized(mask, self._angle_step)
            return self._mask_fft_stack

    def set_interpolation_order(self, order):
        self._interpolation_order = order

    def get_angle_step(self):
        return self._angle_step

    def get_mask_size(self):
        return self._mask_size

    def calculate_mask(self, mask_size, filament_width, mask_width):
        mask = np.zeros(shape=(mask_size, mask_size))
        x0 = mask_size / 2.0 + 0.5
        y0 = mask_size / 2.0 + 0.5
        sigmax = mask_width / 2.355
        varx = sigmax * sigmax
        sigmay = filament_width / 2.355
        vary = sigmay * sigmay
        background_factor = 1.0
        if self._bright_background:
            background_factor = -1.0
        for i in range(0, mask_size):
            for j in range(0, mask_size):
                y = j + 0.5
                x = i + 0.5
                value = background_factor * np.pi * sigmax * (vary - np.power(y - y0, 2)) / (2 * vary * sigmay) * np.exp(-1.0 * (np.power(x - x0, 2) / (2 * varx) + np.power(y - y0, 2) / (2 * vary)))
                if np.sqrt((y - y0) ** 2 + (x - x0) ** 2) > 300:
                    value = 0
                mask[(j, i)] = value

        return mask

    def rotate_and_fft(self, mask, angle):
        rot_mask = scipy.ndimage.interpolation.rotate(mask, angle, reshape=False, order=self._interpolation_order)
        return rot_mask

    def calculate_fourier_mask_stack_vectorized(self, mask, angle_step):
        angle_steps = range(0, 180, angle_step)
        result = map(functools.partial(self.rotate_and_fft, mask), angle_steps)
        self._mask_stack = np.asarray(result)
        result_fft = np.fft.rfft2(self._mask_stack, axes=(-2, -1))
        result_fft = np.moveaxis(result_fft, 0, 2)
        return result_fft