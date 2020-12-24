# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/tests/test_lp_reader.py
# Compiled at: 2020-03-11 12:18:08
# Size of source mod 2**32: 13662 bytes
import io, pytest
from flipy.lp_reader import LpReader
from flipy.lp_variable import VarType

class TestLpReader:

    @pytest.mark.parametrize('term, expected', [
     ('x', ('x', 1)),
     (' x ', ('x', 1)),
     (' 5 x ', ('x', 5)),
     (' -5 x ', ('x', -5)),
     (' + 5 x ', ('x', 5)),
     (' - 5 x ', ('x', -5)),
     (' 5.5 x2y ', ('x2y', 5.5)),
     (' .5 x2y ', ('x2y', 0.5)),
     (' 1.5e3 x ', ('x', 1500)),
     (' 1.5e03 x ', ('x', 1500)),
     ('  10.5e3  x2(lkj290s9_er0)y ', ('x2(lkj290s9_er0)y', 10500)),
     ('  - 10.5e3  x2(lkj290s9_er0)y ', ('x2(lkj290s9_er0)y', -10500)),
     ('0', (None, 0)),
     ('10', (None, 10)),
     ('-10', (None, -10)),
     ('  10  ', (None, 10)),
     ('1e03', (None, 1000)),
     ('-1e03', (None, -1000)),
     ('1e-3', (None, 0.001))])
    def test_parse_term(self, term, expected):
        assert LpReader._parse_term(term) == expected

    def test_parse_term_exceptions(self):
        with pytest.raises(Exception) as (e):
            LpReader._parse_term(' -5 5x')
        assert str(e.value) == "variable '5x' does not have a valid name: A variable name should not begin with a number or a period"
        with pytest.raises(Exception) as (e):
            LpReader._parse_term(' -5 x y')
        assert str(e.value) == "variable 'x y' does not have a valid name: A variable name should not have whitespaces"
        with pytest.raises(Exception) as (e):
            LpReader._parse_term(' -5 x😂')
        assert str(e.value) == "variable 'x😂' does not have a valid name"

    @pytest.mark.parametrize('raw_expr, expected', [
     (
      '', ({}, 0)),
     (
      '100', ({}, 100)),
     (
      'x',
      (
       {'x': 1},
       0)),
     (
      '- x',
      (
       {'x': -1},
       0)),
     (
      '-x',
      (
       {'x': -1},
       0)),
     (
      '5 x',
      (
       {'x': 5},
       0)),
     (
      '5 x - 2 y + 10',
      (
       {'x':5, 
        'y':-2},
       10)),
     (
      '5 x -2 y +3   z -  4 q +  10 -  50  ',
      (
       {'x':5, 
        'y':-2, 
        'z':3, 
        'q':-4},
       -40)),
     (
      '5 x -2 x +  3 y -4 y +  10 -  50  ',
      (
       {'x':3, 
        'y':-1},
       -40)),
     (
      '- x1 + x2 + x3 + 10 x4',
      (
       {'x1':-1, 
        'x2':1, 
        'x3':1, 
        'x4':10},
       0))])
    def test_mathify_expression(self, raw_expr, expected):
        expr = LpReader._mathify_expression(raw_expr)
        assert expr == expected

    def test_trim_comments(self):
        assert LpReader._remove_comments('\\* this is a comment section  *\\') == ''
        assert LpReader._remove_comments('\\* 47caef78e069c0a6d2e4d0eb_relaxation_1 *\\\nMaximize\nOBJ:') == '\nMaximize\nOBJ:'
        assert LpReader._remove_comments('before \\* this is a comment section  *\\ after') == 'before  after'
        assert LpReader._remove_comments('before \\* this is a comment section') == 'before '

    def test_parse_named_expression(self):
        name, expr, const = LpReader._parse_named_expression('obj: x1 + x2 + 3 x3 + 5')
        assert name == 'obj'
        assert expr == {'x1':1,  'x2':1,  'x3':3}
        assert const == 5
        name, expr, const = LpReader._parse_named_expression('obj  :  - x1 + x2 + 3 x3 + 5')
        assert name == 'obj'
        assert expr == {'x1':-1,  'x2':1,  'x3':3}
        assert const == 5

    @pytest.mark.parametrize('constraint, expected', [
     (
      'c1 : 1x1 + 3y <= 20',
      [
       {'name':'c1', 
        'lhs':{'x1':1, 
         'y':3}, 
        'lhs_const':0, 
        'rhs':{},  'rhs_const':20, 
        'sense':'leq'}]),
     (
      '  c1   :  1x1 + 3y <= 20',
      [
       {'name':'c1', 
        'lhs':{'x1':1, 
         'y':3}, 
        'lhs_const':0, 
        'rhs':{},  'rhs_const':20, 
        'sense':'leq'}]),
     (
      'c1 : 1x1 + 3y \n <= 20',
      [
       {'name':'c1', 
        'lhs':{'x1':1, 
         'y':3}, 
        'lhs_const':0, 
        'rhs':{},  'rhs_const':20, 
        'sense':'leq'}]),
     (
      'c1 : \n 1x1 \n + 3y \n <= 20 \n',
      [
       {'name':'c1', 
        'lhs':{'x1':1, 
         'y':3}, 
        'lhs_const':0, 
        'rhs':{},  'rhs_const':20, 
        'sense':'leq'}]),
     (
      '1x1 + 3y <= 20',
      [
       {'name':None, 
        'lhs':{'x1':1, 
         'y':3}, 
        'lhs_const':0, 
        'rhs':{},  'rhs_const':20, 
        'sense':'leq'}])])
    def test_parse_constraints(self, constraint, expected):
        assert LpReader._parse_constraints(constraint) == expected

    def test_parse_constraints_multiline(self):
        constraints = ' c1: - x1 + x2 + x3 + 10 x4 + 10<= 20\n c2: x1 - 3 x2 + x3 <= 30\n c3: x2 - 3.5 x4 = 0\n'
        parsed_constraints = LpReader._parse_constraints(constraints)
        assert parsed_constraints[0]['name'] == 'c1'
        assert parsed_constraints[0]['lhs'] == {'x1':-1,  'x2':1,  'x3':1,  'x4':10.0}
        assert parsed_constraints[0]['lhs_const'] == 10
        assert parsed_constraints[0]['sense'] == 'leq'
        assert parsed_constraints[0]['rhs'] == {}
        assert parsed_constraints[0]['rhs_const'] == 20
        assert parsed_constraints[1]['name'] == 'c2'
        assert parsed_constraints[1]['lhs'] == {'x1':1,  'x2':-3.0,  'x3':1}
        assert parsed_constraints[1]['lhs_const'] == 0
        assert parsed_constraints[1]['sense'] == 'leq'
        assert parsed_constraints[1]['rhs'] == {}
        assert parsed_constraints[1]['rhs_const'] == 30
        assert parsed_constraints[2]['name'] == 'c3'
        assert parsed_constraints[2]['lhs'] == {'x2':1,  'x4':-3.5}
        assert parsed_constraints[2]['lhs_const'] == 0
        assert parsed_constraints[2]['sense'] == 'eq'
        assert parsed_constraints[2]['rhs'] == {}
        assert parsed_constraints[2]['rhs_const'] == 0

    def test_parse_bounds(self):
        bounds = ' x1 free\n x2 = 5\n x3 <= 40\n x4 >= 20\n 80 >= x5 >= 30\n 30 <= x6 <= 80\n\n 40 <=\n  x7 <=\n90\n100\n>= x8\n>= 50\n'
        parsed_bounds = LpReader._parse_bounds(bounds)
        assert parsed_bounds == {'x1':{'geq':-1e+20, 
          'leq':1e+20}, 
         'x2':{'eq': 5.0}, 
         'x3':{'leq': 40.0}, 
         'x4':{'geq': 20.0}, 
         'x5':{'geq':30.0, 
          'leq':80.0}, 
         'x6':{'geq':30.0, 
          'leq':80.0}, 
         'x7':{'geq':40.0, 
          'leq':90.0}, 
         'x8':{'geq':50.0, 
          'leq':100.0}}

    def test_parse_generals(self):
        generals = '\n x1\n  x2\n x3\n\n   x4 \nx5  \nx6\n'
        parsed_generals = LpReader._parse_generals(generals)
        assert parsed_generals == ['x1', 'x2', 'x3', 'x4', 'x5', 'x6']

    def test_split_content_by_section(self):
        lp_str = '\n        Maximize\n        objective section\n        Subject To\n        constraints section\n        Bounds\n        bounds section\n        Binary\n        binaries section\n        Generals\n        generals section\n        End\n        '
        is_maximize, sections = LpReader._split_content_by_sections(lp_str)
        assert is_maximize
        assert sections['objective'] == 'objective section'
        assert sections['constraints'] == 'constraints section'
        assert sections['bounds'] == 'bounds section'
        assert sections['generals'] == 'generals section'
        assert sections['binaries'] == 'binaries section'

    def test_split_content_by_section_different_order(self):
        lp_str = '\n        Maximize\n        objective section\n        Subject To\n        constraints section\n        Binary\n        binaries section\n        Generals\n        generals section\n        Bounds\n        bounds section\n        End\n        '
        is_maximize, sections = LpReader._split_content_by_sections(lp_str)
        assert is_maximize
        assert sections['objective'] == 'objective section'
        assert sections['constraints'] == 'constraints section'
        assert sections['bounds'] == 'bounds section'
        assert sections['generals'] == 'generals section'
        assert sections['binaries'] == 'binaries section'

    def test_split_content_by_section_minimal(self):
        lp_str = '\n        Maximize\n        objective section\n        End\n        '
        is_maximize, sections = LpReader._split_content_by_sections(lp_str)
        assert is_maximize
        assert sections['objective'] == 'objective section'
        assert 'constraints' not in sections
        assert 'bounds' not in sections
        assert 'generals' not in sections
        assert 'binaries' not in sections

    def test_split_content_by_section_exceptions(self):
        lp_str = '\n        Maximize\n        objective section\n        '
        with pytest.raises(Exception) as (e):
            LpReader._split_content_by_sections(lp_str)
        assert str(e.value) == 'file must end with an "end" keyword'
        lp_str = '\n        {\n            "foo": "bar"\n        }\n        '
        with pytest.raises(Exception) as (e):
            LpReader._split_content_by_sections(lp_str)
        assert str(e.value) == 'file must start with an objective'

    def test_find_problem_name(self):
        lp_str = '\n        \\ test problem 123 \\\n        Maximize\n        objective section\n        '
        problem_name = LpReader._find_problem_name(lp_str)
        assert problem_name == 'test problem 123'

    def test_variable_types(self):
        lp_str = '\n        Maximize\n         obj: x1 + 2 x2 + 3 x3 + x4 + 10\n        Subject To\n         c1: - x1 + x2 + x3 + 10 x4 <= 20\n         c2: x1 - 3 x2 + x3 <= 30\n         c3: x2 - 3.5 x4 = 0\n        Bounds\n         0 <= x1 <= 40\n         2 <= x4 <= 3\n         x3 <= 3\n        General\n         x4\n        Binary\n         x2\n        End\n        '
        lp_problem = LpReader.read(io.StringIO(lp_str))
        assert lp_problem.lp_variables['x1'].low_bound == 0
        assert lp_problem.lp_variables['x1'].up_bound == 40
        assert lp_problem.lp_variables['x1'].var_type == VarType.Continuous
        assert lp_problem.lp_variables['x2'].low_bound == 0
        assert lp_problem.lp_variables['x2'].up_bound == 1
        assert lp_problem.lp_variables['x2'].var_type == VarType.Binary
        assert lp_problem.lp_variables['x3'].low_bound == 0
        assert lp_problem.lp_variables['x3'].up_bound == 3.0
        assert lp_problem.lp_variables['x3'].var_type == VarType.Continuous
        assert lp_problem.lp_variables['x4'].low_bound == 2
        assert lp_problem.lp_variables['x4'].up_bound == 3
        assert lp_problem.lp_variables['x4'].var_type == VarType.Integer

    def test_objective(self):
        lp_str = '\n        Maximize\n         obj: x1 + 2 x2 + 3 x3 + x4 + 10\n        Subject To\n         c1: - x1 + x2 + x3 + 10 x4 <= 20\n         c2: x1 - 3 x2 + x3 <= 30\n         c3: x2 - 3.5 x4 = 0\n        Bounds\n         0 <= x1 <= 40\n         2 <= x4 <= 3\n        General\n         x4\n        Binary\n         x2\n        End\n        '
        lp_problem = LpReader.read(io.StringIO(lp_str))
        assert lp_problem.lp_objective.to_lp_terms() == ['x1', '+ 2 x2', '+ 3 x3', '+ x4', '+ 10.0']
        assert lp_problem.lp_objective.name == 'obj'
        assert lp_problem.lp_objective.const == 10

    def test_constraints(self):
        lp_str = '\n        Maximize\n         obj: x1 + 2 x2 + 3 x3 + x4 + 10\n        Subject To\n         c1: - x1 + x2 + x3 + 10 x4 <= 20\n         c2: x1 - 3 x2 + x3 <= 30\n         c3: x2 - 3.5 x4 = 0\n        Bounds\n         0 <= x1 <= 40\n         2 <= x4 <= 3\n        General\n         x4\n        Binary\n         x2\n        End\n        '
        lp_problem = LpReader.read(io.StringIO(lp_str))
        assert lp_problem.lp_constraints['c1'].to_lp_terms() == ['- x1', '+ x2', '+ x3', '+ 10 x4', '<=', '20.0']
        assert lp_problem.lp_constraints['c2'].to_lp_terms() == ['x1', '- 3 x2', '+ x3', '<=', '30.0']
        assert lp_problem.lp_constraints['c3'].to_lp_terms() == ['x2', '- 3.5 x4', '=', '0.0']

    def test_constraints_exceptions(self):
        lp_str = '\n        Maximize\n         obj: x1 + 2 x2 + 3 x3 + x4 + 10\n        Subject To\n         c1: - x1 + x2 + x3 + 10 x4\n         c2: x1 - 3 x2 + x3 <= 30\n         c3: x2 - 3.5 x4 = 0\n        Bounds\n         0 <= x1 <= 40\n         2 <= x4 <= 3\n        General\n         x4\n        Binary\n         x2\n        End\n        '
        with pytest.raises(Exception) as (e):
            lp_problem = LpReader.read(io.StringIO(lp_str))
        assert str(e.value) == "constraint c1: - x1 + x2 + x3 + 10 x4\n         c2: x1 - 3 x2 + x3 <= 30 doesn't appear to be valid"