# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kayleevc/kaylee.py
# Compiled at: 2016-02-16 13:13:48
# Size of source mod 2**32: 7143 bytes
import sys, signal, os.path, subprocess
from gi.repository import GObject, GLib
from kayleevc.recognizer import Recognizer
from kayleevc.util import *
from kayleevc.numbers import NumberParser

class Kaylee:

    def __init__(self):
        self.ui = None
        self.options = {}
        ui_continuous_listen = False
        self.continuous_listen = False
        self.config = Config()
        self.options = vars(self.config.options)
        self.commands = self.options['commands']
        self.number_parser = NumberParser()
        self.hasher = Hasher(self.config)
        self.update_voice_commands_if_changed()
        if self.options['interface']:
            if self.options['interface'] == 'g':
                from kayleevc.gui import GTKInterface as UI
        else:
            if self.options['interface'] == 'gt':
                from kayleevc.gui import GTKTrayInterface as UI
            else:
                print('no GUI defined')
                sys.exit()
        self.ui = UI(self.options, self.options['continuous'])
        self.ui.connect('command', self.process_command)
        icon = self.load_resource('icon.png')
        if icon:
            self.ui.set_icon_active_asset(icon)
        icon_inactive = self.load_resource('icon_inactive.png')
        if icon_inactive:
            self.ui.set_icon_inactive_asset(icon_inactive)
        if self.options['history']:
            self.history = []
        self.language_updater = LanguageUpdater(self.config)
        self.language_updater.update_language_if_changed()
        self.recognizer = Recognizer(self.config)
        self.recognizer.connect('finished', self.recognizer_finished)

    def update_voice_commands_if_changed(self):
        """Use hashes to test if the voice commands have changed"""
        stored_hash = self.hasher['voice_commands']
        hasher = self.hasher.get_hash_object()
        for voice_cmd in self.commands.keys():
            hasher.update(voice_cmd.encode('utf-8'))
            hasher.update('\n'.encode('utf-8'))

        new_hash = hasher.hexdigest()
        if new_hash != stored_hash:
            self.create_strings_file()
            self.hasher['voice_commands'] = new_hash
            self.hasher.store()

    def create_strings_file(self):
        with open(self.config.strings_file, 'w') as (strings):
            for voice_cmd in sorted(self.commands.keys()):
                strings.write(voice_cmd.strip().replace('%d', '') + '\n')

            for word in self.number_parser.number_words:
                strings.write(word + '\n')

    def log_history(self, text):
        if self.options['history']:
            self.history.append(text)
            if len(self.history) > self.options['history']:
                self.history.pop(0)
            with open(self.config.history_file, 'w') as (hfile):
                for line in self.history:
                    hfile.write(line + '\n')

    def run_command(self, cmd):
        """Print the command, then run it"""
        print(cmd)
        subprocess.call(cmd, shell=True)

    def recognizer_finished(self, recognizer, text):
        t = text.lower()
        numt, nums = self.number_parser.parse_all_numbers(t)
        if t in self.commands:
            if self.options['valid_sentence_command']:
                subprocess.call(self.options['valid_sentence_command'], shell=True)
            cmd = self.commands[t]
            if self.options['pass_words']:
                cmd += ' ' + t
            self.run_command(cmd)
            self.log_history(text)
        else:
            if numt in self.commands:
                if self.options['valid_sentence_command']:
                    subprocess.call(self.options['valid_sentence_command'], shell=True)
                cmd = self.commands[numt]
                cmd = cmd.format(*nums)
                if self.options['pass_words']:
                    cmd += ' ' + t
                self.run_command(cmd)
                self.log_history(text)
            else:
                if self.options['invalid_sentence_command']:
                    subprocess.call(self.options['invalid_sentence_command'], shell=True)
                print('no matching command {0}'.format(t))
        if self.ui:
            if not self.continuous_listen:
                self.recognizer.pause()
            self.ui.finished(t)

    def run(self):
        if self.ui:
            self.ui.run()
        else:
            self.recognizer.listen()

    def quit(self):
        sys.exit()

    def process_command(self, UI, command):
        print(command)
        if command == 'listen':
            self.recognizer.listen()
        else:
            if command == 'stop':
                self.recognizer.pause()
            else:
                if command == 'continuous_listen':
                    self.continuous_listen = True
                    self.recognizer.listen()
                else:
                    if command == 'continuous_stop':
                        self.continuous_listen = False
                        self.recognizer.pause()
                    elif command == 'quit':
                        self.quit()

    def load_resource(self, string):
        local_data = os.path.join(os.path.dirname(__file__), '..', 'data')
        paths = ['/usr/share/kaylee/', '/usr/local/share/kaylee', local_data]
        for path in paths:
            resource = os.path.join(path, string)
            if os.path.exists(resource):
                return resource

        return False


def run():
    kaylee = Kaylee()
    GObject.threads_init()
    main_loop = GObject.MainLoop()
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    kaylee.run()
    try:
        main_loop.run()
    except:
        print('time to quit')
        main_loop.quit()
        sys.exit()