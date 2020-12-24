# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bintraypy_cli/cmd.py
# Compiled at: 2016-09-20 07:22:50
# Size of source mod 2**32: 1714 bytes
from plumbum import cli
from bintraypy.bintray import Bintray

class BintrayPyCLI(cli.Application):
    PROGNAME = 'bintraypy'

    def __init__(self, executable):
        super().__init__(executable)
        self.username = None
        self.key = None
        self.url = Bintray.default_url
        self.bintray = None
        return

    @cli.switch(names=['-u', '--username'], argtype=str)
    def username(self, username):
        """
    Sets the authentication username.
    """
        self.username = username

    @cli.switch(names=['-k', '--key'], argtype=str)
    def key(self, key):
        """
    Sets the authentication key.
    """
        self.key = key

    @cli.switch(names=['-l', '--url'], argtype=str)
    def url(self, url):
        """
    Sets the API URL.
    """
        self.url = url

    def main(self):
        if not self.nested_command:
            print('Error: no command given')
            self.help()
            return 1
        self.bintray = Bintray(username=self.username, key=self.key, url=self.url)
        return 0


@BintrayPyCLI.subcommand('upload')
class CreateCommand(cli.Application):
    __doc__ = '\n  Uploads a generic file.\n  '
    remote_file_path = cli.SwitchAttr(names=[
     '-f', '--remote-file-path'], argtype=str, default=None, help='Remote file path. Defaults to the filename of file being uploaded')
    publish = cli.Flag(names=[
     '-p', '--publish'], default=False, help='Publish file after uploading')
    override = cli.Flag(names=[
     '-o', '--override'], default=False, help='Override existing file')

    def main(self, file, organization, repo, package, version):
        bintray = self.parent.bintray
        bintray.upload_generic(file, organization, repo, package, version, self.remote_file_path, self.publish, self.override)
        return 0