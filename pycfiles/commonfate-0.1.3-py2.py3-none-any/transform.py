# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/stf_remote/repositories/commonfate/build/lib/commonfate/transform.py
# Compiled at: 2016-03-22 05:38:41
import numpy as np, itertools, scipy.fftpack

def split(sig, frameShape, hop, weightFrames=True, verbose=False):
    """splits a ndarray into overlapping frames

    sig : ndarray

    frameShape : tuple
        giving the size of each frame. If its shape is
        smaller than that of sig, assume the frame is of size 1
        for all missing dimensions

    hop : tuple
        giving the hopsize in each dimension. If its shape is
        smaller than that of sig, assume the hopsize is 1 for all
        missing dimensions

    weightFrames : bool
        return frames weighted by a ND hamming window

    verbose : bool
        whether to output progress during computation"""
    sigShape = np.array(sig.shape)
    if np.isscalar(frameShape):
        frameShape = (
         frameShape,)
    if np.isscalar(hop):
        hop = (
         hop,)
    frameShape = np.array(frameShape)
    fdim = len(frameShape)
    frameShapeAligned = np.append(frameShape, np.ones(len(sigShape) - len(frameShape))).astype(int)
    hop = np.array(hop)
    hop = np.append(hop, np.ones(len(sigShape) - len(hop))).astype(int)
    framesPos = np.ogrid[[ slice(0, size, step) for size, step in zip(sigShape, hop)
                         ]]
    nDim = len(framesPos)
    for dim in range(nDim):
        framesPos[dim] = framesPos[dim][np.nonzero(np.add(framesPos[dim], frameShapeAligned[dim]) < sigShape[dim])]
        if len(framesPos[dim]):
            if framesPos[dim][(-1)] + hop[dim] < sigShape[dim]:
                framesPos[dim] = np.append(framesPos[dim], framesPos[dim][(-1)] + hop[dim])
        else:
            framesPos[dim] = [
             0]

    framedShape = np.append(frameShape, [ len(x) for x in framesPos ])
    if weightFrames:
        win = 1
        for dim in range(len(frameShape) - 1, -1, -1):
            win = np.outer(np.hamming(frameShapeAligned[dim]), win)

        win = np.squeeze(win)
    framed = np.zeros(framedShape, dtype=sig.dtype)
    nFrames = np.prod([ len(x) for x in framesPos ])
    for iframe, index in enumerate(itertools.product(*[ range(len(x)) for x in framesPos ])):
        if verbose and not iframe % 100:
            print 'Splitting : frame ' + str(iframe) + '/' + str(nFrames)
        frameRange = [
         Ellipsis]
        for dim in range(nDim):
            frameRange += [
             slice(framesPos[dim][index[dim]], min(sigShape[dim], framesPos[dim][index[dim]] + frameShapeAligned[dim]), 1)]

        sigFrame = sig[frameRange]
        sigFrame.shape = sigFrame.shape[:fdim]
        sigFrameRange = [ slice(0, x, 1) for x in sigFrame.shape[:fdim] ]
        framed[sigFrameRange + list(index)] = sigFrame
        if weightFrames:
            framed[([Ellipsis] + list(index))] *= win

    frameShape = [ int(x) for x in frameShape ]
    return framed


def overlapadd(S, fdim, hop, shape=None, weightedFrames=True, verbose=False):
    """n-dimensional overlap-add
    S : ndarray
        containing the stft to be inverted

    fdim : int
        the number of dimensions in S corresponding to
        frame indices.

    hop : tuple
        containing hopsizes along dimensions.
        Missing hopsizes are assumed to be 1

    shape : tuple
        Indicating the original shape of the
        signal for truncating. If None: no truncating is done

    weightedFrames : bool
        True if we need to compensate for the analysis weighting
        (weightFrames of the split function)

    verbose : bool
        whether or not to display progress
    """
    nDim = len(S.shape)
    frameShape = S.shape[:fdim]
    trueFrameShape = np.append(frameShape, np.ones(nDim - len(frameShape))).astype(int)
    if np.isscalar(hop):
        hop = (
         hop,)
    hop = np.array(hop)
    hop = np.append(hop, np.ones(nDim - len(hop))).astype(int)
    sigShape = [ (nframedim - 1) * hopdim + frameshapedim for nframedim, hopdim, frameshapedim in zip(S.shape[fdim:], hop, trueFrameShape)
               ]
    framesPos = [ np.arange(size) * step for size, step in zip(S.shape[fdim:], hop)
                ]
    win = np.array(1)
    for dim in range(fdim):
        if trueFrameShape[dim] == 1:
            win = win[(Ellipsis, None)]
        else:
            key = (None, ) * len(win.shape) + (Ellipsis,)
            win = win[(Ellipsis, None)] * np.hamming(trueFrameShape[dim]).__getitem__(key)

    if weightedFrames:
        win2 = win ** 2
    else:
        win2 = win
    sig = np.zeros(sigShape, dtype=S.dtype)
    weights = np.zeros(sigShape)
    nFrames = np.prod(S.shape[fdim:])
    S *= win[([Ellipsis] + [None] * (len(S.shape) - len(win.shape)))]
    for iframe, index in enumerate(itertools.product(*[ range(len(x)) for x in framesPos ])):
        if verbose and not iframe % 100:
            print 'overlap-add : frame ' + str(iframe) + '/' + str(nFrames)
        frameRange = [
         Ellipsis]
        for dim in range(nDim - fdim):
            frameRange += [
             slice(framesPos[dim][index[dim]], min(sigShape[dim], framesPos[dim][index[dim]] + trueFrameShape[dim]), 1)]

        frameSig = S[([Ellipsis] + list(index))]
        sig[frameRange] += frameSig[([Ellipsis] + [
         None] * (len(sig[frameRange].shape) - len(frameSig.shape)))]
        weights[frameRange] += win2[([Ellipsis] + [
         None] * (len(weights[frameRange].shape) - len(win2.shape)))]

    sig /= weights
    if shape is not None:
        sig_res = np.zeros(shape, S.dtype)
        truncateRange = [ slice(0, min(x, sig.shape[i]), 1) for i, x in enumerate(shape)
                        ]
        sig_res[truncateRange] = sig[truncateRange]
        sig = sig_res
    return sig


def forward(sig, frameShape, hop, real=True, verbose=False):
    """Common Fate Transform
    based on a n-dimenional STFT (Short Time Fourier Transform)

    sig : ndarray
        input signal

    frameShape : tuple
        giving the size of each frame. If its shape is
        smaller than that of sig, assume the frame is of size 1
        for all missing dimensions

    hop : tuple
        giving the hopsize in each dimension. If its shape is
        smaller than that of sig, assume the hopsize is 1 for all
        missing dimensions

    real: bool
        if True, use rfft (discard negative frequencies), if False, use
        fft

    verbose : bool
        whether to output progress during computation"""
    if np.isscalar(frameShape):
        frameShape = (
         frameShape,)
    stft = split(sig, frameShape, hop, True, verbose)
    if real:
        fftFunction = np.fft.rfftn
    else:
        fftFunction = scipy.fftpack.fftn
    stft = fftFunction(stft, frameShape, axes=range(len(frameShape)))
    return stft


def inverse(S, fdim, hop, real=True, shape=None, single=False, verbose=False):
    """Inverse Common Fate Transform

    S : ndarray
        containing the stft to be inverted

    fdim : int
        the number of dimensions in S corresponding to
        frequency indices.

    hop : tuple
        containing hopsizes along dimensions.
        Missing hopsizes are assumed to be 1

    real : bool
        if True, using irfft, if False, using ifft

    shape : tuple
        Indicating the original shape of the
        signal for truncating. If None: no truncating is done

    single : bool
        if True, single precision

    verbose : bool
        whether or not to display progress

    """
    if real:
        if single:
            typeSig = 'float32'
        else:
            typeSig = 'float64'
        ifftFunction = np.fft.irfftn
    else:
        if single:
            typeSig = 'complex64'
        else:
            typeSig = 'complex128'
        ifftFunction = scipy.fftpack.ifftn
    S = ifftFunction(S, axes=range(fdim)).astype(typeSig)
    sig = overlapadd(S, fdim, hop, shape, True, verbose)
    return sig