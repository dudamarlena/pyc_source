# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\commands\install.py
# Compiled at: 2017-04-19 05:14:04
from __future__ import division, print_function, unicode_literals
import hashlib, logging, os, shutil, tempfile, zipfile, tqdm
from six.moves.urllib.error import HTTPError, URLError
from six.moves.urllib.request import urlopen
from rbtools.commands import Command, CommandError
from rbtools.utils.appdirs import user_data_dir
from rbtools.utils.checks import check_install
from rbtools.utils.process import execute

class Install(Command):
    """Install a dependency.

    This allows RBTools to install external dependencies that may be needed for
    some features.
    """
    name = b'install'
    author = b'The Review Board Project'
    description = b'Install an optional dependency.'
    args = b'<package>'
    option_list = []
    package_urls = {b'tfs': b'http://downloads.beanbaginc.com/rb-tfs/rb-tfs.zip'}

    def main(self, package):
        """Run the command.

        Args:
            package (unicode):
                The name of the package to install.

        Raises:
            rbtools.commands.CommandError:
                An error occurred during installation.
        """
        try:
            url = self.package_urls[package]
        except KeyError:
            err = b'Package "%s" not found. Available packages are:\n' % package
            err += (b'\n').join(b'    %s' % package_name for package_name in self.package_urls.keys())
            raise CommandError(err)

        label = b'Downloading %s' % package
        zip_filename = self.download_file(url, label=label)
        try:
            self.check_download(url, zip_filename)
            self.unzip(zip_filename, os.path.join(user_data_dir(b'rbtools'), b'packages', package))
        finally:
            os.unlink(zip_filename)

    def check_download(self, url, zip_filename):
        """Check to see if the file was successfully downloaded.

        If the user has :command:`gpg` installed on their system, use that to
        check that the package was signed. Otherwise, check the sha256sum.

        Args:
            url (unicode):
                The URL that the file came from.

            zip_filename (unicode):
                The filename of the downloaded copy.

        Raises:
            rbtools.commands.CommandError:
                The authenticity of the file could not be verified.
        """
        if check_install(b'gpg'):
            execute([b'gpg', b'--recv-keys', b'4ED1F993'])
            sig_filename = self.download_file(b'%s.asc' % url)
            try:
                retcode, output, errors = execute([
                 b'gpg', b'--verify', sig_filename, zip_filename], with_errors=False, ignore_errors=True, return_error_code=True, return_errors=True)
                if retcode == 0:
                    logging.debug(b'Verified file signature')
                else:
                    raise CommandError(b'Unable to verify authenticity of file downloaded from %s:\n%s' % (
                     url, errors))
            finally:
                os.unlink(sig_filename)

        else:
            logging.info(b'"gpg" not installed. Skipping signature validation.')
            try:
                sha_url = b'%s.sha256sum' % url
                logging.debug(b'Downloading %s', sha_url)
                response = urlopen(sha_url)
                real_sha = response.read().split(b' ')[0]
            except (HTTPError, URLError) as e:
                raise CommandError(b'Error when downloading file: %s' % e)

            with open(zip_filename, b'r') as (f):
                our_sha = hashlib.sha256(f.read()).hexdigest()
            if real_sha == our_sha:
                logging.debug(b'Verified SHA256 hash')
            else:
                logging.debug(b'SHA256 hash does not match!')
                logging.debug(b'  Downloaded file hash was: %s', our_sha)
                logging.debug(b'  Expected hash was: %s', real_sha)
                raise CommandError(b'Unable to verify the checksum of the downloaded copy of %s.\nThis could be due to an invasive proxy or an attempted man-in-the-middle attack.' % url)

    def unzip(self, zip_filename, package_dir):
        """Unzip a .zip file.

        This method will unpack the contents of a .zip file into a target
        directory. If that directory already exists, it will first be removed.

        Args:
            zip_filename (unicode):
                The absolute path to the .zip file to unpack.

            package_dir (unicode):
                The directory to unzip the files into.

        Raises:
            rbtools.commands.CommandError:
                The file could not be unzipped.
        """
        logging.debug(b'Extracting %s to %s', zip_filename, package_dir)
        try:
            if os.path.exists(package_dir):
                if os.path.isdir(package_dir):
                    shutil.rmtree(package_dir)
                else:
                    os.remove(package_dir)
            os.makedirs(package_dir)
        except (IOError, OSError) as e:
            raise CommandError(b'Failed to set up package directory %s: %s' % (
             package_dir, e))

        zip_file = zipfile.ZipFile(zip_filename, b'r')
        try:
            try:
                zip_file.extractall(package_dir)
            except Exception as e:
                raise CommandError(b'Failed to extract file: %s' % e)

        finally:
            zip_file.close()

    def download_file(self, url, label=None):
        """Download the given file.

        This is intended to be used as a context manager, and the bound value
        will be the filename of the downloaded file.

        Args:
            url (unicode):
                The URL of the file to download.

            label (unicode, optional):
                The label to use for the progress bar. If this is not
                specified, no progress bar will be shown.

        Yields:
            unicode:
            The filename of the downloaded file.

        Raises:
            rbtools.commands.CommandError:
                An error occurred while downloading the file.
        """
        logging.debug(b'Downloading %s', url)
        try:
            response = urlopen(url)
            total_bytes = int(response.info().getheader(b'Content-Length').strip())
            read_bytes = 0
            bar_format = b'{desc} {bar} {percentage:3.0f}% [{remaining}]'
            with tqdm.tqdm(total=total_bytes, desc=label or b'', ncols=80, disable=label is None, bar_format=bar_format) as (bar):
                try:
                    f = tempfile.NamedTemporaryFile(delete=False)
                    while read_bytes != total_bytes:
                        chunk = response.read(8192)
                        chunk_length = len(chunk)
                        read_bytes += chunk_length
                        f.write(chunk)
                        bar.update(chunk_length)

                finally:
                    f.close()

            return f.name
        except (HTTPError, URLError) as e:
            raise CommandError(b'Error when downloading file: %s' % e)

        return