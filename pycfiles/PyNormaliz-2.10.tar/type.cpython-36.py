# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/schema/type.py
# Compiled at: 2019-05-20 17:29:00
# Size of source mod 2**32: 2677 bytes
from norm.executable import NormError, NormExecutable
from norm.models import ListLambda, Lambda, Variable, Status
import logging
logger = logging.getLogger(__name__)

class TypeName(NormExecutable):

    def __init__(self, name, version=None):
        """
        The type qualified name
        :param name: name of the type
        :type name: str
        :param version: version of the type
        :type version: str
        """
        super().__init__()
        self.namespace = None
        self.name = name
        self.version = version
        if not self.name is not None:
            raise AssertionError
        elif not self.name != '':
            raise AssertionError

    def __str__(self):
        s = self.namespace + '.' if self.namespace else ''
        s += self.name
        s += self.version if self.version is not None else '$latest'
        return s

    def compile(self, context):
        """
        Retrieve the Lambda function by namespace, name, version.
        Note that user is encoded by the version.
        :rtype: Lambda
        """
        if self.namespace is None:
            lam = self.try_retrieve_type(context.session, context.context_namespace, self.name, self.version)
            if lam is None:
                lam = self.try_retrieve_type(context.session, context.search_namespaces, self.name, self.version, Status.READY)
        else:
            if self.namespace == context.context_namespace:
                lam = self.try_retrieve_type(context.session, self.namespace, self.name, self.version)
            else:
                lam = self.try_retrieve_type(context.session, self.namespace, self.name, self.version, Status.READY)
        self.lam = lam
        return self


class ListType(NormExecutable):

    def __init__(self, intern):
        super().__init__()
        self.intern = intern

    def compile(self, context):
        """
        Return a list type
        :rtype: ListLambda
        """
        lam = self.intern.lam
        if lam.id is None:
            msg = '{} does not seem to be declared yet'.format(self.intern)
            logger.error(msg)
            raise NormError(msg)
        else:
            q = context.session.query(ListLambda, Variable).join(ListLambda.variables).filter(Variable.type_id == lam.id)
            llam = q.first()
            if llam is None:
                llam = ListLambda(lam)
                context.session.add(llam)
            else:
                llam = llam[0]
        self.lam = llam
        return self