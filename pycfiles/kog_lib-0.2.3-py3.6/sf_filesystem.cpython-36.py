# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\kog_lib\filesystem\sf_filesystem.py
# Compiled at: 2020-01-07 05:01:43
# Size of source mod 2**32: 4918 bytes
import fs, os, time
from fs.mountfs import MountFS
from fs.tarfs import TarFS
from fs.zipfs import ZipFS

class SFFS:
    ServerConfig = {}

    def __init__(self):
        self.init()

    @staticmethod
    def help():
        print('\n        ----------------------------SFFileystem类 使用方法---------------------\n        import kog_lib\n        实例化：此时会将当前目录挂载到文件系统\n            root_fs = kog_lib.SFFS()\n        \n        显示当前服务器配置：\n            root_fs.show_current_server_config()\n        \n        新增服务器系统配置：\n            root_fs.add_server_config(s_key,s_path)\n                s_key:服务器简称，例如 "SVR1"\n                s_path:服务器路径，例如 "ssh://username:password@192.168.1.104:22"\n        \n        挂载文件系统：\n            挂载本机其他路径：\n                root_fs.combine_fs("local_samples","/samples")\n            挂载ssh远程服务器\n                root_fs.combine_fs("my_ubuntu","MY_UBUNTU")\n                    ps："MY_UBUNTU"的配置已经add_server_config过了\n            挂载FTP服务器\n                root_fs.combine_fs("surfing_ftp","SFTP")\n                    ps："SFTP"的配置已经add_server_config过了\n            挂载tar和zip文件系统（系统根目录下的压缩包）\n                root_fs.combine_fs("tar_1","/test.tar.gz",write=True,compression="gz")\n                root_fs.combine_fs("zip_1","/test.zip",write=True,compression=0)\n\n        挂载文件系统后，可将各文件系统视为根目录下的子目录，可直接进行各种文件操作，如：\n            ***很多操作在root_fs.close()后才会生效***\n            返回根目录下列表\n                my_fs = root_fs.get_combined_fs()\n                my_fs.listdir("/") \n            打印目录结构\n                my_fs.tree(path="/",max_levels = 1)\n            复制 从my_ubuntu复制到tar压缩包内(仅可向新建的tar中写入，及write=True)\n                my_fs.copy("/my_ubuntu/home/kim/myproj/测试pyfilesystem2.py","/tar_1/1.py",overwrite=True)\n            在tar中创建多层目录，并向此目录复制文件\n                my_fs.makedirs("/tar_1/x/xx")(仅可向新建的tar中写入，及write=True)\n                my_fs.copy("/my_ubuntu/home/kim/myproj/测试pyfilesystem2.py","/tar_1/x/xx/1.py",overwrite=True)\n            复制 从my_ubuntu复制到zip压缩包内(仅可向新建的zip中写入，及write=True)\n                my_fs.copy("/my_ubuntu/home/kim/myproj/测试pyfilesystem2.py","/zip_1/1.py",overwrite=True)\n            在zip中创建多层目录，并向此目录复制文件(仅可向新建的zip中写入，及write=True)\n                my_fs.makedirs("/zip_1/x/xx")\n                my_fs.copy("/my_ubuntu/home/kim/myproj/测试pyfilesystem2.py","/zip_1/x/xx/1.py",overwrite=True)\n                my_fs.copydir("/my_ubuntu/home/kim/myproj/scripts","/local_current/scripts",create=True)    \n            \n            其他更详细的用法见pyfilesystem2的介绍:\n        ----------------------------------------------------------------------\n        ')

    def show_current_server_config(self):
        for key in self.ServerConfig.keys():
            print(key, ' : ', self.ServerConfig[key])

    def add_server_config(self, s_key, s_path):
        if s_key not in self.ServerConfig.keys():
            self.ServerConfig[s_key] = s_path
        else:
            raise ValueError(f"{s_key}已存在，其路径是{self.ServerConfig[s_key]}")

    def init(self):
        self.pwd_path = os.getcwd()
        self._SFFS__local_fs = fs.open_fs(self.pwd_path)
        self._SFFS__combined_fs = MountFS()
        self._SFFS__combined_fs.mount('local_current', self._SFFS__local_fs)
        self.mount_list = {'local_current': self._SFFS__local_fs}

    def combine_fs(self, map_name, path, write=False, compression=None):
        if path in self.ServerConfig.keys():
            one_fs = fs.open_fs(self.ServerConfig[path])
        else:
            if path.endswith('.zip'):
                if write:
                    if os.path.exists(path):
                        raise FileExistsError(f"新建可写{path}失败，该文件已存在")
                one_fs = ZipFS(path, write, compression)
            else:
                if path.endswith('.tar') or path.endswith('.tar.gz') or path.endswith('.tgz'):
                    if write:
                        if os.path.exists(path):
                            raise FileExistsError(f"新建可写{path}失败，该文件已存在")
                    one_fs = TarFS(path, write, compression)
                else:
                    one_fs = fs.open_fs(path)
        self._SFFS__combined_fs.mount(map_name, one_fs)
        self.mount_list[map_name] = one_fs

    def get_combined_fs(self):
        return self._SFFS__combined_fs

    def get_certain_fs(self, map_name):
        return self.mount_list[map_name]

    def close(self):
        self._SFFS__combined_fs.close()