# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepJetCore/preprocessing/preprocessing.py
# Compiled at: 2018-07-12 08:05:01
import numpy
from array import array
import logging

def setTreeName(name):
    from DeepJetCore.compiled import c_meanNormZeroPad
    c_meanNormZeroPad.setTreeName(name)


def setDefaultsZero(inarray):
    inarray[inarray == -999] = 0
    return inarray


def produceWeigths(Tuple, nameX, nameY, bins, classes=[], normed=False):
    """
    provides a weight vector to flatten (typically)  PT and eta
    
    Tuple: are the features that need to be reweighted, it needs to be a recarray that had the fields nameX, 
    nameY and classes. The returned weight vector will flatten the Tuple in a 2D plane nameX,nameY for each 
    class (e.g. is B-quark)

    nameX,nameY: names of the fiels that containt the variables to flattedn (usually eta/Pt)

    bins: are the bins used to flatten the distributions. Please use the syntax as in numpy.histogram2d

    classes: These are the one-hot-encoded classes. The weights are made such that each class is flat in 2D

    """
    weight = []
    hists = []
    countMissedJets = 0
    if classes == []:
        hists.append(numpy.histogram2d(Tuple[nameX], Tuple[nameY], bins, normed=True))
    else:
        for label in classes:
            nameXvec = Tuple[nameX]
            nameYvec = Tuple[nameY]
            valid = Tuple[label] > 0.0
            w_, _, _ = numpy.histogram2d(nameXvec[valid], nameYvec[valid], bins, normed=normed)
            hists.append(w_)

        Axixandlabel = [
         nameX, nameY] + classes
        axisX = bins[0]
        axisY = bins[1]
        for jet in iter(Tuple[Axixandlabel]):
            binX = getBin(jet[nameX], axisX)
            binY = getBin(jet[nameY], axisY)
            if classes == []:
                weight.append(1.0 / hists[0][binX][binY])
            else:
                didappend = 0
                for index, classs in enumerate(classes):
                    if 1 == jet[classs]:
                        weight.append(1.0 / hists[index][binX][binY])
                        if 1.0 / hists[index][binX][binY] > 0.002646:
                            print (
                             classs, ' ', jet[nameX], ' ', jet[nameY], ' weight ', 1.0 / hists[index][binX][binY] / 0.0002646)
                        didappend = 1

                if didappend == 0:
                    countMissedJets += 1
                    weight.append(0)

    if countMissedJets > 0:
        print (
         'WARNING from weight calculator: ', countMissedJets, '/', len(weight), ' had no valid label and got weight 0 (i.e. are ignore, but eat up space and time')
    weight = numpy.asarray(weight)
    print (
     'weight average: ', weight.mean())
    weight = weight / weight.mean()
    return weight


def meanNormProd(Tuple):
    """
    This function makes a reacarray with the same fields (branches in root talk) as the input tree. The recarray has only two entries, the mean [0] and the st. dev. [1] for each field. If an field was an array the mean of all entries is taken. This is to be used to mean normalize the the input features to ML for faster convergence.
    comment: done seldomly, no need for a quicker solution.
    TO DO: we need to add a parser to JSON to interface to C++ or store straight a C++ map as well.
   
    """
    import numpy
    BranchList = Tuple.dtype.names
    dTypeList = []
    mean = ()
    stddev = ()
    formats = ' '
    names = ' '
    for name in iter(BranchList):
        if Tuple[[name]].dtype[0] == 'object':
            chain = numpy.concatenate(Tuple[name])
            chainsize = chain.size
            chain = chain[numpy.invert(numpy.isinf(chain[:]))]
            if chainsize != chain.size:
                logging.warning(' There are Inf in the tuple !!! Removed infinities to keep going, but PLEASE CHECK where the fuck they are comming from ')
            mean = mean + (chain.mean(),)
            addstddev = chain.std()
            if not addstddev:
                addstddev = 1
            stddev = stddev + (addstddev,)
            logging.info('name: %s --> %s' % (name, chain.shape))
            logging.info('%s %s' % (chain.mean(), chain.std()))
            dTypeList.append((name, float))
        else:
            array = Tuple[name].view(numpy.ndarray)
            array = setDefaultsZero(array)
            mean = mean + (array.mean(),)
            addstddev = array.std()
            if not addstddev:
                addstddev = 1
            stddev = stddev + (addstddev,)
            logging.info('name: %s --> %s' % (name, array.shape))
            logging.info('%s %s' % (array.mean(), array.std()))
            formats += 'float32,'
            names += name + ','
            dTypeList.append((name, float))

    y = numpy.array([mean, stddev], dtype=dTypeList)
    return y


def MakeHexagonBox():
    """
    This shoudl return a 1D array with hexagonal coordinates. Zero is the center.
    """
    pass


def getBin(value, bins):
    """
    Get the bin of "values" in axis "bins".
    Not forgetting that we have more bin-boundaries than bins (+1) :)
    """
    for index, bin in enumerate(bins):
        if value < bin:
            return index - 1

    print (
     ' overflow ! ', value, ' out of range ', bins)
    return bins.size - 2


def MakeSparseBox(Tuples, nameX, nameY, binX, binY, nMaxObj):
    """
    To be coded
    """
    pass


def MakeBox(Tuples, nameX, nameY, binX, binY, nMaxObj):
    """ 
    function to build from a set of continuously located variables a binned version, e.g. all elements within phi and eta are gathered into one bin. The methods return a 3D ndarray with to direction (e.g. eta, phi) and as 3D (channels) a zero padded constant length vector with the variables
    
    Tuples: list of tupels (recarray) containg only the set of variables that need to be zero padded. First Tuple is the one to be zero padded, that latter should store for mean substraction and scaling as first
        element. The alttaer can be made with meanNormProd(Tuple)

    nameX, nameY: String with the names on which to apply the cuts
    binX,binY ndarray with the bin boudaries
    nMaxObj: Number of objects per bin. If not reached it will be zero padded. If too long cropped.

    FIXME: many zeros will blow up memory use, should be optimized!!
    """
    Tuple = Tuples[0]
    TuplesMeanDev = Tuples[1]
    BranchList = Tuple.dtype.names
    nInput = len(BranchList)
    BoxList = []
    nMax = nMaxObj * nInput + 1
    cutCounter = 0
    for jet in iter(Tuple):
        array = numpy.zeros((binX.size - 1, binY.size - 1, nMax), dtype=float)
        for index in range(jet[nameX].size):
            binx = getBin(jet[nameX][index], binX)
            biny = getBin(jet[nameY][index], binY)
            if not array[binx][biny][0] * (nInput + 1) >= nMax:
                for PFindex, varname in enumerate(BranchList):
                    if varname == nameX:
                        array[binx][biny][int(array[binx][biny][0] * nInput) + PFindex + 1] = jet[nameX][index] - binX[binx]
                    elif varname == nameY:
                        array[binx][biny][int(array[binx][biny][0] * nInput) + PFindex + 1] = jet[nameY][index] - binY[binx]
                    else:
                        stdDev = TuplesMeanDev[varname][1]
                        if stdDev < 1e-05:
                            stdDev = 1e-05
                        array[binx][biny][int(array[binx][biny][0] * nInput) + PFindex + 1] = (jet[varname][index] - TuplesMeanDev[varname][0]) / stdDev

                array[binx][biny][0] += 1
            else:
                cutCounter += 1

        BoxList.append(array)

    print (
     cutCounter, ' times vector was longer than maximum of: ', nMaxObj)
    return numpy.asarray(BoxList)


def MeanNormApply(Tuple, MeanNormTuple):
    """
    The function subtracts the mean and divedes by the std. deviation.
    It is not intended for fields that are arrays. Flexiable array length features are delt with in makeBox. They are automatically zerpatched and mean subtracted. 
    Tuple: numpy.recarray that contains the features
    MeanNormTuple: numpy.recarray that contains the means and norm
    
    The function retuen a numpy.ndarray! That is mean subtracted and normalized AND all values og -999 are patched to 0 as well!
    """
    import numpy
    arrayList = []
    for field in iter(Tuple.dtype.names):
        if Tuple[field].dtype == 'O':
            print (
             'WARNING: This is means subtraction is not for vectors! The filed is and array. Use MeanNormZeroPad!', field)
        array = Tuple[field].copy().view(numpy.ndarray)
        array = setDefaultsZero(array)
        array = numpy.subtract(array, MeanNormTuple[field][0])
        array = numpy.divide(array, MeanNormTuple[field][1])
        arrayList.append(array)

    return numpy.asarray(arrayList).transpose()


def MeanNormZeroPadBinned(Filename_in, counter, nevents, dimension1, dimension2, binned_info, summed_info):
    """Takes too long to run the binning twice, run it only once and compute at the same time
    both the binned and the summed variables"""
    from DeepJetCore.compiled import c_meanNormZeroPad
    MeanNormTuple, inbranches, nMax = binned_info
    means = []
    norms = []
    for b in inbranches:
        if MeanNormTuple == None:
            means.append(0)
            norms.append(1)
        else:
            means.append(MeanNormTuple[b][0])
            norms.append(MeanNormTuple[b][1])

    x_branch, x_center, x_bins, x_width = dimension1
    y_branch, y_center, y_bins, y_width = dimension2
    mean_std_list, summed_branches = summed_info
    sum_mean = []
    sum_std = []
    for name in mean_std_list:
        sum_mean.append(MeanNormTuple[name][0])
        sum_std.append(MeanNormTuple[name][1])

    summed = numpy.zeros((
     nevents, x_bins, y_bins, len(summed_branches) + 1), dtype='float32')
    binned = numpy.zeros((
     nevents, x_bins, y_bins, nMax, len(inbranches)), dtype='float32')
    c_meanNormZeroPad.particle_binner(Filename_in, counter, x_branch, x_center, x_bins, x_width, y_branch, y_center, y_bins, y_width, binned, norms, means, inbranches, nMax, summed, sum_std, sum_mean, summed_branches)
    return (
     binned, summed)


def createDensityMap(Filename_in, MeanNormTuple, inbranch, nevents, dimension1, dimension2, counter, offset=0, weightbranch=''):
    from DeepJetCore.compiled import c_meanNormZeroPad
    norm = 1.0
    x_branch, x_center, x_bins, x_width = dimension1
    y_branch, y_center, y_bins, y_width = dimension2
    array = numpy.zeros((nevents, x_bins, y_bins, 1), dtype='float32')
    c_meanNormZeroPad.fillDensityMap(array, norm, inbranch, weightbranch, Filename_in, counter, x_branch, x_center, x_bins, x_width, y_branch, y_center, y_bins, y_width, offset)
    return array


def createCountMap(Filename_in, MeanNormTuple, nevents, dimension1, dimension2, counter, offset=0, weightbranch=''):
    from DeepJetCore.compiled import c_meanNormZeroPad
    norm = 1.0
    x_branch, x_center, x_bins, x_width = dimension1
    y_branch, y_center, y_bins, y_width = dimension2
    array = numpy.zeros((nevents, x_bins, y_bins, 1), dtype='float32')
    c_meanNormZeroPad.fillCountMap(array, norm, weightbranch, Filename_in, counter, x_branch, x_center, x_bins, x_width, y_branch, y_center, y_bins, y_width, offset)
    return array


def createDensity(Filename_in, inbranches, modes, nevents, dimension1, dimension2, counterbranch, offsets=None):
    from DeepJetCore.compiled import c_meanNormZeroPad
    layerbranch = ''
    maxlayers = 1
    layeroffset = 0
    norms = [ 1 for x in range(len(inbranches)) ]
    means = []
    if not offsets:
        means = [ 0 for x in range(len(inbranches)) ]
    else:
        means = offsets
    x_branch, x_center, x_bins, x_width = dimension1
    y_branch, y_center, y_bins, y_width = dimension2
    array = numpy.zeros((nevents, x_bins, y_bins, maxlayers, len(inbranches)), dtype='float32')
    c_meanNormZeroPad.fillDensityLayers(array, norms, means, inbranches, modes, layerbranch, maxlayers, layeroffset, Filename_in, counterbranch, x_branch, x_center, x_bins, x_width, y_branch, y_center, y_bins, y_width)
    array = numpy.reshape(array, (nevents, x_bins, y_bins, len(inbranches)))
    return array


def createDensityLayers(Filename_in, MeanNormTuple, inbranches, modes, layerbranch, maxlayers, layeroffset, nevents, dimension1, dimension2, counterbranch, scales=None):
    from DeepJetCore.compiled import c_meanNormZeroPad
    if not scales:
        norms = [ 1 for x in range(len(inbranches)) ]
    else:
        norms = scales
        if not len(scales) == len(inbranches):
            raise ValueError('Scales length must match number of branches')
    means = [ 0 for x in range(len(inbranches)) ]
    x_branch, x_center, x_bins, x_width = dimension1
    y_branch, y_center, y_bins, y_width = dimension2
    array = numpy.zeros((nevents, x_bins, y_bins, maxlayers, len(inbranches)), dtype='float32')
    c_meanNormZeroPad.fillDensityLayers(array, norms, means, inbranches, modes, layerbranch, maxlayers, layeroffset, Filename_in, counterbranch, x_branch, x_center, x_bins, x_width, y_branch, y_center, y_bins, y_width)
    return array


def MeanNormZeroPadParticles(Filename_in, MeanNormTuple, inbranches, nMax, nevents):
    from DeepJetCore.compiled import c_meanNormZeroPad
    array = numpy.zeros((nevents, nMax, len(inbranches)), dtype='float32')
    means = []
    norms = []
    for b in inbranches:
        if MeanNormTuple is None:
            means.append(0)
            norms.append(1)
        else:
            means.append(MeanNormTuple[b][0])
            norms.append(MeanNormTuple[b][1])

    c_meanNormZeroPad.particlecluster(array, [norms], [means], [inbranches], [nMax], Filename_in)
    return array


def MeanNormZeroPad(Filename_in, MeanNormTuple, inbranches_listlist, nMaxslist, nevents):
    """
    The function subtracts the mean and divides by the std. deviation.
    It is intended for fields that are arrays. They are automatically zerpatched and mean subtracted up to nMax.
    New (Jan): due to performance reasons this part has been put in a compiled C++ module that is called here
    """
    import copy
    from DeepJetCore.compiled import c_meanNormZeroPad
    inbranches_listlist = copy.deepcopy(inbranches_listlist)
    nMaxslist = copy.deepcopy(nMaxslist)
    totallengthperjet = 0
    for i in range(len(nMaxslist)):
        if nMaxslist[i] >= 0:
            totallengthperjet += len(inbranches_listlist[i]) * nMaxslist[i]
        else:
            totallengthperjet += len(inbranches_listlist[i])

    array = numpy.zeros((nevents, totallengthperjet), dtype='float32')
    normslist = []
    meanslist = []
    for inbranches in inbranches_listlist:
        means = []
        norms = []
        for b in inbranches:
            if MeanNormTuple is None:
                means.append(0)
                norms.append(1)
            else:
                means.append(MeanNormTuple[b][0])
                norms.append(MeanNormTuple[b][1])

        meanslist.append(means)
        normslist.append(norms)

    c_meanNormZeroPad.process(array, normslist, meanslist, inbranches_listlist, nMaxslist, Filename_in)
    return array