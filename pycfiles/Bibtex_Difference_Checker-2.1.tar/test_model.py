# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Ziauddin/Documents/bibtex_diff_checker/bibtex_diff_checker/test/test_model.py
# Compiled at: 2016-01-09 13:25:54
from model import *
from controller import *
import unittest
from unqlite import *

class ModelTest(unittest.TestCase):

    def test_change_record_db(self):
        list1 = []
        list1.append({'title': 'Haskino: {H}askell and {A}rduino', 'booktitle': 'Practical Aspects of Declarative Languages', 'author': 'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', 'year': '2016', 'ENTRYTYPE': 'inproceedings'})
        (list1.append({'numpages': '12', 'publisher': 'ACM', 'doi': '10.1145/2804302.2804311', 'keyword': 'Design Pattern, FFI, Monads, Remote Procedure Call', 'title': 'The Remote Monad Design Pattern', 'xxurl': 'https://www.youtube.com/watch?v=guMLPr6eBLo', 'booktitle': 'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', 'author': 'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', 'abstract': 'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': 'inproceedings', 'link': 'http://dl.acm.org/citation.cfm?id=2804311', 'location': 'Vancouver, BC, Canada', 'xurl': 'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', 'pages': '59--70', 'address': 'New York, NY, USA'}),)
        test_db = UnQLite()
        test_coll = test_db.collection('test')
        test_coll.create()
        test_coll.store(list1)
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2 = []
        list2.append(('Grebe:15:Haskino', ('year', '2016', 1, rb), ('year', '2017', 1, rb)))
        change_property_db(list2, test_coll)
        actual = test_coll.filter(lambda obj: obj['ID'].startswith('Grebe:15:Haskino'))
        expected_year = '2017'
        assert actual[0]['year'] == expected_year
        tk.destroy()

    def test_add_record_db(self):
        list1 = []
        list1.append({'title': 'Haskino: {H}askell and {A}rduino', 'booktitle': 'Practical Aspects of Declarative Languages', 'author': 'Grebe, Mark and Gill, Andy', 'ID': 'Grebe:15:Haskino', 'year': '2016', 'ENTRYTYPE': 'inproceedings'})
        (list1.append({'numpages': '12', 'publisher': 'ACM', 'doi': '10.1145/2804302.2804311', 'keyword': 'Design Pattern, FFI, Monads, Remote Procedure Call', 'title': 'The Remote Monad Design Pattern', 'xxurl': 'https://www.youtube.com/watch?v=guMLPr6eBLo', 'booktitle': 'Proceedings of the 8th ACM SIGPLAN Symposium on Haskell', 'author': 'Andy Gill and Neil Sculthorpe and Justin Dawson and\nAleksander Eskilson and Andrew Farmer and Mark Grebe\nand Jeffrey Rosenbluth and Ryan Scott and James\nStanton', 'abstract': 'Remote Procedure Calls are expensive.  This paper\ndemonstrates how to reduce the cost of calling\nremote procedures from Haskell by using the\n\\emph{remote monad design pattern}, which amortizes\nthe cost of remote calls.  This gives the Haskell\ncommunity access to remote capabilities that are not\ndirectly supported, at a surprisingly inexpensive\ncost.\n\nWe explore the remote monad design pattern\nthrough six models of remote execution patterns, using a simulated Internet of Things toaster as a\nrunning example.  We consider the expressiveness and\noptimizations enabled by each remote execution\nmodel, and assess the feasibility of our approach.\nWe then present a full-scale case study: a Haskell\nlibrary that provides a Foreign Function Interface\nto the JavaScript Canvas API.  Finally, we discuss\nexisting instances of the remote monad design\npattern found in Haskell libraries.', 'ENTRYTYPE': 'inproceedings', 'link': 'http://dl.acm.org/citation.cfm?id=2804311', 'location': 'Vancouver, BC, Canada', 'xurl': 'http://www.ittc.ku.edu/csdl/fpg/files/Gill-15-RemoteMonad.pdf', 'ID': 'Gill:15:RemoteMonad', 'pages': '59--70', 'address': 'New York, NY, USA'}),)
        test_db = UnQLite()
        test_coll = test_db.collection('test')
        test_coll.create()
        test_coll.store(list1)
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2 = []
        list2.append(('Grebe:15:Haskino', ('object', 'Nothing', 1, rb)))
        add_property_db(list2, test_coll)
        actual = test_coll.filter(lambda obj: obj['ID'].startswith('Grebe:15:Haskino'))
        expected_prop_val = 'Nothing'
        assert actual[0]['object'] == expected_prop_val
        tk.destroy()

    def test_update_bibtexDB(self):
        str = '@inproceedings{Grebe:15:Haskino,\n          year={2016},\n          booktitle={Practical Aspects of Declarative Languages},\n          title={Haskino: {H}askell and {A}rduino},\n          author={Grebe, Mark and Gill, Andy}\n        }\n        '
        bib_database = bibtexparser.loads(str)
        test_db = UnQLite()
        test_coll = test_db.collection('test')
        test_coll.create()
        test_coll.store(bib_database.entries)
        import Tkinter
        tk = Tk()
        rb = IntVar()
        rb.set(1)
        list2 = []
        list2.append(('Grebe:15:Haskino', ('object', 'Nothing', 1, rb)))
        add_property_db(list2, test_coll)
        update_bibtex(True, bib_database, test_coll)
        actual = test_coll.filter(lambda obj: obj['ID'].startswith('Grebe:15:Haskino'))
        expected_prop_val = 'Nothing'
        assert actual[0]['object'] == expected_prop_val
        for elem in bib_database.entries:
            result = elem

        assert result['object'] == 'Nothing'
        tk.destroy()


if __name__ == '__main__':
    unittest.main()