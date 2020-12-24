# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\cvrptw_optimization\single_depot_general_model_pulp.py
# Compiled at: 2020-04-05 02:46:17
# Size of source mod 2**32: 2276 bytes
import cvrptw_optimization.src as inputs
import cvrptw_optimization.src as formulation

def run_single_depot_general_model(depots, customers, transportation_matrix, vehicles, bigm=100000000, mip_gap=0.001, solver_time_limit_minutes=10, enable_solution_messaging=1, solver_type='PULP_CBC_CMD'):
    """
    Run single depot general model
    :param depots:
    :param customers:
    :param transportation_matrix:
    :param vehicles:
    :param bigm:
    :param mip_gap:
    :param solver_time_limit_minutes:
    :param enable_solution_messaging:
    :param solver_type:
    :return:
    """
    print('Running Single Depot General Model')
    print('Getting model inputs')
    model_inputs = inputs.ModelInputs(transportation_matrix, customers, depots, vehicles)
    print('Model')
    model = formulation.ModelFormulation(model_inputs.time_variables_dict, model_inputs.assignment_variables_dict, model_inputs.vertices_dict, model_inputs.vehicles_dict, model_inputs.customers_dict, model_inputs.transit_dict, model_inputs.transit_starting_customers_dict, depots['LOCATION_NAME'].iloc[0])
    print('Formulating the problem')
    model.formulate_problem(bigm)
    print('Solving the model')
    model.solve_model(mip_gap, solver_time_limit_minutes, enable_solution_messaging, solver_type)
    print('Getting model results')
    model.get_model_solution()
    return (
     model.solution_objective, model.solution_path)