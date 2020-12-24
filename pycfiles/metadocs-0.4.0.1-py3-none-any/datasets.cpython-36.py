# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/victor/Documents/Experiments/test-sphynx/v5/PROJECT/moduleD/datasets/datasets.py
# Compiled at: 2018-02-20 08:47:55
# Size of source mod 2**32: 1123 bytes


class Dataset:
    __doc__ = 'Dataset abstract class\n    '

    def __init__(self, name, data):
        """Initialize dataset from name and data it should hold

        Args:
            name (str): Dataset's name
            data (pd.DataFrame): data to store
        """
        self.name = name
        self.data = data

    def get(self, key):
        """get the value for key

        Args:
            key (str): what we're looking for

        Raises:
            NotImplementedError: [abstract method here]

        .. note:: This function accepts only :class:`str` parameters.
        .. warning:: Not implementing this in child classes
             will cause :exc:`NotImplementedError` exception!
        """
        raise NotImplementedError('Method get is not implemented')


class COSI1(Dataset):
    __doc__ = 'Very smart COSI1 dataset class\n    '

    def get(self, key):
        """returns one only value: [key] yes

        Args:
            key (str): what we're looking for

        Returns:
            str: Dummy string
        """
        if key:
            return '[{}] yes'.format(key)
        else:
            return ''