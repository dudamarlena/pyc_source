# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyF3D/filters/MedianFilter.py
# Compiled at: 2017-04-27 19:01:26
import numpy as np, pkg_resources as pkg, pyopencl as cl, pyF3D.FilterClasses as fc

class MedianFilter:
    """
    Class for a 3D median filter of radius 3 (no parameters)
    """

    def __init__(self):
        self.name = 'MedianFilter'
        self.index = -1
        self.clattr = None
        self.atts = None
        return

    def clone(self):
        return MedianFilter()

    def toJSONString(self):
        result = '{ "Name" : "' + self.getName() + '", ' + '" }'
        return result

    def getInfo(self):
        info = fc.FilterInfo()
        info.name = self.getName()
        info.memtype = bytes
        info.overlapX = info.overlapY = info.overlapZ = 4
        return info

    def getName(self):
        return 'MedianFilter'

    def loadKernel(self):
        try:
            filename = '../OpenCL/MedianFilter.cl'
            program = cl.Program(self.clattr.context, pkg.resource_string(__name__, filename)).build()
        except Exception as e:
            raise e

        self.kernel = cl.Kernel(program, 'MedianFilter')
        return True

    def runFilter(self):
        if self.atts.height == 1 and self.atts.slices == 1:
            mid = 1
        else:
            if self.atts.slices == 1:
                mid = 4
            else:
                mid = 13
            globalSize = [0, 0]
            localSize = [0, 0]
            self.clattr.computeWorkingGroupSize(localSize, globalSize, [self.atts.width, self.atts.height, 1])
            try:
                self.kernel.set_args(self.clattr.inputBuffer, self.clattr.outputBuffer, np.int32(self.atts.width), np.int32(self.atts.height), np.int32(self.clattr.maxSliceCount), np.int32(mid))
                cl.enqueue_nd_range_kernel(self.clattr.queue, self.kernel, globalSize, localSize)
            except Exception as e:
                raise e

        cl.enqueue_copy(self.clattr.queue, self.clattr.inputBuffer, self.clattr.outputBuffer)
        self.clattr.queue.finish()
        return True

    def setAttributes(self, CLAttributes, atts, index):
        self.clattr = CLAttributes
        self.atts = atts
        self.index = index