# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/nielsen/api.py
# Compiled at: 2019-11-07 22:38:00
# Size of source mod 2**32: 7224 bytes
"""
chown, chmod, rename, and organize TV show files.
"""
import logging, re
from os import chmod, makedirs, name as os_name, path, rename
from shutil import chown
from nielsen.tv import get_episode_title
from nielsen.config import CONFIG

def get_file_info(filename):
    """Get information about an episode from its filename.
        Returns a dictionary with the following keys:
                - series: Series name
                - season: Season number
                - episode: Episode number
                - title: Episode title (if found/enabled)
                - extension: File extension
        Filename variants:
                The.Flash.2014.217.Flash.Back.HDTV.x264-LOL[ettv].mp4
                The.Glades.S02E01.Family.Matters.HDTV.XviD-FQM.avi
                the.glades.201.family.matters.hdtv.xvid-fqm.avi
                The Glades -02.01- Family Matters.avi
                The Glades -201- Family Matters.avi
                Bones.S04E01E02.720p.HDTV.X264-DIMENSION.mkv
        """
    patterns = [
     re.compile('(?P<series>.+)\\.+(?P<year>\\d{4})\\.(?P<season>\\d{1,2})(?P<episode>\\d{2})\\.*(?P<title>.*)?\\.+(?P<extension>\\w+)$', re.IGNORECASE),
     re.compile('(?P<series>.+)\\.+S(?P<season>\\d{2})\\.?E(?P<episode>\\d{2})\\.*(?P<title>.*)?\\.+(?P<extension>\\w+)$', re.IGNORECASE),
     re.compile('(?P<series>.+)\\.+S?(?P<season>\\d{1,})\\.?E?(?P<episode>\\d{2,})\\.*(?P<title>.*)?\\.+(?P<extension>\\w+)$', re.IGNORECASE),
     re.compile('(?P<series>.+)\\s+-(?P<season>\\d{2})\\.(?P<episode>\\d{2})-\\s*(?P<title>.*)\\.(?P<extension>.+)$'),
     re.compile('(?P<series>.+)\\s+-(?P<season>\\d{1,2})(?P<episode>\\d{2,})-\\s*(?P<title>.*)\\.(?P<extension>.+)$'),
     re.compile('(?P<series>.+)S(?P<season>\\d{1,2})E(?P<episode>\\d{2,}).*\\.(?P<extension>.+)$')]
    tags = re.compile('(1080p|720p|HDTV|WEB|PROPER|REPACK|RERIP).*', re.IGNORECASE)
    for pattern in patterns:
        match = pattern.match(path.basename(filename))
        if match:
            info = match.groupdict(default='')
            info['series'] = info['series'].replace('.', ' ').strip()
            info['season'] = info['season'].strip().zfill(2)
            info['episode'] = info['episode'].strip()
            info['extension'] = info['extension'].strip()
            info['title'] = info.get('title', '').replace('.', ' ').strip()
            info['series'] = filter_series(info['series'])
            info['title'] = re.sub(tags, '', info['title']).strip()
            if info['title'].islower():
                info['title'] = info['title'].title()
            else:
                if not info['title']:
                    if CONFIG.getboolean('Options', 'FetchTitles'):
                        info['title'] = get_episode_title((info['season']),
                          (info['episode']), series=(info['series']))
                if info['title'].lower().startswith('e'):
                    if info['title'][1:3].isnumeric():
                        if int(info['title'][1:3]) == int(info['episode']) + 1:
                            info['episode'] += '-' + info['title'][1:3]
                            info['title'] = info['title'][3:].strip()
                logging.debug("Series: '%s'", info['series'])
                logging.debug("Season: '%s'", info['season'])
                logging.debug("Episode: '%s'", info['episode'])
                logging.debug("Title: '%s'", info['title'])
                logging.debug("Extension: '%s'", info['extension'])
                return info

    logging.info('%s did not match any pattern, skipping.', filename)


def organize_file(filename, series, season):
    """Move files to <MediaPath>/<Series>/Season <Season>."""
    if CONFIG.get('Options', 'MediaPath'):
        new_path = path.join(CONFIG.get('Options', 'MediaPath'), series, 'Season {0}'.format(season))
        logging.debug('Creating and/or moving to: %s', new_path)
        makedirs(new_path, exist_ok=True)
        dst = path.join(new_path, path.basename(filename))
        if path.isfile(dst):
            logging.warning('%s already exists. File will not be moved.', dst)
        else:
            try:
                rename(filename, dst)
                logging.info('Moved to %s', dst)
            except OSError as err:
                try:
                    logging.error(err)
                finally:
                    err = None
                    del err

            return new_path
    logging.error('No MediaPath defined.')
    return


def filter_series(series):
    """Check series name against list and replace with preferred name.
        Use the key/value pairs in the [Filters] section of the config file.
        Match the series name against the left hand side (ignoring case) and
        replace it with the right hand side.
                Castle (2009) = Castle
                Game Of Thrones = Game of Thrones
                Its Always Sunny In Philadelphia = It's Always Sunny in Philadelphia
                Marvel's Agents of S.H.I.E.L.D. = Agents of S.H.I.E.L.D.
                Mr Robot = Mr. Robot
        """
    if CONFIG.has_option('Filters', series):
        return CONFIG.get('Filters', series)
    if series.islower():
        return series.title()
    return series


def process_file(filename):
    """Set ownership and permissions for files, then rename."""
    if path.exists(filename):
        logging.info("Processing '%s'", filename)
    else:
        logging.info("File not found '%s'", filename)
        return
        if os_name == 'posix':
            if CONFIG.get('Options', 'User') or CONFIG.get('Options', 'Group'):
                try:
                    chown(filename, CONFIG.get('Options', 'User') or None, CONFIG.get('Options', 'Group') or None)
                except PermissionError as err:
                    try:
                        logging.error('chown failed. %s', err)
                    finally:
                        err = None
                        del err

        elif CONFIG.get('Options', 'Mode'):
            try:
                chmod(filename, int(CONFIG.get('Options', 'Mode'), 8))
            except PermissionError as err:
                try:
                    logging.error('chmod failed. %s', err)
                finally:
                    err = None
                    del err

            info = get_file_info(filename)
            if info:
                clean = ('{series} -{season}.{episode}- {title}.{extension}'.format)(**info)
                logging.info("Rename to: '%s'", clean)
                parent = path.dirname(filename)
                clean = path.join(parent, clean)
                if CONFIG.getboolean('Options', 'DryRun'):
                    print(filename + ' → ' + clean)
                    return
                if path.isfile(clean):
                    logging.warning('%s already exists. File will not be renamed.', clean)
        else:
            rename(filename, clean)
        if CONFIG.getboolean('Options', 'OrganizeFiles'):
            organize_file(clean, info['series'], info['season'])


def filter_filename(filename):
    """Replace invalid characters in a filename with hyphens. The set of
        invalid characters is determined by the operating system."""
    if os_name == 'posix':
        invalid_chars = re.compile('[/\x00]')
    else:
        if os_name == 'nt':
            invalid_chars = re.compile('[/\\?%*:|"<>]')
        else:
            logging.warning('OS not recognized: %s', os_name)
            return filename
    return re.sub(invalid_chars, '-', filename)