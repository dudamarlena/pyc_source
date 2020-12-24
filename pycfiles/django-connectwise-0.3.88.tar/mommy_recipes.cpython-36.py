# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/cameron/Dev/kanban-dev/django-connectwise/djconnectwise/tests/mommy_recipes.py
# Compiled at: 2019-08-14 13:00:26
# Size of source mod 2**32: 731 bytes
from model_mommy.recipe import Recipe, seq, foreign_key
from djconnectwise.models import ConnectWiseBoard, TicketPriority, Ticket, Company, Member, Project
import names
connectwise_board = Recipe(ConnectWiseBoard,
  name=(seq('Board #')))
member = Recipe(Member,
  identifier=(seq('user')),
  first_name=(lambda : names.get_first_name()),
  last_name=(lambda : names.get_last_name()))
project = Recipe(Project,
  name=(seq('Project #')),
  manager=(foreign_key(member)))
company = Recipe(Company,
  name=(seq('Company #')),
  identifier=(seq('company')))
ticket_priority = Recipe(TicketPriority,
  name=(seq('Priority #')))
ticket = Recipe(Ticket,
  summary=(seq('Summary #')))