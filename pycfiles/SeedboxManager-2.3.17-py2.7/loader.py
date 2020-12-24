# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.cygwin-1.7.35-i686/egg/seedbox/torrent/loader.py
# Compiled at: 2015-06-17 00:29:03
"""Loads torrents into database.

Torrent loader handles searches the directory where torrent files are stored
and adds them to the database cache if not already found.
"""
import glob, logging, os
from oslo_config import cfg
from seedbox.common import tools
from seedbox import constants
from seedbox.db import models
from seedbox.torrent import parser
LOG = logging.getLogger(__name__)
cfg.CONF.import_group('torrent', 'seedbox.options')
COMPRESSED_TYPES = tools.format_file_ext(cfg.CONF.torrent.compressed_filetypes)
VIDEO_TYPES = tools.format_file_ext(cfg.CONF.torrent.video_filetypes)

def load_torrents(dbapi):
    """Loads torrents into database.

    Find all the torrents in the specified directory, verify it is a valid
    torrent file (via parsing) and capture the relevant details. Next create
    a record in the cache for each torrent.
    """
    for torrent_file in glob.glob(os.path.join(cfg.CONF.torrent.torrent_path, '*.torrent')):
        torrent = dbapi.fetch_or_create_torrent(os.path.basename(torrent_file))
        if _is_parsing_required(torrent):
            try:
                torparser = parser.TorrentParser(torrent_file)
            except parser.ParsingError:
                torrent.invalid = True
                torrent.state = constants.CANCELLED
                dbapi.save_torrent(torrent)
                LOG.exception('Torrent Parsing Error: [%s]', torrent_file)
                continue

            media_items = torparser.get_file_details()
            LOG.debug('Total files in torrent %d', len(media_items))
            if _is_torrent_downloading(media_items):
                LOG.debug('torrent still downloading, next...')
                continue
            dbapi.bulk_create_medias(_filter_media(torrent.torrent_id, media_items))


def _is_parsing_required(torrent):
    """Determines if parsing is required.

    Checks the following attributes to determine if parsing is needed:
    - if torrent.invalid is True, skip parsing
    - if torrent.purged is True, skip parsing
    - if len(torrent.media_files) > 0, skip parsing
    """
    parse = True
    if torrent.invalid:
        parse = False
    if torrent.purged:
        parse = False
    if torrent.media_files:
        parse = False
    return parse


def _is_torrent_downloading(media_items):
    """Checks if torrent is still in progress.

    Verify if at least one item still located in the
    inprogress/downloading location

    args:
        media_items: files found inside a torrent
    returns:
        true: if any file is still within incomplete_path
        false: if no file is within incomplete_path
    """
    found = False
    for filename, filesize in media_items:
        if os.path.exists(os.path.join(cfg.CONF.torrent.incomplete_path, filename)):
            found = True
            break

    return found


def _filter_media(torrent_id, media_items):
    """Applies logic to determine if valid media file.

    Handles interacting with torrent parser and getting required details
    from the parser.

    args:
        torrent: includes access to torrent and its location
    """
    file_list = []
    for filename, filesize in media_items:
        media = models.MediaFile.make_empty()
        media.torrent_id = torrent_id
        media.filename = filename
        media.size = filesize
        in_ext = os.path.splitext(filename)[1]
        media.file_ext = in_ext
        media.file_path = None
        media.compressed = False
        media.synced = False
        if in_ext in COMPRESSED_TYPES:
            media.compressed = True
            LOG.debug('found compressed file: %s', filename)
        elif in_ext in VIDEO_TYPES:
            if filesize < cfg.CONF.torrent.minimum_file_size:
                LOG.debug('Based on size, this is a sample file [%s]. Skipping..', filename)
                continue
            else:
                LOG.debug('found video file: %s', filename)
        else:
            LOG.debug('Unsupported filetype (%s); skipping file', in_ext)
            continue
        media.file_path, media.filename = _get_file_path(filename)
        if media.file_path is None:
            LOG.info('Media file [%s] not found', filename)
            continue
        file_list.append(media)
        LOG.debug('Added file to torrent with details: [%s]', media)

    return file_list


def _get_file_path(filename):
    """A list of locations/paths/directories where the media file could exist.

    return:
        location if found
        None if not found
    """
    found_path = None
    found_file = None
    for location in cfg.CONF.torrent.media_paths:
        full_path = os.path.join(location, filename)
        if os.path.exists(full_path):
            found_path, found_file = os.path.split(full_path)
            break

    return (
     found_path, found_file)