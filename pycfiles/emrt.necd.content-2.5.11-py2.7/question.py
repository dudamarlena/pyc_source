# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/utilities/question.py
# Compiled at: 2019-02-15 13:51:23
from AccessControl import getSecurityManager
INVALID_OBS_STATES = [
 'conclusion-discussion', 'close-requested']
PERM_ADD_COMMENT = 'emrt.necd.content: Add Comment'

def validate_qa(question):
    comments = question.values()
    questions = [ q for q in comments if q.portal_type == 'Comment' ]
    answers = [ q for q in comments if q.portal_type == 'CommentAnswer' ]
    return len(questions) == len(answers)


def check_comment_perm(question):
    sm = getSecurityManager()
    return sm.checkPermission(PERM_ADD_COMMENT, question)


class FollowUpPermission(object):

    def __call__(self, question):
        if not question:
            return False
        obs = question.aq_parent
        obs_state = obs.get_status()
        observation_in_right_state = obs_state not in INVALID_OBS_STATES
        question.has_answers()
        return observation_in_right_state and question.has_answers() and validate_qa(question) and check_comment_perm(question)