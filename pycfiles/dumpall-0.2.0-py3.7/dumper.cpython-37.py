# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dumpall/dumper.py
# Compiled at: 2019-10-27 08:53:15
# Size of source mod 2**32: 3542 bytes
"""
@author: HJK
@file: dumper
@time: 2019-10-23
"""
import os, click, aiohttp
from tempfile import NamedTemporaryFile

class BasicDumper(object):
    __doc__ = ' 基本下载类 '

    def __init__(self, url: str, outdir: str):
        self.url = url
        self.outdir = outdir
        self.targets = []
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.106 Safari/537.36 OPR/38.0.2220.41'}

    async def start(self):
        """ 入口方法 """
        await self.dump()

    async def dump(self):
        """ DUMP核心方法，解析索引，创建任务池，调用download """
        pass

    async def download(self, target: tuple):
        """ 下载任务（协程） """
        url, filename = target
        fullname = os.path.join(self.outdir, filename)
        outdir = os.path.dirname(fullname)
        if outdir:
            if not os.path.exists(outdir):
                os.makedirs(outdir)
            else:
                if os.path.isfile(outdir):
                    click.secho(('%s is a file. It will be removed.' % outdir), fg='yellow')
                    os.remove(outdir)
                    os.makedirs(outdir)
        status, data = await self.fetch(url)
        if status != 200 or data is None:
            click.secho(('[%s] %s %s' % (status, url, filename)), fg='red')
            return
        click.secho(('[%s] %s %s' % (status, url, filename)), fg='green')
        data = self.convert(data)
        try:
            with open(fullname, 'wb') as (f):
                f.write(data)
        except IsADirectoryError:
            pass
        except Exception as e:
            try:
                click.secho(('[Failed] %s %s' % (url, filename)), fg='red')
                click.secho((str(e.args)), fg='red')
            finally:
                e = None
                del e

    def convert(self, data: bytes) -> bytes:
        """ 处理数据 """
        return data

    async def fetch(self, url: str, times: int=3) -> tuple:
        """ 从URL获取内容，如果失败默认重试三次 """
        async with aiohttp.ClientSession() as session:
            try:
                resp = await session.get(url, headers=(self.headers))
                ret = (resp.status, await resp.content.read())
            except Exception as e:
                try:
                    if times > 0:
                        return await self.fetch(url, times - 1)
                    click.secho(('Failed %s' % url), fg='red')
                    click.secho((str(e.args)), fg='red')
                    ret = (0, None)
                finally:
                    e = None
                    del e

            return ret

    async def parse(self, url: str):
        """ 从URL下载文件并解析 """
        pass

    async def indexfile(self, url: str) -> NamedTemporaryFile:
        """ 创建一个临时索引文件index/wc.db """
        idxfile = NamedTemporaryFile()
        status, data = await self.fetch(url)
        if not data:
            click.secho(('Failed [%s] %s' % (status, url)), fg='red')
            return
        with open(idxfile.name, 'wb') as (f):
            f.write(data)
        return idxfile