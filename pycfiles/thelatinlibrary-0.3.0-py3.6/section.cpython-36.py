# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thelatinlibrary/section.py
# Compiled at: 2019-01-13 09:19:26
# Size of source mod 2**32: 2763 bytes
from dataclasses import dataclass
from typing import List
from thelatinlibrary.tome import Tome

@dataclass
class Section:
    __doc__ = '\n    The Section class represents a\n    selection of books written by a\n    latin author.\n    '
    name: str
    tomes: List[Tome]

    def contains(self, link: str) -> bool:
        """
        Used to know if a link is already contained
        into the section.

        Args:
            link (str): The link that is being checked.

        Example:
            You can check if a link is contained into this section by using
            this method.

            >>> import thelatinlibrary
            >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
            >>> caesar
            Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')
            >>> caesar.works()
            Works(sections=[Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento',
            ..., tomes=[])
            >>> section = caesar.works().sections[0]
            >>> section.contains("http://www.thelatinlibrary.com/caesar/gall1.shtml")
            True
            >>> section.contains("http://www.thelatinlibrary.com/caesar/bc3.shtml")
            False

        Returns:
            bool: True if the link is found, otherwise False.
        """
        return any(map(lambda tome: link == tome.link, self.tomes))