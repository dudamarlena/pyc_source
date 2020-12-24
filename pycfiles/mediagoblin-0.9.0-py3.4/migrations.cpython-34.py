# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/media_types/video/migrations.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 3956 bytes
from mediagoblin.db.migration_tools import RegisterMigration, inspect_table
from sqlalchemy import MetaData, Column, Unicode
import json
MIGRATIONS = {}

@RegisterMigration(1, MIGRATIONS)
def add_orig_metadata_column(db_conn):
    metadata = MetaData(bind=db_conn.bind)
    vid_data = inspect_table(metadata, 'video__mediadata')
    col = Column('orig_metadata', Unicode, default=None, nullable=True)
    col.create(vid_data)
    db_conn.commit()


@RegisterMigration(2, MIGRATIONS)
def webm_640_to_webm_video(db):
    metadata = MetaData(bind=db.bind)
    file_keynames = inspect_table(metadata, 'core__file_keynames')
    for row in db.execute(file_keynames.select()):
        if row.name == 'webm_640':
            db.execute(file_keynames.update().where(file_keynames.c.id == row.id).values(name='webm_video'))
            continue

    db.commit()


@RegisterMigration(3, MIGRATIONS)
def change_metadata_format(db):
    """Change orig_metadata format for multi-stream a-v"""
    db_metadata = MetaData(bind=db.bind)
    vid_data = inspect_table(db_metadata, 'video__mediadata')
    for row in db.execute(vid_data.select()):
        if not row.orig_metadata:
            continue
        metadata = json.loads(row.orig_metadata)
        new_metadata = {'audio': [],  'video': [],  'common': {}}
        video_key_map = {'videoheight': 'height', 
         'videowidth': 'width', 
         'videorate': 'rate'}
        audio_key_map = {'audiochannels': 'channels'}
        common_key_map = {'videolength': 'length'}
        new_metadata['video'] = [
         dict((v, metadata.get(k)) for k, v in video_key_map.items() if metadata.get(k))]
        new_metadata['audio'] = [
         dict((v, metadata.get(k)) for k, v in audio_key_map.items() if metadata.get(k))]
        new_metadata['common'] = dict((v, metadata.get(k)) for k, v in common_key_map.items() if metadata.get(k))
        new_metadata['common']['tags'] = {'mimetype': metadata.get('mimetype')}
        if 'tags' in metadata:
            new_metadata['video'][0]['tags'] = {}
            new_metadata['audio'][0]['tags'] = {}
            tags = metadata['tags']
            video_keys = [
             'encoder', 'encoder-version', 'video-codec']
            audio_keys = ['audio-codec']
            for t, v in tags.items():
                if t in video_keys:
                    new_metadata['video'][0]['tags'][t] = tags[t]
                elif t in audio_keys:
                    new_metadata['audio'][0]['tags'][t] = tags[t]
                else:
                    new_metadata['common']['tags'][t] = tags[t]

        db.execute(vid_data.update().where(vid_data.c.media_entry == row.media_entry).values(orig_metadata=json.dumps(new_metadata)))

    db.commit()