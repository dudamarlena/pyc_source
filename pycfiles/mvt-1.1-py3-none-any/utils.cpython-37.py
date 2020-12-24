# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nex/projects/mvt/mvt/utils.py
# Compiled at: 2020-02-21 13:21:56
# Size of source mod 2**32: 3760 bytes
import re, datetime, hashlib
from tld import get_tld

def convert_mactime_to_unix(timestamp):
    """Converts Mac Standard Time to a Unix timestamp.
    :param timestamp: MacTime timestamp (either int or float)
    :returns: Unix epoch timestamp
    """
    if type(timestamp) == int:
        if len(str(timestamp)) == 18:
            timestamp = int(str(timestamp)[:9])
    new_epoch = timestamp + 978307200
    try:
        return datetime.datetime.fromtimestamp(new_epoch)
    except:
        return


def convert_timestamp_to_iso(timestamp):
    """Converts Unix timestamp to ISO string.
    :param timestamp: Unix timestamp
    :returns: ISO timestamp string in YYYY-mm-dd HH:MM:SS.ms format
    """
    try:
        return timestamp.strftime('%Y-%m-%d %H:%M:%S.%f')
    except:
        return


def check_for_links(text):
    """Checks if a given text contains HTTP links.
    :param text: Any provided text
    :returns: Search results
    """
    return re.findall('(?P<url>https?://[^\\s]+)', text, re.IGNORECASE)


def get_domain_from_url(url):
    """Get the domain from a URL.
    :param url: URL to parse
    :returns: Just the domain name extracted from the URL
    """
    return get_tld(url, as_object=True, fix_protocol=True).parsed_url.netloc.lower().lstrip('www.')


def get_toplevel_from_url(url):
    """Get only the top level domain from a URL.
    :param url: URL to parse
    :returns: The top level domain extracted from the URL
    """
    return get_tld(url, as_object=True, fix_protocol=True).fld.lower()


def get_sha256_from_file_path(file_path):
    """Calculate the SHA256 hash of a file from a file path.
    :param file_path: Path to the file to hash
    :returns: The SHA256 hash string
    """
    sha256_hash = hashlib.sha256()
    with open(file_path, 'rb') as (handle):
        for byte_block in iter(lambda : handle.read(4096), ''):
            sha256_hash.update(byte_block)

    return sha256_hash.hexdigest()


def keys_bytes_to_string(obj):
    """Convert object keys from bytes to string.
    :param obj: Object to convert from bytes to string.
    :returns: Converted object.
    """
    new_obj = {}
    if not isinstance(obj, dict):
        if isinstance(obj, (tuple, list, set)):
            value = [keys_bytes_to_string(x) for x in obj]
            return value
        return obj
    for key, value in obj.items():
        if isinstance(key, bytes):
            key = key.decode()
        elif isinstance(value, dict):
            value = keys_bytes_to_string(value)
        else:
            if isinstance(value, (tuple, list, set)):
                value = [keys_bytes_to_string(x) for x in value]
        new_obj[key] = value

    return new_obj