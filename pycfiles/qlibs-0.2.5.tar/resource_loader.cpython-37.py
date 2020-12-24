# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/iquant/proj/qlibs/qlibs/resources/resource_loader.py
# Compiled at: 2019-09-29 06:14:35
# Size of source mod 2**32: 3017 bytes
import sys, os.path
from ..util import dict_cache, weak_ref_cache
try:
    from PIL import Image
except ImportError:
    print('Could not import PIL(pillow), image loading is unavailable', file=(sys.stderr))

loader = None

class ImageData:

    def __init__(self, size, data):
        self.size = size
        self.data = data


class Loader:

    def resolve(self, path):
        raise NotImplementedError()

    def handle_prefix(self, path, prefix):
        if prefix is None:
            return path
        if path.startswith(prefix):
            path = path[len(prefix):]
            return path


class SearchLocationLoader(Loader):

    def __init__(self, location, prefix=None):
        self.location = location
        if prefix is None or prefix.endswith('/'):
            self.prefix = prefix
        else:
            raise ValueError("Prefix should end with '/'")

    def resolve(self, path):
        path = self.handle_prefix(path, self.prefix)
        if path is None:
            return
        path = os.path.join(self.location, path)
        if os.path.exists(path):
            return path


class MergerLoader(Loader):

    def __init__(self, loaders, prefix=None):
        self.loaders = loaders
        if prefix is None or prefix.endswith('/'):
            self.prefix = prefix
        else:
            raise ValueError("Prefix should end with '/'")

    def resolve(self, path):
        path = self.handle_prefix(path, self.prefix)
        if path is None:
            return
        for loader in self.loaders:
            resolved = loader.resolve(path)
            if resolved is not None:
                return resolved


def get_lib_res_path():
    return os.path.join(os.path.dirname(__file__), 'storage')


def get_res_path(path):
    resolved = loader.resolve(path)
    if resolved is None:
        raise FileNotFoundError(f"Can't find {path}")
    else:
        return resolved


def get_res_data(path):
    with open(get_res_path(path), 'r') as (f):
        return f.read()


@weak_ref_cache
def get_image_data(r_path, mode='RGB'):
    if os.path.isabs(r_path):
        path = r_path
    else:
        path = get_res_path(r_path)
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert(mode)
    return ImageData(img.size, img.tobytes())


@dict_cache
def get_res_texture(r_path, ctx):
    path = get_res_path(r_path)
    img = Image.open(path).transpose(Image.FLIP_TOP_BOTTOM).convert('RGB')
    txt = ctx.texture(img.size, 3, img.tobytes())
    txt.build_mipmaps()
    return txt


loader = MergerLoader([])

def add_loader(loader_):
    loader.loaders.append(loader_)


def add_location(rel, location, prefix=None):
    add_loader(SearchLocationLoader(os.path.join(os.path.dirname(rel), location), prefix))


loader.loaders.append(SearchLocationLoader((get_lib_res_path()), prefix='qlibs/'))