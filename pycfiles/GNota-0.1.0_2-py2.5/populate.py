# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/GNota/populate.py
# Compiled at: 2007-08-26 22:57:19
from elixir import create_all, metadata, objectstore
from model import *
from controller import GNotaController
import os, os.path
from datetime import date
from decimal import Decimal

def _(s):
    return s


create_and_connect_to_default_database(delete=True)
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
seven_point_five = ScoreSymbolValue(symbol='7.5', value=7.5, scoresystem=zeroten)
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

project = ActivityCategory.select()[(-1)]
homework = ActivityCategory.select()[(-5)]
cat_weight1 = CategoryWeight(category=project, weight=1)
cat_weight2 = CategoryWeight(category=homework, weight=2)
wa = WeightedAverage(name='Weighted Average (C+ average)', cls='WeightedAverage', passing_score=[
 ealcplus])
wa.category_weights.append(cat_weight1)
wa.category_weights.append(cat_weight2)
wa.use_missed_classes = True
wa.maximum_missed_classes = 4
objectstore.flush()
phys = Class(name='Introduction to Physics', course_id='PHY-0123', description="Basic Physics.\nNewton's law.", website='http://www.foobarphysics.org', scoresystem=ExtendedAmericanLetterScoreSystem, criterion=wa)
calculus = Class(name='Calculus 1', course_id='MAT-2453', description='Basic Calculus.\nDerivatives.', website='http://www.foobarmath.org', scoresystem=ExtendedAmericanLetterScoreSystem, criterion=sa)
arts = Class(name='Arts', course_id='ART-1234', description='Da Vinci\nPicasso\nSalvador Dali\n', website='http://www.foobararts.org', scoresystem=zeroten, criterion=sa_best_2_five)
objectstore.flush()
foo = Student(first_name='John', last_name='Foo', code='4895031', photograph='/home/lameiro/photo-foo.bmp', notes='Foo student', year=2007, phone='(12) 3456-7890')
bar = Student(first_name='Mary', last_name='Bar', code='9999999', photograph='/home/lameiro/photo-bar.bmp', notes='Bar student', year=2005, phone='(00) 0000-0000')
baz = Student(first_name='Richard', last_name='Baz', code='42', photograph='/home/lameiro/photo-baz.bmp', notes='Baz student', year=1991, phone='(00) 0000-0000')
print 'Creating students'
for i in range(18):
    Student(first_name='Foo %d' % i, last_name='Quux', code=str(i), photograph='/home/lameiro/photo-foo.jpg', notes='Foo student', year=2007, phone='(12) 3456-7890')

print 'Flushing'
objectstore.flush()
print 'Done'
foo.classes.append(phys)
foo.classes.append(calculus)
foo.classes.append(arts)
phys.students.append(bar)
arts.students.append(baz)
for s in Student.select():
    s.classes.append(phys)

activity_names = [
 _('Homework 1'),
 _('Homework 2'),
 _('Homework 3')]
for an in activity_names:
    a = Activity(name=an, category=homework, activity_class=phys, description='A simple homework', date=date.today(), scoresystem=PassFail)
    foo.activities.append(a)

objectstore.flush()
for ac in foo.activities:
    ac.grade = g = Grade()
    g.activity = ac
    g.student = foo
    g.score = pass_
    pass_.grades.append(g)
    g.assert_grade_type_matches()
    ac.weight = 1

objectstore.flush()
ac = Activity(name='Calculus homework 1', category=homework, activity_class=calculus, description='Integrals', date=date.today(), scoresystem=AmericanLetterScoreSystem)
ac.grade = g = Grade()
g.activity = ac
g.student = foo
foo.grades.append(g)
g.score = alb
alb.grades.append(g)
g.assert_grade_type_matches()
foo.activities.append(ac)
objectstore.flush()
ac = Activity(name='Calculus homework 2', category=homework, activity_class=calculus, description='Taylor series', date=date.today(), scoresystem=AmericanLetterScoreSystem)
ac.grade = g = Grade()
g.activity = ac
g.student = foo
foo.grades.append(g)
g.score = alc
alc.grades.append(g)
g.assert_grade_type_matches()
foo.activities.append(ac)
objectstore.flush()
ac = Activity(name='Arts homework 1', category=homework, activity_class=arts, description='Painting', date=date.today(), scoresystem=zeroten)
ac.grade = g = Grade()
g.activity = ac
g.student = foo
foo.grades.append(g)
g.score = five
five.grades.append(g)
g.assert_grade_type_matches()
foo.activities.append(ac)
objectstore.flush()
ac = Activity(name='Arts homework 2', category=homework, activity_class=arts, description='Sculpture', date=date.today(), scoresystem=zeroten)
ac.grade = g = Grade()
g.activity = ac
g.student = foo
foo.grades.append(g)
g.score = seven_point_five
seven_point_five.grades.append(g)
g.assert_grade_type_matches()
foo.activities.append(ac)
objectstore.flush()