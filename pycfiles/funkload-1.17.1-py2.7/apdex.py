# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/funkload/apdex.py
# Compiled at: 2015-05-06 05:03:08


class Apdex(object):
    """Application Performance Index

    The Apdex score converts many measurements into one number on a
    uniform scale of 0-to-1 (0 = no users satisfied, 1 = all users
    satisfied).

    Visit http://www.apdex.org/ for more information.
    """
    T = 1.5

    @classmethod
    def satisfying(cls, duration):
        return duration < cls.T

    @classmethod
    def tolerable(cls, duration):
        return duration < cls.T * 4

    @classmethod
    def frustrating(cls, duration):
        return duration >= cls.T * 4

    @classmethod
    def score(cls, satisfied_users, tolerating_users, frustrated_users):
        count = sum([satisfied_users, tolerating_users, frustrated_users])
        if count == 0:
            return 0
        numeric_score = (satisfied_users + tolerating_users / 2.0) / count
        klass = cls.get_score_class(numeric_score)
        return klass(numeric_score)

    class Unacceptable(float):
        label = 'UNACCEPTABLE'
        threshold = 0.5

    class Poor(float):
        label = 'POOR'
        threshold = 0.7

    class Fair(float):
        label = 'FAIR'
        threshold = 0.85

    class Good(float):
        label = 'Good'
        threshold = 0.94

    class Excellent(float):
        label = 'Excellent'
        threshold = None

    score_classes = [
     Unacceptable, Poor, Fair, Good, Excellent]

    @classmethod
    def get_score_class(cls, score):
        """Given numeric score, return a score class"""
        for klass in cls.score_classes:
            if klass == cls.Excellent or score < klass.threshold:
                return klass

    @classmethod
    def get_label(cls, score):
        return cls.get_score_class(score).label

    description_para = ' Apdex T: Application Performance Index,\n  this is a numerical measure of user satisfaction, it is based\n  on three zones of application responsiveness:\n\n  - Satisfied: The user is fully productive. This represents the\n    time value (T seconds) below which users are not impeded by\n    application response time.\n\n  - Tolerating: The user notices performance lagging within\n    responses greater than T, but continues the process.\n\n  - Frustrated: Performance with a response time greater than 4*T\n    seconds is unacceptable, and users may abandon the process.\n\n    By default T is set to 1.5s. This means that response time between 0\n    and 1.5s the user is fully productive, between 1.5 and 6s the\n    responsivness is tolerable and above 6s the user is frustrated.\n\n    The Apdex score converts many measurements into one number on a\n    uniform scale of 0-to-1 (0 = no users satisfied, 1 = all users\n    satisfied).\n\n    Visit http://www.apdex.org/ for more information.'
    rating_para = ' Rating: To ease interpretation, the Apdex score is also represented\n  as a rating:\n\n  - U for UNACCEPTABLE represented in gray for a score between 0 and 0.5\n\n  - P for POOR represented in red for a score between 0.5 and 0.7\n\n  - F for FAIR represented in yellow for a score between 0.7 and 0.85\n\n  - G for Good represented in green for a score between 0.85 and 0.94\n\n  - E for Excellent represented in blue for a score between 0.94 and 1.\n'