# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: imagedataextractor/particle_identification.py
# Compiled at: 2019-05-16 11:15:11
from .correction_steps import *
from .scale_reading import *

def particle_identification(img, inlaycoords, testing=False, blocksize=151, blursize=3, invert=False):
    """Runs contour detection and particle filtering
    functions on SEM images.
    
    :param numpy.ndarray img: input image.
    :param list inlaycoords: list of tuples, (x,y,w,h) top left corner, width and 
    height of inlays, including scalebar.
    :param int blocksize: parameter associated with image thresholding.
    :param int blursize: parameter associated with image thresholding.
    :param bool testing: Displays step by step progress for debugging.
    :param bool invert: Invert colors of image, useful for dark particles on light background.

    :return list filteredvertices: List of vertices of particles in image.
    :return list particlediscreteness: List of discreteness index for each particle.
    """
    if len(img.shape) == 2:
        gimg = img
    else:
        gimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img = crop_image(img)
    gimg = crop_image(gimg)
    if invert == True:
        gimg = 255 - gimg
    rows, cols, imgarea, imgmean, imgstdev, crossstdev = image_metrics(gimg)
    filteredvertices = find_draw_contours_main(img, gimg, blocksize, rows, cols, blursize, testing=testing)
    particlediscreteness = []
    if len(filteredvertices) > 0:
        colorlist, arealist, avgcolormean, avgcolorstdev, avgarea = particle_metrics_from_vertices(img, gimg, rows, cols, filteredvertices, invert)
        filteredvertices, arealist = false_positive_correction(filteredvertices, arealist, colorlist, avgcolormean, avgcolorstdev, testing=testing, gimg=gimg)
        filteredvertices = cluster_breakup_correction(filteredvertices, rows, cols, arealist, avgarea, blocksize, testing=testing, detailed_testing=False)
        filteredvertices, _ = edge_correction(filteredvertices, particlediscreteness=None, rows=rows, cols=cols, inlaycoords=inlaycoords, testing=testing, gimg=gimg)
        filteredvertices, particlediscreteness = discreteness_index_and_ellipse_fitting(filteredvertices, img, rows, cols, imgstdev, testing=testing)
        filteredvertices, particlediscreteness = edge_correction(filteredvertices, particlediscreteness, rows, cols, inlaycoords, testing=testing, gimg=gimg)
    return (
     filteredvertices, particlediscreteness)