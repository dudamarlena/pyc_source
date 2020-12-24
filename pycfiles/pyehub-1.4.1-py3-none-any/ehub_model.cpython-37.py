# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/energy_hub/ehub_model.py
# Compiled at: 2019-07-30 13:57:16
# Size of source mod 2**32: 33187 bytes
__doc__ = '\nProvides a class for encapsulating an energy hub model.\n'
import inspect, os, sys
from itertools import product
from typing import Iterable
import logging, yaml, excel_to_request_format
from data_formats import response_format
from data_formats.request_format import Storage
from energy_hub.input_data import InputData
from energy_hub.param_var import ConstantOrVar
from energy_hub.utils import constraint, constraint_list
from pylp import RealVariable, IntegerVariable, BinaryVariable, Status
import pylp
DOMAIN_TO_VARIABLE = {'Continuous':RealVariable, 
 'Integer':IntegerVariable, 
 'Binary':BinaryVariable}
DEFAULT_SOLVER_SETTINGS = {'name':'glpk', 
 'options':{'mipgap': 0.05}}

class InfeasibleConstraintError(Exception):
    """InfeasibleConstraintError"""

    def __init__(self, constraint_name=None, arguments=None):
        if arguments is None:
            message = f"Constraint {constraint_name} is False"
        else:
            message = f"Constraint {constraint_name}{arguments} is False"
        super().__init__(message)


class EHubModel:
    """EHubModel"""

    def __init__(self, *, excel=None, request=None, big_m=99999, max_carbon=None):
        """Create a new Energy Hub using some input data.

        Args:
            excel: The Excel 2003 file for input data
            request: The request format dictionary
        """
        self._data = None
        self._compiled = False
        self._objective = None
        self.BIG_M = big_m
        self.MAX_CARBON = max_carbon
        if excel:
            request = excel_to_request_format.convert(excel)
        else:
            if request:
                self._data = InputData(request)
            if self._data:
                self._constraints = []
                self._prepare()
            else:
                raise RuntimeError("Can't create a hub with no data.")

    def solve(self, solver_settings: dict=None, is_verbose: bool=False):
        """
        Solve the model.

        Args:
            solver_settings: The config options for the solver
            is_verbose: Makes it so the solver prints everything

        Returns:
            The results
        """
        if solver_settings is None:
            solver_settings = DEFAULT_SOLVER_SETTINGS
        else:
            solver = solver_settings['name']
            options = solver_settings['options']
            if options is None:
                options = {}
            self._compiled or self.compile()
        status = pylp.solve(objective=(self.objective), constraints=(self.constraints),
          minimize=True,
          solver=solver,
          verbose=is_verbose)
        attributes = self._public_attributes()
        return response_format.create_response(status, attributes)

    def _prepare(self):
        self._create_sets()
        self._add_parameters()

    def recompile(self):
        """Clear all constraints and variables then compile again."""
        self._constraints = []
        self._compiled = False
        self.compile()

    def compile(self):
        """Build all the constraints and variables of the model."""
        self._add_variables()
        self._add_constraints()
        self.objective = 'total_cost'
        self._compiled = True

    def _create_sets(self):
        data = self._data
        self.time = data.time
        self.technologies = data.converter_names
        self.storages = data.storage_names
        self.streams = data.stream_names
        self.output_streams = data.output_stream_names
        self.demands = data.demand_stream_names
        self.export_streams = data.export_streams
        self.import_streams = data.import_streams
        self.stream_timeseries = data.stream_timeseries
        self.part_load = data.part_load_techs
        self.sources = data.source_stream_names

    def _add_variables(self):
        self._add_capacity_variables()
        self.energy_input = {t:{tech:RealVariable() for tech in self.technologies} for t in self.time}
        self.energy_exported = {t:{out:RealVariable() for out in self.export_streams} for t in self.time}
        self.energy_imported = {t:{out:RealVariable() for out in self.import_streams} for t in self.time}
        self.capacities = ConstantOrVar((self.technologies), model=self, values=(self._data.converters_capacity))
        self.is_installed = {tech:BinaryVariable() for tech in self.technologies}
        self.is_installed_2 = {storage:BinaryVariable() for storage in self.storages}
        self.is_on = {t:{tech:BinaryVariable() for tech in self.part_load} for t in self.time}
        self.total_cost = RealVariable()
        self.operating_cost = RealVariable()
        self.maintenance_cost = RealVariable()
        self.investment_cost = RealVariable()
        self.total_carbon = RealVariable()
        self.energy_to_storage = {t:{storage:RealVariable() for storage in self.storages} for t in self.time}
        self.energy_from_storage = {t:{storage:RealVariable() for storage in self.storages} for t in self.time}
        last_level = self.time[(-1)] + 1
        self.storage_level = {t:{storage:RealVariable() for storage in self.storages} for t in self.time + [last_level]}
        self.storage_capacity = ConstantOrVar((self.storages),
          model=self, values=(self._data.storage_capacity))
        self.capacity_storage = {storage:self.storage_capacity[storage] for storage in self.storages}
        self.capacity_tech = {tech:self.capacities[tech] for tech in self.technologies}

    def _add_parameters(self):
        data = self._data
        self.CONVERSION_EFFICIENCY = data.c_matrix
        self.MAX_CHARGE_RATE = data.storage_charge
        self.MAX_DISCHARGE_RATE = data.storage_discharge
        self.STORAGE_STANDING_LOSSES = data.storage_loss
        self.CHARGING_EFFICIENCY = data.storage_ef_ch
        self.DISCHARGING_EFFICIENCY = data.storage_ef_disch
        self.MIN_STATE_OF_CHARGE = data.storage_min_soc
        self.PART_LOAD = data.part_load
        self.CARBON_FACTORS = data.carbon_factors
        self.CARBON_CREDITS = data.carbon_credits
        self.LINEAR_CAPITAL_COSTS = data.linear_cost
        self.FIXED_CAPITAL_COSTS = data.fixed_capital_costs
        self.LINEAR_STORAGE_COSTS = data.storage_lin_cost
        self.ANNUAL_MAINTENANCE_STORAGE_COSTS = data.storage_annual_maintenance_cost
        self.FIXED_CAPITAL_COSTS_STORAGE = data.storage_fixed_capital_cost
        self.FUEL_PRICES = data.fuel_price
        self.FEED_IN_TARIFFS = data.feed_in
        self.OMV_COSTS = data.variable_maintenance_cost
        self.LOADS = data.loads
        self.TIME_SERIES = data.time_series_data
        self.NET_PRESENT_VALUE_TECH = data.tech_npv
        self.NET_PRESENT_VALUE_STORAGE = data.storage_npv

    @property
    def objective(self):
        """The objective "function" of the model."""
        return self._objective

    @objective.setter
    def objective(self, new_objective):
        self._objective = self.__dict__[new_objective]

    @constraint('time', 'streams')
    def energy_balance(self, t, stream):
        """
        Ensure the loads and exported energy is below the produced energy.

        Args:
            t: A time step
            stream: An output stream
        """
        if stream in self.demands:
            load = self.LOADS[stream][t]
        else:
            load = 0
        lhs = load
        total_q_out = 0
        total_q_in = 0
        for storage in self._get_storages_from_stream(stream):
            total_q_in += self.energy_to_storage[t][storage.name]
            total_q_out += self.energy_from_storage[t][storage.name]

        energy_output = 0
        for tech in self.technologies:
            energy_input = self.energy_input[t][tech]
            conversion_rate = self.CONVERSION_EFFICIENCY[tech][stream]
            energy_output += energy_input * conversion_rate

        if stream in self.export_streams:
            energy_exported = self.energy_exported[t][stream]
        else:
            energy_exported = 0
        if stream in self.import_streams:
            energy_imported = self.energy_imported[t][stream]
        else:
            energy_imported = 0
        rhs = energy_output + total_q_out + energy_imported - total_q_in - energy_exported
        return lhs == rhs

    @constraint()
    def calc_total_cost(self):
        """A constraint for calculating the total cost."""
        return self.total_cost == self.investment_cost + self.operating_cost + self.maintenance_cost

    @constraint()
    def calc_total_carbon(self):
        """A constraint for calculating the total carbon produced."""
        total_carbon_credits = 0
        for stream in self.export_streams:
            if self.CARBON_CREDITS[stream] in self.TIME_SERIES:
                for t in self.time:
                    carbon_credit = self.TIME_SERIES[self.CARBON_CREDITS[stream]][t]
                    energy_exported = self.energy_exported[t][stream]
                    total_carbon_credits += carbon_credit * energy_exported

            else:
                total_energy_exported = sum((self.energy_exported[t][stream] for t in self.time))
                carbon_credit = self.CARBON_CREDITS[stream]
                total_carbon_credits += carbon_credit * total_energy_exported

        total_carbon_emissions = 0
        for stream in self.import_streams:
            if self.CARBON_FACTORS[stream] in self.TIME_SERIES:
                for t in self.time:
                    carbon_factor = self.TIME_SERIES[self.CARBON_FACTORS[stream]][t]
                    energy_used = self.energy_imported[t][stream]
                    total_carbon_emissions += carbon_factor * energy_used

            else:
                total_energy_used = sum((self.energy_imported[t][stream] for t in self.time))
                carbon_factor = self.CARBON_FACTORS[stream]
                total_carbon_emissions += carbon_factor * total_energy_used

        return self.total_carbon == total_carbon_emissions - total_carbon_credits

    @constraint()
    def calc_investment_cost(self):
        """A constraint for calculating the investment cost."""
        storage_cost = sum((self.NET_PRESENT_VALUE_STORAGE[storage] * self.LINEAR_STORAGE_COSTS[storage] * self.storage_capacity[storage] + self.FIXED_CAPITAL_COSTS_STORAGE[storage] * self.is_installed_2[storage] for storage in self.storages))
        tech_cost = sum((self.NET_PRESENT_VALUE_TECH[tech] * (self.LINEAR_CAPITAL_COSTS[tech] * self.capacities[tech] + self.FIXED_CAPITAL_COSTS[tech] * self.is_installed[tech]) for tech in self.technologies))
        cost = tech_cost + storage_cost
        return self.investment_cost == cost

    @constraint()
    def calc_maintenance_cost(self):
        """A constraint for calculating the maintenance cost."""
        cost = 0
        for t in self.time:
            for tech in self.technologies:
                for energy in self.output_streams:
                    cost += self.energy_input[t][tech] * self.CONVERSION_EFFICIENCY[tech][energy] * self.OMV_COSTS[tech]

        for storage in self.storages:
            cost += self.ANNUAL_MAINTENANCE_STORAGE_COSTS[storage] * self.is_installed_2[storage]

        return self.maintenance_cost == cost

    @constraint()
    def calc_operating_cost(self):
        """A constraint for calculating the total operating cost."""
        total_export_income = 0
        for stream in self.export_streams:
            if self.FEED_IN_TARIFFS[stream] in self.TIME_SERIES:
                for t in self.time:
                    price = self.TIME_SERIES[self.FEED_IN_TARIFFS[stream]][t]
                    energy_exported = self.energy_exported[t][stream]
                    total_export_income += price * energy_exported

            else:
                total_energy_exported = sum((self.energy_exported[time][stream] for time in self.time))
                price = self.FEED_IN_TARIFFS[stream]
                total_export_income += price * total_energy_exported

        total_fuel_bill = 0
        for stream in self.import_streams:
            if self.FUEL_PRICES[stream] in self.TIME_SERIES:
                for t in self.time:
                    price = self.TIME_SERIES[self.FUEL_PRICES[stream]][t]
                    energy_used = self.energy_imported[t][stream]
                    total_fuel_bill += price * energy_used

            else:
                total_energy_used = sum((self.energy_imported[time][stream] for time in self.time))
                price = self.FUEL_PRICES[stream]
                total_fuel_bill += price * total_energy_used

        return self.operating_cost == total_fuel_bill - total_export_income

    @constraint('technologies')
    def tech_is_installed(self, tech):
        """
        Set binary to 1 if capacity of tech is > 0.
        Args:
            tech: A converter
        """
        capacity = self.capacities[tech]
        rhs = self.BIG_M * self.is_installed[tech]
        return capacity <= rhs

    @constraint('technologies')
    def tech_is_installed_2(self, tech):
        """
        Set binary to 1 if capacity of tech is > 0.
        Args:
            tech: A converter
        """
        installed = self.is_installed[tech]
        lhs = self.BIG_M * self.capacities[tech]
        return lhs >= installed

    @constraint('storages')
    def storage_is_installed(self, storage):
        """
        Set binary to 1 if capacity of storage is > 0.
        Args:
            storage: A storage
        """
        capacity = self.storage_capacity[storage]
        rhs = self.BIG_M * self.is_installed_2[storage]
        return capacity <= rhs

    @constraint('storages')
    def storage_is_installed_2(self, storage):
        """
        Set binary to 1 if capacity of storage is > 0.
        Args:
            storage: A storage
        """
        installed = self.is_installed_2[storage]
        lhs = self.BIG_M * self.storage_capacity[storage]
        return lhs >= installed

    @constraint('time', 'part_load', 'output_streams')
    def tech_is_on(self, t, disp, out):
        """
        Set binary to on if tech is active.

        Args:
            t: A time step
            disp: A dispatch tech
            out: An output energy stream
        """
        energy_input = self.energy_input[t][disp]
        is_on = self.is_on[t][disp]
        lhs = energy_input
        rhs = self.BIG_M * is_on
        logging.info(f"{lhs} <= {rhs}")
        return lhs <= rhs

    @constraint('time', 'part_load', 'output_streams')
    def tech_is_on_2(self, t, disp, out):
        """
        Set binary to on if tech is active.

        Args:
            t: A time step
            disp: A dispatch tech
            out: An output energy stream
        """
        energy_input = self.energy_input[t][disp]
        is_on = self.is_on[t][disp]
        lhs = self.BIG_M * energy_input
        rhs = is_on
        return lhs >= rhs

    @constraint('time', 'part_load', 'output_streams')
    def tech_part_loads(self, t, disp, out):
        """
        Args:
            t: A time step
            disp: A dispatch tech
            out: An output energy stream
        """
        conversion_rate = self.CONVERSION_EFFICIENCY[disp][out]
        if conversion_rate <= 0:
            return
        part_load = self.PART_LOAD[disp][out]
        capacity = self.capacities[disp]
        energy_input = self.energy_input[t][disp]
        is_on = self.is_on[t][disp]
        lhs = part_load * capacity
        rhs = energy_input * conversion_rate + self.BIG_M * (1 - is_on)
        return lhs <= rhs

    @constraint('time', 'technologies')
    def tech_input_below_capacity(self, t, tech):
        """
        Ensure the energy input by a tech is less than its capacity.

        Args:
            t: A time step
            tech: A converter
        """
        energy_input = self.energy_input[t][tech]
        capacity = self.capacities[tech]
        techinput = next(self._get_tech_input(tech))
        if techinput[0] in self.sources:
            timecap = self.TIME_SERIES[techinput[0]][t]
            return energy_input == timecap * capacity
        return energy_input <= capacity

    @constraint('time', 'technologies')
    def tech_input_positive(self, t, tech):
        """Energy input to tech should be positive."""
        return self.energy_input[t][tech] >= 0

    @constraint('time', 'export_streams')
    def tech_export_positive(self, t, stream):
        """Energy exported should be positive."""
        return self.energy_exported[t][stream] >= 0

    @constraint('time', 'import_streams')
    def tech_import_positive(self, t, stream):
        """Energy exported should be positive."""
        return self.energy_imported[t][stream] >= 0

    @constraint('time', 'storages')
    def storage_level_below_capacity(self, t, storage):
        """
        Ensure the storage's level is below the storage's capacity.

        Args:
            t: A time step
            storage: A storage
        """
        storage_level = self.storage_level[t][storage]
        storage_capacity = self.storage_capacity[storage]
        return storage_level <= storage_capacity

    @constraint('time', 'storages')
    def storage_level_above_minimum(self, t, storage):
        """
        Ensure the storage level is above it's minimum level.

        Args:
            t: A time step
            storage: A storage
        """
        storage_capacity = self.storage_capacity[storage]
        min_soc = self.MIN_STATE_OF_CHARGE[storage]
        storage_level = self.storage_level[t][storage]
        min_storage_level = storage_capacity * min_soc
        return min_storage_level <= storage_level

    @constraint('time', 'storages')
    def storage_discharge_rate(self, t, storage):
        """
        Ensure the discharge rate of a storage is below it's maximum rate.

        Args:
            t: A time step
            storage: A storage
        """
        max_discharge_rate = self.MAX_DISCHARGE_RATE[storage]
        storage_capacity = self.storage_capacity[storage]
        discharge_rate = self.energy_from_storage[t][storage]
        max_rate = max_discharge_rate * storage_capacity
        return discharge_rate <= max_rate

    @constraint('time', 'storages')
    def storage_charge_rate(self, t, storage):
        """
        Ensure the charge rate of a storage is below it's maximum rate.

        Args:
            t: A time step
            storage: A storage
        """
        max_charge_rate = self.MAX_CHARGE_RATE[storage]
        storage_capacity = self.storage_capacity[storage]
        charge_rate = self.energy_to_storage[t][storage]
        max_rate = max_charge_rate * storage_capacity
        return charge_rate <= max_rate

    @constraint('time', 'storages')
    def storage_balance(self, t, storage):
        """
        Calculate the current storage level from the previous level.

        Args:
            t: A time step
            storage: A storage
        """
        next_storage_level = self.storage_level[(t + 1)][storage]
        current_storage_level = self.storage_level[t][storage]
        storage_standing_loss = self.STORAGE_STANDING_LOSSES[storage]
        discharge_rate = self.DISCHARGING_EFFICIENCY[storage]
        charge_rate = self.CHARGING_EFFICIENCY[storage]
        charge_in = self.energy_to_storage[t][storage]
        charge_out = self.energy_from_storage[t][storage]
        calculated_next_storage_level = (1 - storage_standing_loss) * current_storage_level + charge_rate * charge_in - 1 / discharge_rate * charge_out
        return next_storage_level == calculated_next_storage_level

    @constraint('time', 'storages')
    def storage_input_positive(self, t, storage):
        """Energy to storage should be positive."""
        return self.energy_to_storage[t][storage] >= 0

    @constraint('time', 'storages')
    def storage_output_positive(self, t, storage):
        """Energy from the storages should be positive."""
        return self.energy_from_storage[t][storage] >= 0

    @constraint('time', 'storages')
    def storage_level_positive(self, t, storage):
        """Storages' levels should be above zero."""
        return self.storage_level[t][storage] >= 0

    @constraint('storages')
    def storage_looping(self, storage):
        """Ensure that the storage level at the beginning is equal to it's end
        level."""
        last_entry = list(self.time)[(-1)] + 1
        first_entry = list(self.time)[0]
        start_level = self.storage_level[first_entry][storage]
        end_level = self.storage_level[last_entry][storage]
        return start_level == end_level

    @constraint_list()
    def capacity_bounds(self):
        """Ensure the capacities are within their given bounds."""
        for capacity in self._data.capacities:
            variable = getattr(self, capacity.name)
            lower_bound = capacity.lower_bound
            upper_bound = capacity.upper_bound
            if lower_bound is not None:
                if upper_bound is not None:
                    yield lower_bound <= variable
                    yield variable <= upper_bound
            if lower_bound is not None and upper_bound is None:
                yield lower_bound <= variable
            elif lower_bound is None and upper_bound is not None:
                yield variable <= upper_bound
            else:
                raise RuntimeError

    @constraint()
    def max_carbon_level(self):
        """Constraint to set a max carbon cap."""
        if self.MAX_CARBON is not None:
            return self.total_carbon <= float(self.MAX_CARBON)

    def _get_storages_from_stream(self, out: str) -> Iterable[Storage]:
        return (storage for storage in self._data.storages if storage.stream == out)

    def _get_techs_from_output_stream(self, out: str):
        return (tech.name for tech in self._data.converters if tech.outputs == out)

    def _get_tech_input(self, techname: str):
        for tech in self._data.converters:
            if tech.name == techname:
                yield tech.inputs

    def _add_constraint_to_constraints(self, constraint_):
        if constraint_ is True:
            return
        elif constraint_ is False:
            raise InfeasibleConstraintError()
        elif constraint_ is not None:
            self.constraints.append(constraint_)

    def _add_indexed_constraints(self):
        """Add all the constraint decorated functions to the model."""
        methods = [getattr(self, method) for method in dir(self) if callable(getattr(self, method))]
        rules = (rule for rule in methods if hasattr(rule, 'is_constraint'))
        for rule in rules:
            if not rule.enabled:
                logging.info(f"Constraint: {rule.__name__} NOT ENABLED")
                continue
            logging.info(f"Constraint: {rule.__name__}")
            if not rule.args:
                expression = rule()
                try:
                    self._add_constraint_to_constraints(expression)
                except InfeasibleConstraintError:
                    raise InfeasibleConstraintError(rule.__name__)

            else:
                sets = [getattr(self, arg) for arg in rule.args]
                for indices in product(*sets):
                    expression = rule(*indices)
                    try:
                        self._add_constraint_to_constraints(expression)
                    except InfeasibleConstraintError:
                        raise InfeasibleConstraintError(rule.__name__, indices)

    def _add_constraint_lists(self):
        methods = [getattr(self, method) for method in dir(self) if callable(getattr(self, method))]
        rules = (rule for rule in methods if hasattr(rule, 'is_constraint_list'))
        for rule in rules:
            if not rule.enabled:
                logging.info(f"Constraint List: {rule.__name__} NOT ENABLED")
                continue
            logging.info(f"Constraint List: {rule.__name__}")
            for expression in rule():
                self.constraints.append(expression)

    def _add_constraints(self):
        self._add_indexed_constraints()
        self._add_constraint_lists()

    def _add_capacity_variables(self):
        for capacity in self._data.capacities:
            domain = capacity.domain
            name = capacity.name
            try:
                variable = DOMAIN_TO_VARIABLE[domain]()
            except KeyError:
                raise ValueError(f"Cannot create variable of type: {domain}. Can only be: {list(DOMAIN_TO_VARIABLE.keys())}")

            setattr(self, name, variable)

    @property
    def constraints(self):
        """The list of constraints on the model."""
        return self._constraints

    @constraints.setter
    def constraints(self, constraints):
        """Set the constraints of the model."""
        self._constraints = constraints

    @property
    def solution_dict(self):
        fake_status = Status(status='', time=0)
        attributes = self._public_attributes()
        response = response_format.create_response(fake_status, attributes)
        return response['solution']

    def _public_attributes(self):
        return {name:value for name, value in self.__dict__.items() if not name.startswith('_') if not name.startswith('_')}