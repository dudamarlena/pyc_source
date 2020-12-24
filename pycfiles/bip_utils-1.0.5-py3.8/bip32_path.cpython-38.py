# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\bip_utils\bip32_path.py
# Compiled at: 2020-04-16 09:48:59
# Size of source mod 2**32: 3971 bytes
from .bip32_utils import Bip32Utils

class Bip32PathParserConst:
    __doc__ = ' Class container for path parser constants. '
    HARDENED_CHARS = ("'", 'p')
    MASTER_CHAR = 'm'


class Bip32PathParser:
    __doc__ = ' Path parser class. It parses a BIP-0032 path and return a list of its indexes. '

    @staticmethod
    def Parse(path, skip_master=False):
        """ Validate a path.

        Args:
            path (str)                  : Path
            skip_master (bool, optional): True to skip the master in path (e.g. 0/1/2), false otherwise (e.g. m/0/1/2)

        Returns:
            list: List with path indexes
        """
        return Bip32PathParser._Bip32PathParser__ParseElems(path.split('/'), skip_master)

    @staticmethod
    def __ParseElems(path_elems, skip_master):
        """ Parse path elements.

        Args:
            path_elems (list)           : Path element list
            skip_master (bool, optional): True to skip the master in path (e.g. 0/1/2), false otherwise (e.g. m/0/1/2)

        Returns:
            list: List with path indexes
        """
        path_list = []
        for i in range(len(path_elems)):
            path_elem = path_elems[i].strip()
            if len(path_elem) == 0 and i == len(path_elems) - 1:
                pass
            elif i == 0 and not skip_master:
                if path_elem != Bip32PathParserConst.MASTER_CHAR:
                    return []
                path_list.append(Bip32PathParserConst.MASTER_CHAR)
            else:
                path_idx = Bip32PathParser._Bip32PathParser__GetElemIndex(path_elem)
                if path_idx is None:
                    return []
                path_list.append(path_idx)
        else:
            return path_list

    @staticmethod
    def __GetElemIndex(path_elem):
        """ Get index of a path element.

        Args:
            path_elem (str): Path element

        Returns:
            int: Index of the element
            None: If the element is not a valid index
        """
        is_hardened = len(path_elem) > 0 and path_elem[(-1)] in Bip32PathParserConst.HARDENED_CHARS
        if is_hardened:
            path_elem = path_elem[:-1]
        else:
            if not path_elem.isnumeric():
                return
            return is_hardened or int(path_elem)
        return Bip32Utils.HardenIndex(int(path_elem))