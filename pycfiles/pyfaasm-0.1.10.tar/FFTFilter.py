# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyF3D/filters/FFTFilter.py
# Compiled at: 2017-04-27 19:06:13
import numpy as np, pkg_resources as pkg, pyopencl as cl, time, pyF3D.FilterClasses as fc

class FFTFilter:
    """
    Class for a FFT filter of specified direction

    Parameters
    ----------
    FFTChoice: str, optional
        Must be either 'Foward' or 'Inverse', to specify the direction of the operation
    """
    FFTChoice = [
     'Forward', 'Inverse']

    def __init__(self, FFTChoice='Forward'):
        import warnings
        warnings.warn('FFT Filter not yet implemented', RuntimeWarning)
        if FFTChoice not in self.FFTChoice:
            raise ValueError("'FFTChoice' parameter must be either 'Forward' or 'Inverse'")
        self.name = 'FFTFilter'
        self.selectedFFTChoice = FFTChoice
        self.clattr = None
        self.atts = None
        return

    def toJSONString(self):
        result = '{ + "Name" : "' + self.getName() + '" , '
        result += '"fftChoice" : "' + str(self.selectedFFTChoice) + '" , }'
        return result

    def clone(self):
        return FFTFilter(FFTChoice=self.selectedFFTChoice)

    def getInfo(self):
        info = fc.FilterInfo()
        info.name = self.getName()
        info.memtype = float
        info.useTempBuffer = True
        info.overlapX = info.overlapY = info.overlapZ = 0
        return info

    def getName(self):
        return 'FFTFilter'

    def loadKernel(self):
        try:
            filename = '../OpenCL/FFTFilter.cl'
            program = cl.Program(self.clattr.context, pkg.resource_string(__name__, filename)).build()
        except Exception as e:
            raise e

        self.kernel = cl.Kernel(program, 'FFTFilter')
        return True

    def runFilter(self):
        direction = 1 if self.selectedFFTChoice == 'Forward' else -1
        globalSize = [
         0, 0]
        localSize = [0, 0]
        self.clattr.computeWorkingGroupSize(localSize, globalSize, [self.atts.height, self.atts.slices, 1])
        try:
            self.kernel.set_args(self.clattr.inputBuffer, self.clattr.outputBuffer, self.clattr.outputTmpBuffer, np.int32(direction), np.int32(self.atts.width), np.int32(self.atts.height), np.int32(self.clattr.maxSliceCount), np.int32(0))
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