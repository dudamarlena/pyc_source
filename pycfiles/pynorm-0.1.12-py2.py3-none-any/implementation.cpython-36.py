# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ax/Workspace/norm/norm/executable/schema/implementation.py
# Compiled at: 2019-05-21 17:25:41
# Size of source mod 2**32: 4164 bytes
from pandas import DataFrame, Series, Index
from norm.executable import NormExecutable
from norm.executable.schema.declaration import TypeDeclaration
from norm.executable.expression import NormExpression
from norm.models import Lambda, Status
import logging
logger = logging.getLogger(__name__)

class TypeImplementation(NormExecutable):

    def __init__(self, type_, op, query, description):
        super().__init__()
        self.type_ = type_
        self.op = op
        self.query = query
        self.description = description

    def compile(self, context):
        """
        Three types of implementations
            * new implementation (:=) removes all revisions from this version
            * conjunctive implementation (&=)
            * disjunctive implementation (|=)
        """
        lam = self.type_.lam
        if lam.status != Status.DRAFT:
            logger.info('Lambda: {} is not in DRAFT mode. Import first'.format(lam))
            lam = Lambda(namespace=(context.context_namespace), name=(lam.name), description=(lam.description), variables=(lam.variables),
              user=(context.user))
        if self.description is not None:
            if self.description.strip() != '':
                self.query.description = self.description
        self.lam = lam
        return self

    def execute(self, context):
        from norm.engine import ImplType
        from norm.models.norm import RevisionType
        lam = self.lam
        delta = self.query.execute(context)
        if isinstance(delta, DataFrame):
            if self.query.lam is not self.lam:
                if self.lam is not self.query.lam.cloned_from:
                    delta.index.name = ''
            if delta.index.name != lam.VAR_OID:
                delta = lam.fill_primary(delta)
                delta = lam.fill_time(delta)
                delta = lam.fill_oid(delta)
        elif isinstance(delta, Index):
            assert delta.name == lam.VAR_OID
            cols = [v.name for v in lam.variables if v.name in self.query.lam]
            delta = self.query.lam.data.loc[(delta, cols)]
            delta = lam.fill_primary(delta)
            delta = lam.fill_time(delta)
            delta = lam.fill_oid(delta.reset_index(drop=True))
        else:
            qs = str(self.query)
            if self.op == ImplType.DEF:
                if any(rev.query == qs for rev in lam.revisions):
                    return lam
                if len(lam.revisions) > 0:
                    lam.remove_revisions()
                lam.revise(qs, self.description, delta, RevisionType.DISJUNCTION)
            else:
                if self.op == ImplType.OR_DEF:
                    lam.revise(qs, self.description, delta, RevisionType.DISJUNCTION)
                elif self.op == ImplType.AND_DEF:
                    if isinstance(delta, Series):
                        if len(delta) == 1:
                            vname = delta.name
                            vvalue = delta.values[0]
                            delta = DataFrame(index=(lam.data.index))
                            delta[vname] = vvalue
                            delta = lam.fill_time(delta)
                        else:
                            if delta.index.name == lam.VAR_OID:
                                delta = DataFrame(delta)
                                delta = lam.fill_time(delta)
                    else:
                        if isinstance(delta, DataFrame):
                            delta = lam.fill_time(delta)
                        lam.revise(qs, self.description, delta, RevisionType.CONJUNCTION)
        return lam