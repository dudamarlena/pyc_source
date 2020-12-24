# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ad254919/aiida_plugin/aiida-bigdft/aiida_bigdft/PyBigDFT/BigDFT/Datasets.py
# Compiled at: 2019-07-30 07:30:05
__doc__ = 'Calculation datasets.\n\nThis module deals with the handling of series of calculations.\nClasses and functions of this module are meant to simplify the approach to\nensemble calculations with the code, and to deal with parallel executions of\nmultiple instances of the code.\n\n'
from Calculators import Runner

def name_from_id(id):
    """Hash the id into a run name
    Construct the name of the run from the id dictionary

    Args:
        id (dict): id associated to the run

    Returns:
       str: name of the run associated to the dictionary ``id``
    """
    keys = id.keys()
    keys.sort()
    name = ''
    for k in keys:
        name += k + ':' + str(id[k]) + ','

    return name.rstrip(',')


class Dataset(Runner):
    """A set of calculations.

    Such class contains the various instances of a set of calculations with the
    code.
    The different calculations are labelled by parameter values and information
    that might then be retrieved for inspection and plotting.

    Args:
      label (str): The label of the dataset. It will be needed to identify the
          instance for example in plot titles or in the running directory.
      run_dir (str): path of the directory where the runs will be performed.
      input (dict): Inputfile to be used for the runs as default,
             can be overridden by the specific inputs of the run

    """

    def __init__(self, label='BigDFT dataset', run_dir='runs', **kwargs):
        """
        Set the dataset ready for appending new runs
        """
        from copy import deepcopy
        from futile.Utils import make_dict
        newkwargs = deepcopy(kwargs)
        Runner.__init__(self, label=label, run_dir=run_dir, **newkwargs)
        self.runs = []
        self.calculators = []
        self.results = {}
        self.ids = []
        self.names = []
        self._post_processing_function = None
        return

    def append_run(self, id, runner, **kwargs):
        """Add a run into the dataset.

        Append to the list of runs to be performed the corresponding runner and
           the arguments which are associated to it.

        Args:
          id (dict): the id of the run, useful to identify the run in the
             dataset. It has to be a dictionary as it may contain
             different keyword. For example a run might be classified as
             ``id = {'hgrid':0.35, 'crmult': 5}``.
          runner (Runner): the runner class to which the remaining keyword
             arguments will be passed at the input.

        Raises:
          ValueError: if the provided id is identical to another previously
             appended run.

        Todo:
           include id in the runs specification

        """
        from copy import deepcopy
        name = name_from_id(id)
        if name in self.names:
            raise ValueError('The run id', name, ' is already provided, modify the run id.')
        self.names.append(name)
        inp_to_append = deepcopy(self._global_options)
        inp_to_append.update(deepcopy(kwargs))
        irun = len(self.runs)
        self.runs.append(inp_to_append)
        self.ids.append(id)
        found = False
        for calc in self.calculators:
            if calc['calc'] == runner:
                calc['runs'].append(irun)
                found = True
                break

        if not found:
            self.calculators.append({'calc': runner, 'runs': [irun]})

    def process_run(self):
        """
        Run the dataset, by performing explicit run of each of the item of the
           runs_list.
        """
        self._run_the_calculations()
        return {}

    def _run_the_calculations(self, selection=None):
        for c in self.calculators:
            calc = c['calc']
            for r in c['runs']:
                if selection is not None and r not in selection:
                    continue
                inp = self.runs[r]
                name = self.names[r]
                self.results[r] = calc.run(name=name, **inp)

        return

    def set_postprocessing_function(self, func):
        """Set the callback of run.

        Calls the function ``func`` after having performed the appended runs.

        Args:
           func (func): function that process the `inputs` `results` and
               returns the value of the `run` method of the dataset.
               The function is called as ``func(self)``.

        """
        self._post_processing_function = func

    def post_processing(self, **kwargs):
        """
        Calls the Dataset function with the results of the runs as arguments
        """
        if self._post_processing_function is not None:
            return self._post_processing_function(self)
        else:
            return self.results
            return

    def fetch_results(self, id=None, attribute=None, run_if_not_present=True):
        """Retrieve some attribute from some of the results.

        Selects out of the results the objects which have in their ``id``
        at least the dictionary specified as input. May return an attribute
        of each result if needed.

        Args:
           id (dict): dictionary of the retrieved id. Return a list of the runs
               that have the ``id`` argument inside the provided ``id`` in the
               order provided by :py:meth:`append_run`.
           attribute (str): if present, provide the attribute of each of the
               results instead of the result object
           run_if_not_present (bool): If the run has not yet been performed in the dataset then perform it.

        Example:
           >>> study=Dataset()
           >>> study.append_run(id={'cr': 3},input={'dft':{'rmult':[3,8]}})
           >>> study.append_run(id={'cr': 4},input={'dft':{'rmult':[4,8]}})
           >>> study.append_run(id={'cr': 3, 'h': 0.5},
           >>>                  input={'dft':{'hgrids': 0.5, 'rmult':[4,8]}})
           >>> #append other runs if needed
           >>> study.run()  #run the calculations (optional if run_if_not_present=True)
           >>> # returns a list of the energies of first and the third result in this example
           >>> data=study.fetch_results(id={'cr': 3},attribute='energy')
        """
        name = '' if id is None else name_from_id(id)
        fetch_indices = []
        selection_to_run = []
        for irun, n in enumerate(self.names):
            if name not in n:
                continue
            if run_if_not_present and irun not in self.results:
                selection_to_run.append(irun)
            fetch_indices.append(irun)

        if len(selection_to_run) > 0:
            self._run_the_calculations(selection=selection_to_run)
        data = []
        for irun in fetch_indices:
            r = self.results[irun]
            data.append(r if attribute is None else getattr(r, attribute))

        return data

    def seek_convergence(self, rtol=1e-05, atol=1e-08, selection=None, **kwargs):
        """
        Search for the first result of the dataset which matches the provided
        tolerance parameter. The results are in dataset order
        (provided by the :py:meth:`append_run` method) if `selection` is not specified.
        Employs the numpy :py:meth:`allclose` method for comparison.

        Args:
          rtol (float): relative tolerance parameter
          atol (float): absolute tolerance parameter
          selection (list): list of the id of the runs in which to perform the convergence search.
               Each id should be unique in the dataset.
          **kwargs: arguments to be passed to the :py:meth:`fetch_results` method.

        Returns:
          id,result (tuple): the id of the last run which matches the convergence, together with the result,
                if convergence is reached.

        Raises:
           LookupError: if the parameter for convergence were not found. The dataset has to be enriched or
               the convergence parameters loosened.
        """
        from numpy import allclose
        from futile.Utils import write
        to_get = self.ids if selection is None else selection
        id_ref = to_get[0]
        write('Fetching results for id "', id_ref, '"')
        ref = self.fetch_results(id=id_ref, **kwargs)
        ref = ref[0]
        for id in to_get[1:]:
            write('Fetching results for id "', id, '"')
            val = self.fetch_results(id=id, **kwargs)
            val = val[0]
            if allclose(ref, val, rtol=rtol, atol=atol):
                res = self.fetch_results(id=id_ref)
                label = self.get_global_option('label')
                write('Convergence reached in Dataset "' + label + '" for id "', id_ref, '"')
                return (
                 id_ref, res[0])
            ref = val
            id_ref = id

        raise LookupError('Convergence not reached, enlarge the dataset or change tolerance values')
        return


def combine_datasets(*args):
    """
    Define a new instance of the dataset class that should provide
    as a result a list of the runs of the datasets
    """
    full = Dataset(label='combined_dataset')
    for dt in args:
        for irun, runs in enumerate(dt.runs):
            calc = dt.get_runner(irun)
            (id, dt.get_id(irun))
            full.append_run(id, calc, **runs)

    full.set_postprocessing_function(_combined_postprocessing_functions)


def _combined_postprocessing_functions(runs, results, **kwargs):
    pass