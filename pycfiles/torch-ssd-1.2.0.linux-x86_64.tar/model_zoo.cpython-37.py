# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/utils/model_zoo.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 3160 bytes
import os, sys, torch
from ssd.utils.dist_util import is_main_process, synchronize
try:
    from torch.hub import _download_url_to_file
    from torch.hub import urlparse
    from torch.hub import HASH_REGEX
except ImportError:
    from torch.utils.model_zoo import _download_url_to_file
    from torch.utils.model_zoo import urlparse
    from torch.utils.model_zoo import HASH_REGEX

def cache_url(url, model_dir=None, progress=True):
    """Loads the Torch serialized object at the given URL.
    If the object is already present in `model_dir`, it's deserialized and
    returned. The filename part of the URL should follow the naming convention
    ``filename-<sha256>.ext`` where ``<sha256>`` is the first eight or more
    digits of the SHA256 hash of the contents of the file. The hash is used to
    ensure unique names and to verify the contents of the file.
    The default value of `model_dir` is ``$TORCH_HOME/models`` where
    ``$TORCH_HOME`` defaults to ``~/.torch``. The default directory can be
    overridden with the ``$TORCH_MODEL_ZOO`` environment variable.
    Args:
        url (string): URL of the object to download
        model_dir (string, optional): directory in which to save the object
        progress (bool, optional): whether or not to display a progress bar to stderr
    Example:
        >>> cached_file = maskrcnn_benchmark.utils.model_zoo.cache_url('https://s3.amazonaws.com/pytorch/models/resnet18-5c106cde.pth')
    """
    if model_dir is None:
        torch_home = os.path.expanduser(os.getenv('TORCH_HOME', '~/.torch'))
        model_dir = os.getenv('TORCH_MODEL_ZOO', os.path.join(torch_home, 'models'))
    else:
        if not os.path.exists(model_dir):
            os.makedirs(model_dir)
        parts = urlparse(url)
        filename = os.path.basename(parts.path)
        if filename == 'model_final.pkl':
            filename = parts.path.replace('/', '_')
        cached_file = os.path.join(model_dir, filename)
        if not os.path.exists(cached_file):
            if is_main_process():
                sys.stderr.write('Downloading: "{}" to {}\n'.format(url, cached_file))
                hash_prefix = HASH_REGEX.search(filename)
                if hash_prefix is not None:
                    hash_prefix = hash_prefix.group(1)
                    if len(hash_prefix) < 6:
                        hash_prefix = None
                _download_url_to_file(url, cached_file, hash_prefix, progress=progress)
    synchronize()
    return cached_file


def load_state_dict_from_url(url, map_location='cpu'):
    cached_file = cache_url(url)
    return torch.load(cached_file, map_location=map_location)