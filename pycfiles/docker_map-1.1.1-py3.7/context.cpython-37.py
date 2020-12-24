# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/build/context.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 9578 bytes
from __future__ import unicode_literals
import tarfile, fnmatch, os, re
from .buffer import DockerTempFile
from .dockerfile import DockerFile
LITERAL_PATTERN = re.compile('\\\\(.)')

def preprocess_matches(input_items):
    """
    Converts, as far as possible, Go filepath.Match patterns into Python regular expression patterns. Blank lines are
    ignored.

    This is a generator of two-element-tuples, with the first item as the compiled regular expression. Items prefixed
    with an exclamation mark are considered negative exclusions, i.e. exemptions. These have the second tuple item set
    to ``True``, others to ``False``.

    :param input_items: Input patterns to convert.
    :return: Generator of converted patterns.
    :rtype: collections.Iterable[(__RegEx, bool)]
    """
    for i in input_items:
        s = i.strip()
        if not s:
            continue
        elif s[0] == '!':
            is_negative = True
            match_str = s[1:]
            if not match_str:
                continue
        else:
            is_negative = False
            match_str = s
        yield (
         re.compile(fnmatch.translate(LITERAL_PATTERN.sub('[\\g<1>]', match_str))), is_negative)


def get_exclusions(path):
    """
    Generates exclusion patterns from a ``.dockerignore`` file located in the given path. Returns ``None`` if the
    file does not exist.

    :param path: Path to look up the ``.dockerignore`` in.
    :type path: unicode | str
    :return: List of patterns, that can be passed into :func:`get_filter_func`.
    :rtype: list[(__RegEx, bool)]
    """
    if not os.path.isdir(path):
        return
    else:
        dockerignore_file = os.path.join(path, '.dockerignore')
        return os.path.isfile(dockerignore_file) or None
    with open(dockerignore_file, 'rb') as (dif):
        return list(preprocess_matches(dif.readlines()))


def get_filter_func(patterns, prefix):
    """
    Provides a filter function that can be used as filter argument on ``tarfile.add``. Generates the filter based on
    the patterns and prefix provided. Patterns should be a list of tuples. Each tuple consists of a compiled RegEx
    pattern and a boolean, indicating if it is an ignore entry or a negative exclusion (i.e. an exemption from
    exclusions). The prefix is used to match relative paths inside the tar file, and is removed from every entry
    passed into the functions.

    Note that all names passed into the returned function must be paths under the provided prefix. This condition is
    not checked!

    :param patterns: List of patterns and negative indicator.
    :type patterns: list[(__RegEx, bool)]
    :param prefix: Prefix to strip from all file names passed in. Leading and trailing path separators are removed.
    :type prefix: unicode | str
    :return: tarinfo.TarInfo -> tarinfo.TarInfo | NoneType
    """
    prefix_len = len(prefix.strip(os.path.sep)) + 1
    if any((i[1] for i in patterns)):

        def _exclusion_func(tarinfo):
            name = tarinfo.name[prefix_len:]
            exclude = False
            for match_str, is_negative in patterns:
                if is_negative:
                    if not exclude:
                        continue
                    if match_str.match(name) is not None:
                        exclude = False
                    elif exclude:
                        continue
                    elif match_str.match(name) is not None:
                        exclude = True

            if exclude:
                return
            return tarinfo

    else:
        exclusions = [i[0] for i in patterns]

        def _exclusion_func(tarinfo):
            name = tarinfo.name[prefix_len:]
            if any((match_str.match(name) is not None for match_str in exclusions)):
                return
            return tarinfo

    return _exclusion_func


class DockerContext(DockerTempFile):
    __doc__ = '\n    Class for constructing a Docker context tarball, that can be sent to the remote API. If a :class:`~DockerFile`\n    instance is added, the resulting Dockerfile and files added there are considered automatically.\n\n    :param dockerfile: Optional :class:`~DockerFile` instance, or file path to a Dockerfile.\n    :type dockerfile: DockerFile | unicode | str\n    :param compression: Compression for the tarball; default is gzip (`gz`); use `bz2` for bzip2.\n    :type compression: unicode | str\n    :param encoding: Encoding for the tarfile; default is `utf-8`.\n    :type encoding: unicode | str\n    :param finalize: Finalize the tarball immediately.\n    :type finalize: bool\n    :param kwargs: Additional kwargs for :func:`tarfile.open`.\n    '

    def __init__(self, dockerfile=None, compression='gz', encoding='utf-8', finalize=False, **kwargs):
        super(DockerContext, self).__init__()
        open_mode = 'w:{0}'.format(compression or '')
        if compression == 'gz':
            self._stream_encoding = 'gzip'
        else:
            if compression == 'bz2':
                self._stream_encoding = 'bzip2'
            else:
                self._stream_encoding = None
        self.tarfile = (tarfile.open)(mode=open_mode, fileobj=self._fileobj, encoding=encoding, **kwargs)
        if dockerfile is not None:
            self.add_dockerfile(dockerfile)
        if finalize:
            if dockerfile is None:
                raise ValueError('Cannot finalize the docker context tarball without a dockerfile object.')
            self.finalize()

    def add(self, name, arcname=None, **kwargs):
        """
        Add a file or directory to the context tarball.

        :param name: File or directory path.
        :type name: unicode | str
        :param args: Additional args for :meth:`tarfile.TarFile.add`.
        :param kwargs: Additional kwargs for :meth:`tarfile.TarFile.add`.
        """
        if os.path.isdir(name):
            exclusions = get_exclusions(name)
            if exclusions:
                target_prefix = os.path.abspath(arcname or name)
                kwargs.setdefault('filter', get_filter_func(exclusions, target_prefix))
        (self.tarfile.add)(name, arcname=arcname, **kwargs)

    def addfile(self, *args, **kwargs):
        """
        Add a file to the tarball using a :class:`~tarfile.TarInfo` object. For details, see
        :meth:`tarfile.TarFile.addfile`.

        :param args: Args to :meth:`tarfile.TarFile.addfile`.
        :param kwargs: Kwargs to :meth:`tarfile.TarFile.addfile`
        """
        (self.tarfile.addfile)(*args, **kwargs)

    def addarchive(self, name):
        """
        Add (i.e. copy) the contents of another tarball to this one.

        :param name: File path to the tar archive.
        :type name: unicode | str
        """
        with tarfile.open(name, 'r') as (st):
            for member in st.getmembers():
                self.tarfile.addfile(member, st.extractfile(member.name))

    def add_dockerfile(self, dockerfile):
        """
        Add a Dockerfile to the context. If it is a :class:`DockerFile` instance, files and archive contents added there
        will automatically be copied to the tarball. The :class:`DockerFile` will be finalized.

        :param dockerfile: :class:`DockerFile` instance or file path to a Dockerfile.
        :type dockerfile: DockerFile | unicode | str
        """
        if isinstance(dockerfile, DockerFile):
            dockerfile.finalize()
            dockerfile_obj = dockerfile.fileobj
            for path, arcname in dockerfile._files:
                self.add(path, arcname=arcname)

            for archive in dockerfile._archives:
                self.addarchive(archive)

            tarinfo = tarfile.TarInfo('Dockerfile')
            tarinfo.size = dockerfile_obj.tell()
            dockerfile_obj.seek(0)
            self.tarfile.addfile(tarinfo, dockerfile_obj)
        else:
            self.add(dockerfile, arcname='Dockerfile')

    def gettarinfo(self, *args, **kwargs):
        """
        Returns a :class:`~tarfile.TarInfo` object. See :meth:`tarfile.TarFile.gettarinfo`.

        :param args: Args to :meth:`tarfile.TarFile.gettarinfo`.
        :param kwargs: Kwargs to :meth:`tarfile.TarFile.gettarinfo`.
        :return: :class:`~tarfile.TarInfo` object.
        :rtype: tarfile.TarInfo
        """
        return (self.tarfile.gettarinfo)(*args, **kwargs)

    def finalize(self):
        """
        Finalizes the context tarball and sets the file position to 0. The tar file is then closed, but the underlying
        file object can still be read.
        """
        self.tarfile.close()
        self._fileobj.seek(0)

    @property
    def name(self):
        """
        Returns the name of the underlying file object.

        :return: Name of the file object.
        :rtype: unicode | str
        """
        return self._fileobj.name

    @property
    def stream_encoding(self):
        """
        Returns the stream encoding, as used when calling :meth:`docker.client.Client.build`.

        :return: Stream encoding.
        :rtype: unicode | str
        """
        return self._stream_encoding

    def save(self, name):
        """
        Saves the entire Docker context tarball to a separate file.

        :param name: File path to save the tarball into.
        :type name: unicode | str
        """
        with open(name, 'wb+') as (f):
            while True:
                buf = self._fileobj.read()
                if not buf:
                    break
                f.write(buf)