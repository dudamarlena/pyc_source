# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/containerdiff/modules/history.py
# Compiled at: 2016-05-22 16:09:46
# Size of source mod 2**32: 2214 bytes
"""Show diff in container image history."""
import difflib, docker, logging, containerdiff
logger = logging.getLogger(__name__)

def dockerfile_from_image(ID, cli):
    """Return list of commands used to create image 'ID'. These
    commands is an output from docker history.
    """
    info = cli.inspect_image(ID)
    commands = []
    history = cli.history(ID)
    for item in history:
        if '/bin/sh -c #(nop) ' in item['CreatedBy']:
            commands.append(item['CreatedBy'][18:])
        else:
            commands.append(item['CreatedBy'])

    commands.reverse()
    return commands


def run(image1, image2):
    """Test history of the image.

    Adds one key to the output of the diff tool:
    "history" - unified_diff style changes in commands used to create
                the image
    """
    ID1, metadata1, output_dir1 = image1
    ID2, metadata2, output_dir2 = image2
    logger.info('Testing history of the image')
    cli = docker.AutoVersionClient(base_url=containerdiff.docker_socket)
    history1 = dockerfile_from_image(ID1, cli)
    history2 = dockerfile_from_image(ID2, cli)
    diff = [item for item in difflib.unified_diff(history1, history2, n=0) if not item.startswith(('+++',
                                                                                                   '---',
                                                                                                   '@@'))]
    return {'history': diff}