# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/ollin/estimation/occupancy/single_species.py
# Compiled at: 2018-10-19 09:51:47
from ..stanmodels import StanModel
from .base import OccupancyEstimate
CODE = '\ndata {\n    int<lower=0> steps;\n    int<lower=0> cams;\n    int<lower=0, upper=1> detections[cams, steps];\n\n    // Parameters for Ocuppancy Beta Prior\n    real<lower=0> alpha_oc;\n    real<lower=0> beta_oc;\n\n    // Parameters for detectionsectability Beta Prior\n    real<lower=0> alpha_det;\n    real<lower=0> beta_det;\n}\ntransformed data {\n    int<lower=0> counts[cams]; // detectionsection count per site\n    for(m in 1:cams) {\n        counts[m] = sum(detections[m]);\n    }\n}\nparameters {\n    real<lower=0, upper=1> occupancy;\n    real<lower=0, upper=1> detectability;\n}\nmodel {\n    occupancy ~ beta(alpha_oc, beta_oc);\n    detectability ~ beta(alpha_det, beta_det);\n\n    for (j in 1:cams) {\n        if (counts[j] == 0)\n            target += log_sum_exp(\n                binomial_lpmf(counts[j] | steps, detectability) + log(occupancy),\n                log(1 - occupancy));\n        else\n            target += log(occupancy) + binomial_lpmf(counts[j] | steps, detectability);\n    }\n}\n'

class Model(StanModel):
    """McKenzie Model for Single Species - Single Season occupancy estimation.

    # TODO

    """
    name = 'McKenzie Single Species - Single Season'
    stancode = CODE

    def prepare_data(self, detection, priors):
        steps, cams = detection.detections.shape
        data = {'steps': steps, 
           'cams': cams, 
           'detections': detection.detections.T.astype(int).tolist(), 
           'alpha_det': priors.get('alpha_det', 1), 
           'beta_det': priors.get('beta_det', 1), 
           'alpha_oc': priors.get('alpha_oc', 1), 
           'beta_oc': priors.get('beta_oc', 1)}
        return data

    def estimate(self, detection, method='MAP', priors=None):
        stan_result = super(Model, self).estimate(detection, method, priors)
        occupancy = stan_result['occupancy']
        detectability = stan_result['detectability']
        est = OccupancyEstimate(occupancy, self, detection, detectability=detectability)
        return est