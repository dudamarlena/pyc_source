# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/pycopula/archimedean_generators.py
# Compiled at: 2018-02-19 15:55:05
# Size of source mod 2**32: 2463 bytes
__doc__ = '\n\tThis file contains the generators and their inverses for common archimedean copulas.\n'
import numpy as np

def boundsConditions(x):
    if x < 0 or x > 1:
        raise ValueError('Unable to compute generator for x equals to {}'.format(x))


def claytonGenerator(x, theta):
    boundsConditions(x)
    if theta == 0:
        raise ValueError('The parameter of a Clayton copula must not be equal to 0.')
    if theta < -1:
        raise ValueError('The parameter of a Clayton copula must be greater than -1 and different from 0.')
    return 1.0 / theta * (x ** (-theta) - 1.0)


def claytonGeneratorInvert(x, theta):
    if theta == 0:
        raise ValueError('The parameter of a Clayton copula must not be equal to 0.')
    if theta < -1:
        raise ValueError('The parameter of a Clayton copula must be greater than -1 and different from 0.')
    return (1.0 + theta * x) ** (-1.0 / theta)


def gumbelGenerator(x, theta):
    boundsConditions(x)
    if theta < 1:
        raise ValueError('The parameter of a Gumbel copula must be greater than 1.')
    return (-np.log(x)) ** theta


def gumbelGeneratorInvert(x, theta):
    if theta < 1:
        raise ValueError('The parameter of a Gumbel copula must be greater than 1.')
    return np.exp(-x ** (1.0 / theta))


def frankGenerator(x, theta):
    boundsConditions(x)
    if theta == 0:
        raise ValueError('The parameter of a Frank copula must not be equal to 0.')
    return -np.log((np.exp(-theta * x) - 1.0) / (np.exp(-theta) - 1.0))


def frankGeneratorInvert(x, theta):
    if theta == 0:
        raise ValueError('The parameter of a Frank copula must not be equal to 0.')
    return -1.0 / theta * np.log(1.0 + np.exp(-x) * (np.exp(-theta) - 1.0))


def joeGenerator(x, theta):
    boundsConditions(x)
    if theta < 1:
        raise ValueError('The parameter of a Joe copula must be greater than 1.')
    return -np.log(1.0 - (1.0 - x) ** theta)


def joeGeneratorInvert(x, theta):
    if theta < 1:
        raise ValueError('The parameter of a Joe copula must be greater than 1.')
    return 1.0 - (1.0 - np.exp(-x)) ** (1.0 / theta)


def aliMikhailHaqGenerator(x, theta):
    boundsConditions(x)
    if theta < -1 or theta >= 1:
        raise ValueError('The parameter of an Ali-Mikhail-Haq copula must be between -1 included and 1 excluded.')
    return np.log((1.0 - theta * (1.0 - x)) / x)


def aliMikhailHaqGeneratorInvert(x, theta):
    if theta < -1 or theta >= 1:
        raise ValueError('The parameter of an Ali-Mikhail-Haq copula must be between -1 included and 1 excluded.')
    return (1.0 - theta) / (np.exp(x) - theta)