# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/SWHT/display.py
# Compiled at: 2017-08-08 14:46:57
"""
Functions to display images and coefficients
"""
import matplotlib.pyplot as plt, matplotlib.patches, numpy as np, swht, util

def disp2D(img, dmode='dB', cmap='jet'):
    """Display 2D projected image
    img: 2D array of complex flux values
    dmode: string, data mode (abs, dB (absolute value in log units), real, imaginary, phase)
    cmap: string, matplotlib colormap name
    """
    if dmode.startswith('abs'):
        img = np.abs(img)
    else:
        if dmode.startswith('dB'):
            img = 10.0 * np.log10(np.abs(img))
        else:
            if dmode.startswith('real'):
                img = img.real
            else:
                if dmode.startswith('imag'):
                    img = img.imag
                elif dmode.startswith('phase'):
                    img = np.angle(img)
                else:
                    print 'WARNING: Unknown data mode, defaulting to absolute value'
                    img = np.abs(img)
                img = np.fliplr(img)
                fig, ax = plt.subplots(1, 1)
                ax.yaxis.set_ticks([])
                ax.xaxis.set_ticks([])
                ax.patch.set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['right'].set_visible(False)
                plt.imshow(img, interpolation='nearest', cmap=plt.get_cmap(cmap))
                xc = img.shape[0] / 2.0 - 0.5
                yc = img.shape[1] / 2.0 - 0.5
                ax.add_patch(matplotlib.patches.Circle((xc, yc), img.shape[0] / 2.0, fill=False))
                altLines = 5
                deltaAlt = img.shape[0] / (2.0 * altLines)
                for al in range(1, altLines):
                    ax.add_patch(matplotlib.patches.Circle((xc, yc), xc - deltaAlt * al, fill=False, linestyle='dotted', alpha=0.7))

            azLines = 6
            deltaAz = np.pi / azLines
            for az in range(azLines):
                plt.plot(np.array([np.cos(az * deltaAz), np.cos(az * deltaAz + np.pi)]) / 2.0 + 0.5, np.array([np.sin(az * deltaAz), np.sin(az * deltaAz + np.pi)]) / 2.0 + 0.5, 'k:', alpha=0.7, transform=ax.transAxes)

        for az in range(2 * azLines):
            plt.text(img.shape[0] * (1.06 * np.sin(az * deltaAz - np.pi) / 2.0 + 0.5), img.shape[0] * (1.06 * np.cos(az * deltaAz - np.pi) / 2.0 + 0.5), '%.0f' % (az * deltaAz * 180.0 / np.pi), horizontalalignment='center')

    plt.colorbar()
    return (
     fig, ax)


def disp2DStokes(xx, xy, yx, yy, cmap='jet'):
    """Display 2D projected Stokes images
    xx, xy, yx, yy: 2D array of complex flux values
    cmap: string, matplotlib colormap name
    """
    iIm = (xx + yy).real
    qIm = (xx - yy).real
    uIm = (xy + yx).real
    vIm = (yx - xy).imag
    fig, ax = plt.subplots(2, 2)
    plt.axes(ax[(0, 0)])
    plt.imshow(iIm)
    plt.xlabel('Pixels (E-W)')
    plt.ylabel('Pixels (N-S)')
    plt.colorbar()
    plt.title('I')
    plt.axes(ax[(0, 1)])
    plt.imshow(qIm)
    plt.xlabel('Pixels (E-W)')
    plt.ylabel('Pixels (N-S)')
    plt.colorbar()
    plt.title('Q')
    plt.axes(ax[(1, 0)])
    plt.imshow(uIm)
    plt.xlabel('Pixels (E-W)')
    plt.ylabel('Pixels (N-S)')
    plt.colorbar()
    plt.title('U')
    plt.axes(ax[(1, 1)])
    plt.imshow(vIm)
    plt.xlabel('Pixels (E-W)')
    plt.ylabel('Pixels (N-S)')
    plt.colorbar()
    plt.title('V')
    return (
     fig, ax)


def disp3D(img, phi, theta, dmode='abs', cmap='jet'):
    """Display 3D, equal in phi and theta (Driscoll and Healy mapping) image
    img: 2D array of complex flux values
    phi: 2D array of phi values
    theta: 2D array of theta values
        img, phi, theta are of the same shape, they are the output of swht.make3Dimage()
    dmode: string, data mode (abs, real, imaginary, phase)
    cmap: string, matplotlib colormap name
    """
    if dmode.startswith('abs'):
        img = np.abs(img)
    elif dmode.startswith('real'):
        img = img.real
    elif dmode.startswith('imag'):
        img = img.imag
    elif dmode.startswith('phase'):
        img = np.angle(img)
    else:
        print 'WARNING: Unknown data mode, defaulting to absolute value'
        img = np.abs(img)
    X, Y, Z = util.sph2cart(theta, phi)
    from mpl_toolkits.mplot3d import Axes3D
    from matplotlib import cm
    from matplotlib.colors import Normalize
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    imin = img.min()
    imax = img.max()
    scalarMap = cm.ScalarMappable(norm=Normalize(vmin=imin, vmax=imax), cmap=plt.get_cmap(cmap))
    scalarMap.set_array(img)
    C = scalarMap.to_rgba(img)
    surf = ax.plot_surface(X, Y, Z, rstride=1, cstride=1, facecolors=C, antialiased=True)
    fig.colorbar(scalarMap)
    return (fig, ax)


def dispCoeffs(imgCoeffs, zeroDC=True, vis=False):
    """Display SWHT image coefficient values in a 2 rows x 3 columns plot
    imgCoeffs: SWHT image coefficients array
    zeroDC: zero out DC coefficient values
    vis: convert image coefficients to visibility coefficients

    returns: matplotlib figure and subplots
    """
    fig, ax = plt.subplots(2, 3)
    if vis:
        imgCoeffs = swht.computeblm(imgCoeffs, reverse=True)
    if zeroDC:
        imgCoeffs[(0, 0)] = 0
    plt.axes(ax[(0, 0)])
    plt.imshow(imgCoeffs.real, interpolation='nearest')
    plt.title('Real Components')
    plt.colorbar()
    plt.axes(ax[(0, 1)])
    plt.title('Imaginary Components')
    plt.imshow(imgCoeffs.imag, interpolation='nearest')
    plt.colorbar()
    plt.axes(ax[(1, 0)])
    plt.title('Amplitude (dB)')
    plt.imshow(10.0 * np.log10(np.abs(imgCoeffs)), interpolation='nearest')
    plt.colorbar()
    plt.axes(ax[(1, 1)])
    plt.title('Phase')
    plt.imshow(np.angle(imgCoeffs), interpolation='nearest')
    plt.colorbar()
    plt.axes(ax[(0, 2)])
    coeffsFlat = []
    mms = []
    lls = []
    for ll in np.arange(imgCoeffs.shape[0]):
        for mm in np.arange(-1 * ll, ll + 1):
            mms.append(mm)
            lls.append(ll)
            coeffsFlat.append(imgCoeffs[(ll, ll + mm)])

    coeffsFlat = np.array(coeffsFlat)
    plt.ylabel('Amplitude (dB)')
    plt.xlabel('l')
    plt.plot(lls, 10.0 * np.log10(np.abs(coeffsFlat)), '.')
    plt.axes(ax[(1, 2)])
    plt.ylabel('Amplitude (dB)')
    plt.xlabel('m')
    plt.plot(mms, 10.0 * np.log10(np.abs(coeffsFlat)), '.')
    return (
     fig, ax)


def dispVis3D(uvw):
    """3D plot of UVW coverage/sampling
    uvw: (N, 3) array of UVW coordinates

    returns: matplotlib figure and subplots
    """
    from mpl_toolkits.mplot3d import Axes3D
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.scatter(uvw[:, 0], uvw[:, 1], uvw[:, 2], edgecolors='none', alpha=0.5)
    ax.set_xlabel('U (m)')
    ax.set_ylabel('V (m)')
    ax.set_zlabel('W (m)')
    return (
     fig, ax)


def dispVis2D(uvw):
    """2D plot of UV coverage/sampling
    uvw: (N, 3) array of UVW coordinates

    returns: matplotlib figure and subplots
    """
    fig, ax = plt.subplots(2, 1, figsize=(6, 8))
    ax[0].plot(uvw[:, 0], uvw[:, 1], '.', alpha=0.5)
    ax[0].set_xlabel('U (m)')
    ax[0].set_ylabel('V (m)')
    ax[1].plot(np.sqrt(uvw[:, 0] ** 2.0 + uvw[:, 1] ** 2.0), uvw[:, 2], '.', alpha=0.5)
    ax[1].set_xlabel('UVdist (m)')
    ax[1].set_ylabel('W (m)')
    return (
     fig, ax)