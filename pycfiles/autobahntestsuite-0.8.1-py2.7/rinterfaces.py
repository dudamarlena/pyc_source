# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/autobahntestsuite/rinterfaces.py
# Compiled at: 2018-12-17 11:51:20
__all__ = ('RITestDb', 'RITestRunner')
import zope
from zope.interface import Interface, Attribute

class RITestDb(Interface):
    """
   A Test database provides storage and query capabilities for test cases, results and related data.

   This interface is remoted as a set of WAMP endpoints.
   """
    URI = Attribute('The base URI under which methods are exposed for WAMP.')

    def importSpec(spec):
        """
      Import a test specification into the test database.

      Returns a pair `(op, id)`, where `op` specifies the operation that
      actually was carried out:

          - None: unchanged
          - 'U': updated
          - 'I': inserted

      The `id` is the new (or existing) database object ID for the spec.
      """
        pass

    def getSpecs(activeOnly=True):
        """
      """
        pass

    def getSpec(specId):
        """
      """
        pass

    def getSpecByName(name):
        """
      Find a (currently active, if any) test specification by name.
      """
        pass

    def getTestRuns(limit=10):
        """
      Return a list of latest testruns.
      """
        pass

    def getTestResult(resultId):
        """
      Get a single test result by ID.

      :param resultId: The ID of the test result to retrieve.
      :type resultId: str
      :returns Deferred -- A single instance of TestResult.
      """
        pass

    def getTestRunIndex(runId):
        """
      """
        pass

    def getTestRunSummary(runId):
        """
      """
        pass


class RITestRunner(Interface):
    """
   """

    def run(specName, saveResults=True):
        """
      """
        pass