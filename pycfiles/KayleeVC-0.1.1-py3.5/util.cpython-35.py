# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kayleevc/util.py
# Compiled at: 2016-02-28 12:30:17
# Size of source mod 2**32: 7130 bytes
import re, json, hashlib, os
from argparse import ArgumentParser, Namespace
import requests
from gi.repository import GLib

class Config:
    __doc__ = 'Keep track of the configuration of Kaylee'
    program_name = 'kaylee'
    conf_dir = os.path.join(GLib.get_user_config_dir(), program_name)
    cache_dir = os.path.join(GLib.get_user_cache_dir(), program_name)
    data_dir = os.path.join(GLib.get_user_data_dir(), program_name)
    command_file = os.path.join(conf_dir, 'commands.conf')
    opt_file = os.path.join(conf_dir, 'options.json')
    history_file = os.path.join(cache_dir, program_name + 'history')
    hash_file = os.path.join(cache_dir, 'hash.json')
    strings_file = os.path.join(data_dir, 'sentences.corpus')
    lang_file = os.path.join(data_dir, 'lm')
    dic_file = os.path.join(data_dir, 'dic')

    def __init__(self):
        self._make_dir(self.conf_dir)
        self._make_dir(self.cache_dir)
        self._make_dir(self.data_dir)
        self.parser = ArgumentParser()
        self.parser.add_argument('-i', '--interface', type=str, dest='interface', action='store', help="Interface to use (if any). 'g' for GTK or 'gt' for GTK" + ' system tray icon')
        self.parser.add_argument('-c', '--continuous', action='store_true', dest='continuous', default=False, help="Start interface with 'continuous' listen enabled")
        self.parser.add_argument('-p', '--pass-words', action='store_true', dest='pass_words', default=False, help='Pass the recognized words as arguments to the shell' + ' command')
        self.parser.add_argument('-H', '--history', type=int, action='store', dest='history', help='Number of commands to store in history file')
        self.parser.add_argument('-m', '--microphone', type=int, action='store', dest='microphone', default=None, help='Audio input card to use (if other than system default)')
        self.parser.add_argument('--valid-sentence-command', type=str, dest='valid_sentence_command', action='store', help='Command to run when a valid sentence is detected')
        self.parser.add_argument('--invalid-sentence-command', type=str, dest='invalid_sentence_command', action='store', help='Command to run when an invalid sentence is detected')
        self._read_options_file()
        self.parser.parse_args(namespace=self.options)

    def _make_dir(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)

    def _read_options_file(self):
        try:
            with open(self.opt_file, 'r') as (f):
                self.options = json.load(f)
                self.options = Namespace(**self.options)
        except FileNotFoundError:
            self.options = Namespace()


class Hasher:
    __doc__ = 'Keep track of hashes for Kaylee'

    def __init__(self, config):
        self.config = config
        try:
            with open(self.config.hash_file, 'r') as (f):
                self.hashes = json.load(f)
        except IOError:
            self.hashes = {}

    def __getitem__(self, hashname):
        try:
            return self.hashes[hashname]
        except (KeyError, TypeError):
            return

    def __setitem__(self, hashname, value):
        self.hashes[hashname] = value

    def get_hash_object(self):
        """Returns an object to compute a new hash"""
        return hashlib.sha256()

    def store(self):
        """Store the current hashes into a the hash file"""
        with open(self.config.hash_file, 'w') as (f):
            json.dump(self.hashes, f)


class LanguageUpdater:
    __doc__ = '\n    Handles updating the language using the online lmtool.\n\n    This class provides methods to check if the corpus has changed, and to\n    update the language to match the new corpus using the lmtool.  This allows\n    us to automatically update the language if the corpus has changed, saving\n    the user from having to do this manually.\n    '

    def __init__(self, config):
        self.config = config
        self.hasher = Hasher(config)

    def update_language_if_changed(self):
        """Test if the language has changed, and if it has, update it"""
        if self.language_has_changed():
            self.update_language()
            self.save_language_hash()

    def language_has_changed(self):
        """Use hashes to test if the language has changed"""
        self.stored_hash = self.hasher['language']
        hasher = self.hasher.get_hash_object()
        with open(self.config.strings_file, 'rb') as (sfile):
            buf = sfile.read()
            hasher.update(buf)
        self.new_hash = hasher.hexdigest()
        return self.new_hash != self.stored_hash

    def update_language(self):
        """Update the language using the online lmtool"""
        print('Updating language using online lmtool')
        host = 'http://www.speech.cs.cmu.edu'
        url = host + '/cgi-bin/tools/lmtool/run'
        response_text = ''
        with open(self.config.strings_file, 'rb') as (corpus):
            files = {'corpus': corpus}
            values = {'formtype': 'simple'}
            r = requests.post(url, files=files, data=values)
            response_text = r.text
        path_re = '.*<title>Index of (.*?)</title>.*'
        number_re = '.*TAR([0-9]*?)\\.tgz.*'
        for line in response_text.split('\n'):
            if re.search(path_re, line):
                path = host + re.sub(path_re, '\\1', line)
            elif re.search(number_re, line):
                number = re.sub(number_re, '\\1', line)
                break

        lm_url = path + '/' + number + '.lm'
        dic_url = path + '/' + number + '.dic'
        self._download_file(lm_url, self.config.lang_file)
        self._download_file(dic_url, self.config.dic_file)

    def save_language_hash(self):
        self.hasher['language'] = self.new_hash
        self.hasher.store()

    def _download_file(self, url, path):
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(path, 'wb') as (f):
                for chunk in r:
                    f.write(chunk)