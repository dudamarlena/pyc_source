# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/meya_cli/fs_events.py
# Compiled at: 2018-09-14 11:23:44
from __future__ import absolute_import
import os, time
from watchdog.events import FileSystemEventHandler
from meya_cli.delete_command import DeleteCommand
from meya_cli.meya_api import MeyaAPIException
from meya_cli.meya_config import MEYA_CONFIG_FILE, parse_meya_config
from meya_cli.upload_command import UploadCommand

class ScheduledCommand(object):

    def __init__(self, scheduled_time, command):
        self.scheduled_time = scheduled_time
        self.command = command

    def try_perform(self):
        if time.time() <= self.scheduled_time:
            try:
                self.command.perform()
            except MeyaAPIException as err:
                print err

            return True
        return False


class MeyaFileSystemEventHandler(FileSystemEventHandler):

    def __init__(self, config):
        self.config = config
        self.scheduled_commands = {}

    def defer(self, path, command):
        self.scheduled_commands[path] = ScheduledCommand(time.time() + self.config.watch_command_delay, command)

    def on_deleted(self, event):
        if event.is_directory:
            return
        if self.config.should_ignore_path(event.src_path):
            return
        if not self.config.path_matches_autosync_patterns(event.src_path):
            return
        self.defer(event.src_path, DeleteCommand(self.config, [event.src_path]))

    def on_created(self, event):
        if event.is_directory:
            return
        self._on_file_update(event)

    def on_modified(self, event):
        if event.is_directory:
            return
        self._on_file_update(event)

    def _on_file_update(self, event):
        if os.path.basename(event.src_path) == MEYA_CONFIG_FILE:
            self._update_conf()
        if self.config.path_matches_autosync_patterns(event.src_path):
            self.defer(event.src_path, UploadCommand(self.config, [event.src_path]))

    def _update_conf(self):
        conf_file = os.path.join(self.config.root_dir, MEYA_CONFIG_FILE)
        print 'RELOADING MEYA CONFIG AT ' + conf_file
        self.config = parse_meya_config(self.config.root_dir, conf_file)

    def on_moved(self, event):
        if event.is_directory:
            return
        if os.path.basename(event.dest_path) == MEYA_CONFIG_FILE:
            self._update_conf()
        if self.config.path_matches_autosync_patterns(event.src_path) and not self.config.should_ignore_path(event.src_path):
            self.defer(event.src_path, DeleteCommand(self.config, [event.src_path]))
        if self.config.path_matches_autosync_patterns(event.dest_path):
            self.defer(event.dest_path, UploadCommand(self.config, [event.dest_path]))

    def step(self, time_step):
        time.sleep(time_step)
        for path in list(self.scheduled_commands.keys()):
            if self.scheduled_commands[path].try_perform():
                del self.scheduled_commands[path]