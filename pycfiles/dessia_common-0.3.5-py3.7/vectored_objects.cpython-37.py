# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dessia_common/vectored_objects.py
# Compiled at: 2020-04-10 11:33:20
# Size of source mod 2**32: 11437 bytes
"""
Created on Wed Feb 19 15:56:12 2020

@author: jezequel
"""
from typing import List, Dict
import numpy as np, pandas as pd
from dessia_common import DessiaObject, Parameter

class ParetoSettings(DessiaObject):
    _generic_eq = True
    _ordered_attributes = ['name', 'enabled', 'minimized_attributes']

    def __init__(self, minimized_attributes: Dict[(str, bool)], enabled: bool=True, name: str=''):
        self.enabled = enabled
        self.minimized_attributes = minimized_attributes
        DessiaObject.__init__(self, name=name)


class ObjectiveSettings(DessiaObject):
    _generic_eq = True
    _ordered_attributes = ['name', 'enabled', 'n_near_values']

    def __init__(self, n_near_values: int=4, enabled: bool=True, name: str=''):
        self.n_near_values = n_near_values
        self.enabled = enabled
        DessiaObject.__init__(self, name=name)


class Objective(DessiaObject):
    __doc__ = '\n    Defines an objective function\n\n    :param coeff_names: List of strings representing ordered variables names.\n    :type coeff_names: [str]\n    :param coeff_values: List of floats representing coefficients.\n    :type coeff_values: [float]\n\n    Order is kept. It means that coefficients are applied to the variables\n    in the same order as they are defined.\n    '
    _generic_eq = True
    _standalone_in_db = False
    _ordered_attributes = ['name', 'scaled', 'settings', 'coefficients']
    _non_serializable_attributes = ['coeff_names']

    def __init__(self, coefficients: Dict[(str, float)], settings: ObjectiveSettings, scaled: bool=False, name: str=''):
        self.coefficients = coefficients
        self.coeff_names = list(coefficients.keys())
        self.settings = settings
        self.scaled = scaled
        DessiaObject.__init__(self, name=name)

    def apply_to_catalog(self, catalog):
        ordered_names = sorted((self.coeff_names), key=(lambda s: catalog.get_variable_index(s)))
        parameters = catalog.parameters(ordered_names)
        ratings = []
        means = catalog.means([p.name for p in parameters])
        for line in catalog.array:
            objective = sum([catalog.get_value_by_name(line, p.name) * self.coefficients[p.name] / m if self.scaled else catalog.get_value_by_name(line, p.name) * self.coefficients[p.name] for p, m in zip(parameters, means)])
            ratings.append(objective)

        return ratings


class Catalog(DessiaObject):
    __doc__ = '\n    Defines a Catalog object that gathers a collection of VectoredObjects\n\n    :param pareto_attributes: List of strings representing names of variables\n                              used for pareto computations.\n    :type pareto_attributes: [str]\n    :param minimize: List of booleans representing if pareto for this variable\n                     should be searched in maximum or minimum direction.\n    :type minimize: [bool]\n    :param objectives: List of objectives to apply to catalog vectored objects\n    :type objectives: [Objective]\n    :param n_near_values: Integer that gives the number of best solutions given by objectives\n    :type n_near_values: int\n    # :param objects: List of vectored objects.\n    # :type objects: [VectoredObject]\n    :param choice_variables: List of string. List of variable names that represent choice arguments\n    :type choice_variables: [str]\n    :param name: Name of the catalog\n    :type name: str\n\n    '
    _generic_eq = True
    _standalone_in_db = True
    _ordered_attributes = ['name', 'pareto_settings', 'objectives']
    _non_editable_attributes = ['array', 'variables', 'choice_variables']
    _export_formats = ['csv']

    def __init__(self, array: List[List[float]], variables: List[str], pareto_settings: ParetoSettings, objectives: List[Objective], choice_variables: List[str]=None, name: str=''):
        DessiaObject.__init__(self, name=name)
        self.array = array
        self.variables = variables
        self.choice_variables = choice_variables
        self.pareto_settings = pareto_settings
        self.objectives = objectives

    def _display_angular(self):
        """
        Configures catalog display on frontend

        :return: List of displays dictionnaries
        """
        filters = [{'attribute':variable,  'operator':'gt',  'bound':0} for j, variable in enumerate(self.variables) if not isinstance(self.array[0][j], str) if variable in self.choice_variables]
        values = [{variable:self.get_value_by_name(line, variable) for variable in self.variables} for line in self.array]
        pareto_indices = pareto_frontier(catalog=self)
        all_near_indices = {}
        for iobjective, objective in enumerate(self.objectives):
            if objective.settings.enabled:
                ratings = np.array(objective.apply_to_catalog(self))
                threshold = objective.settings.n_near_values
                near_indices = list(np.argpartition(ratings, threshold)[:threshold])
                all_near_indices[iobjective] = near_indices

        datasets = []
        if self.pareto_settings.enabled:
            pareto_points = [i for i in range(len(values)) if pareto_indices[i]]
            datasets.append({'label':'Pareto frontier',  'color':'#ffcc00', 
             'values':pareto_points})
        for iobjective, near_indices in all_near_indices.items():
            objective = self.objectives[iobjective]
            if objective.name:
                label = objective.name
            else:
                label = 'Near Values ' + str(iobjective)
            near_points = [i for i in range(len(values)) if i in near_indices]
            near_dataset = {'label':label,  'color':None, 
             'values':near_points}
            datasets.append(near_dataset)

        dominated_points = [self.pareto_settings.enabled or i for i in range(len(values)) if self.pareto_settings.enabled if pareto_indices[i]]
        datasets.append({'label':'Dominated points',  'color':'#99b4d6', 
         'values':dominated_points})
        displays = [
         {'angular_component':'results', 
          'filters':filters, 
          'datasets':datasets, 
          'values':values, 
          'references_attribute':'array'}]
        return displays

    def export_csv(self, attribute_name: str, indices: List[int], file: str):
        """
        Exports a reduced list of objects to .csv file

        :param attribute_name: Name of the attribute in which the list is stored
        :type attribute_name: str
        :param indices: List of integers that represents selected indices of object
                        in attribute_name sequence
        :type indices: [int]
        :param file: Target file
        """
        attribute = getattr(self, attribute_name)
        lines = [attribute[i] for i in indices]
        array = np.array(lines)
        data_frame = pd.DataFrame(array, columns=(self.variables))
        data_frame.to_csv(file, index=False)

    def parameters(self, variables: List[str]):
        """
        Computes Parameter objects from catalog structural data

        :param variables: List of string. Names of arguments of which
                         it should create a parameter.
        :type variables: [string]

        :return: List of Parameter objects
        """
        parameters = []
        for variable in variables:
            values = self.get_values(variable)
            parameters.append(Parameter(lower_bound=(min(values)), upper_bound=(max(values)),
              name=variable))

        return parameters

    def get_variable_index(self, name):
        return self.variables.index(name)

    def get_values(self, variable):
        values = [self.get_value_by_name(line, variable) for line in self.array]
        return values

    def get_value_by_name(self, line, name):
        j = self.get_variable_index(name)
        value = line[j]
        return value

    def mean(self, variable):
        values = self.get_values(variable)
        mean = sum(values) / len(values)
        return mean

    def means(self, variables: List[str]):
        means = []
        for variable in variables:
            means.append(self.mean(variable))

        return means

    def build_costs(self):
        """
        Build list of costs that are used to compute Pareto frontier.

        The cost of an attribute that is to be minimized is, for each object of catalog,
        its value minus the lower bound of of its values in the whole dataset.
        On the contrary, the cost of an attribute that is to be maximised is,
        the upper_bound of the dataset for this parameter minus the value
        of the attribute of each object of the catalog.

        For a Pareto frontier of dimensions n_costs, each vectored object of the catalog
        (n_points vectored objects in the catalog) will give a numpy array of dimensions (,n_costs)

        All put together build_costs method results in a numpy array :

        :return: A(n_points, n_costs)
        """
        pareto_parameters = self.parameters(self.pareto_settings.minimized_attributes.keys())
        costs = np.zeros((len(self.array), len(pareto_parameters)))
        for i, line in enumerate(self.array):
            for j, parameter in enumerate(pareto_parameters):
                if self.pareto_settings.minimized_attributes[parameter.name]:
                    value = self.get_value_by_name(line, parameter.name) - parameter.lower_bound
                else:
                    value = parameter.upper_bound - self.get_value_by_name(line, parameter.name)
                costs[(i, j)] = value

        return costs


def pareto_frontier(catalog: Catalog):
    """
    Find the pareto-efficient points

    :param catalog: Catalog object on which to apply pareto_frontier computation
    :return: A (n_points, ) boolean array, indicating whether each point is Pareto efficient
    """
    costs = catalog.build_costs()
    is_efficient = np.ones((costs.shape[0]), dtype=bool)
    for index, cost in enumerate(costs):
        if is_efficient[index]:
            is_efficient[is_efficient] = np.any((costs[is_efficient] < cost), axis=1)
            is_efficient[index] = True

    return is_efficient


def from_csv(filename: str, end: int=None, remove_duplicates: bool=False):
    """
    Generates MBSEs from given .csv file.
    """
    array = np.genfromtxt(filename, dtype=None, delimiter=',', names=True, encoding=None)
    variables = [v for v in array.dtype.fields.keys()]
    lines = []
    for i, line in enumerate(array):
        if end is not None:
            if i >= end:
                break
        if remove_duplicates:
            if not remove_duplicates or line.tolist() not in lines:
                lines.append(line.tolist())

    return (
     lines, variables)