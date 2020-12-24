# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vasctrees/mayaviCTA.py
# Compiled at: 2012-06-28 14:46:47
from enthought.mayavi import mlab
import numpy as np, random

def viewGraph(g, sub=3, title=''):
    mlab.figure(bgcolor=(0, 0, 0), size=(900, 900))
    nodes = g.nodes()
    random.shuffle(nodes)
    nodes = np.array(nodes[0:100])
    edges = g.edges(data=True)
    print len(edges)
    raw_input('continue')
    count = 0
    for n1, n2, edge in edges:
        count += 1
        if count % 100 == 0:
            print count
        path = [
         n1] + edge['path'] + [n2]
        pa = np.array(path)
        mlab.plot3d(pa[::sub, 2], pa[::sub, 1], pa[::sub, 0], color=(0, 1, 0), tube_radius=0.75)

    mlab.view(-125, 54, 'auto', 'auto')
    mlab.roll(-175)
    mlab.title(title, height=0.1)
    mlab.show()


def viewImgWithNodes(img, spacing, contours, g, title=''):
    mlab.figure(bgcolor=(0, 0, 0), size=(900, 900))
    nodes = np.array(g.nodes())
    dsize = 4 * np.ones(nodes.shape[0], dtype='float32')
    print dsize.shape, nodes.shape
    mlab.points3d(nodes[:, 2], nodes[:, 1], nodes[:, 0], dsize, color=(0.0, 0.0, 1.0), scale_factor=0.25)
    for n1, n2, edge in g.edges(data=True):
        path = [n1] + edge['path'] + [n2]
        pa = np.array(path)
        mlab.plot3d(pa[:, 2], pa[:, 1], pa[:, 0], color=(0, 1, 0), tube_radius=0.25)

    mlab.view(-125, 54, 'auto', 'auto')
    mlab.roll(-175)
    mlab.title(title, height=0.1)
    mlab.show()


def viewImg2(img, spacing, contours):
    print 'In viewImg2: (min,max)=(%f,%f)' % (img.min(), img.max())
    print 'contours=', contours
    mlab.figure(bgcolor=(0, 0, 0), size=(400, 400))
    src = mlab.pipeline.scalar_field(img)
    src.spacing = [
     1, 1, 1]
    src.update_image_data = True
    blur = mlab.pipeline.user_defined(src, filter='ImageGaussianSmooth')
    mlab.pipeline.iso_surface(src, contours=contours)
    mlab.view(-125, 54, 'auto', 'auto')
    mlab.roll(-175)
    mlab.show()


def viewImg(img, spacing, contours):
    mlab.figure(bgcolor=(0, 0, 0), size=(400, 400))
    src = mlab.pipeline.scalar_field(img)
    src.spacing = [
     1, 1, 1]
    src.update_image_data = True
    blur = mlab.pipeline.user_defined(blur, filter='ImageGaussianSmooth')
    print 'blur type is', type(blur), blur.max()
    mlab.pipeline.contour3d(blur)
    mlab.view(-125, 54, 'auto', 'auto')
    mlab.roll(-175)
    mlab.show()