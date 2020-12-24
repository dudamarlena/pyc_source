# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/springheel/gentrans.py
# Compiled at: 2019-12-29 20:35:50
# Size of source mod 2**32: 2462 bytes
import json

def generateTranslations(lang, strings_path):
    """
    Get language strings from the translation file.

    Parameters
    ----------
    lang : str
        The site language.
    strings_path : str
        The path to the strings.json translation file.
    Returns
    -------
    strings : dict
        All sorts of UI strings in the site language. Sub-dict
        "language_names" has language code-name mappings.
    """
    with open(strings_path, 'r', encoding='utf-8') as (f):
        json_data = json.load(f)
    strings = {}
    string_names = [
     'home_s', 'char_s', 'caption_s', 'transcript_s', 'archive_s', 'tags_s', 'extra_s', 'store_s', 'chapter_s', 'first_s', 'prev_s', 'next_s', 'last_s', 'firsts_s', 'prevs_s', 'nexts_s', 'lasts_s', 'golatest_s', 'gofirst_s', 'goarchive_s', 'complete_s', 'inprogress_s', 'hiatus_s', 'statline_s', 'ccpdw', 'cc', 'no_comment', 'no_transcript', 'rss_s', 'h1_s', 'stylesheet_name_s', 'skip_s', 'page_s', 'meta_s', 'generator_s', 'archive_l_s', 'page_alt_s', 'image_s']
    for i in string_names:
        try:
            translated_value = json_data[i][lang]
            strings[i] = translated_value
        except KeyError:
            default_value = json_data[i]['en']
            strings[i] = default_value

    else:
        strings['language_names'] = json_data['language_names']
        return strings