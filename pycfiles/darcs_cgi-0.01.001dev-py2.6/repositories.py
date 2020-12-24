# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/darcscgi/controllers/repositories.py
# Compiled at: 2009-09-11 13:58:44
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from darcscgi.lib.base import BaseController, render
from pylons import app_globals
from darcscgi.lib.helpers import filelisting, safefile, decodeMessage, verify_patch, apply_patch, quarantine_prune, quarantine
import os, urllib, paste.fileapp
log = logging.getLogger(__name__)

class RepositoriesController(BaseController):

    def patch_wrapper(self, repository):
        if request.method == 'POST':
            if app_globals.is_repository(repository):
                if app_globals.repositories[repository]['allow-write']:
                    content_type = request.headers.get('Content-Type', '').lower()
                    if content_type == 'message/rfc822':
                        return self._post(repository)
                    if content_type == 'application/x-www-form-urlencoded':
                        return self._push(repository)
                    abort(412)
                else:
                    abort(403)
            else:
                abort(404)
        else:
            abort(412)

    def _push(self, repository):
        length = len(request.body)
        if length > app_globals.repositories[repository]['patch-max-size'] * 1024 * 1024:
            abort(413)
        elif length <= 0:
            abort(411)
        else:
            message = urllib.unquote_plus(request.body)
            patch = decodeMessage(message)
            globals = app_globals._current_obj()
            return self._patch_generator(globals, repository, patch, length)

    def _post(self, repository):
        length = int(request.environ.get('CONTENT_LENGTH', -1))
        if length > app_globals.repositories[repository]['patch-max-size'] * 1024 * 1024:
            abort(413)
        elif length <= 0:
            abort(411)
        else:
            message = request.environ['wsgi.input'].read(length)
            patch = decodeMessage(message)
            globals = app_globals._current_obj()
            return self._patch_generator(globals, repository, patch, length)

    def _patch_generator(self, globals, repository, patch, length):
        if globals.repositories[repository]['verify-write'] == False:
            repository_path = globals.repositories[repository]['location']
            command = [globals.globalSettings['darcs']]
            command_options = globals.globalSettings['darcs-options']
            for output in apply_patch(repository, repository_path, patch, command, command_options):
                yield output

        else:
            quarantine_path = globals.globalSettings['quarantine-location']
            max_patches = globals.repositories[repository]['quarantine-max-patches']
            max_size = globals.repositories[repository]['quarantine-max-size'] * 1024 * 1024
            min_trust = globals.repositories[repository]['keyring-min-trust']
            keyring_dirpath = globals.globalSettings['keyring-location']
            keyring_basepath = globals.repositories[repository]['verify-write']
            (verify_bool, verify_string) = verify_patch(keyring_dirpath, keyring_basepath, patch, min_trust, False, False)
            yield verify_string
            if verify_bool:
                repository_path = globals.repositories[repository]['location']
                command = [globals.globalSettings['darcs']]
                command_options = globals.globalSettings['darcs-options']
                for output in apply_patch(repository, repository_path, patch, command, command_options):
                    yield output

            return_message = quarantine_prune(repository, quarantine_path, max_patches, max_size, length)
            if return_message is not None:
                yield return_message
            else:
                for output in quarantine(repository, quarantine_path, patch):
                    yield output

                return

    def fetch_wrapper(self, repository, path):
        if app_globals.is_repository(repository):
            if app_globals.repositories[repository]['allow-read']:
                location = app_globals.repositories[repository]['location']
                return self._fetch(repository, path, location)
            abort(403)
        else:
            abort(404)

    def _fetch(self, repository, path, location):
        if app_globals.repositories[repository]['verify-read'] == False:
            result = safefile(location, path)
            if result:
                fapp = paste.fileapp.FileApp(result, allowed_methods=('GET', 'HEAD',
                                                                      'POST'))
                return fapp(request.environ, self.start_response)
            abort(403)
        else:
            authentication = request.params.get('sig')
            if authentication:
                min_trust = app_globals.repositories[repository]['keyring-min-trust']
                keyring_dirpath = app_globals.globalSettings['keyring-location']
                keyring_basepath = app_globals.repositories[repository]['verify-read']
                (verify_bool, verify_string, verify_post) = verify_patch(keyring_dirpath, keyring_basepath, authentication, min_trust, True, True)
                if verify_bool and verify_post == 'welcome\n':
                    result = safefile(location, path)
                    if result:
                        fapp = paste.fileapp.FileApp(result, allowed_methods=('GET',
                                                                              'HEAD',
                                                                              'POST'))
                        return fapp(request.environ, self.start_response)
                    abort(403)
                else:
                    abort(403)
            else:
                abort(415)