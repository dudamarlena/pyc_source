# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/ubcpi/persistence.py
# Compiled at: 2015-09-09 20:34:03
from submissions import api as sub_api
ANSWER_LIST_KEY = 'answers'
VOTE_KEY = 'vote'
RATIONALE_KEY = 'rationale'

def get_answers_for_student(student_item):
    """
    Retrieve answers from backend for a student and question

    Args:
        student_item (dict): The location of the problem this submission is
            associated with, as defined by a course, student, and item.

    Returns:
        Answers: answers for the student
    """
    submissions = sub_api.get_submissions(student_item)
    if not submissions:
        return Answers()
    latest_submission = submissions[0]
    latest_answer_item = latest_submission.get('answer', {})
    return Answers(latest_answer_item.get(ANSWER_LIST_KEY, []))


def add_answer_for_student(student_item, vote, rationale):
    """
    Add an answer for a student to the backend

    Args:
        student_item (dict): The location of the problem this submission is
            associated with, as defined by a course, student, and item.
        vote (int): the option that student voted for
        rationale (str): the reason why the student vote for the option
    """
    answers = get_answers_for_student(student_item)
    answers.add_answer(vote, rationale)
    sub_api.create_submission(student_item, {ANSWER_LIST_KEY: answers.get_answers_as_list()})


class Answers:
    """
    The class that encapsulate the answers (original and revised) from a student

    The revision is used to identify the original (0) answer or revised (1) answer. It could be extended
    in the future if this xblock supports more than one round of revision.
    """

    def __init__(self, answers=None):
        if not answers:
            self.raw_answers = []
        else:
            self.raw_answers = answers

    def _safe_get(self, revision, key):
        """
        Get an answer data (vote or rationale) by revision

        Args:
            revision (int): the revision number for student answer, could be
                0 (original) or 1 (revised)
            key (str); key for retrieve answer data, could be VOTE_KEY or
                RATIONALE_KEY

        Returns:
            the answer data or None if revision doesn't exists
        """
        if self.has_revision(revision):
            return self.raw_answers[revision].get(key)
        else:
            return
            return

    def has_revision(self, revision):
        """
        Check if the answer has a revision

        Args:
            revision (int): the revision number for student answer, could be
                0 (original) or 1 (revised)

        Returns:
            bool: True if answer have the revision, False otherwise
        """
        return len(self.raw_answers) > revision

    def get_vote(self, revision):
        """
        Get the student voted option by revision

        Args:
            revision (int): the revision number for student answer, could be
                0 (original) or 1 (revised)

        Returns:
            int: The option index that student voted
        """
        return self._safe_get(revision, VOTE_KEY)

    def get_rationale(self, revision):
        """
        Get the student rationale by revision

        Args:
            revision (int): the revision number for student answer, could be
                0 (original) or 1 (revised)

        Returns:
            str: The rationale that why student voted for the option
        """
        return self._safe_get(revision, RATIONALE_KEY)

    def add_answer(self, vote, rationale):
        """
        Add an answer

        Args:
            vote (int): the option that student voted for
            rationale (str): the reason why the student vote for the option
        """
        self.raw_answers.append({VOTE_KEY: vote, 
           RATIONALE_KEY: rationale})

    def get_answers_as_list(self):
        """
        Return the answers as a list
        """
        return self.raw_answers