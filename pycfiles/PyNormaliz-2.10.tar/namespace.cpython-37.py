# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/schema/namespace.py
# Compiled at: 2019-05-19 18:32:04
# Size of source mod 2**32: 4171 bytes
from norm.executable import NormExecutable, NormError
from norm.executable.schema.type import TypeName
from norm.models import Status
import logging
from norm.models.norm import new_version
logger = logging.getLogger(__name__)

class Import(NormExecutable):

    def __init__(self, namespace=None, type_=None, variable=None):
        """
        Import the namespace, if the variable name is given, the imported type is cloned to the
        current context with the variable name
        :param namespace: the namespace
        :type namespace: str
        :param type_: the type
        :type type_: TypeName
        :param variable: the variable
        :type variable: str
        """
        super().__init__()
        assert namespace is not None
        assert namespace != ''
        self.namespace = namespace
        self.type_ = type_
        self.variable = variable

    def compile(self, context):
        """
        Imports follow the following logic:
            * imported namespace is stored in the context
            * imported type is cloned in the context namespace as a draft
            * imported type with alias is cloned and renamed in the context namespace as a draft
        """
        if self.namespace not in context.search_namespaces:
            context.search_namespaces.append(self.namespace)
        elif self.type_:
            if self.type_.namespace != self.namespace:
                self.type_.namespace = self.namespace
                self.type_.compile(context)
            lam = self.type_.lam
            if lam is None:
                msg = 'Can not find the type {} in namespace {}'.format(self.type_.name, self.namespace)
                logger.error(msg)
                raise NormError(msg)
            if self.variable:
                alias = lam.clone()
                alias.namespace = context.context_namespace
                alias.name = self.variable
                context.session.add(alias)
                self.lam = alias
            else:
                self.lam = lam
        else:
            from norm.models.norm import Lambda
            self.lam = Lambda(self.namespace, '*')
        return self


class Export(NormExecutable):

    def __init__(self, namespace=None, type_=None, alias=None):
        """
        Export the type to the namespace
        :param namespace: the namespace
        :type namespace: str or None
        :param type_: the type
        :type type_: TypeName
        :param alias: the alias in the namespace
        :type alias: str or None
        """
        super().__init__()
        assert type_ is not None
        self.namespace = namespace
        self.type_ = type_
        self.alias = alias

    def compile(self, context):
        session = context.session
        lam = self.type_.lam
        if lam is None:
            msg = 'Can not find the type {} in namespace {}'.format(self.type_.name, self.type_.namespace)
            logger.error(msg)
            raise NormError(msg)
        if lam.status != Status.DRAFT:
            msg = 'Type {} is not in the draft status'
            logger.error(msg)
            raise NormError(msg)
        elif self.namespace is None or self.namespace.strip() == '':
            if lam.cloned_from:
                lam.namespace = lam.cloned_from.namespace
            else:
                lam.namespace = context.user_namespace
        else:
            lam.namespace = self.namespace
        old_lam_name = lam.name
        if self.alias:
            lam.name = self.alias
        lam.version = new_version()
        lam.status = Status.READY
        new_lam = lam.clone()
        new_lam.namespace = context.context_namespace
        new_lam.name = old_lam_name
        session.add(new_lam)
        from norm.config import cache
        cache[(context.context_namespace, new_lam.name, None, None)] = new_lam
        self.lam = lam
        return self