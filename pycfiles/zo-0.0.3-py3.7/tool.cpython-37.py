# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/zo/aa/tool.py
# Compiled at: 2020-04-03 02:46:48
# Size of source mod 2**32: 1717 bytes
import hashlib, os, socket
from typing import Any
from zo.pydantic import BaseModel
import zo.log as log

def calc_hash(v, hash_factory=hashlib.sha3_256):
    h = hash_factory()
    v = v if isinstance(v, (bytes, bytearray)) else str(v).encode()
    assert isinstance(v, (bytes, bytearray)), f"calc_hash type error = {type(v)}"
    h.update(v)
    return h.hexdigest()


def calc_file_hash(path, hash_factory=hashlib.sha3_256, chunk_num_blocks=128):
    h = hash_factory()
    assert os.path.exists(path), f"File not exists? {[path]}"
    with open(path, 'rb') as (f):
        for chunk in iter(lambda : f.read(chunk_num_blocks * h.block_size), ''):
            h.update(chunk)

    return h.hexdigest()


class HostInfo(BaseModel):
    hostname = ''
    hostname: str
    ip = '-'
    ip: str

    def __init__(self, **data):
        (super().__init__)(**data)
        self.get_hostname()
        self.get_ip()

    def get_hostname(self):
        try:
            self.hostname = socket.gethostname()
        except Exception as e:
            try:
                log.error(f"get host name  e={e}")
            finally:
                e = None
                del e

    def get_ip(self):
        for conn_ip in ('223.5.5.5', '1.2.4.8', '1.1.1.1'):
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                try:
                    s.connect((conn_ip, 80))
                    self.ip = s.getsockname()[0]
                    break
                except Exception as e:
                    try:
                        log.error(f"conn_ip={conn_ip} e={e}")
                    finally:
                        e = None
                        del e

            finally:
                s.close()

    def show(self):
        print(self.__dict__)


def to_str(v: Any, split_co='_'):
    if isinstance(v, list):
        return split_co.join([str(_) for _ in v])
    return str(v)