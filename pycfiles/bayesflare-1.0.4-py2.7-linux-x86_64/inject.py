# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bayesflare/inject/inject.py
# Compiled at: 2017-04-26 11:11:14


def inject_model(lightcurve, model, instance=0):
    """
    Function to inject a model instance into a Light curve

    Parameters
    ----------
    lightcurve : BayesFlare Lightcurve instance
       The light curve which the model should be injected into.

    model : BayesFlare Model instance
       The model which should be injected into `lightcurve`.

    instance : int
       The component of `model` which should be injected.

    Returns
    -------
    lightcurve : BayesFlare Lightcurve instance
       The light curve with an injected model.

    """
    M = model(instance).clc
    L = lightcurve.clc
    lightcurve.clc = L + M
    lightcurve.original = M
    return lightcurve