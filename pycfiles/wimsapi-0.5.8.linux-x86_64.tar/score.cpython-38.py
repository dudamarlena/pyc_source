# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/wimsapi/score.py
# Compiled at: 2020-05-04 16:09:45
# Size of source mod 2**32: 5871 bytes


class ExerciseScore:
    __doc__ = "Used to store every kind of score of a WIMS Exercise received from ADM/RAW.\n\n    The following table give the correspondense between WIMS, ADM/RAW's getsheetscores job,\n    and wimsapi value:\n        \n            +-----------------+----------------+----------+\n            |    Exercise     |    ADM/RAW     | WIMSAPI  |\n            +-----------------+----------------+----------+\n            | Points required | requires       | required |\n            | Weigth          | exo_weights    | weight   |\n            | Quality         | mean_detail    | quality  |\n            | Cumul           | got_detail     | cumul    |\n            | Best scores     | best_detail    | best     |\n            | Acquired        | level_detail   | acquired |\n            | Last Result     | last_detail    | last     |\n            | Number of tries | try_detail     | tries    |\n            +-----------------+----------------+----------+\n\n    Parameters:\n        exo - (Exercise) Exercise corresponding to these scores.\n        user - (User) User corresponding to these scores.\n        quality - (float) Quality score ([0, 10]) as given by WIMS.\n        cumul - (float) Cumul score ([0, 100]) as given by WIMS.\n        best - (float) Level of success ([0, 100]) as given by WIMS.\n        acquired - (float) Acquisition score ([0, required]) as given by WIMS.\n        last - (float) Last score obtained ([0, required]) as given by WIMS.\n        weight - (int) Weight of the sheet in the Class' score.\n        tries - (int) Number of try as given by WIMS."

    def __init__(self, exo, user, quality, cumul, best, acquired, last, required, weight, tries, **kwargs):
        self.exo = exo
        self.user = user
        self.quality = quality
        self.cumul = cumul
        self.best = best
        self.acquired = acquired
        self.last = last
        self.weight = weight
        self.tries = tries
        self.required = required

    def __eq__(self, other):
        if isinstance(other, ExerciseScore):
            a = dict(self.__dict__)
            b = dict(other.__dict__)
            a['exo'] = a['exo'].qexo if a['exo'] is not None else None
            b['exo'] = b['exo'].qexo if b['exo'] is not None else None
            a['user'] = a['user'].quser if a['user'] is not None else None
            b['user'] = b['user'].quser if b['user'] is not None else None
            return a == b
        return False


class SheetScore:
    __doc__ = 'Used to store every kind of score of a WIMS Sheet received from ADM/RAW.\n    \n    The following table give the correspondense between WIMS, ADM/RAW\'s getsheetscores job,\n    and wimsapi value:\n            \n            +-------------+--------------+----------+\n            |    WIMS     |   ADM/RAW    | WIMSAPI  |\n            +-------------+--------------+----------+\n            | Score       |      -       | score    |\n            | Quality     | user_quality | quality  |\n            | Cumul       | user_percent | cumul    |\n            | Best scores | user_best    | best     |\n            | Acquired    | user_level   | acquired |\n            | Weigth      | sheet_weight | weight   |\n            +-------------+--------------+----------+\n    \n    Calculated through ADM/RAW\'s "sheet_formula".\n    \n    Parameters:\n        sheet - (Sheet) Sheet corresponding to these scores.\n        user - (User) User corresponding to these scores.\n        score - (float) Global score ([0, 10]) as given by WIMS.\n        quality - (float) Quality score ([0, 10]) as given by WIMS.\n        cumul - (float) Cumul score ([0, 100]) as given by WIMS.\n        best - (float) Level of success ([0, 100]) as given by WIMS.\n        acquired - (float) Acquisition score ([0, 10]) as given by WIMS.\n        weight - (int) Weight of the sheet in the Class\' score.\n        exercises - (List[ExerciseScore]) List of the scores obtained for each exercises.'

    def __init__(self, sheet, user, score, quality, cumul, best, acquired, weight, exercises, **kwargs):
        self.sheet = sheet
        self.user = user
        self.score = score
        self.quality = quality
        self.cumul = cumul
        self.best = best
        self.acquired = acquired
        self.weight = weight
        self.exercises = exercises

    def __eq__(self, other):
        if isinstance(other, SheetScore):
            a = dict(self.__dict__)
            b = dict(other.__dict__)
            a['sheet'] = a['sheet'].qsheet if a['sheet'] is not None else None
            b['sheet'] = b['sheet'].qsheet if b['sheet'] is not None else None
            a['user'] = a['user'].quser if a['user'] is not None else None
            b['user'] = b['user'].quser if b['user'] is not None else None
            return a == b
        return False


class ExamScore:
    __doc__ = 'Used to store the score of a WIMS Exam as received from ADM/RAW.\n    \n    Parameters:\n        exam - (Exam) Exam corresponding to these scores.\n        user - (User) User corresponding to these scores.\n        score - (float) Global score ([0, 10]) as given by WIMS.\n        attempts - (int) Number of attempts at this exam.'

    def __init__(self, exam, user, score, attempts):
        self.exam = exam
        self.user = user
        self.score = score
        self.attempts = attempts

    def __eq__(self, other):
        if isinstance(other, ExamScore):
            a = dict(self.__dict__)
            b = dict(other.__dict__)
            a['exam'] = a['exam'].qexam if a['exam'] is not None else None
            b['exam'] = b['exam'].qexam if b['exam'] is not None else None
            a['user'] = a['user'].quser if a['user'] is not None else None
            b['user'] = b['user'].quser if b['user'] is not None else None
            return a == b
        return False