# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /opt/adagios/adagios/userdata.py
# Compiled at: 2018-05-16 10:07:32
import os, json, collections, settings

class User(object):
    """ Handles authentified users, provides preferences management. """
    SAVED_SEARCHES = 'saved_searches'

    def __init__(self, request, autosave=False):
        """ Instantiates one user's preferences.

        Args:
          request (Request): The incoming Django request.

        Kwargs:
          autosave (bool): if True, preferences are automatically saved.
        """
        self._request = request
        self._autosave = autosave
        try:
            self._username = request.META.get('REMOTE_USER', 'anonymous')
        except Exception:
            self._username = 'anonymous'

        self._conffile = self._get_prefs_location()
        self._check_path(self._conffile)
        for k, v in self._get_conf().iteritems():
            self.__dict__[k] = v

    def _check_path(self, path):
        """ Checks the userdata folder, try to create it if it doesn't
        exist."""
        folder = os.path.dirname(path)
        if not os.path.isdir(folder):
            try:
                os.makedirs(folder)
            except:
                raise Exception("Folder %s can't be created. Be sure Adagios has write access on its parent." % folder)

    def _get_prefs_location(self):
        """ Returns the location of the preferences file of the
        specified user. """
        try:
            user_prefs_path = settings.USER_PREFS_PATH
        except:
            raise Exception('You must define USER_PREFS_PATH in settings.py')

        return os.path.join(user_prefs_path, self._username + '.json')

    def _get_default_conf(self):
        try:
            d = settings.PREFS_DEFAULT
        except:
            d = dict()

        return d

    def _get_conf(self):
        """ Returns the json preferences for the specified user. """
        try:
            with open(self._conffile) as (f):
                conf = json.loads(f.read())
        except IOError:
            conf = self._get_default_conf()
        except ValueError:
            conf = self._get_default_conf()

        return conf

    def __getattr__(self, name):
        """ Provides None as a default value. """
        if name not in self.__dict__.keys():
            return None
        else:
            return self.__dict__[name]

    def __setattr__(self, name, value):
        """ Saves the preferences if autosave is set. """
        self.__dict__[name] = value
        if self._autosave and not name.startswith('_'):
            self.save()

    def set_pref(self, name, value):
        """ Explicitly sets a user preference. """
        self.__dict__[name] = value

    def to_dict(self):
        d = {}
        for k in filter(lambda x: not x.startswith('_'), self.__dict__.keys()):
            d[k] = self.__dict__[k]

        return d

    def save(self):
        """ Saves  the preferences in JSON format. """
        d = self.to_dict()
        try:
            with open(self._conffile, 'w') as (f):
                f.write(json.dumps(d))
        except IOError:
            raise Exception("Couldn't write settings into file %s. Be sure to have write permissions on the parent folder." % self._conffile)

        self.trigger_hooks()

    def trigger_hooks(self):
        """ Triggers the hooks when preferences are changed. """
        from django.utils import translation
        try:
            self._request.session['django_language'] = self.language
            translation.activate(self.language)
        except Exception as e:
            pass