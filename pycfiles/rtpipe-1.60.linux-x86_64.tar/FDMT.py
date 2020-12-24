# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cbe-master/realfast/anaconda/envs/deployment/lib/python2.7/site-packages/rtpipe/FDMT.py
# Compiled at: 2017-06-21 14:37:45
Licence = '\n<OWNER> = Barak Zackay (Weizmann Institute of Science)\n<YEAR> = 2014\n\nIn the original BSD license, both occurrences of the phrase "COPYRIGHT HOLDERS AND CONTRIBUTORS" in the disclaimer read "REGENTS AND CONTRIBUTORS".\n\nHere is the license template:\n\nCopyright (c) 2014, Barak Zackay (Weizmann Institute of Science)\nAll rights reserved.\n\nRedistribution and use in source and binary forms, with or without modification, are permitted provided that the following conditions are met:\n\n1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.\n\n2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following disclaimer in the documentation and/or other materials provided with the distribution.\n\nTHIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.\n'
import numpy as np, logging
logger = logging.getLogger(__name__)

def FDMT(data, f_min, f_max, maxDT, dataType):
    r"""
    This function implements the  FDMT algorithm.
    Input: Input visibility array (nints, nbl, nchan, npol)
           f_min,f_max are the base-band begin and end frequencies.
                   The frequencies should be entered in MHz 
           maxDT - the maximal delay (in time bins) of the maximal dispersion.
                   Appears in the paper as N_{\Delta}
                   A typical input is maxDT = N_f
           dataType - a valid numpy dtype.
                      reccomended: either int32, or int64.
    Output: The dispersion measure transform of the Input matrix.
            The output dimensions are [Input.shape[1],maxDT]
    
    For details, see algorithm 1 in Zackay & Ofek (2014)
    """
    nint, nbl, nchan, npol = data.shape
    niters = int(np.log2(nchan))
    assert nchan in 2 ** np.arange(30) and nint in 2 ** np.arange(30), 'Input dimensions must be a power of 2'
    logger.info(('Input data dimensions: {0}').format(data.shape))
    data = FDMT_initialization(data, f_min, f_max, maxDT, dataType)
    logger.info(('Iterating {0} times to calculate to maxDT of {1}').format(niters, maxDT))
    for i_t in range(1, niters + 1):
        data = FDMT_iteration(data, maxDT, nchan, f_min, f_max, i_t, dataType)

    nint, dT, nbl, nchan, npol = data.shape
    assert nchan == 1, 'Channel axis should have length 1 after all FDMT iterations.'
    return np.rollaxis(data[:, :, :, 0, :], 1)


def FDMT_params(f_min, f_max, maxDT, inttime):
    """
    Summarize DM grid and other parameters.
    """
    maxDM = inttime * maxDT / (0.0041488 * (1 / f_min ** 2 - 1 / f_max ** 2))
    logger.info(('Freqs from {0}-{1}, MaxDT {2}, Int time {3} => maxDM {4}').format(f_min, f_max, maxDT, inttime, maxDM))


def dmtoind(dm, f_min, f_max, nchan0, inttime, it):
    """
    Given FDMT state, return indices to slice partial FDMT solution and sump to a given DM
    """
    if it > 0:
        correction = dF / 2.0
    else:
        correction = 0
    shift = []
    nchan = nchan0 / 2 ** iteration_num
    for i_F in range(nchan):
        f_start = (f_max - f_min) / float(nchan) * i_F + f_min
        f_end = (f_max - f_min) / float(nchan) * (i_F + 1) + f_min
        f_middle = (f_end - f_start) / 2.0 + f_start - correction
        f_middle_larger = (f_end - f_start) / 2 + f_start + correction
        dT_middle = int(round(i_dT * (1.0 / f_middle ** 2 - 1.0 / f_start ** 2) / (1.0 / f_end ** 2 - 1.0 / f_start ** 2)))
        dT_middle_larger = int(round(i_dT * (1.0 / f_middle_larger ** 2 - 1.0 / f_start ** 2) / (1.0 / f_end ** 2 - 1.0 / f_start ** 2)))
        shift.append((-dT_middle_larger, i_F))


def FDMT_initialization(datain, f_min, f_max, maxDT, dataType):
    r"""
    Input: datain - visibilities of (nint, nbl, nchan, npol)
        f_min,f_max - are the base-band begin and end frequencies.
            The frequencies can be entered in both MHz and GHz, units are factored out in all uses.
        maxDT - the maximal delay (in time bins) of the maximal dispersion.
            Appears in the paper as N_{\Delta}
            A typical input is maxDT = N_f
        dataType - To naively use FFT, one must use floating point types.
            Due to casting, use either complex64 or complex128.
    Output: dataout, 3d array, with dimensions [nint, N_d0, nbl, nchan, npol]
            where N_d0 is the maximal number of bins the dispersion curve travels at one frequency bin
    
    For details, see algorithm 1 in Zackay & Ofek (2014)
    """
    nint, nbl, nchan, npol = datain.shape
    deltaF = (f_max - f_min) / float(nchan)
    deltaT = int(np.ceil((maxDT - 1) * (1.0 / f_min ** 2 - 1.0 / (f_min + deltaF) ** 2) / (1.0 / f_min ** 2 - 1.0 / f_max ** 2)))
    dataout = np.zeros([nint, deltaT + 1, nbl, nchan, npol], dataType)
    dataout[:, 0, :, :, :] = datain
    for i_dT in xrange(1, deltaT + 1):
        dataout[i_dT:, i_dT, :, :, :] = dataout[i_dT:, i_dT - 1, :, :, :] + datain[:-i_dT]

    return dataout


def FDMT_iteration(datain, maxDT, nchan0, f_min, f_max, iteration_num, dataType):
    r"""
        Input: 
            Input - 3d array, with dimensions [nint, N_d0, nbl, nchan, npol]
            f_min,f_max - are the base-band begin and end frequencies.
                The frequencies can be entered in both MHz and GHz, units are factored out in all uses.
            maxDT - the maximal delay (in time bins) of the maximal dispersion.
                Appears in the paper as N_{\Delta}
                A typical input is maxDT = N_f
            dataType - To naively use FFT, one must use floating point types.
                Due to casting, use either complex64 or complex128.
            iteration num - Algorithm works in log2(Nf) iterations, each iteration changes all the sizes (like in FFT)
        Output: 
            5d array, with dimensions [nint, N_d1, nbl, nchan/2, npol]
        where N_d1 is the maximal number of bins the dispersion curve travels at one output frequency band
        
        For details, see algorithm 1 in Zackay & Ofek (2014)
    """
    nint, dT, nbl, nchan, npol = datain.shape
    deltaF = 2 ** iteration_num * (f_max - f_min) / float(nchan0)
    dF = (f_max - f_min) / float(nchan0)
    deltaT = int(np.ceil((maxDT - 1) * (1.0 / f_min ** 2 - 1.0 / (f_min + deltaF) ** 2) / (1.0 / f_min ** 2 - 1.0 / f_max ** 2)))
    logger.debug(('deltaT = {0}').format(deltaT))
    logger.debug(('N_f = {0}').format(nchan0 / 2 ** iteration_num))
    dataout = np.zeros((nint, deltaT + 1, nbl, nchan / 2, npol), dataType)
    logger.debug(('input_dims = {0}').format(datain.shape))
    logger.debug(('output_dims = {0}').format(dataout.shape))
    ShiftOutput = 0
    ShiftInput = 0
    F_jumps = nchan / 2
    if iteration_num > 0:
        correction = dF / 2.0
    else:
        correction = 0
    for i_F in range(F_jumps):
        f_start = (f_max - f_min) / float(F_jumps) * i_F + f_min
        f_end = (f_max - f_min) / float(F_jumps) * (i_F + 1) + f_min
        f_middle = (f_end - f_start) / 2.0 + f_start - correction
        f_middle_larger = (f_end - f_start) / 2 + f_start + correction
        deltaTLocal = int(np.ceil((maxDT - 1) * (1.0 / f_start ** 2 - 1.0 / f_end ** 2) / (1.0 / f_min ** 2 - 1.0 / f_max ** 2)))
        logger.debug(('deltaT {0} deltaTLocal {1}').format(deltaT, deltaTLocal))
        for i_dT in range(deltaTLocal + 1):
            dT_middle = int(round(i_dT * (1.0 / f_middle ** 2 - 1.0 / f_start ** 2) / (1.0 / f_end ** 2 - 1.0 / f_start ** 2)))
            dT_middle_index = dT_middle + ShiftInput
            dT_middle_larger = int(round(i_dT * (1.0 / f_middle_larger ** 2 - 1.0 / f_start ** 2) / (1.0 / f_end ** 2 - 1.0 / f_start ** 2)))
            dT_rest = i_dT - dT_middle_larger
            dT_rest_index = dT_rest + ShiftInput
            logger.debug(('{0}:{1}, {2}+{3}, {4} <= {5}, {6}').format(i_T_min, i_T_max, i_dT, ShiftOutput, i_F, dT_middle_index, 2 * i_F))
            i_T_min = 0
            i_T_max = dT_middle_larger
            dataout[i_T_min:i_T_max, i_dT + ShiftOutput, :, i_F, :] = datain[i_T_min:i_T_max, dT_middle_index, :, 2 * i_F, :]
            i_T_min = dT_middle_larger
            i_T_max = nint
            dataout[i_T_min:i_T_max, i_dT + ShiftOutput, :, i_F, :] = datain[i_T_min:i_T_max, dT_middle_index, :, 2 * i_F, :] + datain[i_T_min - dT_middle_larger:i_T_max - dT_middle_larger, dT_rest_index, :, 2 * i_F + 1, :]

    return dataout