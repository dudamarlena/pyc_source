# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/juancomish/miniconda3/lib/python3.7/site-packages/pyehub/multiple_hubs.py
# Compiled at: 2019-07-30 13:57:16
# Size of source mod 2**32: 17944 bytes
"""
Solving energy hub model for n number of hubs with any network of connections wanted between the hubs.

To run for multiple hubs:
    $ python multiple_hubs.py -n NUMBER OF HUBS

If n (NUMBER OF HUBS) is not inputted the code will not run.

Naming input excel files:
    file names should start with "hub" followed by increasing numbers starting from 0.
    The files should be in the 'network' folder

To set the connections between the hubs ( the links):
   All the links between the hubs should be set in a separate excel file in the 'network' folder.
   It should be called "network.xlsx"

   The default set up is one directional connections.
   To set bidirectional connections, the connections should be defined per each direction, i.e:

        one direction:  link 0:  start_id: 0   end_id: 1

        bidirectional:  link 0:  start_id: 0   end_id: 1,
                        link 1:  start_id: 1   end_id: 0

    The link ids should start from 0 and increase by 1.
    The node ids (start_id and end_id) correspond to hubs numbering in the names of the hubs excel files.

Note:
Do not name constraints specific names in the EHubModel class -> will not be able to construct constraints in multiple_hubs
"""
import argparse, os, numpy as np
from energy_hub.param_var import ConstantOrVar
from energy_hub import EHubModel
from energy_hub.utils import constraint
from energy_hub.input_data import InputData
from outputter import print_section, output_excel
import network_to_request_format, pylp
from pylp import RealVariable, BinaryVariable, IntegerVariable
import pdb
DOMAIN_TO_VARIABLE = {'Continuous':RealVariable, 
 'Integer':IntegerVariable, 
 'Binary':BinaryVariable}

class NetworkModel(EHubModel):
    __doc__ = '\n    A subclass that allows connections between hubs.\n    '

    def __init__(self, *, excel=None, request=None, name=None, network=None, network_request=None, hub_id=None, max_carbon=None):
        super().__init__(excel=excel, request=request, max_carbon=max_carbon)
        self.name = name
        self.hub_id = hub_id
        if network:
            network_request = network_to_request_format.convert(network)
        else:
            if network_request:
                self._net_data = InputData(network_request)
            if self._net_data:
                self.links = self._net_data.links_ids
                self.link_capacities = ConstantOrVar((self.links), model=self, values=(self._net_data.link_capacity))
                self.network_cost = RealVariable()
                self.is_link_installed = {link:BinaryVariable() for link in self.links}
                self.LINK_LENGTH = self._net_data.link_length
                self.FIXED_NETWORK_INVESTMENT_COST = self._net_data.fixed_network_investment_cost
                self.LINK_PROPORTIONAL_COST = self._net_data.link_proportional_cost
            else:
                raise RuntimeError("Can't create a network with no data.")

    def _add_variables(self):
        super()._add_variables()
        self._add_link_capacity_variables()
        for i in self._net_data.capacities:
            self._data.capacities.append(i)

    @constraint('links')
    def link_is_installed(self, link):
        """
        Set binary to 1 if capacity of link is > 0.
        Args:
            link: A link
        """
        capacity = self.link_capacities[link]
        rhs = self.BIG_M * self.is_link_installed[link]
        return capacity <= rhs

    @constraint('links')
    def link_is_installed_2(self, link):
        """
        Set binary to 1 if capacity of link is > 0.
        Args:
            link: A link
        """
        installed = self.is_link_installed[link]
        lhs = self.BIG_M * self.link_capacities[link]
        return lhs >= installed

    @constraint()
    def calc_network_investment_cost(self):
        """
        Calculating investment cost for the links the hub has.
        Cost split between 2 hubs that are connected with the same link

        """
        cost = 0
        for i, link in enumerate(self.links):
            if self._net_data.link_start[i] == self.hub_id or self._net_data.link_end[i] == self.hub_id:
                cost += self.FIXED_NETWORK_INVESTMENT_COST * self.LINK_LENGTH[link] * self.is_link_installed[link] + self.link_capacities[link] * self.LINK_LENGTH[link] * self.LINK_PROPORTIONAL_COST

        cost = cost / 2
        return self.network_cost == cost

    @constraint()
    def calc_total_cost(self):
        parent_constraint = super().calc_total_cost()
        old_cost = parent_constraint.rhs
        return self.total_cost == old_cost + self.network_cost

    def _add_link_capacity_variables(self):
        for capacity in self._net_data.capacities:
            domain = capacity.domain
            name = capacity.name
            try:
                variable = DOMAIN_TO_VARIABLE[domain]()
            except KeyError:
                raise ValueError(f"Cannot create variable of type: {domain}. Can only be: {list(DOMAIN_TO_VARIABLE.keys())}")

            setattr(self, name, variable)


@constraint()
def network_constraint(hub, link_end, link_start):
    """
    Yields the constraints that allow a network connection between two hubs.

    Args:
        hub: The hub
        link_end: all the links that the hub ends at
        link_start: all the links that the hub start at
    Yields:
       A network energy balanced constraints for each hub
    """
    for t in hub.time:
        link_starting = []
        link_ending = []
        for i in range(len(link_start)):
            link_starting.append(link_start[i][t])

        for i in range(len(link_end)):
            link_ending.append(link_end[i][t])

        yield hub.energy_exported[t]['Net_export'] - hub.energy_imported[t]['Net_import'] + sum(link_ending) - sum(link_starting) == 0


@constraint()
def power_balance_constraint(hub_index, hubs, Bmatrix, angles):
    for t in hubs[0].time:
        line_flows_from_hub = sum([Bmatrix[hub_index][other_hub_index] * angles[other_hub_index][t] for other_hub_index in range(len(hubs))])
        yield sum([-line_flows_from_hub, hubs[hub_index].energy_exported[t]['Net_export'] - hubs[hub_index].energy_imported[t]['Net_import']]) == 0


@constraint()
def swing_hub_constraint(hub_index, hubs, angles):
    for t in hubs[hub_index].time:
        yield angles[hub_index][t] == 0


@constraint()
def link_capacity_constraint(link, hub, i):
    """
    Constraint for the flow in the links.
    """
    for flow in link:
        yield flow >= 0
        yield flow <= hub.link_capacities[i]


@constraint()
def linear_power_flow_constraint(power, angle_from, angle_to, time, reactance):
    """
    Constraint for linear powerflows
    """
    for t in time:
        yield power[t] == 1 / reactance * (angle_from[t] - angle_to[t])


def multiple_hubs(minimize_carbon=False, output_filename=None, input_files=None, network_excel=None, network_request=None, max_carbon=None, n=0, solver='glpk'):
    """
    Core function for solving of multiple PyEHub models.
    """
    if network_excel:
        network_excel_file = network_excel
        network_request = network_to_request_format.convert(network_excel_file)
        if network_request:
            _net_data = InputData(network_request)
        else:
            raise RuntimeError("Can't create a network with no network data.")
    else:
        hubs = []
        for i in range(0, n):
            if input_files is None:
                file_name = f"Input_files/network_input/hub{i + 1}.xlsx"
            else:
                file_name = f"{input_files}{i + 1}.xlsx"
            excel_file = file_name
            hub = NetworkModel(excel=excel_file, name=f"hub{i + 1}", max_carbon=max_carbon, network=network_excel_file,
              network_request=network_request,
              hub_id=i)
            hubs.append(hub)

        constraints = []
        for hub in hubs:
            hub.recompile()
            for constr in hub.constraints:
                constraints.append(constr)

        connections = []
        for i in _net_data.links_ids:
            start = _net_data.link_start[i]
            end = _net_data.link_end[i]
            link_type = _net_data.link_type[i]
            reactance = _net_data.link_reactance[i]
            connections.insert(i, (start, end, link_type, reactance))

        print(connections)
        links = []
        energy_flow = {t:{out:RealVariable() for out in range(len(connections))} for t in hubs[0].time}
        num_hubs = len(hubs)
        default_reactance = 0.05
        voltage_angle = {t:{node:RealVariable() for node in range(num_hubs)} for t in hubs[0].time}
        angles = []
        for i in range(num_hubs):
            hub = hubs[0]
            angle = []
            for t in hub.time:
                angle.append(voltage_angle[t][i])

            angles.insert(i, angle)

        for i in range(len(connections)):
            hub = hubs[0]
            flow = []
            for t in hub.time:
                flow.append(energy_flow[t][i])

            links.insert(i, flow)

        Bmatrix = np.zeros((num_hubs, num_hubs))
        for i in range(len(connections)):
            if connections[i][2].lower() == 'power':
                try:
                    link_reactance = float(connections[i][3])
                except ValueError:
                    link_reactance = default_reactance

                hub_from_id = connections[i][0]
                hub_to_id = connections[i][1]
                Bmatrix[(hub_from_id, hub_to_id)] += -1 / link_reactance
                Bmatrix[(hub_to_id, hub_from_id)] += -1 / link_reactance
            for j in range(0, num_hubs):
                Bmatrix[(j, j)] = -1 * sum(Bmatrix[j, :])

        for i in range(len(connections)):
            if connections[i][2].lower() == 'power':
                try:
                    link_reactance = float(connections[i][3])
                except ValueError:
                    link_reactance = default_reactance

                angle_from = angles[connections[i][0]]
                angle_to = angles[connections[i][1]]
                power = links[i]
                time = hubs[0].time
                for c in linear_power_flow_constraint(power, angle_from, angle_to, time, link_reactance):
                    constraints.append(c)

        for hub in hubs:
            for i, link in enumerate(links):
                for c in link_capacity_constraint(link, hub, i):
                    constraints.append(c)

        LINK_THERMAL_LOSS = _net_data.link_thermal_loss
        if len(hubs) > 1:
            for c in swing_hub_constraint(0, hubs, angles):
                constraints.append(c)

        for k, hub in enumerate(hubs):
            link_start = []
            link_end = []
            power_line_flag = 0
            for i in range(len(connections)):
                if connections[i][2].lower == 'power':
                    power_line_flag = 1
                elif connections[i][0] == k:
                    link_start.append(links[i])
                if connections[i][1] == k:
                    links[i] = np.array(links[i])
                    links[i] = links[i] * LINK_THERMAL_LOSS[i]
                    link_end.append(links[i])

            if power_line_flag == 0:
                for c in network_constraint(hub, link_end, link_start):
                    constraints.append(c)

            if power_line_flag == 1:
                for c in power_balance_constraint(k, hubs, Bmatrix, angles):
                    constraints.append(c)

        objective = hubs[0].objective
        for hub in hubs[1:]:
            objective += hub.objective

        status = pylp.solve(objective=objective, constraints=constraints, minimize=True, solver=solver)
        sheets = [
         'Other',
         'LOADS',
         'SOLAR_EM',
         'energy_exported',
         'energy_from_storage',
         'energy_imported',
         'energy_to_storage',
         'is_on',
         'storage_level',
         'capacity_storage',
         'capacity_tech']
        if minimize_carbon:
            ext = '_minimized_carbon'
        else:
            ext = '_minimized_cost'
    hub_dict_list = []
    tcar = 0
    tcost = 0
    tnetwork = 0
    for i, hub in enumerate(hubs):
        hub_dict_list.append(hub.solution_dict)
        if output_filename is None:
            output_excel((hub.solution_dict), f"{hub.name}{ext}.xlsx", sheets=sheets)
            print_section(f"{hub.name}{ext}", hub.solution_dict)
        else:
            output_excel((hub.solution_dict), f"{output_filename}_{i}{ext}.xlsx", sheets=sheets)
            print_section(f"{hub.name}_{i}{ext}", hub.solution_dict)
        tcar += hub.solution_dict['total_carbon']
        tcost += hub.solution_dict['total_cost']
        tnetwork += hub.solution_dict['network_cost']

    for i, hub in enumerate(hubs):
        half_heading = '===='
        for t in hub.time:
            net_imp = hub.solution_dict['energy_imported'][t]['Net_import']
            net_exp = hub.solution_dict['energy_exported'][t]['Net_export']
            if net_imp != 0 and net_exp != 0:
                print(f"{half_heading} {'Warning:'} {half_heading} \n{'Export & import at the same time for hub: '} {i}{'; For time step: '} {t} ")

    print('\nAbsolute total carbon:\t' + str(tcar))
    print(('Absolute total cost:\t' + str(tcost)), end='\n\n')
    for hub in hubs:
        print(hub.name + ' network cost: ' + str(hub.solution_dict['network_cost']))

    print('\nAbsolute total network cost:\t' + str(tnetwork))
    return hub_dict_list


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line utility to run tests.')
    parser.add_argument('-c', '--carbon', action='store_true', help='Optimize based on the total carbon level.')
    parser.add_argument('-o', '--output_filename', type=str, help='The name that the output should be stored under.')
    parser.add_argument('-v', '--carbon_value', type=float, help='The value that the carbon should try to be.')
    parser.add_argument('-n', '--number_of_hubs', type=int, help='The number of hubs to be used')
    parser.add_argument('-i', '--input_files', type=str, help='The name of the directory and the beginning of thethe input files ')
    parser.add_argument('--network', type=str, help='The name that the network excel file')
    args = parser.parse_args()
    multiple_hubs(args.carbon, args.output_filename, args.input_files, args.network, args.carbon_value, args.number_of_hubs)