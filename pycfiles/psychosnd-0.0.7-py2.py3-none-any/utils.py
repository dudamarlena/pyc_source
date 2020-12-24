# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/qbilius/mh17/Dropbox (MIT)/psychopy_ext/psychopy_ext/utils.py
# Compiled at: 2016-09-17 20:12:03
__doc__ = '\nA collection of useful functions.\n'
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, subprocess, warnings, tempfile, io, zipfile, tarfile, urllib, shutil, numpy as np, scipy.ndimage, skimage, skimage.io, skimage.transform

def call_matlab(script_path):
    cmd = ('matlab -nojvm -nodisplay -nosplash -r {}; exit').format(script_path)
    subprocess.call(cmd.split())


def _load_image_orig(imname, flatten=False, resize=1.0):
    im = scipy.misc.imread(imname, flatten=flatten)
    if len(im.shape) == 0:
        im = skimage.img_as_float(skimage.io.imread(imname, as_grey=flatten)).astype(np.float32)
    im = scipy.misc.imresize(im, resize).astype(np.float32)
    im /= 255.0
    return im


def load_image(im, flatten=False, color=False, resize=1.0, interp_order=1, keep_alpha=False):
    """
    Load an image converting from grayscale or alpha as needed.

    Adapted from
    `caffe <https://github.com/BVLC/caffe/blob/master/python/caffe/io.py>`_.

    :Args:
        im (str or np.ndarray)
    :Kwargs:
        - flatten (bool)
            flag for color format. True (default) loads as RGB while False
            loads as intensity (if image is already grayscale).
        - color
        - resize
        - interp_order
        - keep_alpha
    :Returns:
        An image with type np.float32 in range [0, 1]
        of size (H x W x 3) in RGB or of size (H x W x 1) in grayscale.
    """
    keep_alpha = False if flatten else keep_alpha
    if isinstance(im, (str, unicode)):
        im = skimage.img_as_float(skimage.io.imread(im, flatten=flatten))
    else:
        im = np.array(im).astype(float)
        if np.max(im) > 1:
            warnings.warn('Image values exceed the interval [0,1].')
        if im.ndim > 2 and flatten:
            raise Exception('You must convert the image to grayscale yourself.')
    if not flatten:
        if im.ndim == 2:
            if color:
                im = im[:, :, np.newaxis]
                im = np.tile(im, (1, 1, 3))
        elif im.shape[2] == 4 and not keep_alpha:
            im = im[:, :, :3]
    if not isinstance(resize, (tuple, list, np.ndarray)):
        resize = [
         resize, resize] + (im.ndim - 2) * [1]
    if any([ r != 1 for r in resize ]):
        new_dims = []
        for s, res in zip(im.shape, resize):
            n = s * res if res < 1 else res
            new_dims.append(n)
            im = resize_image(im, resize, interp_order=interp_order)

    return im


def resize_image(im, new_dims, interp_order=1):
    """
    Resize an image array with interpolation.

    From
    `caffe <https://github.com/BVLC/caffe/blob/master/python/caffe/io.py>`_.

    :Args:
        - im (numpy.ndarray)
            (H x W x K) ndarray
        - new_dims (tuple)
            (height, width) tuple of new dimensions.
    :Kwargs:
        interp_order (int, default: 1)
            Interpolation order, default is linear.
    :Returns:
        Resized ndarray with shape (new_dims[0], new_dims[1], K)
    """
    if im.shape[(-1)] == 4:
        alpha = resize_image(im[:, :, 3], (new_dims[0], new_dims[1]), interp_order=interp_order)
        im_rgb = resize_image(im[:, :, :3], (new_dims[0], new_dims[1], 3), interp_order=interp_order)
        return np.dstack([im_rgb, alpha])
    if im.ndim == 2 or im.shape[(-1)] == 1 or im.shape[(-1)] == 3:
        im_min, im_max = im.min(), im.max()
        if im_max > im_min:
            im_std = (im - im_min) / (im_max - im_min)
            resized_std = skimage.transform.resize(im_std, new_dims, order=interp_order)
            resized_im = resized_std * (im_max - im_min) + im_min
        else:
            ret = np.empty((new_dims[0], new_dims[1], im.shape[(-1)]), dtype=np.float32)
            ret.fill(im_min)
            return ret
    else:
        scale = tuple(np.array(new_dims, dtype=float) / np.array(im.shape[:2]))
        resized_im = scipy.ndimage.zoom(im, scale + (1, ), order=interp_order)
    return resized_im.astype(np.float32)


def create_phase_mask(imname, output_path=None):
    """Generate phase-scrambled mask

    Adapted from: http://visionscience.com/pipermail/visionlist/2007/002181.html
    """
    if output_path is None:
        output_path = os.path.dirname(imname)
    im = load_image(imname, color=True)
    out_im = np.zeros_like(im)
    rnd_arr = np.random.rand(im.shape[0], im.shape[1])
    rnd_arr = np.angle(np.fft.fft2(rnd_arr))
    for dim in range(im.shape[2]):
        res_im = np.fft.fft2(im[:, :, dim])
        out_fft = np.abs(res_im) * np.exp(complex(0.0, 1.0) * (np.angle(res_im) + rnd_arr))
        out_im[:, :, dim] = np.fft.ifft2(out_fft).real

    out_im /= np.max(out_im)
    return out_im


def extract_archive(name, folder_name=None, path=''):
    """
    Extracts zip, tar and tar.gz archives.

    This function can extract both files available locally or from a give URL.
    Moreover, it always extracts contents to a folder (instead of a big mess of
    files if the original archive was not archived as a single folder).

    :Args:
        name (str)
            Path or URL to the file you want to extract.
    :Kwargs:
        - folder_name (str, default: None)
            Folder name where the contents of the archive will be extracted.
            If everything in the archive is already in a single folder, this
            name will be used instead. If the archive is not a single folder,
            then a new folder will be created using this name and all contents
            will be extracted there.
        - path (str, default: '')
            Path to where archive will be extracted. Note that `folder_name`
            will **always** be appended to it.
    """
    try:
        r = urllib.urlopen(name)
    except:
        r = open(name)

    full_path, ext = os.path.splitext(name)
    if folder_name is None:
        folder_name = os.path.basename(full_path)
    path = os.path.join(path, folder_name)
    namelist = []
    if ext == '.zip':
        readin = zipfile.ZipFile(fileobj=io.BytesIO(r.read()))
    elif ext in ('.tar', '.gz'):
        readin = tarfile.open(fileobj=io.BytesIO(r.read()), mode='r:gz')
    else:
        raise ('Extension "{}" not recognized').format(ext)
    with readin as (z):
        tmpdir = tempfile.mkdtemp()
        z.extractall(tmpdir)
        fnames = os.listdir(tmpdir)
        if len(fnames) == 1:
            src = os.path.join(tmpdir, fnames[0])
            shutil.move(src, path)
            shutil.rmtree(tmpdir)
        else:
            src = tmpdir
            shutil.move(src, path)
        namelist = []
        for root, dirs, files in os.walk(path):
            namelist.extend(dirs)
            namelist.extend(files)

    return (path, namelist)