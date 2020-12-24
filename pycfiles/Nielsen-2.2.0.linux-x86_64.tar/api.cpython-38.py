# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.8/site-packages/nielsen/api.py
# Compiled at: 2020-05-04 23:52:25
# Size of source mod 2**32: 7316 bytes
"""
chown, chmod, rename, and organize TV show files.
"""
import logging, re, pathlib
from os import name as os_name
import nielsen.files
from nielsen.tv import get_episode_title
from nielsen.config import CONFIG

def get_file_info(file):
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
    if not isinstance(file, pathlib.Path):
        file = pathlib.PurePath(file)
    patterns = [
     re.compile('(?P<series>.+)\\.+(?P<year>\\d{4})\\.(?P<season>\\d{1,2})(?P<episode>\\d{2})\\.*(?P<title>.*)?\\.+(?P<extension>\\w+)$', re.IGNORECASE),
     re.compile('(?P<series>.+)\\.+S(?P<season>\\d{2})\\.?E(?P<episode>\\d{2})\\.*(?P<title>.*)?\\.+(?P<extension>\\w+)$', re.IGNORECASE),
     re.compile('(?P<series>.+)\\.+S?(?P<season>\\d{1,})\\.?E?(?P<episode>\\d{2,})\\.*(?P<title>.*)?\\.+(?P<extension>\\w+)$', re.IGNORECASE),
     re.compile('(?P<series>.+)\\s+-(?P<season>\\d{2})\\.(?P<episode>\\d{2})-\\s*(?P<title>.*)\\.(?P<extension>.+)$'),
     re.compile('(?P<series>.+)\\s+-(?P<season>\\d{1,2})(?P<episode>\\d{2,})-\\s*(?P<title>.*)\\.(?P<extension>.+)$'),
     re.compile('(?P<series>.+)S(?P<season>\\d{1,2})E(?P<episode>\\d{2,}).*\\.(?P<extension>.+)$')]
    tags = re.compile('(1080p|720p|HDTV|WEB|PROPER|REPACK|RERIP).*', re.IGNORECASE)
    for pattern in patterns:
        match = pattern.match(file.name)
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
        logging.info('%s did not match any pattern, skipping.', file)


def organize_file(filename, series, season):
    """Move files to <MediaPath>/<Series>/Season <Season>. Returns a Path
        object representing the new location, or None on failure."""
    if not CONFIG.has_option('Options', 'MediaPath'):
        logging.error('No MediaPath defined.')
        return None
    mediapath = pathlib.PurePath(CONFIG.get('Options', 'MediaPath'))
    src = pathlib.Path(filename)
    dst = pathlib.Path(mediapath / series / f"Season {season}" / src.name)
    nielsen.files.create_hierarchy(dst)
    nielsen.files.move(src, dst)
    return dst


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
        If no filter is found, return the original string in title case.
        """
    return CONFIG.get('Filters', series, fallback=(series.title()))


def process_file(filename):
    """Set ownership and permissions for files, then rename, and optionally
        organize."""
    file = pathlib.Path(filename)
    if file.exists():
        logging.info("Processing '%s'", filename)
    else:
        logging.info("File not found '%s'", filename)
        return file
        if isinstance(file, pathlib.PosixPath):
            nielsen.files.set_file_ownership(file)
            nielsen.files.set_file_mode(file)
        info = get_file_info(file)
        if info:
            form = CONFIG.get('Options', 'Format')
            name = sanitize_filename((form.format)(**info))
            logging.info("Rename to: '%s'", name)
            clean = pathlib.PurePath(file.parent / name)
            if CONFIG.getboolean('Options', 'DryRun'):
                print(f"{file} → {clean}")
                return file
            elif file == clean:
                logging.warning('%s already exists. File will not be renamed.', clean)
            else:
                file = file.rename(clean)
            if CONFIG.getboolean('Options', 'OrganizeFiles'):
                file = organize_file(file, info['series'], info['season'])
        return file


def sanitize_filename(filename, system_type=os_name):
    """Replace characters which are invalid for a file basename in the string
        `filename` with hyphens. The set of invalid characters is determined by the
        operating system. For example, an episode title of `AC/DC` would cause the
        operating system to treat everything before the forward-slash as another
        directory. This function returns the same string as provided, but with an
        episode title token of `AC-DC`."""
    if system_type == 'posix':
        invalid_chars = re.compile('[/\x00]')
    else:
        if system_type == 'nt':
            invalid_chars = re.compile('[/\\?%*:|"<>]')
        else:
            logging.warning('OS not recognized: %s', os_name)
            return filename
    return re.sub(invalid_chars, '-', filename)