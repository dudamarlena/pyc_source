# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: D:\Projects\A_MSU_NASA\VS\TimeSeriesAnalysis\pyiomica\utilityFunctions.py
# Compiled at: 2019-10-14 10:33:04
# Size of source mod 2**32: 3216 bytes
__doc__ = 'Utility functions'
import multiprocessing
from .globalVariables import *

def readMathIOmicaData(fileName):
    """Read text files exported by MathIOmica and convert to Python data

    Parameters:
        fileName: str
            Path of directories and name of the file containing data

    Returns:
        data
            Python data

    Usage:
        data = readMathIOmicaData("../../MathIOmica/MathIOmica/MathIOmicaData/ExampleData/rnaExample")
    """
    if os.path.isfile(fileName):
        with open(fileName, 'r') as (tempFile):
            data = tempFile.read()
        data = data.replace('\n', '').replace('{', '(').replace('}', ')').replace('->', ':').replace('|>', '}')
        data = data.replace('<|', '{').replace('^', '*').replace('`', '*').replace('Missing[]', '"Missing[]"')
        data = data.replace('\\', '')
    else:
        print('File not found (%s)' % fileName)
    returning = None
    try:
        returning = eval(data)
    except:
        print('Error occured while converting data (%s)' % fileName)

    return returning


def runCPUs(NumberOfAvailableCPUs, func, list_of_tuples_of_func_params):
    """Parallelize function call with multiprocessing.Pool.

    Parameters:
        NumberOfAvailableCPUs: int
            Number of processes to create

        func: function
            Function to apply, must take at most one argument

        list_of_tuples_of_func_params: list
            Function parameters

    Returns:
        2d numpy.array
            Results of func in a numpy array

    Usage:
        results = runCPUs(4, pAutocorrelation, [(times[i], data[i], allTimes) for i in range(10)])
    """
    instPool = multiprocessing.Pool(processes=NumberOfAvailableCPUs)
    return_values = instPool.map(func, list_of_tuples_of_func_params)
    instPool.close()
    instPool.join()
    return np.vstack(return_values)


def createReverseDictionary(inputDictionary):
    """Efficient way to create a reverse dictionary from a dictionary.
    Utilizes Pandas.Dataframe.groupby and Numpy arrays indexing.
    
    Parameters: 
        inputDictionary: dictionary
            Dictionary to reverse

    Returns:
        dictionary
            Reversed dictionary

    Usage:
        revDict = createReverseDictionary(Dict)
    """
    keys, values = np.array(list(inputDictionary.keys())), np.array(list(inputDictionary.values()))
    df = pd.DataFrame(np.array([[keys[i], value] for i in range(len(keys)) for value in values[i]]))
    dfGrouped = df.groupby(df.columns[1])
    keys, values = list(dfGrouped.indices.keys()), list(dfGrouped.indices.values())
    GOs = df.values.T[0]
    return dict(zip(keys, [GOs[value].tolist() for value in values]))


def createDirectories(path):
    """Create a path of directories, unless the path already exists.

    Parameters:
        path: str
            Path directory

    Returns:
        None

    Usage:
        createDirectories("/pathToFolder1/pathToSubFolder2")
    """
    if path == '':
        return
    if not os.path.exists(path):
        os.makedirs(path)