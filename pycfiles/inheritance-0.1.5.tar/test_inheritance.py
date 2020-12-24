# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/brentp/src/inheritance/inheritance/tests/test_inheritance.py
# Compiled at: 2019-01-16 14:26:29
from __future__ import print_function
import sys
from inheritance import Sample, Family, EvalFamily
mom = Sample('mom', affected=False)
dad = Sample('dad', affected=False)
kid = Sample('kid', affected=True)
kid.mom, kid.dad = mom, dad
fam = Family([mom, dad, kid], 'a')

def make_fam1():
    fam = Family.from_ped('#family_id  sample_id   paternal_id maternal_id sex phenotype\n1   dad   0   0   1  1\n1   mom   grandpa   grandma   2  1\n1   kid   dad   mom   1  2\n1   kid2   dad   mom   1  1\n1   grandma 0   0     2  1\n1   grandpa 0   0     1  1')
    return fam


def make_fam2():
    fam = Family.from_ped('#family_id  sample_id   paternal_id maternal_id sex phenotype\n1   dad   0   0   1  1\n1   mom   grandpa   grandma   2  2\n1   kid   dad   mom   1  2\n1   kid2   dad   mom   1  1\n1   grandma 0   0     2  2\n1   grandpa 0   0     1  1')
    return fam


def test_xrec_with_het_male_and_unaffected_parents():
    mom = Sample('mom', affected=False)
    dad = Sample('dad', affected=False)
    kid = Sample('kid', sex='male', affected=True)
    kid.mom = mom
    kid.dad = dad
    fam = Family([kid, dad, mom], 'xrec')
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HET, Family.HOM_REF, Family.HOM_REF]
    assert not efam.x_rec()


def test_xrec_with_hom_alt_female_and_unaffected_parents():
    mom = Sample('mom', affected=False)
    dad = Sample('dad', affected=False)
    kid = Sample('kid', sex='female', affected=True)
    kid.mom = mom
    kid.dad = dad
    fam = Family([kid, dad, mom], 'xrec')
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HOM_ALT, Family.HOM_REF, Family.HOM_REF]
    assert efam.x_rec()


def test_x_denovo_with_missing_parent():
    """ can't be x DN if parent is missing"""
    mom = Sample('mom', affected=False)
    dad = Sample('dad', affected=False)
    kid = Sample('kid', sex='male', affected=True)
    kid.dad = dad
    fam = Family([kid, dad], 'xdn')
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HOM_ALT, Family.HOM_REF]
    assert not efam.x_denovo()


def test_sex():
    import sys
    f = next(iter(make_fam1().values()))
    assert [ s.sample_id for s in f.males ] == ['dad', 'kid', 'kid2', 'grandpa'], f.males
    assert [ s.sample_id for s in f.females ] == ['mom', 'grandma'], f.males


def test_fam():
    assert fam.subjects == [mom, dad, kid]


def test_samples():
    assert repr(mom) != '', repr(mom)


def test_attrs():
    assert mom.affected is False
    assert kid.affected is True
    assert fam.family_id == 'a', fam.family_id
    assert dad.sample_id == 'dad'


def test_auto_rec():
    assert 'gt_types[kid] == 3' in fam.auto_rec()
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HET, Family.HET, Family.HOM_ALT]
    assert efam.auto_rec()
    efam.gt_types = [
     Family.HET, Family.HET, Family.HET]
    assert not efam.auto_rec()


def test_x_denovo():
    efam = EvalFamily(fam)
    fam.subjects[0].sex = 'female'
    fam.subjects[1].sex = 'male'
    fam.subjects[2].sex = 'female'
    efam.gt_types = [Family.HOM_REF, Family.HOM_REF, Family.HET]
    assert efam.x_denovo()
    efam.gt_types[1] = Family.HET
    assert not efam.x_denovo()
    efam.gt_types[1] = Family.HOM_REF
    fam.subjects[2].sex = 'male'
    assert efam.x_denovo()


def test_xrec():
    efam = EvalFamily(fam)
    fam.subjects[0].sex = 'female'
    fam.subjects[1].sex = 'male'
    fam.subjects[2].sex = 'female'
    efam.gt_types = [Family.HET, Family.HOM_REF, Family.HOM_ALT]
    assert efam.x_rec()
    fam.subjects[2].sex = 'male'
    efam.gt_types = [Family.HET, Family.HOM_REF, Family.HOM_ALT]
    assert efam.x_rec()
    fam.subjects[2].sex = 'female'
    efam.gt_types = [
     Family.HOM_ALT, Family.HOM_REF, Family.HOM_ALT]
    assert not efam.x_rec()


def test_xdom():
    efam = EvalFamily(fam)
    fam.subjects[0].sex = 'female'
    fam.subjects[1].sex = 'male'
    fam.subjects[2].sex = 'female'
    efam.gt_types = [Family.HET, Family.HOM_REF, Family.HOM_ALT]
    assert not efam.x_dom()
    fam.subjects[0].affected = False
    assert not efam.x_dom()
    efam.gt_types[2] = Family.HET
    fam.subjects[0].affected = True
    assert efam.x_dom()
    fam.subjects[0].affected = False
    fam.subjects[1].affected = True
    assert not efam.x_dom()
    efam.gt_types = [
     Family.HOM_REF, Family.HET, Family.HOM_ALT]
    assert not efam.x_dom()
    fam.subjects[0].sex = 'female'
    fam.subjects[1].sex = 'male'
    fam.subjects[2].sex = 'female'
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HOM_REF, Family.HOM_ALT, Family.HET]
    import sys
    fam.subjects[0].affected = False
    fam.subjects[1].affected = True
    fam.subjects[2].affected = True
    assert efam.x_dom()


def test_auto_rec_kid_unaffected():
    kid.affected = False
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HET, Family.HET, Family.HOM_ALT]
    assert not efam.auto_rec()
    kid.affected = True


def test_auto_rec_extended():
    fam = make_fam1()
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HET, Family.HET, Family.HOM_ALT, Family.HET, Family.HET, Family.HET]
    assert efam.auto_rec()
    efam.subjects[5].affected = True
    assert not efam.auto_rec()
    efam.subjects[5].affected = False
    efam.gt_types[3] = Family.HOM_ALT
    assert not efam.auto_rec()
    assert efam.auto_rec(only_affected=False)
    efam.gt_types[3] = Family.HET
    assert efam.auto_rec()
    efam.gt_depths = [
     9] * 6
    assert not efam.auto_rec(min_depth=10)
    efam.gt_depths[2] = 1000
    assert not efam.auto_rec(min_depth=10)
    efam.gt_depths = [
     100] * 6
    assert efam.auto_rec(min_depth=10)
    efam.subjects[2].affected = False
    assert not efam.auto_rec(min_depth=10)


def test_auto_dom_extended():
    fam = make_fam2()
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, True, True, False, True, False]
    efam.gt_types = [
     Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    assert efam.auto_dom()
    efam.gt_types[0] = Family.HET
    assert not efam.auto_dom()
    assert efam.auto_dom(only_affected=False)
    efam.gt_types[0] = Family.HOM_REF
    assert efam.auto_dom()
    efam.gt_depths = [9] * 6
    assert not efam.auto_dom(min_depth=10)
    for f in efam.subjects:
        f.affected = True

    assert not efam.auto_dom()
    for f in efam.subjects:
        f.affected = False

    assert not efam.auto_dom()


def test_denovo():
    fam = make_fam2()
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, True, True, False, True, False]
    efam.gt_types = [
     Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    assert not efam.de_novo()


def test_comphet_pair():
    fam = make_fam2()
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, True, True, False, True, False]
    efam.gt_types = [Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    res = efam.comp_het()
    assert res
    efam.gt_types[0] = Family.HET
    res = efam.comp_het()
    assert res
    efam.gt_types[0] = Family.HOM_ALT
    res = efam.comp_het()
    assert not res


def test_comphet_with_denovo():
    mom = Sample('mom', affected=False)
    dad = Sample('dad', affected=False)
    kid = Sample('kid', sex='male', affected=True)
    kid.mom = mom
    kid.dad = dad
    fam = Family([dad, mom, kid], 'comphet_dn')
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, False, True]
    gt_types1 = [
     Family.HET, Family.HOM_REF, Family.HET]
    gt_bases1 = ['A/C', 'A/A', 'A/C']
    gt_types2 = [
     Family.HOM_REF, Family.HOM_REF, Family.HET]
    gt_bases2 = ['T/T', 'T/T', 'T/C']
    efam.gt_types = gt_types1
    res = efam.comp_het_pair(gt_types1, gt_bases1, gt_types2, gt_bases2)
    assert res['candidate']
    assert res['affected_phased'] == []
    assert res['unaffected_phased'] == []
    assert len(res['affected_dn']) == 1


def test_inherited_denovo():
    kid = Sample('kid', sex='female', affected=True)
    mom = Sample('mom', sex='female', affected=True)
    dad = Sample('dad', sex='male', affected=False)
    gma = Sample('gma', sex='female', affected=False)
    gpa = Sample('gpa', sex='male', affected=False)
    kid.mom = mom
    kid.dad = dad
    mom.mom = gma
    mom.dad = gpa
    fam = Family([kid, mom, dad, gma, gpa], 'inherited_denovo')
    efam = EvalFamily(fam)
    efam.gt_types = [Family.HET, Family.HET, Family.HOM_REF, Family.HOM_REF, Family.HOM_REF]
    assert efam.de_novo()
    assert efam.de_novo(strict=False)


def test_comphet_with_denovo_and_unsib():
    mom = Sample('mom', affected=False)
    dad = Sample('dad', affected=False)
    kid = Sample('kid', sex='male', affected=True)
    sib = Sample('sib', sex='male', affected=False)
    kid.mom = mom
    kid.dad = dad
    sib.mom = mom
    sib.dad = dad
    fam = Family([dad, mom, kid, sib], 'comphet_dn')
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, False, True, False]
    gt_types1 = [
     Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    gt_bases1 = ['A/C', 'A/A', 'A/C', 'A/A']
    gt_types2 = [
     Family.HOM_REF, Family.HOM_REF, Family.HET, Family.HET]
    gt_bases2 = ['T/T', 'T/T', 'T/C', 'T/C']
    efam.gt_types = gt_types1
    res = efam.comp_het_pair(gt_types1, gt_bases1, gt_types2, gt_bases2)
    assert res['affected_phased'] == []
    assert res['unaffected_phased'] == []
    assert len(res['affected_dn']) == 0


def test_comphet_pattern():
    fam = make_fam2()
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, True, True, False, True, False]
    gt_types1 = [Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    gt_types2 = [Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    efam.gt_types = gt_types1
    gt_bases1 = ['A/C', 'A/A', 'A/C', 'A/A', 'A/A', 'A/C', 'A/A']
    gt_bases2 = ['A/C', 'A/A', 'A/C', 'A/A', 'A/A', 'A/C', 'A/A']
    res = efam.comp_het_pair(gt_types1, gt_bases1, gt_types2, gt_bases2)


def test_comp_het_priority():
    fam = make_fam1()
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, False, True, False, False, False]
    gt_types1 = [Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    gt_types2 = [Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF, Family.HOM_REF, Family.HOM_REF]
    gt_bases1 = ['A/A', 'A/C', 'A/C', 'A/A', 'A/A', 'A/C', 'A/A']
    gt_bases2 = ['A/C', 'A/A', 'A/C', 'A/A', 'A/A', 'A/A', 'A/A']
    gt_phases = [False] * len(gt_bases2)
    efam.gt_types = gt_types1
    res = efam.comp_het_pair(gt_types1, gt_bases1, gt_types2, gt_bases2, gt_phases, gt_phases, 'A', 'C', 'A', 'C')
    assert res['candidate'] is True, res
    assert res['priority'] == 1


def test_comp_het_missing():
    fam = make_fam1()
    efam = EvalFamily(fam)
    assert [ f.affected for f in efam.subjects ] == [False, False, True, False, False, False]
    gt_types1 = [Family.HOM_REF, Family.HET, Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF]
    gt_types2 = [Family.HET, Family.HOM_REF, Family.HET, Family.HOM_REF, Family.HOM_REF, Family.HOM_REF]
    gt_bases1 = ['A/A', 'A/C', '.', 'A/A', 'A/A', 'A/C', 'A/A']
    gt_bases2 = ['A/C', 'A/A', 'A/C', 'A/A', 'A/A', 'A/A', 'A/A']
    gt_phases = [False] * len(gt_bases2)
    efam.gt_types = gt_types1
    res = efam.comp_het_pair(gt_types1, gt_bases1, gt_types2, gt_bases2, gt_phases, gt_phases, 'A', 'C', 'A', 'C')
    assert res['candidate'] is False, res


def test_comp_het_singleton():
    kid = Sample('kid', affected=True)
    efam = EvalFamily(Family([kid], 'singleton'))
    efam.gt_types = [Family.HET]
    res = efam.comp_het_pair([Family.HET], ['A/C'], [Family.HET], ['A/C'], [
     False], [False], 'A', 'C', 'A', 'C')
    assert res['candidate']
    assert res['priority'] == 2, res


def test_comp_het_all_hets():
    efam = EvalFamily(Family([dad, mom, kid], 'triox'))
    efam.gt_types = [
     Family.HET] * 3
    res = efam.comp_het_pair([Family.HET] * 3, ['A/C'] * 3, [
     Family.HET] * 3, ['A/C'] * 3, [
     False] * 3, [False] * 3, 'A', 'C', 'A', 'C')
    assert res['candidate']
    assert res['priority'] == 3


def test_comp_het_one_parent():
    mom._i = 0
    kid._i = 1
    kid.dad = None
    kid.mom = None
    efam = EvalFamily(Family([mom, kid], 'pair_mom'))
    efam.gt_types = [Family.HET] * 2
    res = efam.comp_het_pair([Family.HET] * 2, ['A/C'] * 2, [
     Family.HET] * 2, ['A/C'] * 2, [
     False] * 2, [False] * 2, 'A', 'C', 'A', 'C')
    assert res['candidate']
    assert res['priority'] == 3, res['priority']
    res = efam.comp_het_pair([Family.HOM_REF, Family.HET] * 2, ['A/A', 'A/C'], [
     Family.HET, Family.HET], ['A/C'] * 2, [
     False] * 2, [False] * 2, 'A', 'C', 'A', 'C')
    assert res['candidate']
    assert res['priority'] == 2, res['priority']
    res = efam.comp_het_pair([Family.HOM_REF, Family.HOM_REF] * 2, ['A/A', 'A/A'], [
     Family.HET, Family.HET], ['A/C'] * 2, [
     False] * 2, [False] * 2, 'A', 'C', 'A', 'C')
    assert not res['candidate']
    return


kid2 = Sample('kid2', affected=True, sex='female')

def test_comp_het_one_parent_2kids():
    """
    test that we cant have a candidate when a parent is HOM_REF at both sites.
    """
    mom._i = 0
    kid._i = 1
    kid2._i = 2
    kid.dad = None
    kid.mom = None
    kid.mom = mom
    efam = EvalFamily(Family([mom, kid, kid2], '2kids'))
    efam.gt_types = [Family.HOM_REF, Family.HET, Family.HET]
    res = efam.comp_het_pair([
     Family.HOM_REF, Family.HET, Family.HET], [
     'T/T', 'T/C', 'T/C'], [
     Family.HOM_REF, Family.HET, Family.HET], [
     'A/A', 'A/C', 'A/C'], [
     False] * 3, [
     False] * 3, 'T', 'C', 'A', 'C', fast_mode=False, allow_unaffected=True)
    assert not res['candidate'], res
    return


def test_x_dom_parents():
    mom = Sample('mom', affected=False, sex='female')
    dad = Sample('dad', affected=False, sex='male')
    kid = Sample('kid', affected=True, sex='female')
    kid.mom, kid.dad = mom, dad
    efam = EvalFamily(Family([dad, mom, kid], 'trio'))
    efam.gt_types = [Family.HOM_REF, Family.HOM_REF, Family.HET]
    assert not efam.x_dom()
    efam.gt_types = [
     Family.HET, Family.HOM_REF, Family.HET]
    assert not efam.x_dom()
    dad.affected = True
    assert efam.x_dom()
    kid.sex = 'male'
    assert not efam.x_dom()


def test_x_rec():
    mom = Sample('mom_1239NIH', affected=False, sex='female')
    dad = Sample('dad_1240NIH', affected=False, sex='male')
    kid_aff = Sample('kidaff_1238NIH', affected=True, sex='female')
    kid_aff.mom = mom
    kid_aff.dad = dad
    efam = EvalFamily(Family([dad, mom, kid_aff], 'oler-trio'))
    efam.gt_types = [
     Family.HOM_REF, Family.HOM_REF, Family.HOM_ALT]
    assert efam.x_rec()