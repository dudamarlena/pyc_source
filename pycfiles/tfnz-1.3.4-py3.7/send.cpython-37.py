# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/tfnz/send.py
# Compiled at: 2018-05-18 20:34:30
# Size of source mod 2**32: 4077 bytes
import hashlib, logging, io, lzma
from tarfile import TarFile, ReadError
from .docker import Docker

class Sender:

    @staticmethod
    def layer_stack(descr):
        """Returns a list of the layers necessary to create the passed docker image id."""
        layers = descr['RootFS']['Layers']
        single_run_layers = []
        last_layer = None
        for layer in layers:
            layer = layer[7:]
            if layer == last_layer:
                continue
            single_run_layers.append(layer)
            last_layer = layer

        return single_run_layers

    @staticmethod
    def upload_requirements(layers, conn):
        return conn.send_blocking_cmd(b'upload_requirements', {'layers': layers}).params

    @staticmethod
    def send(docker_image_id, layers, conn):
        """Internal use: Send the missing layers to the location."""
        if len(layers) == 0:
            logging.info('No layers need uploading for: ' + docker_image_id)
            return
        logging.info('Waiting for Docker to export image...')
        tarball = Docker.tarball(docker_image_id)
        try:
            raw_top_tar = io.BytesIO(tarball)
            top_tar = TarFile(fileobj=raw_top_tar)
        except ReadError:
            raise RuntimeError('Local docker does not appear to have image: ' + docker_image_id)

        for member in top_tar.getmembers():
            logging.debug('Examining: ' + str(member))
            if '/layer.tar' not in str(member):
                continue
            layer_data = top_tar.extractfile(member).read()
            sha256 = hashlib.sha256(layer_data).hexdigest()
            if sha256 in layers:
                logging.info('Uploading: ' + sha256[:16])
                slab_size = 4194304
                data_loc = 0
                slab = 0
                data_length = len(layer_data)
                logging.info('Uploading slabs: ' + str(data_length // slab_size + 1))
                while data_loc < data_length:
                    end_byte = (slab + 1) * slab_size
                    if end_byte >= len(layer_data):
                        end_byte = len(layer_data)
                    send_data = lzma.compress((layer_data[data_loc:end_byte]), preset=1)
                    reply = conn.send_blocking_cmd(b'upload_slab', {'sha256':sha256,  'slab':slab}, bulk=send_data)
                    logging.info(reply.params['log'])
                    data_loc += slab_size
                    slab += 1

                msg = conn.send_blocking_cmd(b'upload_complete', {'sha256':sha256,  'slabs':slab}, timeout=300)
                logging.info(msg.params['log'])