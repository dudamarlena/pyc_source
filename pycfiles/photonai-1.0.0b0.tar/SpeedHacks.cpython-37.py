# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/SpeedHacks.py
# Compiled at: 2019-09-26 08:58:51
# Size of source mod 2**32: 1759 bytes


class PhotonBaseConstraint:
    __doc__ = '\n    The PHOTON base interface for any performance constraints that could speed up hyperparameter search.\n    After a particular configuration is tested in one fold, the performance constraint objects are called to\n    evaluate if the configuration is promising. If not, further testing in other folds is skipped to increase speed.\n    '

    def __init__(self, *kwargs):
        pass

    def shall_continue(self, inner_folds):
        """
        Function to evaluate if the constraint is reached.
        If it returns True, the testing of the configuration is continued.
        If it returns False, further testing of the configuration is skipped to increase speed of the hyperparameter search.

        Parameters
        ----------
        * 'inner_folds' [List of MDBInnerFold]:
            All performance metrics and other scoring information for the current configuration's performance.
            Can be used to evaluate if the configuration has any potential to serve the model's learning task.
        """
        pass


class MinimumPerformance:
    __doc__ = "\n    Tests if a configuration performs better than a given limit for a particular metric.\n\n    Example\n    -------\n    MinimumPerformance('accuracy', 0.96) tests if the configuration has at least a performance of 0.96 in the first fold.\n    If not further testing of the configuration is skipped, as it is regarded as not promising enough.\n    "

    def __init__(self, metric, smaller_than):
        self.metric = metric
        self.smaller_than = smaller_than

    def shall_continue(self, inner_folds):
        if inner_folds[0].validation.metrics[self.metric] < self.smaller_than:
            return False
        return True