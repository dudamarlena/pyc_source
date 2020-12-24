# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/phishdetect/phishdetect-admin/phishdetectadmin/config.py
# Compiled at: 2020-01-02 10:05:19
# Size of source mod 2**32: 1847 bytes
import os, yaml
storage_folder = os.path.join(os.getenv('HOME'), '.config', 'phishdetect')
config_path = os.path.join(storage_folder, 'config')
archived_events_path = os.path.join(storage_folder, 'events')

def load_config():
    if not os.path.exists(config_path):
        return
    with open(config_path, 'r') as (handle):
        return yaml.load(handle)


def save_config(config):
    with open(config_path, 'w') as (handle):
        yaml.dump(config, handle, default_flow_style=False)


def load_archived_events():
    archived_events = []
    if not os.path.exists(archived_events_path):
        return archived_events
    with open(archived_events_path, 'r') as (handle):
        for line in handle:
            line = line.strip()
            if line == '':
                continue
            archived_events.append(line)

    return archived_events


def archive_event(uuid):
    uuid = uuid.strip()
    archived_events = load_archived_events()
    if uuid in archived_events:
        return
    with open(archived_events_path, 'a') as (handle):
        handle.write('{}\n'.format(uuid))