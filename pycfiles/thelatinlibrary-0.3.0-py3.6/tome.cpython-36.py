# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thelatinlibrary/tome.py
# Compiled at: 2019-01-13 09:45:03
# Size of source mod 2**32: 3884 bytes
from dataclasses import dataclass
from typing import List, Optional
import requests
from bs4 import BeautifulSoup
from thelatinlibrary import settings

@dataclass
class Tome:
    __doc__ = '\n    The Tome class represents one of the\n    multiple volumes used to write a book.\n    '
    link: str
    name: str
    _text = ''

    def text(self, reload: Optional[bool]=None, save: Optional[bool]=None) -> List[str]:
        """
        The text contained in the tome.

        Args:
            reload (Optional[bool]): If the response should be reloaded and the already stored content ignored.
            save (Optional[bool]): If the response should be saved.

        Example:
            You can get what an author wrote in a tome using this method.

            >>> import thelatinlibrary
            >>> caesar = thelatinlibrary.get_author("http://www.thelatinlibrary.com/caes.html")
            >>> caesar
            Author(link='http://www.thelatinlibrary.com/caes.html', name='Caesar')
            >>> works = caesar.works()
            >>> works
            Works(sections=[Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento',
            ..., tomes=[])
            >>> de_bello_gallico = works.sections[0]
            >>> de_bello_gallico
            Section(name='Commentariorum Libri VII De Bello Gallico Cum A. Hirti Supplemento', ...
            Tome(link='http://www.thelatinlibrary.com/caesar/gall8.shtml', name='Liber VIII')])
            >>> tome = de_bello_gallico.tomes[0]
            >>> tome
            Tome(link='http://www.thelatinlibrary.com/caesar/gall1.shtml', name='Liber I')
            >>> tome.text()
            ['[1] 1 Gallia est omnis divisa in partes tres, ...', ..., '...ad conventus agendos profectus est.']

        Return:
            List[str]: All the paragraphs of the tome.
        """
        if reload is None:
            reload = settings.reload
        else:
            if save is None:
                save = settings.save
            if not reload:
                if self._text:
                    return self._text
        text = requests.get(self.link).text
        parser = BeautifulSoup(text, 'html5lib')
        if '404' in parser.title.string:
            return []
        else:
            paragraphs = []
            texts = list(parser.find_all('p'))[1:-1]
            for text in texts:
                paragraphs.append(text.text.strip().rstrip())

            if save:
                self._text = paragraphs
            return paragraphs