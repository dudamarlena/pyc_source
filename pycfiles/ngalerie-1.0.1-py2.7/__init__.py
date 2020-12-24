# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ngalerie/__init__.py
# Compiled at: 2011-08-20 07:46:58
"""
This command has the following behaviour

"""
__version__ = '1.0.1'
import argparse, os, sys, errno, glob
try:
    import Image
except ImportError:
    print 'To use this program, you need to install Python Imaging Library- http://www.pythonware.com/products/pil/'
    sys.exit(1)

try:
    import pyexiv2
except ImportError:
    print 'To use this program, you need to install pyexiv2- http://tilloy.net/dev/pyexiv2/'
    sys.exit(1)

_SIZE_MINI = 200
_SIZE_MAXI = 600
_MINI_DIRNAME = None
_MAXI_DIRNAME = ''
_COPYRIGHT = 'Remy Hubscher - http://www.trunat.fr/'
_ARTIST = 'Remy Hubscher'

def list_jpeg(directory):
    """Return a list of the JPEG files in the directory"""
    file_list = []
    for ext in ('jpg', 'JPG'):
        file_list += glob.glob(os.path.join(directory, '*.' + ext))

    return [ os.path.basename(f) for f in file_list ]


def _mkdir(path):
    try:
        os.makedirs(path)
    except OSError as exc:
        if exc.errno == errno.EEXIST:
            pass
        else:
            raise


def main():
    parser = argparse.ArgumentParser(description='A command interface to manage CAMERA JPG files', prog='NGalerie')
    parser.add_argument(dest='indir', nargs='?', help='Path where to find the raw pictures')
    parser.add_argument(dest='outdir', nargs='?', help='Path where to put generated pictures')
    parser.add_argument('-r', '--rename', dest='rename', action='store_true', help='Use EXIF.Image.DateTime information to rename the picture')
    parser.add_argument('--resize', dest='resize', default=None, type=int, help='Ask to resize pictures eventually set the size')
    parser.add_argument('-t', '--rotate', dest='rotate', action='store_true', help='Ask to force rotate the picture using EXIF information')
    parser.add_argument('--max-dir', dest='max_dir', default=_MAXI_DIRNAME, help='The prefix directory for resized files')
    parser.add_argument('--thumb-dir', dest='thumb_dir', default=_MINI_DIRNAME, help='The prefix directory for thumbnails')
    parser.add_argument('--thumb-size', dest='thumb_size', default=_SIZE_MINI, type=int, help='The size for thumbnails if thumb-dir only works with --resize')
    parser.add_argument('--artist', dest='artist', default=_ARTIST, help='Name of the artist')
    parser.add_argument('--copyright', dest='copyright', default=_COPYRIGHT, help='Copyright of the pictures')
    parser.add_argument('--version', action='version', version=__version__, help='Print the NGalerie version and exit')
    args = parser.parse_args()
    if not args.indir or not args.outdir:
        print parser.print_help()
        return 1
    else:
        max_size = _SIZE_MAXI if args.resize is None else args.resize
        max_dir = os.path.join(args.outdir, args.max_dir)
        thumb_dir = os.path.join(args.outdir, args.thumb_dir) if args.thumb_dir else None
        print max_dir, thumb_dir if thumb_dir else ''
        _mkdir(max_dir)
        if thumb_dir is not None:
            _mkdir(thumb_dir)
        for infile in list_jpeg(args.indir):
            if thumb_dir is not None:
                mini = os.path.join(thumb_dir, infile)
            grand = os.path.join(max_dir, infile)
            file_path = os.path.join(args.indir, infile).decode('utf-8')
            metadata = pyexiv2.ImageMetadata(file_path)
            metadata.read()
            metadata['Exif.Image.Artist'] = args.artist
            metadata['Exif.Image.Copyright'] = args.copyright
            if thumb_dir:
                mini = os.path.join(thumb_dir, infile)
            grand = os.path.join(max_dir, infile)
            if args.rename:
                key = 'Exif.Image.DateTime'
                if 'Exif.Photo.DateTimeOriginal' in metadata.exif_keys:
                    key = 'Exif.Photo.DateTimeOriginal'
                if key in metadata.exif_keys:
                    filename = metadata[key].value.strftime('%Y-%m-%d_%H-%M-%S.jpg')
                    if thumb_dir:
                        mini = os.path.join(thumb_dir, filename)
                    grand = os.path.join(max_dir, filename)
                    counter = 0
                    while os.path.isfile(grand):
                        counter += 1
                        filename = metadata[key].value.strftime('%Y-%m-%d_%H-%M-%S') + '_%d.jpg' % counter
                        if thumb_dir is not None:
                            mini = os.path.join(thumb_dir, filename)
                        grand = os.path.join(max_dir, filename)

            im = Image.open(file_path)
            if args.resize:
                size = (
                 max_size, max_size)
                im.thumbnail(size, Image.ANTIALIAS)
            if 'Exif.Image.Orientation' in metadata.exif_keys and args.rotate:
                orientation = metadata['Exif.Image.Orientation']
                if orientation == 2:
                    mirror = im.transpose(Image.FLIP_LEFT_RIGHT)
                elif orientation == 3:
                    mirror = im.transpose(Image.ROTATE_180)
                elif orientation == 4:
                    mirror = im.transpose(Image.FLIP_TOP_BOTTOM)
                elif orientation == 5:
                    mirror = im.transpose(Image.FLIP_TOP_BOTTOM).transpose(Image.ROTATE_270)
                elif orientation == 6:
                    mirror = im.transpose(Image.ROTATE_270)
                elif orientation == 7:
                    mirror = im.transpose(Image.FLIP_LEFT_RIGHT).transpose(Image.ROTATE_270)
                elif orientation == 8:
                    mirror = im.transpose(Image.ROTATE_90)
                else:
                    mirror = im.copy()
                metadata['Exif.Image.Orientation'] = 1
            else:
                mirror = im.copy()
            mirror.save(grand, 'JPEG', quality=85)
            img_grand = pyexiv2.ImageMetadata(grand)
            img_grand.read()
            metadata.copy(img_grand)
            img_grand.write()
            print grand
            if thumb_dir:
                size = (
                 args.thumb_size, args.thumb_size)
                mirror.thumbnail(size, Image.ANTIALIAS)
                mirror.save(mini, 'JPEG', quality=85)
                print mini
                print

        return 0


if __name__ == '__main__':
    sys.exit(main())