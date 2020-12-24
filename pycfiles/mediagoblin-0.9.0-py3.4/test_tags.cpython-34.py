# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tests/test_tags.py
# Compiled at: 2016-03-29 15:18:42
# Size of source mod 2**32: 2283 bytes
from mediagoblin.tools import text

def test_list_of_dicts_conversion(test_app):
    """
    When the user adds tags to a media entry, the string from the form is
    converted into a list of tags, where each tag is stored in the database
    as a dict. Each tag dict should contain the tag's name and slug. Another
    function performs the reverse operation when populating a form to edit tags.
    """
    assert text.convert_to_tag_list_of_dicts('sleep , 6    AM, chainsaw! ') == [{'name': 'sleep',  'slug': 'sleep'}, {'name': '6 AM',  'slug': '6-am'}, {'name': 'chainsaw!',  'slug': 'chainsaw'}]
    assert text.convert_to_tag_list_of_dicts('echo,echo') == [
     {'name': 'echo',  'slug': 'echo'}]
    assert text.convert_to_tag_list_of_dicts('echo,#echo') == [
     {'name': '#echo',  'slug': 'echo'}]
    assert text.media_tags_as_string([{'name': 'yin',  'slug': 'yin'}, {'name': 'yang',  'slug': 'yang'}]) == 'yin, yang'