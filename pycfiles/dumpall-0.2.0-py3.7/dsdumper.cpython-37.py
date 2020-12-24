# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dumpall/addons/dsdumper.py
# Compiled at: 2019-10-27 08:59:54
# Size of source mod 2**32: 2207 bytes
"""
@author: HJK
@file: dsdumper
@time: 2019-10-26
"""
import re, click, asyncio
from urllib.parse import urlparse
from asyncio.queues import Queue
from ..thirdparty import dsstore
from ..dumper import BasicDumper

class Dumper(BasicDumper):
    __doc__ = ' .DS_Store dumper '

    def __init__(self, url, outdir):
        super(Dumper, self).__init__(url, outdir)
        self.base_url = re.sub('/\\.DS_Store.*', '', url)
        self.url_queue = Queue()

    async def start(self):
        """ dumper 入口方法 """
        await self.url_queue.put(self.base_url)
        await self.parse_loop()
        await self.dump()

    async def dump(self):
        task_pool = []
        for target in self.targets:
            task_pool.append(asyncio.create_task(self.download(target)))

        for t in task_pool:
            await t

    async def parse_loop(self):
        """ 从url_queue队列中读取URL，根据URL获取并解析DS_Store """
        while not self.url_queue.empty():
            base_url = await self.url_queue.get()
            status, ds_data = await self.fetch(base_url + '/.DS_Store')
            if not (status != 200 or ds_data):
                continue
            try:
                ds = dsstore.DS_Store(ds_data)
                for filename in set(ds.traverse_root()):
                    new_url = '%s/%s' % (base_url, filename)
                    await self.url_queue.put(new_url)
                    fullname = urlparse(new_url).path.lstrip('/')
                    self.targets.append((new_url, fullname))

            except Exception as e:
                try:
                    click.secho((str(e.args)), fg='red')
                finally:
                    e = None
                    del e