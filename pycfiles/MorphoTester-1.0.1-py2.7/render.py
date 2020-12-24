# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/MorphoTester/render.py
# Compiled at: 2015-09-30 15:18:52
"""
Created on Sep 8, 2011

This module contains three functions that plot the 2D projection of a 3D mesh in
the XY plane and measure the absolute area of the mesh projection. The function 
plotmeshoutline() plots a) the provided mesh in blue over the X and Y axes and 
b) a red scalebar where length is known in coordinate units and pixels. This 
produces a "flat" 2D projection of the 3D mesh input on the XY plane. The plot
is then returned as a StringIO file-like object and the scalebar pixel length 
is returned as a float. The function areafromrender() uses the image buffer and
the scalebar pixel length to derive the absolute projection area ("outline
area") of the 3D mesh in the XY plane.

@author: Julia M. Winchester
"""
import matplotlib
matplotlib.use('AGG')
import matplotlib.pyplot as plt, Image
from StringIO import StringIO
from numpy import array, amax, amin, square

def countpixels(image, colorlist):
    return sum(list(image).count(color) for color in colorlist)


def areafromrender(linelength, strbuffer):
    strbuffer.seek(0)
    img = Image.open(strbuffer).getdata()
    strbuffer.close()
    redpixie = countpixels(img, [(255, 0, 0, 255), (255, 127, 127, 255)])
    bluepixie = len(list(img)) - countpixels(img, [(255, 0, 0, 255), (255, 255, 255, 255), (255, 155, 155, 255), (255, 188, 188, 255), (255, 230, 230, 255), (255, 205, 205, 255)])
    print 'blue pixels = ' + str(bluepixie)
    rope = float(linelength)
    print 'line = ' + str(rope)
    redballoon = float(redpixie)
    print 'red pixels = ' + str(redballoon)
    return float(bluepixie) * (square(rope) / square(redballoon))


def plotmeshoutline(mesh):
    xarray = mesh[0][:, 0]
    yarray = mesh[0][:, 1]
    xaxismin = amin(xarray) - 0.5
    xaxismax = amax(xarray) + 0.5
    yaxismin = amin(yarray) - 0.5
    yaxismax = amax(yarray) + 0.5
    linelength = amax(yarray) - amin(yarray) + 1
    fig = plt.figure()
    ax = fig.add_subplot(111)
    linesquare = matplotlib.patches.Polygon([[xaxismin, yaxismin], [xaxismin, yaxismax]], ec='r', fc='r')
    plt.axis([xaxismin, xaxismax, yaxismin, yaxismax])
    ax.add_patch(linesquare)
    ax.set_xscale('linear')
    ax.set_yscale('linear')
    ax.set_aspect(1)
    ax.axis('off')
    vert = array([ face[:, [0, 1]] for face in mesh[1] ])
    polygons = matplotlib.collections.PolyCollection(vert, facecolor='b', edgecolor='b')
    ax.add_collection(polygons)
    imgbuffer = StringIO()
    plt.savefig(imgbuffer, format='png')
    return (linelength, imgbuffer)


def meshprojectionarea(mesh):
    linelength, imgbuffer = plotmeshoutline(mesh)
    return areafromrender(linelength, imgbuffer)