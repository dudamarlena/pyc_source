# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dumpall/addons/gitdumper.py
# Compiled at: 2019-10-24 09:39:43
# Size of source mod 2**32: 1648 bytes
import re, zlib, click
from aiomultiprocess import Pool
from ..dumper import BasicDumper
from thirdparty.gin import parse

class Dumper(BasicDumper):

    def __init__(self, url, outdir):
        super(Dumper, self).__init__(url, outdir)
        self.base_url = re.sub('.git.*', '.git', url)

    async def start(self):
        """ 入口方法 """
        await self.dump()

    async def dump(self):
        """ .git DUMP核心方法，解析索引，创建进程池，调用download """
        idxfile = await self.indexfile(self.base_url + '/index')
        for entry in parse(idxfile.name):
            if 'sha1' in entry.keys():
                sha1 = entry.get('sha1', '').strip()
                filename = entry.get('name', '').strip()
            if sha1:
                if not filename:
                    continue
                url = '%s/objects/%s/%s' % (self.base_url, sha1[:2], sha1[2:])
                self.targets.append((url, filename))

        idxfile.close()
        async with Pool() as pool:
            await pool.map(self.download, self.targets)

    def convert(self, data: bytes) -> bytes:
        """ 用zlib对数据进行解压 """
        if data:
            try:
                data = zlib.decompress(data)
                data = re.sub(b'blob \\d+\\x00', b'', data)
            except Exception as e:
                try:
                    click.secho((str(e.args)), fg='red')
                finally:
                    e = None
                    del e

        return data