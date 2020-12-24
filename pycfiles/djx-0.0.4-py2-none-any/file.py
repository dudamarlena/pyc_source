# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-n_sfyb/Django/django/contrib/sessions/backends/file.py
# Compiled at: 2019-02-14 00:35:16
import datetime, errno, logging, os, shutil, tempfile
from django.conf import settings
from django.contrib.sessions.backends.base import VALID_KEY_CHARS, CreateError, SessionBase, UpdateError
from django.contrib.sessions.exceptions import InvalidSessionKey
from django.core.exceptions import ImproperlyConfigured, SuspiciousOperation
from django.utils import timezone
from django.utils.encoding import force_text

class SessionStore(SessionBase):
    """
    Implements a file based session store.
    """

    def __init__(self, session_key=None):
        self.storage_path = type(self)._get_storage_path()
        self.file_prefix = settings.SESSION_COOKIE_NAME
        super(SessionStore, self).__init__(session_key)

    @classmethod
    def _get_storage_path(cls):
        try:
            return cls._storage_path
        except AttributeError:
            storage_path = getattr(settings, 'SESSION_FILE_PATH', None)
            if not storage_path:
                storage_path = tempfile.gettempdir()
            if not os.path.isdir(storage_path):
                raise ImproperlyConfigured("The session storage path %r doesn't exist. Please set your SESSION_FILE_PATH setting to an existing directory in which Django can store session data." % storage_path)
            cls._storage_path = storage_path
            return storage_path

        return

    def _key_to_file(self, session_key=None):
        """
        Get the file associated with this session key.
        """
        if session_key is None:
            session_key = self._get_or_create_session_key()
        if not set(session_key).issubset(set(VALID_KEY_CHARS)):
            raise InvalidSessionKey('Invalid characters in session key')
        return os.path.join(self.storage_path, self.file_prefix + session_key)

    def _last_modification(self):
        """
        Return the modification time of the file storing the session's content.
        """
        modification = os.stat(self._key_to_file()).st_mtime
        if settings.USE_TZ:
            modification = datetime.datetime.utcfromtimestamp(modification)
            modification = modification.replace(tzinfo=timezone.utc)
        else:
            modification = datetime.datetime.fromtimestamp(modification)
        return modification

    def _expiry_date(self, session_data):
        """
        Return the expiry time of the file storing the session's content.
        """
        expiry = session_data.get('_session_expiry')
        if not expiry:
            expiry = self._last_modification() + datetime.timedelta(seconds=settings.SESSION_COOKIE_AGE)
        return expiry

    def load(self):
        session_data = {}
        try:
            with open(self._key_to_file(), 'rb') as (session_file):
                file_data = session_file.read()
            if file_data:
                try:
                    session_data = self.decode(file_data)
                except (EOFError, SuspiciousOperation) as e:
                    if isinstance(e, SuspiciousOperation):
                        logger = logging.getLogger('django.security.%s' % e.__class__.__name__)
                        logger.warning(force_text(e))
                    self.create()

                expiry_age = self.get_expiry_age(expiry=self._expiry_date(session_data))
                if expiry_age <= 0:
                    session_data = {}
                    self.delete()
                    self.create()
        except (IOError, SuspiciousOperation):
            self._session_key = None

        return session_data

    def create(self):
        while True:
            self._session_key = self._get_new_session_key()
            try:
                self.save(must_create=True)
            except CreateError:
                continue

            self.modified = True
            return

    def save(self, must_create=False):
        if self.session_key is None:
            return self.create()
        else:
            session_data = self._get_session(no_load=must_create)
            session_file_name = self._key_to_file()
            try:
                flags = os.O_WRONLY | getattr(os, 'O_BINARY', 0)
                if must_create:
                    flags |= os.O_EXCL | os.O_CREAT
                fd = os.open(session_file_name, flags)
                os.close(fd)
            except OSError as e:
                if must_create and e.errno == errno.EEXIST:
                    raise CreateError
                if not must_create and e.errno == errno.ENOENT:
                    raise UpdateError
                raise

            dir, prefix = os.path.split(session_file_name)
            try:
                output_file_fd, output_file_name = tempfile.mkstemp(dir=dir, prefix=prefix + '_out_')
                renamed = False
                try:
                    try:
                        os.write(output_file_fd, self.encode(session_data).encode())
                    finally:
                        os.close(output_file_fd)

                    shutil.move(output_file_name, session_file_name)
                    renamed = True
                finally:
                    if not renamed:
                        os.unlink(output_file_name)

            except (OSError, IOError, EOFError):
                pass

            return

    def exists(self, session_key):
        return os.path.exists(self._key_to_file(session_key))

    def delete(self, session_key=None):
        if session_key is None:
            if self.session_key is None:
                return
            session_key = self.session_key
        try:
            os.unlink(self._key_to_file(session_key))
        except OSError:
            pass

        return

    def clean(self):
        pass

    @classmethod
    def clear_expired(cls):
        storage_path = cls._get_storage_path()
        file_prefix = settings.SESSION_COOKIE_NAME
        for session_file in os.listdir(storage_path):
            if not session_file.startswith(file_prefix):
                continue
            session_key = session_file[len(file_prefix):]
            session = cls(session_key)
            session.create = lambda : None
            session.load()