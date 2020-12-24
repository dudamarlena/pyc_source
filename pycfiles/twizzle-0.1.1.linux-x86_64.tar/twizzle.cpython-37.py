# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python3.7/site-packages/twizzle/twizzle.py
# Compiled at: 2019-06-24 18:49:59
# Size of source mod 2**32: 10431 bytes
from sqlitedict import SqliteDict
import numpy as np
DB_CHALLENGES_KEY = 'challenges'
DB_TESTS_KEY = 'tests'

class Twizzle(object):
    __doc__ = 'Twizzle multi purpose benchmarking system -- base class\n    '

    def __init__(self, sDBPath):
        """Constructor of the Twizzle class

        Note:
            Please pass the path of the SQLite 
            as parameter
        Args:
            sDBPath (str): Path to the SQLite database.
        """
        if sDBPath is None:
            raise Exception('Path to SQL-Database has to be defined')
        self._db = SqliteDict(sDBPath)

    def add_challenge--- This code section failed: ---

 L.  56         0  LOAD_DEREF               'sName'
                2  POP_JUMP_IF_FALSE    28  'to 28'
                4  LOAD_FAST                'aOriginalObjects'
                6  LOAD_CONST               None
                8  COMPARE_OP               is
               10  POP_JUMP_IF_TRUE     28  'to 28'
               12  LOAD_FAST                'aComparativeObjects'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_TRUE     28  'to 28'
               20  LOAD_FAST                'aTargetDecisions'
               22  LOAD_CONST               None
               24  COMPARE_OP               is
               26  POP_JUMP_IF_FALSE    36  'to 36'
             28_0  COME_FROM            18  '18'
             28_1  COME_FROM            10  '10'
             28_2  COME_FROM             2  '2'

 L.  57        28  LOAD_GLOBAL              Exception
               30  LOAD_STR                 'Parameters can not be None.'
               32  CALL_FUNCTION_1       1  '1 positional argument'
               34  RAISE_VARARGS_1       1  'exception instance'
             36_0  COME_FROM            26  '26'

 L.  58        36  LOAD_GLOBAL              len
               38  LOAD_FAST                'aOriginalObjects'
               40  CALL_FUNCTION_1       1  '1 positional argument'
               42  LOAD_GLOBAL              len
               44  LOAD_FAST                'aComparativeObjects'
               46  CALL_FUNCTION_1       1  '1 positional argument'
               48  DUP_TOP          
               50  ROT_THREE        
               52  COMPARE_OP               ==
               54  POP_JUMP_IF_FALSE    68  'to 68'
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'aTargetDecisions'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  COMPARE_OP               ==
               64  POP_JUMP_IF_TRUE     78  'to 78'
               66  JUMP_FORWARD         70  'to 70'
             68_0  COME_FROM            54  '54'
               68  POP_TOP          
             70_0  COME_FROM            66  '66'

 L.  59        70  LOAD_GLOBAL              Exception

 L.  60        72  LOAD_STR                 'Image sets and target decisions have to have the same amount of entries.'
               74  CALL_FUNCTION_1       1  '1 positional argument'
               76  RAISE_VARARGS_1       1  'exception instance'
             78_0  COME_FROM            64  '64'

 L.  61        78  LOAD_GLOBAL              all
               80  LOAD_GENEXPR             '<code_object <genexpr>>'
               82  LOAD_STR                 'Twizzle.add_challenge.<locals>.<genexpr>'
               84  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               86  LOAD_FAST                'aOriginalObjects'
               88  GET_ITER         
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  CALL_FUNCTION_1       1  '1 positional argument'
               94  POP_JUMP_IF_FALSE   114  'to 114'
               96  LOAD_GLOBAL              all
               98  LOAD_GENEXPR             '<code_object <genexpr>>'
              100  LOAD_STR                 'Twizzle.add_challenge.<locals>.<genexpr>'
              102  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              104  LOAD_FAST                'aComparativeObjects'
              106  GET_ITER         
              108  CALL_FUNCTION_1       1  '1 positional argument'
              110  CALL_FUNCTION_1       1  '1 positional argument'
              112  POP_JUMP_IF_TRUE    122  'to 122'
            114_0  COME_FROM            94  '94'

 L.  62       114  LOAD_GLOBAL              Exception

 L.  63       116  LOAD_STR                 'All objects have to be defined as path given as string.'
              118  CALL_FUNCTION_1       1  '1 positional argument'
              120  RAISE_VARARGS_1       1  'exception instance'
            122_0  COME_FROM           112  '112'

 L.  64       122  LOAD_GLOBAL              all
              124  LOAD_GENEXPR             '<code_object <genexpr>>'
              126  LOAD_STR                 'Twizzle.add_challenge.<locals>.<genexpr>'
              128  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              130  LOAD_FAST                'aTargetDecisions'
              132  GET_ITER         
              134  CALL_FUNCTION_1       1  '1 positional argument'
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  POP_JUMP_IF_TRUE    176  'to 176'
              140  LOAD_GLOBAL              isinstance
              142  LOAD_FAST                'aTargetDecisions'
              144  LOAD_GLOBAL              np
              146  LOAD_ATTR                ndarray
              148  CALL_FUNCTION_2       2  '2 positional arguments'
              150  POP_JUMP_IF_TRUE    176  'to 176'
              152  LOAD_FAST                'aTargetDecisions'
              154  LOAD_ATTR                dtype
              156  LOAD_GLOBAL              np
              158  LOAD_METHOD              dtype
              160  LOAD_STR                 'bool'
              162  CALL_METHOD_1         1  '1 positional argument'
              164  COMPARE_OP               ==
              166  POP_JUMP_IF_TRUE    176  'to 176'

 L.  65       168  LOAD_GLOBAL              Exception
              170  LOAD_STR                 'The target decisions have to be boolean only.'
              172  CALL_FUNCTION_1       1  '1 positional argument'
              174  RAISE_VARARGS_1       1  'exception instance'
            176_0  COME_FROM           166  '166'
            176_1  COME_FROM           150  '150'
            176_2  COME_FROM           138  '138'

 L.  68       176  LOAD_FAST                'self'
              178  LOAD_ATTR                _db
              180  LOAD_METHOD              get
              182  LOAD_GLOBAL              DB_CHALLENGES_KEY
              184  BUILD_LIST_0          0 
              186  CALL_METHOD_2         2  '2 positional arguments'
              188  STORE_FAST               'aChallenges'

 L.  72       190  LOAD_CLOSURE             'sName'
              192  BUILD_TUPLE_1         1 
              194  LOAD_LISTCOMP            '<code_object <listcomp>>'
              196  LOAD_STR                 'Twizzle.add_challenge.<locals>.<listcomp>'
              198  MAKE_FUNCTION_8          'closure'
              200  LOAD_FAST                'aChallenges'
              202  GET_ITER         
              204  CALL_FUNCTION_1       1  '1 positional argument'
              206  STORE_FAST               'aChallengesSameName'

 L.  73       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'aChallengesSameName'
              212  CALL_FUNCTION_1       1  '1 positional argument'
              214  LOAD_CONST               0
              216  COMPARE_OP               !=
              218  POP_JUMP_IF_FALSE   232  'to 232'

 L.  74       220  LOAD_GLOBAL              Exception

 L.  75       222  LOAD_STR                 'Challenge name %s is already in use. Define an other one. Aborting.'
              224  LOAD_DEREF               'sName'
              226  BINARY_MODULO    
              228  CALL_FUNCTION_1       1  '1 positional argument'
              230  RAISE_VARARGS_1       1  'exception instance'
            232_0  COME_FROM           218  '218'

 L.  78       232  LOAD_DEREF               'sName'
              234  LOAD_FAST                'aOriginalObjects'

 L.  79       236  LOAD_FAST                'aComparativeObjects'
              238  LOAD_FAST                'aTargetDecisions'
              240  LOAD_CONST               ('challenge', 'originalObjects', 'comparativeObjects', 'targetDecisions')
              242  BUILD_CONST_KEY_MAP_4     4 
              244  STORE_FAST               'dicChallenge'

 L.  81       246  LOAD_FAST                'dicMetadata'
          248_250  POP_JUMP_IF_FALSE   260  'to 260'

 L.  82       252  LOAD_FAST                'dicMetadata'
              254  LOAD_FAST                'dicChallenge'
              256  BUILD_MAP_UNPACK_2     2 
              258  STORE_FAST               'dicChallenge'
            260_0  COME_FROM           248  '248'

 L.  83       260  LOAD_FAST                'aChallenges'
              262  LOAD_METHOD              append
              264  LOAD_FAST                'dicChallenge'
              266  CALL_METHOD_1         1  '1 positional argument'
              268  POP_TOP          

 L.  84       270  LOAD_FAST                'aChallenges'
              272  LOAD_FAST                'self'
              274  LOAD_ATTR                _db
              276  LOAD_GLOBAL              DB_CHALLENGES_KEY
              278  STORE_SUBSCR     

 L.  85       280  LOAD_FAST                'self'
              282  LOAD_ATTR                _db
              284  LOAD_METHOD              commit
              286  CALL_METHOD_0         0  '0 positional arguments'
              288  POP_TOP          

Parse error at or near `COME_FROM' instruction at offset 36_0

    def del_challenge(self, sName):
        """ deletes an existing challenge by its name

        Args:
            sName (str): the name of the challenge to be deleted

        Returns:
            None
        """
        aChallenges = self._db.getDB_CHALLENGES_KEY[]
        aMatches = [ch for ch in aChallenges if ch['challenge'] == sName]
        if len(aMatches) == 0:
            raise Exception('No challenge named %s found.' % sName)
        aChallenges.removeaMatches[0]
        self._db[DB_CHALLENGES_KEY] = aChallenges
        self._db.commit

    def get_challenges(self):
        """ getting a list of all defined challenges

        Returns:
            :obj:`list` of :obj:: `obj`:  List of all defined challenges
        """
        return self._db.getDB_CHALLENGES_KEY[]

    def get_challenge(self, sChallengeName):
        """ getting a single challenge object

        Args:
            sChallengeName (str): the name of the challenge to get

          Returns:
            :obj:: `obj`:  Object defining the challenge having the name sChallengeName
        """
        aChallenges = self._db.getDB_CHALLENGES_KEY[]
        aMatches = [ch for ch in aChallenges if ch['challenge'] == sChallengeName]
        if len(aMatches) == 0:
            raise Exception('No challenge with name %s found.' % sChallengeName)
        return aMatches[0]

    def clear_challenges(self):
        """ clears all challenge entries from the database """
        self._db[DB_CHALLENGES_KEY] = []
        self._db.commit

    def run_test(self, sChallengeName, fnCallback, dicCallbackParameters={}, autosave_to_db=False):
        """ run single challenge as test using given callback function and optional params

        Note:
            fnCallback has to fullfill following specifications

            Parameters:
            fnCallback(aOriginalObjects, aComparativeObjects, **dicCallbackParameters)
            - aOriginalObjects: list of strings describing paths to original objects
            - aComparativeObjects: list of strings describing paths to comparative objects
            ... arbitrary number of further parameters

            Returns:
            aDecisions, dicAdditionalInformation = fnCallback(...)
            - aDecisions: list of boolean decisions describing wether the algorithm has decided that the original object 
                          and the comparative objects are the same (True) or not (False)
            - dicAdditionalInformation: the algorithm can supply additional information that can be used in the evaluation 
                                        later on to compare different settings

        Args:
            sChallengeName (str): the challenge that should be executed
            fnCallback (function): Pointer to wrapper-function that tests a challenge on a specific algorithm
                                    and makes decisions whether the objects are the same or not depending on its decision algorithm
            dicCallbackParameters (:obj:): Dictionary defining parameters for the function in fnCallback

        Returns:
            dicTest: dictionary of test results that can be saved to db
        """
        if not (sChallengeName and fnCallback):
            raise Exception('Parameters are not allowed to be None.')
        dicChallenge = self.get_challengesChallengeName
        sChallengeName = dicChallenge['challenge']
        aOriginalObjects = dicChallenge['originalObjects']
        aComparativeObjects = dicChallenge['comparativeObjects']
        aTargetDecisions = dicChallenge['targetDecisions']
        aDecisions, dicAdditionalInformation = fnCallback(
         aOriginalObjects, aComparativeObjects, **dicCallbackParameters)
        if len(aDecisions) != len(aTargetDecisions):
            raise Exception('Array of Decisions is not the same size as given set of objects. Aborting.')
        lTestsetSize = len(aTargetDecisions)
        lErrors = np.count_nonzero(np.arrayaDecisions != np.arrayaTargetDecisions)
        dErrorRate = lErrors / lTestsetSize
        lTP = np.sumnp.logical_and(aDecisions == True)(aTargetDecisions == True)
        lTN = np.sumnp.logical_and(aDecisions == False)(aTargetDecisions == False)
        lFP = np.sumnp.logical_and(aDecisions == True)(aTargetDecisions == False)
        lFN = np.sumnp.logical_and(aDecisions == False)(aTargetDecisions == True)
        dAccuracy = (lTP + lTN) / (lTP + lTN + lFP + lFN)
        dPrecision = lTP / (lTP + lFP)
        dRecall = lTP / (lTP + lFN)
        dF1score = 2 * (dPrecision * dRecall / (dPrecision + dRecall))
        dFAR = lFP / (lFP + lTN)
        dFRR = lFP / (lFP + lTN)
        dicTest = dicAdditionalInformation
        dicTest['challenge'] = sChallengeName
        dicTest['errorrate'] = dErrorRate
        dicTest['TP'] = lTP
        dicTest['TN'] = lTN
        dicTest['FP'] = lFP
        dicTest['FN'] = lFN
        dicTest['accuracy'] = dAccuracy
        dicTest['recall'] = dRecall
        dicTest['precision'] = dPrecision
        dicTest['F1_score'] = dF1score
        dicTest['FAR'] = dFAR
        dicTest['FRR'] = dFRR
        if autosave_to_db:
            self._Twizzle__save_testdicTest
        return dicTest

    def __save_test(self, dicTest):
        """ saves a test object to the database"""
        if not dicTest:
            raise Exception('Test object must not be None.')
        aTests = self._db.getDB_TESTS_KEY[]
        aTests.appenddicTest
        self._db[DB_TESTS_KEY] = aTests
        self._db.commit

    def save_test_threadsafe(self, dicTest, lock):
        """ saves a test object to the database threadsafe"""
        lock.acquire
        self._Twizzle__save_testdicTest
        lock.release

    def get_tests(self):
        """getting all tests

        Returns:
            :obj:`list` of :obj:: `obj`:  List of all tests executed
        """
        return self._db.getDB_TESTS_KEY[]

    def clear_tests(self):
        """ delete all tests from the database """
        self._db[DB_TESTS_KEY] = []
        self._db.commit