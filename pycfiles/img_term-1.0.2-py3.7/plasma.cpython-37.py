# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/img_term/plasma.py
# Compiled at: 2019-06-13 01:37:09
# Size of source mod 2**32: 3641 bytes
import numpy as np
from matplotlib import cm
from itertools import cycle
import pyopencl as cl, pyopencl.array

class Plasma:

    def __init__(self, rows, columns):
        self.height = columns
        self.width = rows
        color_maps = [
         'inferno', 'gnuplot', 'magma', 'viridis', 'plasma', 'cubehelix', 'gnuplot2', 'ocean', 'terrain',
         'CMRmap', 'nipy_spectral']
        maps = [np.array(list(map(lambda i: (np.array(cm.get_cmap(x, 256)(i)[:-1]) * 255).astype(np.uint8), np.arange(0, 256)))) for x in color_maps]
        tup = (
         maps[0],
         maps[0][::-1],
         maps[1],
         maps[1][::-1],
         maps[2],
         maps[2][::-1],
         maps[5],
         maps[5][::-1],
         maps[3],
         maps[4][::-1],
         maps[6],
         maps[7][::-1],
         maps[8],
         maps[9][::-1],
         maps[10],
         maps[10][::-1])
        self.cols = np.concatenate(tup)
        self.cols = np.concatenate((self.cols, self.cols[::-1]))
        self.step = 0
        denoms = np.sin(np.arange(0, 2 * np.pi, 0.01)) + 3
        self.denom = cycle(denoms)
        self.up = True
        self.half_len = len(self.cols) / 32.0
        self.ctx = cl.Context([cl.get_platforms()[1].get_devices()[0]])
        self.queue = cl.CommandQueue(self.ctx)
        self.lut = np.empty(len(self.cols), cl.array.vec.char3)
        for idx, i in enumerate(self.cols):
            self.lut[idx][0] = i[2]
            self.lut[idx][1] = i[1]
            self.lut[idx][2] = i[0]

        mf = cl.mem_flags
        self.lut_opencl = cl.Buffer((self.ctx), (mf.READ_ONLY | mf.COPY_HOST_PTR), hostbuf=(self.lut))
        prg = cl.Program(self.ctx, '\n               __kernel void plasma(__global uchar4 *img,\n                                    __constant uchar4 *lut,\n                                    float const denom,\n                                    uint step,\n                                    uint const height,\n                                    uint const width,\n                                    uint const colours) {{\n                   const int x = get_global_id(0);\n                   const int y = get_global_id(1);\n                   const int index = y * height + x;\n                   const float half_len = {0};\n                   const int h = step + half_len + (half_len * native_sin((float)native_sqrt(pow(x - width / 2.,2)+ pow(y - height / 2.,2)) / denom));\n                   if( h  < colours) {{\n                       img[index] = lut[h];\n                   }} else {{\n                       img[index] = lut[colours - h];\n                   }}\n               }}\n           '.format(self.half_len)).build()
        self.krnl = prg.plasma
        self.out_img = img = np.zeros((self.width * self.height, 4), np.uint8)
        self.out_buffer = cl.Buffer(self.ctx, mf.WRITE_ONLY, img.nbytes)

    def __call__(self):
        self.krnl(self.queue, (self.height, self.width), None, self.out_buffer, self.lut_opencl, np.float32(next(self.denom)), np.uint32(self.step), np.uint32(self.height), np.uint32(self.width), np.uint32(len(self.cols)))
        self.step += 5
        self.step %= len(self.cols)
        cl.enqueue_copy(self.queue, self.out_img, self.out_buffer).wait()
        return self.out_img.reshape((self.width, self.height, 4))[:, :, :3]