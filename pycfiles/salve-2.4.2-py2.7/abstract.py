# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/salve/filesys/abstract.py
# Compiled at: 2015-11-06 23:45:35
import abc
from contextlib import contextmanager
from salve import Enum, with_metaclass
from .access import access_codes

class Filesys(with_metaclass(abc.ABCMeta)):
    """
    This defines the properties of the filesystem layer, through which
    interactions with the underlying files and directories take place. This
    includes fetching the FilesysElement objects that represent the
    files/directories at certain paths.
    """
    element_types = Enum('FILE', 'DIR', 'LINK')

    @abc.abstractmethod
    def lookup_type(self, path):
        """
        Lookup the type of a given path.

        Args:
            @path
            The path to the file, dir, or link to lookup.
        """
        pass

    @abc.abstractmethod
    def chmod(self, path, mode, *args, **kwargs):
        """
        Chmods the file or directory to a given mode, in the form of an octal
        int. Follows symlinks.

        On real files and directories, should behave like

        >>> os.chmod(path, mode)

        Args:
            @path
            The path to the file to chmod.

            @mode
            An octal int for ugo-style permissions, as in 0o777 or 0o644
        """
        pass

    @abc.abstractmethod
    def chown(self, path, uid, gid, *args, **kwargs):
        """
        Chowns the file or directory to a given user in the form of a uid and a
        given group in the form of a gid. Does not follow symlinks.

        On real files and directories, should behave like

        >>> os.lchown(path, uid, gid)

        If one of the values is not changing, this can be handled through a
        stat() call, a la

        >>> self.chown(path, new_uid, self.stat(path).st_gid)

        or

        >>> self.chown(path, self.stat(path).st_uid, new_gid)

        Args:
            @path
            The path to the file, directory, or link to chown.

            @uid
            The integer uid to set on the file or directory.

            @gid
            The integer gid to set on the file or directory.
        """
        pass

    @abc.abstractmethod
    def stat(self, path, *args, **kwargs):
        """
        Get the results of a stat on the file or directory, raising an OSError
        (errno=2, no such file or directory) if it does not exist. Only
        guaranteed to return an object, of an unspecified type, with the
        attributes
            st_mode - protection bits
            st_ino - inode number
            st_nlink - number of hard links
            st_uid - user id of owner
            st_gid - group id of owner
            st_size - size of file, in bytes
            st_atime - time of most recent access
            st_mtime - time of most recent content modification
            st_ctime - time of most recent metadata change

        Does not follow symlinks, so on real filesystem access, this is the
        equivalent of doing

        >>> os.lstat(self.path)

        but it is not safe to assume that nothing else happens. There may be
        other processing at play. In other words, don't call os.lstat on the
        underlying file and expect the same things to happen.

        Args:
            @path
            The path to the file, dir, or link to stat
        """
        pass

    @abc.abstractmethod
    def access(self, path, mode, *args, **kwargs):
        """
        Preform an access check as with os.access, returning True or False
        depending on the type of access available.
        Follows symlinks, assuming (as on Linux platforms) that symlink
        permissions are those of the destination.

        Args:
            @path
            The path to the file whose access should be checked.

            @mode
            As per os.access, this must either be
                filesys.access_codes.F_OK
            or an inclusive OR of
                filesys.access_codes.W_OK
                filesys.access_codes.R_OK
                filesys.access_codes.X_OK
            When operating on a real file, arguments are presumably passed
            transparently through to the os.access() function, after a
            translation step.
        """
        pass

    @abc.abstractmethod
    def exists(self, path, *args, **kwargs):
        """
        Returns true if the file/dir exists, and false if it does not.

        This is meaningful in general, as creating an abstract file or
        directory to refer to a location does not necessarily indicate that any
        file or directory creation has taken place. That would require an
        explicit creation action, which in the case of a virtualized filesys
        means (more or less) flipping a boolean flag, and in the case of a real
        filesystem means applying a mkdir or touch operation.

        Does not follow symlinks, so this is not equivalent to an invocation of

        >>> self.access(path, os.F_OK)

        but instead will behave much like

        >>> os.lexists(path)

        in which broken symlinks still appear as "present"
        """
        pass

    @abc.abstractmethod
    def hash(self, path, *args, **kwargs):
        """
        Get a hash of the contents of the file or link at @path.
        Generally used for quick comparison of files and symlinks, much like a
        symbol table for fast string comparisons. This will be a sha512 hash of
        any files, and a sha256 hash of any symlinks' paths (not the contents
        of the linked file).
        The hash() operation has no significance on directories, and its
        behavior on them is undefined.

        Args:
            @path
            The path to the file or link to hash.
        """
        pass

    @abc.abstractmethod
    def copy(self, src, dst, *args, **kwargs):
        """
        Copies a file or directory (recursive) from the source to the
        destination, given as paths.

        Args:
            @src
            The source file, as a path.

            @dst
            The destination file, as a path.
        """
        pass

    @abc.abstractmethod
    def walk(self, path, *args, **kwargs):
        """
        An iterator over the contents of the directory at @path, yielding
        3-tuples of the form

        (dirname, subdirs, files)

        where dirname is the path to the directory rooted at @path, subdirs
        is a list of subdirectory names (which will be included in later
        iterations), and files is a list of file names found inside of the
        directory at dirname.

        If the directory does not exist, the iterator is empty, as opposed to a
        single iteration with (name, [], []), as would be given if it were an
        existing empty directory.

        Args:
            @path
            The path to the directory to walk.
        """
        pass

    @abc.abstractmethod
    def touch(self, path, *args, **kwargs):
        """
        Create a file, using the default system umask (whatever it is) and
        the current euid and egid values. Doesn't do any fancy logic about
        chmoding or chowning the file after creation -- simply brings it into
        the world in whatever state is sensible.

        Args:
            @path
            The path to the file to create.
        """
        pass

    @abc.abstractmethod
    def mkdir(self, path, recursive=True, *args, **kwargs):
        """
        Create the directory at @path. Behaves very much like touch(),
        using the current umask and not performing any special logic on the
        resulting directory.

        Args:
            @path
            The path to the directory to create.

        KWArgs:
            @recursive=True
            When true, create all parent directories necessary for a directory
            to exist. When false, if an ancestor directory does not exist, an
            OSError will be thrown.
        """
        pass

    @abc.abstractmethod
    def symlink(self, path, target, *args, **kwargs):
        """
        Creates a symlink at @target to @path

        Like touch(), this does not do any special logic on
        ownership &c, but simply creates the symlink with whatever settings are
        applied by the current effective uid and gid.

        Args:
            @path
            The destination path to which the symlink points

            @target
            The target location at which the symlink should be created
        """
        pass

    @abc.abstractmethod
    @contextmanager
    def open(self, path, *args, **kwargs):
        """
        Open the file at @path, returning a file-like object for interaction.
        Since this method itself is a contextmanager, it must follow the
        contextlib __enter__, yield, __exit__ paradigm. It can be used to wrap
        existing contextmanagers like so:

        >>> def open(self, mode):
        >>>     enter()
        >>>     with open(path, *args, **kwargs) as f:
        >>>         yield f
        >>>     exit()
        """
        pass

    def get_existing_ancestor(self, path):
        """
        Find the nearest ancestor of a file, dir, or link that passes an
        existence check.

        Args:
            @path
            An absolute path whose prefix should be inspected.
        """
        pass

    def writable_path_or_ancestor(self, path):
        """
        Check if a path points at a writable file/dir.
        Doesn't restrict itself to the results of access(), but also checks
        access on parent dirs,

        Args:
            @path
            An absolute path to a file/dir which should be inspected.
        """
        if self.access(path, access_codes.W_OK):
            return True
        if self.access(path, access_codes.F_OK):
            return False
        containing_dir = self.get_existing_ancestor(path)
        if self.access(containing_dir, access_codes.W_OK):
            return True
        return False