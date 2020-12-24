# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/charman/src/concrete-python/tests/test_twitter.py
# Compiled at: 2018-02-27 16:09:54
# Size of source mod 2**32: 12522 bytes
from __future__ import unicode_literals
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar, json
from pytest import fixture, mark
from concrete.util import json_tweet_object_to_Communication, twitter_lid_to_iso639_3
TWEET_TXT = 'Barber tells me - his son is colorblind / my hair is auburn / and auburn is a shade of green'
TWEET_ID = 238426131689242624
TWEET_ID_STR = '238426131689242624'
RT_TWEET_TXT = 'Barber tells me'
RT_TWEET_ID = 238426131689242623
RT_TWEET_ID_STR = '238426131689242623'
REPLY_TWEET_ID = 238426131689242622
REPLY_TWEET_ID_STR = '238426131689242622'

@fixture
def tweet():
    return {'text': TWEET_TXT, 
     'id_str': TWEET_ID_STR, 
     'id': TWEET_ID, 
     'created_at': 'Wed Aug 27 13:08:45 +0000 2008', 
     'user': {'screen_name': 'charman', 
              'name': 'C Harman', 
              'lang': 'ja', 
              'verified': False, 
              'id': 1234, 
              'id_str': '1234', 
              'geo_enabled': True, 
              'created_at': 'Wed Aug 27 13:08:05 +0000 2008', 
              'friends_count': 37, 
              'statuses_count': 38, 
              'listed_count': 39, 
              'favourites_count': 41, 
              'followers_count': 42, 
              'location': 'San Francisco, CA', 
              'time_zone': 'Pacific Time (US & Canada)', 
              'description': 'The Real Twitter API.', 
              'url': 'http://dev.twitter.com', 
              'utc_offset': -18000}, 
     
     'entities': {'hashtags': [
                               {'indices': [32, 36], 
                                'text': 'lol'}], 
                  
                  'user_mentions': [
                                    {'name': 'Twitter API', 
                                     'indices': [4, 15], 
                                     'screen_name': 'twitterapi', 
                                     'id': 6253282, 
                                     'id_str': '6253282'}], 
                  
                  'urls': [
                           {'indices': [32, 52], 
                            'url': 'http://t.co/IOwBrTZR', 
                            'display_url': 'youtube.com/watch?v=oHg5SJ…', 
                            'expanded_url': 'http://www.youtube.com/watch?v=oHg5SJYRHA0'}]}, 
     
     'coordinates': {'coordinates': [-75.5, 40.25], 
                     'type': 'Point'}, 
     
     'place': {'attributes': {'street_address': '795 Folsom St', 
                              'region': 'Mid Atlantic', 
                              'locality': 'Washington, DC'}, 
               
               'bounding_box': {'coordinates': [
                                                [[-77.25, 38.5],
                                                 [
                                                  -76.0, 38.5],
                                                 [
                                                  -76.0, 38.125],
                                                 [
                                                  -77.25, 38.125]]], 
                                
                                'type': 'Polygon'}, 
               
               'country': 'United States', 
               'country_code': 'US', 
               'full_name': 'Washington, DC', 
               'id': '01fbe706f872cb32', 
               'name': 'Washington', 
               'place_type': 'city', 
               'url': 'http://api.twitter.com/1/geo/id/01fbe706f872cb32.json'}, 
     
     'retweeted_status': {'text': RT_TWEET_TXT, 
                          'id_str': RT_TWEET_ID_STR, 
                          'id': RT_TWEET_ID, 
                          'created_at': 'Wed Aug 27 13:08:44 +0000 2008', 
                          'user': {'screen_name': 'charman2', 
                                   'name': 'C Harman 2', 
                                   'lang': 'ja', 
                                   'verified': False, 
                                   'id': 1235, 
                                   'id_str': '1235'}, 
                          
                          'entities': {'hashtags': [], 
                                       'user_mentions': [], 
                                       'urls': []}}, 
     
     'in_reply_to_status_id': REPLY_TWEET_ID, 
     'in_reply_to_status_id_str': REPLY_TWEET_ID_STR, 
     'in_reply_to_screen_name': 'charman3', 
     'in_reply_to_user_id': 1236, 
     'in_reply_to_user_id_str': '1236', 
     'retweeted': False, 
     'retweet_count': 1585, 
     'truncated': True, 
     'source': '<a href="http://itunes.apple.com/us/app/twitter/id409789998?mt=12" >Twitter for Mac</a>', 
     'lang': 'en'}


def test_twitter_lid_conversion():
    @py_assert0 = 'eng'
    @py_assert4 = 'en-gb'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'msa'
    @py_assert4 = 'msa'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'hun'
    @py_assert4 = 'hu'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'zho'
    @py_assert4 = 'zh-cn'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'zho'
    @py_assert4 = 'zh-tw'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'und'
    @py_assert4 = 'und'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'eng'
    @py_assert4 = 'eng'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'xxx'
    @py_assert4 = 'xxx'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'und'
    @py_assert4 = 'xx'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'ind'
    @py_assert4 = 'in'
    @py_assert6 = twitter_lid_to_iso639_3(@py_assert4)
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==', ), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py3)s(%(py5)s)\n}', ), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(twitter_lid_to_iso639_3) if 'twitter_lid_to_iso639_3' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(twitter_lid_to_iso639_3) else 'twitter_lid_to_iso639_3', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = 'assert %(py9)s' % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None


@mark.parametrize('omitted_fields,omitted_assertions', [((), ()),
 (('lang',), ('lid',)),
 (('coordinates',), ('coordinates',)),
 (('place',), ('place',)),
 (('retweeted_status',), ('retweet',)),
 (('in_reply_to_status_id', 'in_reply_to_status_id_str', 'in_reply_to_user_id', 'in_reply_to_user_id_str', 'in_reply_to_screen_name'),
 ('reply',))])
def test_json_tweet_object_to_Communication(tweet, omitted_fields, omitted_assertions):
    for field in omitted_fields:
        del tweet[field]

    comm = json_tweet_object_to_Communication(tweet)
    tweet_info = comm.communicationMetadata.tweetInfo
    omitted_assertions = set(omitted_assertions)
    @py_assert3 = comm.id
    @py_assert1 = TWEET_ID_STR == @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.id\n}',), (TWEET_ID_STR, @py_assert3)) % {'py2': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(TWEET_ID_STR) if 'TWEET_ID_STR' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TWEET_ID_STR) else 'TWEET_ID_STR'}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = comm.text
    @py_assert1 = TWEET_TXT == @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.text\n}',), (TWEET_TXT, @py_assert3)) % {'py2': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(TWEET_TXT) if 'TWEET_TXT' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TWEET_TXT) else 'TWEET_TXT'}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = json.loads
    @py_assert6 = comm.originalText
    @py_assert8 = @py_assert3(@py_assert6)
    @py_assert1 = tweet == @py_assert8
    if not @py_assert1:
        @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py9)s\n{%(py9)s = %(py4)s\n{%(py4)s = %(py2)s.loads\n}(%(py7)s\n{%(py7)s = %(py5)s.originalText\n})\n}',), (tweet, @py_assert8)) % {'py2': @pytest_ar._saferepr(json) if 'json' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(json) else 'json', 'py0': @pytest_ar._saferepr(tweet) if 'tweet' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet) else 'tweet', 'py7': @pytest_ar._saferepr(@py_assert6), 'py4': @pytest_ar._saferepr(@py_assert3), 'py5': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py9': @pytest_ar._saferepr(@py_assert8)}
        @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
        raise AssertionError(@pytest_ar._format_explanation(@py_format12))
    @py_assert1 = @py_assert3 = @py_assert6 = @py_assert8 = None
    @py_assert0 = 1219842525
    @py_assert4 = comm.startTime
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.startTime\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 1219842525
    @py_assert4 = comm.endTime
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.endTime\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert3 = tweet_info.id
    @py_assert1 = TWEET_ID == @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.id\n}',), (TWEET_ID, @py_assert3)) % {'py2': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(TWEET_ID) if 'TWEET_ID' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TWEET_ID) else 'TWEET_ID'}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert3 = tweet_info.text
    @py_assert1 = TWEET_TXT == @py_assert3
    if not @py_assert1:
        @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.text\n}',), (TWEET_TXT, @py_assert3)) % {'py2': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(TWEET_TXT) if 'TWEET_TXT' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(TWEET_TXT) else 'TWEET_TXT'}
        @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
        raise AssertionError(@pytest_ar._format_explanation(@py_format7))
    @py_assert1 = @py_assert3 = None
    @py_assert0 = 'Wed Aug 27 13:08:45 +0000 2008'
    @py_assert4 = tweet_info.createdAt
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.createdAt\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = tweet_info.retweeted
    @py_assert4 = False
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.retweeted\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = 1585
    @py_assert4 = tweet_info.retweetCount
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.retweetCount\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert1 = tweet_info.truncated
    @py_assert4 = True
    @py_assert3 = @py_assert1 is @py_assert4
    if not @py_assert3:
        @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.truncated\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert1 = @py_assert3 = @py_assert4 = None
    @py_assert0 = '<a href="http://itunes.apple.com/us/app/twitter/id409789998?mt=12" >Twitter for Mac</a>'
    @py_assert4 = tweet_info.source
    @py_assert2 = @py_assert0 == @py_assert4
    if not @py_assert2:
        @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.source\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
        @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
        raise AssertionError(@pytest_ar._format_explanation(@py_format8))
    @py_assert0 = @py_assert2 = @py_assert4 = None
    @py_assert0 = 'jpn'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.lang
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.lang\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'charman'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.screenName
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.screenName\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'C Harman'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.name
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.name\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 1234
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.id
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.id\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert1 = tweet_info.user
    @py_assert3 = @py_assert1.geoEnabled
    @py_assert6 = True
    @py_assert5 = @py_assert3 is @py_assert6
    if not @py_assert5:
        @py_format8 = @pytest_ar._call_reprcompare(('is',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py2)s\n{%(py2)s = %(py0)s.user\n}.geoEnabled\n} is %(py7)s',), (@py_assert3, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py2': @pytest_ar._saferepr(@py_assert1), 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert1 = @py_assert3 = @py_assert5 = @py_assert6 = None
    @py_assert0 = 'Wed Aug 27 13:08:05 +0000 2008'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.createdAt
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.createdAt\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 37
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.friendsCount
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.friendsCount\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 38
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.statusesCount
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.statusesCount\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 39
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.listedCount
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.listedCount\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 41
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.favouritesCount
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.favouritesCount\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 42
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.followersCount
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.followersCount\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'San Francisco, CA'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.location
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.location\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'Pacific Time (US & Canada)'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.timeZone
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.timeZone\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'The Real Twitter API.'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.description
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.description\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 'http://dev.twitter.com'
    @py_assert4 = tweet_info.user
    @py_assert6 = @py_assert4.url
    @py_assert2 = @py_assert0 == @py_assert6
    if not @py_assert2:
        @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.user\n}.url\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
        @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
        raise AssertionError(@pytest_ar._format_explanation(@py_format10))
    @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    @py_assert0 = 18000
    @py_assert2 = -@py_assert0
    @py_assert5 = tweet_info.user
    @py_assert7 = @py_assert5.utcOffset
    @py_assert3 = @py_assert2 == @py_assert7
    if not @py_assert3:
        @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('-%(py1)s == %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.user\n}.utcOffset\n}',), (@py_assert2, @py_assert7)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5)}
        @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
        raise AssertionError(@pytest_ar._format_explanation(@py_format11))
    @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = None
    if 'retweet' in omitted_assertions:
        omitted_assertions.remove('retweet')
        @py_assert1 = tweet_info.retweetedStatusId
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.retweetedStatusId\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = tweet_info.retweetedUserId
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.retweetedUserId\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = tweet_info.retweetedScreenName
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.retweetedScreenName\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        @py_assert3 = tweet_info.retweetedStatusId
        @py_assert1 = RT_TWEET_ID == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.retweetedStatusId\n}',), (RT_TWEET_ID, @py_assert3)) % {'py2': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(RT_TWEET_ID) if 'RT_TWEET_ID' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(RT_TWEET_ID) else 'RT_TWEET_ID'}
            @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert0 = 1235
        @py_assert4 = tweet_info.retweetedUserId
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.retweetedUserId\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'charman2'
        @py_assert4 = tweet_info.retweetedScreenName
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.retweetedScreenName\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
    if 'reply' in omitted_assertions:
        omitted_assertions.remove('reply')
        @py_assert1 = tweet_info.inReplyToStatusId
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.inReplyToStatusId\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = tweet_info.inReplyToUserId
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.inReplyToUserId\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
        @py_assert1 = tweet_info.inReplyToScreenName
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.inReplyToScreenName\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        @py_assert3 = tweet_info.inReplyToStatusId
        @py_assert1 = REPLY_TWEET_ID == @py_assert3
        if not @py_assert1:
            @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert1,), ('%(py0)s == %(py4)s\n{%(py4)s = %(py2)s.inReplyToStatusId\n}',), (REPLY_TWEET_ID, @py_assert3)) % {'py2': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py4': @pytest_ar._saferepr(@py_assert3), 'py0': @pytest_ar._saferepr(REPLY_TWEET_ID) if 'REPLY_TWEET_ID' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(REPLY_TWEET_ID) else 'REPLY_TWEET_ID'}
            @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert1 = @py_assert3 = None
        @py_assert0 = 1236
        @py_assert4 = tweet_info.inReplyToUserId
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.inReplyToUserId\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
        @py_assert0 = 'charman3'
        @py_assert4 = tweet_info.inReplyToScreenName
        @py_assert2 = @py_assert0 == @py_assert4
        if not @py_assert2:
            @py_format6 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py5)s\n{%(py5)s = %(py3)s.inReplyToScreenName\n}',), (@py_assert0, @py_assert4)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert0 = @py_assert2 = @py_assert4 = None
    if 'entities' in omitted_assertions:
        omitted_assertions.remove('entities')
        @py_assert1 = tweet_info.entities
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.entities\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        @py_assert0 = 1
        @py_assert5 = tweet_info.entities
        @py_assert7 = @py_assert5.hashtagList
        @py_assert9 = len(@py_assert7)
        @py_assert2 = @py_assert0 == @py_assert9
        if not @py_assert2:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.entities\n}.hashtagList\n})\n}',), (@py_assert0, @py_assert9)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert0 = 'lol'
        @py_assert3 = tweet_info.entities.hashtagList[0]
        @py_assert5 = @py_assert3.text
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.text\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 32
        @py_assert3 = tweet_info.entities.hashtagList[0]
        @py_assert5 = @py_assert3.startOffset
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.startOffset\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 36
        @py_assert3 = tweet_info.entities.hashtagList[0]
        @py_assert5 = @py_assert3.endOffset
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.endOffset\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 1
        @py_assert5 = tweet_info.entities
        @py_assert7 = @py_assert5.userMentionList
        @py_assert9 = len(@py_assert7)
        @py_assert2 = @py_assert0 == @py_assert9
        if not @py_assert2:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.entities\n}.userMentionList\n})\n}',), (@py_assert0, @py_assert9)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert0 = 6253282
        @py_assert3 = tweet_info.entities.userMentionList[0]
        @py_assert5 = @py_assert3.id
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.id\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'Twitter API'
        @py_assert3 = tweet_info.entities.userMentionList[0]
        @py_assert5 = @py_assert3.name
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.name\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'twitterapi'
        @py_assert3 = tweet_info.entities.userMentionList[0]
        @py_assert5 = @py_assert3.screenName
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.screenName\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 4
        @py_assert3 = tweet_info.entities.userMentionList[0]
        @py_assert5 = @py_assert3.startOffset
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.startOffset\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 15
        @py_assert3 = tweet_info.entities.userMentionList[0]
        @py_assert5 = @py_assert3.endOffset
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.endOffset\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 1
        @py_assert5 = tweet_info.entities
        @py_assert7 = @py_assert5.urlList
        @py_assert9 = len(@py_assert7)
        @py_assert2 = @py_assert0 == @py_assert9
        if not @py_assert2:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py10)s\n{%(py10)s = %(py3)s(%(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.entities\n}.urlList\n})\n}',), (@py_assert0, @py_assert9)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py10': @pytest_ar._saferepr(@py_assert9), 'py8': @pytest_ar._saferepr(@py_assert7), 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert0 = 'http://t.co/IOwBrTZR'
        @py_assert3 = tweet_info.entities.urlList[0]
        @py_assert5 = @py_assert3.url
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.url\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'youtube.com/watch?v=oHg5SJ…'
        @py_assert3 = tweet_info.entities.urlList[0]
        @py_assert5 = @py_assert3.displayUrl
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.displayUrl\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'http://www.youtube.com/watch?v=oHg5SJYRHA0'
        @py_assert3 = tweet_info.entities.urlList[0]
        @py_assert5 = @py_assert3.expandedUrl
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.expandedUrl\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 32
        @py_assert3 = tweet_info.entities.urlList[0]
        @py_assert5 = @py_assert3.startOffset
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.startOffset\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 52
        @py_assert3 = tweet_info.entities.urlList[0]
        @py_assert5 = @py_assert3.endOffset
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.endOffset\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
    if 'coordinates' in omitted_assertions:
        omitted_assertions.remove('coordinates')
        @py_assert1 = tweet_info.coordinates
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.coordinates\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        @py_assert0 = 'Point'
        @py_assert4 = tweet_info.coordinates
        @py_assert6 = @py_assert4.type
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.coordinates\n}.type\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 75.5
        @py_assert2 = -@py_assert0
        @py_assert5 = tweet_info.coordinates
        @py_assert7 = @py_assert5.coordinates
        @py_assert9 = @py_assert7.longitude
        @py_assert3 = @py_assert2 == @py_assert9
        if not @py_assert3:
            @py_format11 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('-%(py1)s == %(py10)s\n{%(py10)s = %(py8)s\n{%(py8)s = %(py6)s\n{%(py6)s = %(py4)s.coordinates\n}.coordinates\n}.longitude\n}',), (@py_assert2, @py_assert9)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py10': @pytest_ar._saferepr(@py_assert9), 'py4': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format13 = ('' + 'assert %(py12)s') % {'py12': @py_format11}
            raise AssertionError(@pytest_ar._format_explanation(@py_format13))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = @py_assert7 = @py_assert9 = None
        @py_assert0 = 40.25
        @py_assert4 = tweet_info.coordinates
        @py_assert6 = @py_assert4.coordinates
        @py_assert8 = @py_assert6.latitude
        @py_assert2 = @py_assert0 == @py_assert8
        if not @py_assert2:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.coordinates\n}.coordinates\n}.latitude\n}',), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
    if 'place' in omitted_assertions:
        omitted_assertions.remove('place')
        @py_assert1 = tweet_info.place
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.place\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        @py_assert0 = 'Mid Atlantic'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.attributes
        @py_assert8 = @py_assert6.region
        @py_assert2 = @py_assert0 == @py_assert8
        if not @py_assert2:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.attributes\n}.region\n}',), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
        @py_assert0 = 'Washington, DC'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.attributes
        @py_assert8 = @py_assert6.locality
        @py_assert2 = @py_assert0 == @py_assert8
        if not @py_assert2:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.attributes\n}.locality\n}',), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
        @py_assert0 = '795 Folsom St'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.attributes
        @py_assert8 = @py_assert6.streetAddress
        @py_assert2 = @py_assert0 == @py_assert8
        if not @py_assert2:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.attributes\n}.streetAddress\n}',), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
        @py_assert0 = 'Polygon'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.boundingBox
        @py_assert8 = @py_assert6.type
        @py_assert2 = @py_assert0 == @py_assert8
        if not @py_assert2:
            @py_format10 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py9)s\n{%(py9)s = %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.boundingBox\n}.type\n}',), (@py_assert0, @py_assert8)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6), 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format12 = ('' + 'assert %(py11)s') % {'py11': @py_format10}
            raise AssertionError(@pytest_ar._format_explanation(@py_format12))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = @py_assert8 = None
        @py_assert0 = 77.25
        @py_assert2 = -@py_assert0
        @py_assert4 = tweet_info.place.boundingBox.coordinateList[0]
        @py_assert6 = @py_assert4.longitude
        @py_assert3 = @py_assert2 == @py_assert6
        if not @py_assert3:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('-%(py1)s == %(py7)s\n{%(py7)s = %(py5)s.longitude\n}',), (@py_assert2, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 38.5
        @py_assert3 = tweet_info.place.boundingBox.coordinateList[0]
        @py_assert5 = @py_assert3.latitude
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.latitude\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 76.0
        @py_assert2 = -@py_assert0
        @py_assert4 = tweet_info.place.boundingBox.coordinateList[1]
        @py_assert6 = @py_assert4.longitude
        @py_assert3 = @py_assert2 == @py_assert6
        if not @py_assert3:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('-%(py1)s == %(py7)s\n{%(py7)s = %(py5)s.longitude\n}',), (@py_assert2, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 38.5
        @py_assert3 = tweet_info.place.boundingBox.coordinateList[1]
        @py_assert5 = @py_assert3.latitude
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.latitude\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 76.0
        @py_assert2 = -@py_assert0
        @py_assert4 = tweet_info.place.boundingBox.coordinateList[2]
        @py_assert6 = @py_assert4.longitude
        @py_assert3 = @py_assert2 == @py_assert6
        if not @py_assert3:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('-%(py1)s == %(py7)s\n{%(py7)s = %(py5)s.longitude\n}',), (@py_assert2, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 38.125
        @py_assert3 = tweet_info.place.boundingBox.coordinateList[2]
        @py_assert5 = @py_assert3.latitude
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.latitude\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 77.25
        @py_assert2 = -@py_assert0
        @py_assert4 = tweet_info.place.boundingBox.coordinateList[3]
        @py_assert6 = @py_assert4.longitude
        @py_assert3 = @py_assert2 == @py_assert6
        if not @py_assert3:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert3,), ('-%(py1)s == %(py7)s\n{%(py7)s = %(py5)s.longitude\n}',), (@py_assert2, @py_assert6)) % {'py7': @pytest_ar._saferepr(@py_assert6), 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 38.125
        @py_assert3 = tweet_info.place.boundingBox.coordinateList[3]
        @py_assert5 = @py_assert3.latitude
        @py_assert2 = @py_assert0 == @py_assert5
        if not @py_assert2:
            @py_format7 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py6)s\n{%(py6)s = %(py4)s.latitude\n}',), (@py_assert0, @py_assert5)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format9 = ('' + 'assert %(py8)s') % {'py8': @py_format7}
            raise AssertionError(@pytest_ar._format_explanation(@py_format9))
        @py_assert0 = @py_assert2 = @py_assert3 = @py_assert5 = None
        @py_assert0 = 'United States'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.country
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.country\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'US'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.countryCode
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.countryCode\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'Washington, DC'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.fullName
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.fullName\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = '01fbe706f872cb32'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.id
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.id\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'Washington'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.name
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.name\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'city'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.placeType
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.placeType\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
        @py_assert0 = 'http://api.twitter.com/1/geo/id/01fbe706f872cb32.json'
        @py_assert4 = tweet_info.place
        @py_assert6 = @py_assert4.url
        @py_assert2 = @py_assert0 == @py_assert6
        if not @py_assert2:
            @py_format8 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py7)s\n{%(py7)s = %(py5)s\n{%(py5)s = %(py3)s.place\n}.url\n}',), (@py_assert0, @py_assert6)) % {'py3': @pytest_ar._saferepr(tweet_info) if 'tweet_info' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(tweet_info) else 'tweet_info', 'py1': @pytest_ar._saferepr(@py_assert0), 'py5': @pytest_ar._saferepr(@py_assert4), 'py7': @pytest_ar._saferepr(@py_assert6)}
            @py_format10 = ('' + 'assert %(py9)s') % {'py9': @py_format8}
            raise AssertionError(@pytest_ar._format_explanation(@py_format10))
        @py_assert0 = @py_assert2 = @py_assert4 = @py_assert6 = None
    if 'lid' in omitted_assertions:
        omitted_assertions.remove('lid')
        @py_assert1 = comm.lidList
        @py_assert4 = None
        @py_assert3 = @py_assert1 is @py_assert4
        if not @py_assert3:
            @py_format6 = @pytest_ar._call_reprcompare(('is',), (@py_assert3,), ('%(py2)s\n{%(py2)s = %(py0)s.lidList\n} is %(py5)s',), (@py_assert1, @py_assert4)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py5': @pytest_ar._saferepr(@py_assert4), 'py0': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm'}
            @py_format8 = ('' + 'assert %(py7)s') % {'py7': @py_format6}
            raise AssertionError(@pytest_ar._format_explanation(@py_format8))
        @py_assert1 = @py_assert3 = @py_assert4 = None
    else:
        @py_assert0 = 1
        @py_assert5 = comm.lidList
        @py_assert7 = len(@py_assert5)
        @py_assert2 = @py_assert0 == @py_assert7
        if not @py_assert2:
            @py_format9 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py8)s\n{%(py8)s = %(py3)s(%(py6)s\n{%(py6)s = %(py4)s.lidList\n})\n}',), (@py_assert0, @py_assert7)) % {'py3': @pytest_ar._saferepr(len) if 'len' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(len) else 'len', 'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(comm) if 'comm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(comm) else 'comm', 'py8': @pytest_ar._saferepr(@py_assert7), 'py6': @pytest_ar._saferepr(@py_assert5)}
            @py_format11 = ('' + 'assert %(py10)s') % {'py10': @py_format9}
            raise AssertionError(@pytest_ar._format_explanation(@py_format11))
        @py_assert0 = @py_assert2 = @py_assert5 = @py_assert7 = None
        kvm = comm.lidList[0].languageToProbabilityMap
        @py_assert1 = ['eng']
        @py_assert3 = set(@py_assert1)
        @py_assert8 = kvm.keys
        @py_assert10 = @py_assert8()
        @py_assert12 = set(@py_assert10)
        @py_assert5 = @py_assert3 == @py_assert12
        if not @py_assert5:
            @py_format14 = @pytest_ar._call_reprcompare(('==',), (@py_assert5,), ('%(py4)s\n{%(py4)s = %(py0)s(%(py2)s)\n} == %(py13)s\n{%(py13)s = %(py6)s(%(py11)s\n{%(py11)s = %(py9)s\n{%(py9)s = %(py7)s.keys\n}()\n})\n}',), (@py_assert3, @py_assert12)) % {'py2': @pytest_ar._saferepr(@py_assert1), 'py13': @pytest_ar._saferepr(@py_assert12), 'py0': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py7': @pytest_ar._saferepr(kvm) if 'kvm' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(kvm) else 'kvm', 'py11': @pytest_ar._saferepr(@py_assert10), 'py4': @pytest_ar._saferepr(@py_assert3), 'py6': @pytest_ar._saferepr(set) if 'set' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(set) else 'set', 'py9': @pytest_ar._saferepr(@py_assert8)}
            @py_format16 = ('' + 'assert %(py15)s') % {'py15': @py_format14}
            raise AssertionError(@pytest_ar._format_explanation(@py_format16))
        @py_assert1 = @py_assert3 = @py_assert5 = @py_assert8 = @py_assert10 = @py_assert12 = None
        @py_assert0 = 1.0
        @py_assert3 = kvm['eng']
        @py_assert2 = @py_assert0 == @py_assert3
        if not @py_assert2:
            @py_format5 = @pytest_ar._call_reprcompare(('==',), (@py_assert2,), ('%(py1)s == %(py4)s',), (@py_assert0, @py_assert3)) % {'py1': @pytest_ar._saferepr(@py_assert0), 'py4': @pytest_ar._saferepr(@py_assert3)}
            @py_format7 = ('' + 'assert %(py6)s') % {'py6': @py_format5}
            raise AssertionError(@pytest_ar._format_explanation(@py_format7))
        @py_assert0 = @py_assert2 = @py_assert3 = None
    @py_assert1 = not omitted_assertions
    if not @py_assert1:
        @py_format2 = ('' + 'assert not %(py0)s') % {'py0': @pytest_ar._saferepr(omitted_assertions) if 'omitted_assertions' in @py_builtins.locals() or @pytest_ar._should_repr_global_name(omitted_assertions) else 'omitted_assertions'}
        raise AssertionError(@pytest_ar._format_explanation(@py_format2))
    @py_assert1 = None