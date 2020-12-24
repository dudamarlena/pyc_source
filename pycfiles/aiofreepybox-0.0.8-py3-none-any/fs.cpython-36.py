# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/c/Users/luc_t_000/projects/freepybox/aiofreepybox/api/fs.py
# Compiled at: 2018-12-03 18:01:41
# Size of source mod 2**32: 1637 bytes
import base64, os, logging
logger = logging.getLogger(__name__)

class Fs:

    def __init__(self, access):
        self._access = access
        self._path = '/'

    def pwd(self):
        """
        Returns the working directory
        """
        return self._path

    async def cd(self, path):
        """
        Changes the current directory
        """
        if await self._path_exists(path):
            self._path = os.path.join(self._path, path)
        else:
            logger.error('{0} does not exist'.format(os.path.join(self._path, path)))

    async def _path_exists(self, path):
        """
        Returns True if the path exists
        """
        try:
            await self.get_file_info(os.path.join(self._path, path))
            return True
        except:
            return False

    async def ls(self):
        """
        List directory
        """
        return [i['name'] for i in await self.list_file(self._path)]

    async def get_tasks_list(self):
        """
        Returns the collection of all tasks
        """
        return await self._access.get('fs/tasks/')

    async def list_file(self, path):
        """
        Returns the list of files for the given path
        """
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return await self._access.get('fs/ls/{0}'.format(path_b64))

    async def get_file_info(self, path):
        """
        Returns information for the given path
        """
        path_b64 = base64.b64encode(path.encode('utf-8')).decode('utf-8')
        return await self._access.get('fs/ls/{0}'.format(path_b64))