# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danyvohl/code/shwirl/extern/vispy/ext/_bundled/cassowary/simplex_solver.py
# Compiled at: 2017-04-05 22:12:59
# Size of source mod 2**32: 21586 bytes
from __future__ import print_function, unicode_literals, absolute_import, division
from .edit_info import EditInfo
from .error import RequiredFailure, ConstraintNotFound, InternalError
from .expression import Expression, StayConstraint, EditConstraint, ObjectiveVariable, SlackVariable, DummyVariable
from .tableau import Tableau
from .utils import approx_equal, EPSILON, STRONG, WEAK

class SolverEditContext(object):

    def __init__(self, solver):
        self.solver = solver

    def __enter__(self):
        self.solver.begin_edit()

    def __exit__(self, type, value, tb):
        self.solver.end_edit()


class SimplexSolver(Tableau):

    def __init__(self):
        super(SimplexSolver, self).__init__()
        self.stay_error_vars = []
        self.error_vars = {}
        self.marker_vars = {}
        self.objective = ObjectiveVariable('Z')
        self.edit_var_map = {}
        self.slack_counter = 0
        self.artificial_counter = 0
        self.dummy_counter = 0
        self.auto_solve = True
        self.needs_solving = False
        self.optimize_count = 0
        self.rows[self.objective] = Expression()
        self.edit_variable_stack = [0]

    def __repr__(self):
        parts = []
        parts.append('stay_error_vars: %s' % self.stay_error_vars)
        parts.append('edit_var_map: %s' % self.edit_var_map)
        return super(SimplexSolver, self).__repr__() + '\n' + '\n'.join(parts)

    def add_constraint(self, cn, strength=None, weight=None):
        if strength or weight:
            cn = cn.clone()
            if strength:
                cn.strength = strength
            if weight:
                cn.weight = weight
            expr, eplus, eminus, prev_edit_constant = self.new_expression(cn)
            if not self.try_adding_directly(expr):
                self.add_with_artificial_variable(expr)
            self.needs_solving = True
            if cn.is_edit_constraint:
                i = len(self.edit_var_map)
                self.edit_var_map[cn.variable] = EditInfo(cn, eplus, eminus, prev_edit_constant, i)
            if self.auto_solve:
                self.optimize(self.objective)
                self.set_external_variables()
            return cn

    def add_edit_var(self, v, strength=STRONG):
        return self.add_constraint(EditConstraint(v, strength))

    def remove_edit_var(self, v):
        self.remove_constraint(self.edit_var_map[v].constraint)

    def edit(self):
        return SolverEditContext(self)

    def resolve(self):
        self.dual_optimize()
        self.set_external_variables()
        self.infeasible_rows.clear()
        self.reset_stay_constants()

    def new_expression(self, cn):
        expr = Expression(constant=cn.expression.constant)
        eplus = None
        eminus = None
        prev_edit_constant = None
        for v, c in cn.expression.terms.items():
            e = self.rows.get(v)
            if not e:
                expr.add_variable(v, c)
            else:
                expr.add_expression(e, c)

        if cn.is_inequality:
            self.slack_counter = self.slack_counter + 1
            slack_var = SlackVariable(prefix='s', number=self.slack_counter)
            expr.set_variable(slack_var, -1)
            self.marker_vars[cn] = slack_var
            if not cn.is_required:
                self.slack_counter = self.slack_counter + 1
                eminus = SlackVariable(prefix='em', number=self.slack_counter)
                expr.set_variable(eminus, 1)
                z_row = self.rows[self.objective]
                z_row.set_variable(eminus, cn.strength * cn.weight)
                self.insert_error_var(cn, eminus)
                self.note_added_variable(eminus, self.objective)
        else:
            if cn.is_required:
                self.dummy_counter = self.dummy_counter + 1
                dummy_var = DummyVariable(number=self.dummy_counter)
                eplus = dummy_var
                eminus = dummy_var
                prev_edit_constant = cn.expression.constant
                expr.set_variable(dummy_var, 1)
                self.marker_vars[cn] = dummy_var
            else:
                self.slack_counter = self.slack_counter + 1
                eplus = SlackVariable(prefix='ep', number=self.slack_counter)
                eminus = SlackVariable(prefix='em', number=self.slack_counter)
                expr.set_variable(eplus, -1)
                expr.set_variable(eminus, 1)
                self.marker_vars[cn] = eplus
                z_row = self.rows[self.objective]
                sw_coeff = cn.strength * cn.weight
                z_row.set_variable(eplus, sw_coeff)
                self.note_added_variable(eplus, self.objective)
                z_row.set_variable(eminus, sw_coeff)
                self.note_added_variable(eminus, self.objective)
                self.insert_error_var(cn, eminus)
                self.insert_error_var(cn, eplus)
                if cn.is_stay_constraint:
                    self.stay_error_vars.append((eplus, eminus))
                elif cn.is_edit_constraint:
                    prev_edit_constant = cn.expression.constant
        if expr.constant < 0:
            expr.multiply(-1.0)
        return (
         expr, eplus, eminus, prev_edit_constant)

    def begin_edit(self):
        assert len(self.edit_var_map) > 0
        self.infeasible_rows.clear()
        self.reset_stay_constants()
        self.edit_variable_stack.append(len(self.edit_var_map))

    def end_edit(self):
        assert len(self.edit_var_map) > 0
        self.resolve()
        self.edit_variable_stack.pop()
        self.remove_edit_vars_to(self.edit_variable_stack[(-1)])

    def remove_all_edit_vars(self):
        self.remove_edit_vars_to(0)

    def remove_edit_vars_to(self, n):
        try:
            removals = []
            for v, cei in self.edit_var_map.items():
                if cei.index >= n:
                    removals.append(v)

            for v in removals:
                self.remove_edit_var(v)

            assert len(self.edit_var_map) == n
        except ConstraintNotFound:
            raise InternalError('Constraint not found during internal removal')

    def add_stay(self, v, strength=WEAK, weight=1.0):
        return self.add_constraint(StayConstraint(v, strength, weight))

    def remove_constraint(self, cn):
        self.needs_solving = True
        self.reset_stay_constants()
        z_row = self.rows[self.objective]
        e_vars = self.error_vars.get(cn)
        if e_vars:
            for cv in e_vars:
                try:
                    z_row.add_expression(self.rows[cv], -cn.weight * cn.strength, self.objective, self)
                except KeyError:
                    z_row.add_variable(cv, -cn.weight * cn.strength, self.objective, self)

        try:
            marker = self.marker_vars.pop(cn)
        except KeyError:
            raise ConstraintNotFound()

        if not self.rows.get(marker):
            col = self.columns[marker]
            exit_var = None
            min_ratio = 0.0
            for v in col:
                if v.is_restricted:
                    expr = self.rows[v]
                    coeff = expr.coefficient_for(marker)
                    if coeff < 0:
                        r = -expr.constant / coeff
                        if exit_var is None or r < min_ratio:
                            min_ratio = r
                            exit_var = v

            if exit_var is None:
                for v in col:
                    if v.is_restricted:
                        expr = self.rows[v]
                        coeff = expr.coefficient_for(marker)
                        r = expr.constant / coeff
                        if exit_var is None or r < min_ratio:
                            min_ratio = r
                            exit_var = v

            if exit_var is None:
                if len(col) == 0:
                    self.remove_column(marker)
                else:
                    exit_var = [v for v in col if v != self.objective][(-1)]
                if exit_var is not None:
                    self.pivot(marker, exit_var)
                if self.rows.get(marker):
                    expr = self.remove_row(marker)
                if e_vars:
                    for v in e_vars:
                        if v != marker:
                            self.remove_column(v)

                if cn.is_stay_constraint:
                    pass
            if e_vars:
                remaining = []
                while self.stay_error_vars:
                    p_evar, m_evar = self.stay_error_vars.pop()
                    found = False
                    try:
                        e_vars.remove(p_evar)
                        found = True
                    except KeyError:
                        pass

                    try:
                        e_vars.remove(m_evar)
                        found = True
                    except KeyError:
                        pass

                    if not found:
                        remaining.append((p_evar, m_evar))

                self.stay_error_vars = remaining
        elif cn.is_edit_constraint:
            assert e_vars is not None
            self.remove_column(self.edit_var_map[cn.variable].edit_minus)
            del self.edit_var_map[cn.variable]
        if e_vars:
            for e_var in e_vars:
                del self.error_vars[e_var]

        if self.auto_solve:
            self.optimize(self.objective)
            self.set_external_variables()

    def resolve_array(self, new_edit_constants):
        for v, cei in self.edit_var_map.items():
            self.suggest_value(v, new_edit_constants[cei.index])

        self.resolve()

    def suggest_value(self, v, x):
        cei = self.edit_var_map.get(v)
        if not cei:
            raise InternalError('suggestValue for variable %s, but var is not an edit variable' % v)
        delta = x - cei.prev_edit_constant
        cei.prev_edit_constant = x
        self.delta_edit_constant(delta, cei.edit_plus, cei.edit_minus)

    def solve(self):
        if self.needs_solving:
            self.optimize(self.objective)
            self.set_external_variables()

    def set_edited_value(self, v, n):
        if v not in self.columns or v not in self.rows:
            v.value = n
        if not approx_equal(n, v.value):
            self.add_edit_var(v)
            self.begin_edit()
            self.suggest_value(v, n)
            self.end_edit()

    def add_var(self, v):
        if v not in self.columns or v not in self.rows:
            self.add_stay(v)

    def add_with_artificial_variable(self, expr):
        self.artificial_counter = self.artificial_counter + 1
        av = SlackVariable(prefix='a', number=self.artificial_counter)
        az = ObjectiveVariable('az')
        az_row = expr.clone()
        self.add_row(az, az_row)
        self.add_row(av, expr)
        self.optimize(az)
        az_tableau_row = self.rows[az]
        if not approx_equal(az_tableau_row.constant, 0.0):
            self.remove_row(az)
            self.remove_column(av)
            raise RequiredFailure()
        e = self.rows.get(av)
        if e is not None:
            if e.is_constant:
                self.remove_row(av)
                self.remove_row(az)
                return
            entry_var = e.any_pivotable_variable()
            self.pivot(entry_var, av)
        assert av not in self.rows
        self.remove_column(av)
        self.remove_row(az)

    def try_adding_directly(self, expr):
        subject = self.choose_subject(expr)
        if subject is None:
            return False
        expr.new_subject(subject)
        if subject in self.columns:
            self.substitute_out(subject, expr)
        self.add_row(subject, expr)
        return True

    def choose_subject(self, expr):
        subject = None
        found_unrestricted = False
        found_new_restricted = False
        retval_found = False
        retval = None
        for v, c in expr.terms.items():
            if found_unrestricted:
                if not v.is_restricted:
                    if v not in self.columns:
                        retval_found = True
                        retval = v
                        break
            elif v.is_restricted:
                if not found_new_restricted and not v.is_dummy and c < 0:
                    col = self.columns.get(v)
                    if col == None or len(col) == 1 and self.objective in self.columns:
                        subject = v
                        found_new_restricted = True
                    else:
                        subject = v
                    found_unrestricted = True

        if retval_found:
            return retval
        if subject:
            return subject
        coeff = 0.0
        for v, c in expr.terms.items():
            if not v.is_dummy:
                retval_found = True
                retval = None
                break
            if v not in self.columns:
                subject = v
                coeff = c

        if retval_found:
            return retval
        if not approx_equal(expr.constant, 0.0):
            raise RequiredFailure()
        if coeff > 0:
            expr = expr * -1
        return subject

    def delta_edit_constant(self, delta, plus_error_var, minus_error_var):
        expr_plus = self.rows.get(plus_error_var)
        if expr_plus is not None:
            expr_plus.constant = expr_plus.constant + delta
            if expr_plus.constant < 0.0:
                self.infeasible_rows.add(plus_error_var)
            return
        expr_minus = self.rows.get(minus_error_var)
        if expr_minus is not None:
            expr_minus.constant = expr_minus.constant - delta
            if expr_minus.constant < 0:
                self.infeasible_rows.add(minus_error_var)
            return
        try:
            for basic_var in self.columns[minus_error_var]:
                expr = self.rows[basic_var]
                c = expr.coefficient_for(minus_error_var)
                expr.constant = expr.constant + c * delta
                if basic_var.is_restricted and expr.constant < 0:
                    self.infeasible_rows.add(basic_var)

        except KeyError:
            pass

    def dual_optimize(self):
        z_row = self.rows.get(self.objective)
        while self.infeasible_rows:
            exit_var = self.infeasible_rows.pop()
            entry_var = None
            expr = self.rows.get(exit_var)
            if expr and expr.constant < 0:
                ratio = float('inf')
                for v, cd in expr.terms.items():
                    if cd > 0 and v.is_pivotable:
                        zc = z_row.coefficient_for(v)
                        r = zc / cd
                        if r < ratio:
                            entry_var = v
                            ratio = r

                if ratio == float('inf'):
                    raise InternalError('ratio == nil (MAX_VALUE) in dual_optimize')
                self.pivot(entry_var, exit_var)

    def optimize(self, z_var):
        self.optimize_count = self.optimize_count + 1
        z_row = self.rows[z_var]
        entry_var = None
        exit_var = None
        while True:
            objective_coeff = 0.0
            for v, c in sorted(z_row.terms.items(), key=lambda x: x[0].name):
                if v.is_pivotable and c < objective_coeff:
                    objective_coeff = c
                    entry_var = v
                    break

            if objective_coeff >= -EPSILON or entry_var is None:
                return
            min_ratio = float('inf')
            r = 0
            for v in self.columns[entry_var]:
                if v.is_pivotable:
                    expr = self.rows[v]
                    coeff = expr.coefficient_for(entry_var)
                    if coeff < 0:
                        r = -expr.constant / coeff
                        if r < min_ratio:
                            min_ratio = r
                            exit_var = v

            if min_ratio == float('inf'):
                raise RequiredFailure('Objective function is unbounded')
            self.pivot(entry_var, exit_var)

    def pivot(self, entry_var, exit_var):
        if entry_var is None:
            print('WARN - entry_var is None')
        if exit_var is None:
            print('WARN - exit_var is None')
        p_expr = self.remove_row(exit_var)
        p_expr.change_subject(exit_var, entry_var)
        self.substitute_out(entry_var, p_expr)
        self.add_row(entry_var, p_expr)

    def reset_stay_constants(self):
        for p_var, m_var in self.stay_error_vars:
            expr = self.rows.get(p_var)
            if expr is None:
                expr = self.rows.get(m_var)
            if expr:
                expr.constant = 0.0

    def set_external_variables(self):
        for v in self.external_parametric_vars:
            if self.rows.get(v):
                pass
            else:
                v.value = 0.0

        for v in self.external_rows:
            expr = self.rows[v]
            v.value = expr.constant

        self.needs_solving = False

    def insert_error_var(self, cn, var):
        constraint_set = self.error_vars.get(var)
        if not constraint_set:
            constraint_set = set()
            self.error_vars[cn] = constraint_set
        constraint_set.add(var)
        self.error_vars.setdefault(var, set()).add(var)