# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/modules/metadata.py
# Compiled at: 2016-05-22 17:26:05
# Size of source mod 2**32: 3452 bytes
"""Show diff of container image metadata."""
import docker, difflib, logging, containerdiff
logger = logging.getLogger(__name__)

def expand_dict(data, path=''):
    """Expand Python dict or list object (which replresents JSON
    object) into list. Every element of list is a string and it has two
    logical parts divided by " = ". So every list element has this
    form: "<path> = <value>".

    <path> consists of strings joined together by ":" . Each part of
    this <path> tells where to find the <value> in Python dict. After
    expanding a list every value in the list has the same prefix.

    <value> is string, number, bool or None.

    For example this dict {"foo":1, "bar":{"a":2, "b":["x=1", "y=2"]}}
    results to ["foo = 1", "bar:a = 2", "bar:b = x=1", "bar:b = y=2"].

    expand_dict also takes second parameter path. This parameter is by
    default "", but can be set to add some prefix to elements of result
    list.

    Returns list of strings.
    """
    if isinstance(data, list):
        result = []
        for item in data:
            result.extend(expand_dict(item, path))

        return result
    if isinstance(data, dict):
        result = []
        for item in data:
            result.extend(expand_dict(data[item], path + item + ':'))

        return result
    return [path[:-1] + ' = ' + str(data)]


def test_metadata(ID1, ID2, old, new):
    """Test changes in metadata of the image.

    'ID1' - ID of first image
    'ID2' - ID of second image
    'old' - metadata of files from first image
    'new' - metadata of files from second image

    Expands the metadata from `docker inspect` to the list of strings
    (see ouput of "expand_dict" function in this module). Returns
    unified_diff of these strings.
    """
    expanded_old = expand_dict(old)
    expanded_new = expand_dict(new)
    diff = [item for item in difflib.unified_diff(expanded_old, expanded_new, n=0) if not item.startswith(('+++',
                                                                                                           '---',
                                                                                                           '@@'))]
    return list(diff)


def run(image1, image2):
    """Test metadata of the image.

    Adds one key to the output of the diff tool:
    "metadata" - unified_diff style changes in metadata (see output of
                "test_metadata" function in this module)
    """
    ID1, metadata1, output_dir1 = image1
    ID2, metadata2, output_dir2 = image2
    logger.info('Testing metadata of the image.')
    cli = docker.AutoVersionClient(base_url=containerdiff.docker_socket)
    inspect_metadata1 = cli.inspect_image(ID1)
    inspect_metadata2 = cli.inspect_image(ID2)
    diff = test_metadata(ID1, ID2, inspect_metadata1, inspect_metadata2)
    return {'metadata': diff}