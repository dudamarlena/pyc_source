# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/polical/TareaClass.py
# Compiled at: 2020-05-12 16:47:43
# Size of source mod 2**32: 325 bytes


class Tarea:

    def __init__(self, id, title, description, due_date, subjectID):
        self.id = id
        self.title = title
        self.description = description
        self.due_date = due_date
        self.subjectID = subjectID

    def print(self):
        print(self.id, self.title, self.due_date, self.subjectID)