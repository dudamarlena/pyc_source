# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\rbtools\utils\review_request.py
# Compiled at: 2017-04-19 05:14:04
import logging
from rbtools.api.errors import APIError
from rbtools.clients.errors import InvalidRevisionSpecError
from rbtools.commands import CommandError
from rbtools.utils.match_score import Score
from rbtools.utils.repository import get_repository_id
from rbtools.utils.users import get_user

def get_draft_or_current_value(field_name, review_request):
    """Returns the draft or current field value from a review request.

    If a draft exists for the supplied review request, return the draft's
    field value for the supplied field name, otherwise return the review
    request's field value for the supplied field name.
    """
    if review_request.draft:
        fields = review_request.draft[0]
    else:
        fields = review_request
    return fields[field_name]


def get_possible_matches(review_requests, summary, description, limit=5):
    """Returns a sorted list of tuples of score and review request.

    Each review request is given a score based on the summary and
    description provided. The result is a sorted list of tuples containing
    the score and the corresponding review request, sorted by the highest
    scoring review request first.
    """
    candidates = []
    for review_request in review_requests.all_items:
        summary_pair = (
         get_draft_or_current_value('summary', review_request),
         summary)
        description_pair = (
         get_draft_or_current_value('description', review_request),
         description)
        score = Score.get_match(summary_pair, description_pair)
        candidates.append((score, review_request))

    sorted_candidates = sorted(candidates, key=lambda m: (
     m[0].summary_score, m[0].description_score), reverse=True)
    return sorted_candidates[:limit]


def get_revisions(tool, cmd_args):
    """Returns the parsed revisions from the command line arguments.

    These revisions are used for diff generation and commit message
    extraction. They will be cached for future calls.
    """
    try:
        revisions = tool.parse_revision_spec(cmd_args)
    except InvalidRevisionSpecError:
        if not tool.supports_diff_extra_args:
            raise
        revisions = None

    return revisions


def find_review_request_by_change_id--- This code section failed: ---

 L.  86         0  LOAD_CONST               'id,commit_id,changenum,status,url,absolute_url'
                3  STORE_FAST            5  'only_fields'

 L.  87         6  LOAD_FAST             4  'revisions'
                9  LOAD_CONST               'tip'
               12  BINARY_SUBSCR    
               13  STORE_FAST            6  'change_id'

 L.  88        16  LOAD_GLOBAL           0  'logging'
               19  LOAD_ATTR             1  'debug'
               22  LOAD_CONST               'Attempting to find review request from tip revision ID: %s'

 L.  89        25  LOAD_FAST             6  'change_id'
               28  BINARY_MODULO    
               29  CALL_FUNCTION_1       1  None
               32  POP_TOP          

 L.  91        33  LOAD_FAST             6  'change_id'
               36  LOAD_ATTR             2  'split'
               39  LOAD_CONST               ':'
               42  LOAD_CONST               1
               45  CALL_FUNCTION_2       2  None
               48  LOAD_CONST               1
               51  BINARY_SUBSCR    
               52  STORE_FAST            6  'change_id'

 L.  93        55  BUILD_MAP_0           0  None
               58  STORE_FAST            7  'optional_args'

 L.  95        61  LOAD_FAST             6  'change_id'
               64  LOAD_ATTR             3  'isdigit'
               67  CALL_FUNCTION_0       0  None
               70  POP_JUMP_IF_FALSE    92  'to 92'

 L.  98        73  LOAD_GLOBAL           4  'int'
               76  LOAD_FAST             6  'change_id'
               79  CALL_FUNCTION_1       1  None
               82  LOAD_FAST             7  'optional_args'
               85  LOAD_CONST               'changenum'
               88  STORE_SUBSCR     
               89  JUMP_FORWARD          0  'to 92'
             92_0  COME_FROM            89  '89'

 L. 100        92  LOAD_GLOBAL           5  'get_user'
               95  LOAD_FAST             0  'api_client'
               98  LOAD_FAST             1  'api_root'
              101  LOAD_CONST               'auth_required'
              104  LOAD_GLOBAL           6  'True'
              107  CALL_FUNCTION_258   258  None
              110  STORE_FAST            8  'user'

 L. 101       113  LOAD_GLOBAL           7  'get_repository_id'

 L. 102       116  LOAD_FAST             2  'repository_info'
              119  LOAD_FAST             1  'api_root'
              122  LOAD_FAST             3  'repository_name'
              125  CALL_FUNCTION_3       3  None
              128  STORE_FAST            9  'repository_id'

 L. 106       131  LOAD_FAST             1  'api_root'
              134  LOAD_ATTR             8  'get_review_requests'
              137  LOAD_CONST               'repository'
              140  LOAD_FAST             9  'repository_id'
              143  LOAD_CONST               'from_user'

 L. 107       146  LOAD_FAST             8  'user'
              149  LOAD_ATTR             9  'username'
              152  LOAD_CONST               'commit_id'

 L. 108       155  LOAD_FAST             6  'change_id'
              158  LOAD_CONST               'only_links'

 L. 109       161  LOAD_CONST               'self'
              164  LOAD_CONST               'only_fields'

 L. 110       167  LOAD_FAST             5  'only_fields'

 L. 111       170  LOAD_FAST             7  'optional_args'
              173  CALL_FUNCTION_KW_1280  1280  None
              176  STORE_FAST           10  'review_requests'

 L. 113       179  LOAD_FAST            10  'review_requests'
              182  POP_JUMP_IF_FALSE   295  'to 295'

 L. 114       185  LOAD_FAST            10  'review_requests'
              188  LOAD_ATTR            10  'total_results'
              191  STORE_FAST           11  'count'

 L. 117       194  LOAD_FAST            11  'count'
              197  LOAD_CONST               0
              200  COMPARE_OP            4  >
              203  POP_JUMP_IF_FALSE   295  'to 295'

 L. 118       206  LOAD_FAST            11  'count'
              209  LOAD_CONST               1
              212  COMPARE_OP            2  ==
              215  POP_JUMP_IF_TRUE    231  'to 231'
              218  LOAD_ASSERT              AssertionError
              221  LOAD_CONST               '%d review requests were returned'
              224  LOAD_FAST            11  'count'
              227  BINARY_MODULO    
              228  RAISE_VARARGS_2       2  None

 L. 119       231  LOAD_FAST            10  'review_requests'
              234  LOAD_CONST               0
              237  BINARY_SUBSCR    
              238  STORE_FAST           12  'review_request'

 L. 120       241  LOAD_GLOBAL           0  'logging'
              244  LOAD_ATTR             1  'debug'
              247  LOAD_CONST               'Found review request %s with status %s'

 L. 121       250  LOAD_FAST            12  'review_request'
              253  LOAD_ATTR            12  'id'
              256  LOAD_FAST            12  'review_request'
              259  LOAD_ATTR            13  'status'
              262  BUILD_TUPLE_2         2 
              265  BINARY_MODULO    
              266  CALL_FUNCTION_1       1  None
              269  POP_TOP          

 L. 123       270  LOAD_FAST            12  'review_request'
              273  LOAD_ATTR            13  'status'
              276  LOAD_CONST               'discarded'
              279  COMPARE_OP            3  !=
              282  POP_JUMP_IF_FALSE   292  'to 292'

 L. 124       285  LOAD_FAST            12  'review_request'
              288  RETURN_END_IF    
            289_0  COME_FROM           282  '282'
              289  JUMP_ABSOLUTE       295  'to 295'
              292  JUMP_FORWARD          0  'to 295'
            295_0  COME_FROM           292  '292'

 L. 126       295  LOAD_CONST               None
              298  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 295


def guess_existing_review_request(repository_info, repository_name, api_root, api_client, tool, revisions, guess_summary, guess_description, is_fuzzy_match_func=None, no_commit_error=None, submit_as=None):
    """Try to guess the existing review request ID if it is available.

    The existing review request is guessed by comparing the existing
    summary and description to the current post's summary and description,
    respectively. The current post's summary and description are guessed if
    they are not provided.

    If the summary and description exactly match those of an existing
    review request, that request is immediately returned. Otherwise,
    the user is prompted to select from a list of potential matches,
    sorted by the highest ranked match first.

    Note that this function calls the ReviewBoard API with the only_fields
    paramater, thus the returned review request will contain only the fields
    specified by the only_fields variable.
    """
    only_fields = 'id,summary,description,draft,url,absolute_url'
    if submit_as:
        username = submit_as
    else:
        user = get_user(api_client, api_root, auth_required=True)
        username = user.username
    repository_id = get_repository_id(repository_info, api_root, repository_name)
    try:
        review_requests = api_root.get_review_requests(repository=repository_id, from_user=username, status='pending', expand='draft', only_fields=only_fields, only_links='draft', show_all_unpublished=True)
        if not review_requests:
            raise CommandError('No existing review requests to update for user %s.' % user.username)
    except APIError as e:
        raise CommandError('Error getting review requests for user %s: %s' % (
         user.username, e))

    summary = None
    description = None
    if not guess_summary or not guess_description:
        try:
            commit_message = tool.get_commit_message(revisions)
            if commit_message:
                if not guess_summary:
                    summary = commit_message['summary']
                if not guess_description:
                    description = commit_message['description']
            elif callable(no_commit_error):
                no_commit_error()
        except NotImplementedError:
            raise CommandError('--summary and --description are required.')

    if not summary and not description:
        return
    else:
        possible_matches = get_possible_matches(review_requests, summary, description)
        exact_match_count = num_exact_matches(possible_matches)
        for score, review_request in possible_matches:
            if score.is_exact_match() and exact_match_count == 1 or callable(is_fuzzy_match_func) and is_fuzzy_match_func(review_request):
                return review_request

        return


def num_exact_matches(possible_matches):
    """Returns the number of exact matches in the possible match list."""
    count = 0
    for score, request in possible_matches:
        if score.is_exact_match():
            count += 1

    return count