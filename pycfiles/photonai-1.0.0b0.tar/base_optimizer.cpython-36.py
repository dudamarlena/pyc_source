# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/base_optimizer.py
# Compiled at: 2019-09-11 10:06:07
# Size of source mod 2**32: 1936 bytes


class PhotonBaseOptimizer:
    __doc__ = '\n    The PHOTON interface for hyperparameter search optimization algorithms.\n    '

    def __init__(self, *kwargs):
        pass

    def prepare(self, pipeline_elements: list, maximize_metric: bool):
        """
        Initializes hyperparameter search.
        Assembles all hyperparameters of the pipeline_element list in order to prepare the hyperparameter search space.
        Hyperparameters can be accessed via pipe_element.hyperparameters.
        """
        pass

    def ask(self):
        """
        When called, returns the next configuration that should be tested.

        Returns
        -------
        next config to test
        """
        pass

    def tell(self, config, performance):
        """
        Parameters
        ----------
        * 'config' [dict]:
            The configuration that has been trained and tested
        * 'performance' [dict]:
            Metrics about the configuration's generalization capabilities.
        """
        pass

    def plot(self, results_folder):
        """
        Plot optimizer specific visualizations
        :param results_folder:
        :return:
        """
        pass

    def plot_objective(self):
        """
        Uses plot_objective function of Scikit-Optimize to plot hyperparameters and partial dependences.
        :return:
        matplotlib figure
        """
        raise NotImplementedError('plot_objective is not yet available for this optimizer. Currently supported forskopt.')

    def plot_evaluations(self):
        """
        Uses plot_evaluations function of Scikit-Optimize to plot hyperparameters and respective performance estimates.
        :return:
        matplotlib figure
        """
        raise NotImplementedError('plot_evaluations is not yet available for this optimizer. Currently supported forskopt.')