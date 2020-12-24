# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jwql/tests/test_preview_image.py
# Compiled at: 2019-08-26 11:08:03
# Size of source mod 2**32: 3613 bytes
"""Tests for the ``preview_image`` module.

Authors
-------

    - Johannes Sahlmann
    - Lauren Chambers

Use
---

    These tests can be run via the command line (omit the ``-s`` to
    suppress verbose output to ``stdout``):

    ::

        pytest -s test_preview_image.py
"""
import glob, os, pytest, shutil
from astropy.io import fits
from jwql.utils.preview_image import PreviewImage
from jwql.utils.utils import get_config, ensure_dir_exists
TEST_DIRECTORY = os.path.join(os.environ['HOME'], 'preview_image_test')
ON_JENKINS = '/home/jenkins' in os.path.expanduser('~')

@pytest.fixture(scope='module')
def test_directory(test_dir=TEST_DIRECTORY):
    """Create a test directory for preview image.

    Parameters
    ----------
    test_dir : str
        Path to directory used for testing

    Yields
    -------
    test_dir : str
        Path to directory used for testing

    """
    ensure_dir_exists(test_dir)
    yield test_dir
    if os.path.isdir(test_dir):
        shutil.rmtree(test_dir)
    jpgs = glob.glob(os.path.join(get_config()['test_dir'], '*.jpg'))
    thumbs = glob.glob(os.path.join(get_config()['test_dir'], '*.thumbs'))
    for file in jpgs + thumbs:
        os.remove(file)


def get_test_fits_files():
    """Get a list of the FITS files on central storage to make preview images.

    Returns
    -------
    filenames : list
        List of filepaths to FITS files
    """
    if not ON_JENKINS:
        filenames = glob.glob(os.path.join(get_config()['test_dir'], '*.fits'))
        assert len(filenames) > 0
        return filenames
    else:
        return []


@pytest.mark.skipif(ON_JENKINS, reason='Requires access to central storage.')
@pytest.mark.parametrize('filename', get_test_fits_files())
def test_make_image(test_directory, filename):
    """Use PreviewImage.make_image to create preview images of a sample
    JWST exposure.

    Assert that the number of JPGs created corresponds to the number of
    integrations.

    Parameters
    ----------
    test_directory : str
        Path of directory used for testing
    filename : str
        Path of FITS image to generate preview of
    """
    header = fits.getheader(filename)
    for create_thumbnail in (False, True):
        try:
            image = PreviewImage(filename, 'SCI')
            image.clip_percent = 0.01
            image.scaling = 'log'
            image.cmap = 'viridis'
            image.output_format = 'jpg'
            image.thumbnail = create_thumbnail
            if create_thumbnail:
                image.thumbnail_output_directory = test_directory
            else:
                image.preview_output_directory = test_directory
            image.make_image()
        except ValueError as error:
            print(error)

        if create_thumbnail:
            extension = 'thumb'
        else:
            extension = 'jpg'
        preview_image_filenames = glob.glob(os.path.join(test_directory, '*.{}'.format(extension)))
        assert len(preview_image_filenames) == header['NINTS']
        for file in preview_image_filenames:
            os.remove(file)