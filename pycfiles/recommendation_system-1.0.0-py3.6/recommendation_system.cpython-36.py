# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/recommendation_system/recommendation_system.py
# Compiled at: 2017-09-29 02:52:18
# Size of source mod 2**32: 3630 bytes
from scipy.optimize import fmin_cg
import numpy as np, pandas as pd

def normalize(df, unknown='?', max_value=5, min_value=0):
    """ Normalize the columns of the data frame 'df'
        Also return a matrix containing 0s for missing postions and 1s for others
    """
    normalized_df = pd.DataFrame()
    R_df = pd.DataFrame()
    to_subtract = (max_value - min_value) / 2.0
    for column in df.columns:
        normalized_df[column] = df[column].apply(lambda x: 0 if x == unknown else x - to_subtract)
        R_df[column] = df[column].apply(lambda x: 0 if x == unknown else 1)

    return (np.array(normalized_df), np.array(R_df))


def cost_function(params, R, Y, no_features, no_movies, no_viewers, regularize_coeff=0):
    """ Sum of Squared errors + regularization term 
    """
    X = np.array(params[:no_features * no_movies])
    X = X.reshape(no_movies, no_features)
    theta = np.array(params[no_features * no_movies:])
    theta = theta.reshape(no_features, no_viewers)
    interm = R * np.dot(X, theta)
    regularization_term = (X ** 2).sum() + (theta ** 2).sum() * regularize_coeff
    return 0.5 * (((interm - Y) ** 2).sum() + regularization_term)


def cost_function_gradient(params, R, Y, no_features, no_movies, no_viewers, regularize_coeff=0):
    """
    """
    X = np.array(params[:no_features * no_movies])
    X = X.reshape(no_movies, no_features)
    theta = np.array(params[no_features * no_movies:])
    theta = theta.reshape(no_features, no_viewers)
    D = (np.dot(X, theta) - Y) * R
    X_prime = np.dot(D, theta.transpose()) + regularize_coeff * X
    theta_prime = np.dot(X.transpose(), D) + regularize_coeff * theta
    return np.concatenate([X_prime.ravel(), theta_prime.ravel()])


def complete_recommendation_table(df, no_features=None, unknown='?', max_value=10, min_value=0, regularization_coeff=0.2):
    """ Complete the recommender system data frame
    """
    no_features = no_features if no_features else len(df) + 1
    no_viewers = len(df.columns)
    no_movies = len(df)
    to_subtract = (max_value + min_value) / 2.0
    normalized_Y, R = normalize(df)
    theta = np.random.rand(no_features, no_viewers)
    X = np.random.rand(no_movies, no_features)
    initial_params = list(X.ravel()) + list(theta.ravel())
    arguments = (
     R, normalized_Y, no_features, no_movies, no_viewers, regularization_coeff)
    params = fmin_cg(cost_function, initial_params, fprime=cost_function_gradient,
      args=arguments)
    X = np.array(params[:no_features * no_movies])
    X = X.reshape(no_movies, no_features)
    theta = np.array(params[no_features * no_movies:])
    theta = theta.reshape(no_features, no_viewers)
    results = np.dot(X, theta) + to_subtract
    results = pd.DataFrame(results, index=(df.index), columns=(df.columns))
    return results


if __name__ == '__main__':
    Y_df = pd.DataFrame({'Bob':[5, '?', 4],  'Cathy':[5, 4, '?'],  'Dave':[2, 5, 5]}, index=['Toy Story', 'Despicble Me', 'Spiderman'])
    output = complete_recommendation_table(Y_df, (len(Y_df) + 1), unknown='?', max_value=5, min_value=0, regularization_coeff=0.2)
    print(output)