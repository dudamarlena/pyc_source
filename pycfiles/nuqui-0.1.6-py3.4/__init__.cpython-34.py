# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nuqui/__init__.py
# Compiled at: 2018-02-13 04:50:02
# Size of source mod 2**32: 522 bytes
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .dbobjects import Base, Question, User, Meal, Score
import pkg_resources
db_path = pkg_resources.resource_filename('nuqui', 'data/nuqui.db')
engine = create_engine('sqlite:///' + db_path)
Base.metadata.bind = engine
SESSION = sessionmaker(bind=engine)
Base.metadata.create_all()
session = SESSION()
session.close()
from .nuqui import remove_user, create_user, add_meal, evaluate, get_predefined_question_dict_with_random_answers, get_score