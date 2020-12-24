# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/GNota/default_db.py
# Compiled at: 2007-09-11 01:44:49
from elixir import create_all, metadata, objectstore
from model import *
from controller import GNotaController
import os, os.path
from datetime import date
from decimal import Decimal
import sys

def _(s):
    return s


try:
    delete = sys.argv[1] == 'delete'
except IndexError:
    delete = False

gnota_homedir = os.path.join(os.path.expanduser('~'), '.gnota')
dbpath = os.path.join(gnota_homedir, 'gnota.sqlite')
if not delete and os.path.exists(dbpath):
    sys.exit(0)
create_and_connect_to_default_database(delete)
gc = GNotaController()
pass_ = ScoreSymbolValue(symbol=_('Pass'), value=1)
fail = ScoreSymbolValue(symbol=_('Fail'), value=0)
PassFail = DiscreteValuesScoreSystem(name=_('Pass/Fail'), description=_('Pass or Fail score system.'), scores=[
 pass_, fail], cls='DiscreteValuesScoreSystem')
ala = ScoreSymbolValue(symbol='A', value=4)
alb = ScoreSymbolValue(symbol='B', value=3)
alc = ScoreSymbolValue(symbol='C', value=2)
ald = ScoreSymbolValue(symbol='D', value=1)
alf = ScoreSymbolValue(symbol='F', value=0)
AmericanLetterScoreSystem = DiscreteValuesScoreSystem(name=_('Letter Grade'), description=_('American Letter Grade'), scores=[
 ala, alb, alc, ald, alf], cls='DiscreteValuesScoreSystem')
ealaplus = ScoreSymbolValue(symbol='A+', value=4)
eala = ScoreSymbolValue(symbol='A', value=4)
ealaminus = ScoreSymbolValue(symbol='A-', value=3.7)
ealbplus = ScoreSymbolValue(symbol='B+', value=3.3)
ealb = ScoreSymbolValue(symbol='B', value=3)
ealbminus = ScoreSymbolValue(symbol='B-', value=2.7)
ealcplus = ScoreSymbolValue(symbol='C+', value=2.3)
ealc = ScoreSymbolValue(symbol='C', value=2)
ealcminus = ScoreSymbolValue(symbol='C-', value=1.7)
ealdplus = ScoreSymbolValue(symbol='D+', value=1.3)
eald = ScoreSymbolValue(symbol='D', value=1)
ealdminus = ScoreSymbolValue(symbol='D-', value=0.7)
ealf = ScoreSymbolValue(symbol='F', value=0)
ExtendedAmericanLetterScoreSystem = DiscreteValuesScoreSystem(name=_('Extended Letter Grade'), description=_('American Extended Letter Grade'), scores=[
 ealaplus, eala, ealaminus,
 ealbplus, ealb, ealbminus,
 ealcplus, ealc, ealcminus,
 ealdplus, eald, ealdminus,
 ealf], cls='DiscreteValuesScoreSystem')
zero = ScoreSymbolValue(symbol='0', value=0.0)
ten = ScoreSymbolValue(symbol='10', value=10.0)
zeroten = RangedValuesScoreSystem(name=_('Zero/Ten scoresystem'), description=_('Zero/Ten ranged scoresystem'), min=zero, max=ten, cls='RangedValuesScoreSystem')
objectstore.flush()
five = ScoreSymbolValue(symbol='5', value=5.0, scoresystem=zeroten)
dac = DummyApprovationCriterion(name='Dummy Criterion', passing_score=[
 eala], cls='DummyApprovationCriterion')
sa = SimpleAverage(name='Simple average (Average C)', passing_score=[
 ealc], cls='SimpleAverage')
sa_five = SimpleAverage(name='Simple average (Average 5)', passing_score=[
 five], cls='SimpleAverage')
sa_best_2_five = SimpleAverageOfBestN(name='Simple average of best 2 (Average 5)', passing_score=[
 five], N=2, cls='SimpleAverageOfBestN')
activity_categories = [
 _('Assignment'),
 _('Essay'),
 _('Exam'),
 _('Homework'),
 _('Journal'),
 _('Lab'),
 _('Presentation'),
 _('Project')]
for ac in activity_categories:
    gc.add_category(name=ac)

objectstore.flush()