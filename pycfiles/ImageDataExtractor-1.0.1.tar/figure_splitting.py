# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: imagedataextractor/figure_splitting.py
# Compiled at: 2019-05-16 11:15:11
"""
Photo Detection
===============

Detect photos in figures.

@authors: Matt Swain and Ed Beard

IMPORTANT NOTE!!!!

TODO : This code is from Matt's currently unpublished FigureDataExtractor code. We must ask his permission before
publishing it with this code.

Ed Beard has copied the bits that he used in the splitting of figures, which were originally imported from FigureDataExtractor

"""
from __future__ import print_function, unicode_literals
from __future__ import absolute_import, division
from .grid_splitting import *
from .photo_splitting import get_photos
import cv2, glob, io, csv
from skimage import io as skio
from skimage.color import gray2rgb
from skimage import img_as_float
import matplotlib.pyplot as plt, matplotlib.patches as patches, logging
log = logging.getLogger(__name__)

def imread(f):
    """Read an image from a file.

    :param string|file f: Filename or file-like object.
    :return: Image array.
    :rtype: numpy.ndarray
    """
    img = skio.imread(f, plugin=b'pil')
    if len(img.shape) == 2:
        log.debug(b'Converting greyscale image to RGB...')
        img = gray2rgb(img)
    img = img_as_float(img)
    return img


def imsave(f, img):
    """Save an image to file.

    :param string|file f: Filename or file-like object.
    :param numpy.ndarray img: Image to save. Of shape (M,N) or (M,N,3) or (M,N,4).
    """
    skio.imsave(f, img, plugin=b'pil')


def split_by_photo(input_imgs, csv_input_path, output_imgs=b'', csv_output_path=b'', split=False):
    """ Identifies and segments photo areas
    :param bool multithreaded: Runs in parallel across all processors if True
    :param bool split: Leave true to save each segmented image separately, False to label and display bboxes on one image

    """
    print(b'Running plot area evaluation')
    print(b'Creating output directory if it doesnt exist...')
    if not os.path.exists(output_imgs):
        os.makedirs(output_imgs)
    print(b'Deleting output from previous run')
    files = glob.glob(os.path.join(output_imgs, b'*.png'))
    for f in files:
        os.remove(f)

    print(b'Reading sample input from: %s' % csv_input_path)
    inf = io.open(csv_input_path, b'r')
    sample_csvreader = csv.reader(inf)
    print(b'Writing output to: %s' % csv_output_path)
    outf = open(csv_output_path, b'w')
    output_csvwriter = csv.writer(outf)
    print(b'Loading images from: %s' % input_imgs)
    next(sample_csvreader)
    if split:
        results = [ run_worker_split_images(row, input_imgs, output_imgs) for row in sample_csvreader ]
    else:
        results = [ run_worker(row, input_imgs, output_imgs) for row in sample_csvreader ]
    output_csvwriter.writerow([b'fig_id', b'plot_id', b'left', b'right', b'top', b'bottom'])
    for im in results:
        for row in im:
            output_csvwriter.writerow(row)

    inf.close()
    outf.close()


def run_worker(row, input_imgs, output_imgs):
    """Detect photos in a figure, save an overlay file, and return output CSV rows."""
    filename = row[0][:-5] + b'_' + row[1] + b'.gif'
    print(b'Processing: %s' % filename)
    impath = os.path.join(input_imgs, filename)
    img = imread(impath)
    photos = get_photos(img)
    output_rows = []
    plt.rcParams[b'image.cmap'] = b'gray'
    fig = plt.figure()
    ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
    ax.set_axis_off()
    fig.add_axes(ax)
    ax.imshow(img)
    for i, photo in enumerate(photos):
        photo_id = i + 1
        ax.add_patch(patches.Rectangle((photo.left, photo.top), photo.width, photo.height, alpha=0.2, facecolor=b'r'))
        ax.text(photo.left, photo.top + photo.height / 4, b'[%s]' % photo_id, size=photo.height / 5, color=b'r')
        output_rows.append([row[0], photo_id, photo.left, photo.right, photo.top, photo.bottom])

    dpi = fig.get_dpi()
    fig.set_size_inches(img.shape[1] / float(dpi), img.shape[0] / float(dpi))
    plt.savefig(os.path.join(output_imgs, (b'{}_{}.png').format(row[0][:-5], row[1])))
    plt.close()
    return output_rows


def run_worker_split_images(row, input_imgs, output_imgs):
    """Detect photos in a figure, save all images to separate pngs"""
    filename = row[0][:-5] + b'_' + row[1] + b'.gif'
    print(b'Processing: %s' % filename)
    impath = os.path.join(input_imgs, filename)
    img = imread(impath)
    photos = get_photos(img)
    output_rows = []
    for i, photo in enumerate(photos):
        photo_id = i + 1
        if photo.area < 50000:
            print(b'Pixel number : %s . Rejecting.' % photo.area)
        else:
            print(b'Pixel number : %s' % photo.area)
            out_img = img[photo.top:photo.bottom, photo.left:photo.right]
            plt.rcParams[b'image.cmap'] = b'gray'
            fig = plt.figure()
            ax = plt.Axes(fig, [0.0, 0.0, 1.0, 1.0])
            ax.set_axis_off()
            fig.add_axes(ax)
            ax.imshow(out_img)
            output_rows.append([row[0], photo_id, photo.left, photo.right, photo.top, photo.bottom])
            dpi = fig.get_dpi()
            fig.set_size_inches(out_img.shape[1] / float(dpi), out_img.shape[0] / float(dpi))
            plt.savefig(os.path.join(output_imgs, (b'{}_{}_{}.png').format(row[0][:-5], row[1], photo_id)))
            plt.close()

    return output_rows


def split_by_grid(input_imgs, output_imgs=b''):
    """ Splits all input figures by detecting regular grid structrues """
    print(b'Creating output directory if it doesnt exist...')
    if not os.path.exists(output_imgs):
        os.makedirs(output_imgs)
    imgs = glob.glob(os.path.join(input_imgs, b'*.png'))
    for img in imgs:
        split_fig_by_grid(img, output_imgs)


def split_fig_by_grid(figname, output_dir, eval_fig=False):
    """Splits figures mined from publications into their constituent images. Note: Must be used on the 
    products of FDE's figure splitting process.

    :param string figname: Name of the input figure.
    :param bool eval_fig: Optionally output an annotated version of the input for evaluation.

    :return list fig_split_final: list of constituent images as numpy.ndarrays.
    """
    fig = cv2.imread(figname)
    if len(fig.shape) == 2:
        gfig = fig
    else:
        gfig = cv2.cvtColor(fig, cv2.COLOR_BGR2GRAY)
    fig_split_final, evaluation_fig = line_detection_and_split(gfig, eval_img=eval_fig)
    if fig_split_final is not None and eval_fig == True:
        cv2.imwrite(b'eval_' + str(figname).split(b'/')[(-1)], evaluation_fig)
    index = 0
    for fig in fig_split_final:
        cv2.imwrite(os.path.join(output_dir, str(index) + b'_' + str(figname).split(b'/')[(-1)]), fig)
        index += 1

    return fig_split_final