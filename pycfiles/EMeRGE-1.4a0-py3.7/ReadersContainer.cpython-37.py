# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\ResultDashboard\ReadersContainer.py
# Compiled at: 2020-02-02 04:10:03
# Size of source mod 2**32: 1566 bytes
"""
All file reader must inherit 'FileReader' class and implement the readfile function appropriately

List of file readers implemented currently

CSVReader - takes csvfile and kwargs spits out pandas dataframe
TomlReader - takes tomlfile and splits out dictionary
PickleReader - takes pickle file and splits out what had been stored

"""

def ReadFromFile(filepath, **kwargs):
    import os
    file_extension = os.path.splitext(filepath)[(-1)].lower()
    assert file_extension in Mapping_dict, '{} is not yet implemented to read ....'.format(file_extension)
    return ReaderWrapper((Mapping_dict[file_extension]), filepath, **kwargs)


def ReaderWrapper(ReaderClass, filepath, **kwargs):
    return (ReaderClass.ReadFile)(filepath, **kwargs)


class FileReader:

    def ReadFile(filepath, **kwargs):
        pass


class ReadPickle(FileReader):

    def ReadFile(picklefilepath, **kwargs):
        import pickle
        return pickle.load(open(picklefilepath, 'rb'))


class ReadCSV(FileReader):

    def ReadFile(csvfilepath, **kwargs):
        import pandas as pd
        return (pd.read_csv)(csvfilepath, **kwargs)


class ReadToml(FileReader):

    def ReadFile(tomlfilepath, **kwargs):
        import toml
        texts = ''
        file = open(tomlfilepath, 'r')
        contents = texts.join(file.readlines())
        content_dict = toml.loads(contents, _dict=dict)
        return content_dict


Mapping_dict = {'.csv':ReadCSV, 
 '.toml':ReadToml, 
 '.p':ReadPickle}