# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datascienceutils/explain.py
# Compiled at: 2017-11-27 01:36:20
# Size of source mod 2**32: 483 bytes


def interpret(dataframe, model):
    features = dataframe.columns
    from skater import Interpretation
    from skater.model import InMemoryModel
    df_np = dataframe.as_matrix()
    interpreter = Interpretation(df_np, feature_names=features)
    skater_model = InMemoryModel((model.predict), examples=(df_np[:10]))
    interpreter.feature_importance.feature_importance(skater_model)
    interpreter.partial_dependence.plot_partial_dependence([features[0], features[1]], skater_model)