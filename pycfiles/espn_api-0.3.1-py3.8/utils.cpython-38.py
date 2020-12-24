# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/espn_api/football/utils.py
# Compiled at: 2020-04-25 13:44:14
# Size of source mod 2**32: 2223 bytes


def json_parsing(obj, key):
    """Recursively pull values of specified key from nested JSON."""
    arr = []

    def extract(obj, arr, key):
        if isinstance(obj, dict):
            for k, v in obj.items():
                if (isinstance(v, dict) or isinstance)(v, list):
                    if v:
                        if isinstance(v[0], (list, dict)):
                            extract(v, arr, key)

            if k == key:
                arr.append(v)
        else:
            if isinstance(obj, list):
                for item in obj:
                    extract(item, arr, key)

        return arr

    results = extract(obj, arr, key)
    if results:
        return results[0]
    return results


def square_matrix(X):
    """Squares a matrix"""
    result = [[0.0 for x in range(len(X))] for y in range(len(X))]
    for i in range(len(X)):
        for j in range(len(X)):
            for k in range(len(X)):
                result[i][j] += X[i][k] * X[k][j]

        else:
            return result


def add_matrix(X, Y):
    """Adds two matrices"""
    result = [[0.0 for x in range(len(X))] for y in range(len(X))]
    for i in range(len(X)):
        for j in range(len(X)):
            result[i][j] = X[i][j] + Y[i][j]
        else:
            return result


def two_step_dominance(X):
    """Returns result of two step dominance formula"""
    matrix = add_matrix(square_matrix(X), X)
    result = [sum(x) for x in matrix]
    return result


def power_points(dominance, teams, week):
    """Returns list of power points"""
    power_points = []
    for i, team in zip(dominance, teams):
        avg_score = sum(team.scores[:week]) / week
        avg_mov = sum(team.mov[:week]) / week
        power = '{0:.2f}'.format(int(i) * 0.8 + int(avg_score) * 0.15 + int(avg_mov) * 0.05)
        power_points.append(power)
    else:
        power_tup = [(
         i, j) for i, j in zip(power_points, teams)]
        return sorted(power_tup, key=(lambda tup: float(tup[0])), reverse=True)