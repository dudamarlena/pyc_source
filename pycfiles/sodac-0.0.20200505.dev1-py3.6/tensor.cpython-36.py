# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/tensor.py
# Compiled at: 2020-05-05 13:45:11
# Size of source mod 2**32: 4621 bytes
import collections, copy, logging, cached_property
from haoda import ir
from haoda import util
from soda import grammar
import soda.util
_logger = logging.getLogger().getChild(__name__)

class Tensor:
    __doc__ = 'A tensor that corresponse to an input, local, or output.\n\n  This class is used in the high-level DAG for stencil dependency analysis.\n  Each tensor either is an input tensor, or has at least 1 parent tensor, which\n  will be used to generate this tensor. Meanwhile, each tensor either is an\n  output tensor, or has at least 1 child tensor, which will be computed using\n  this tensor.\n\n  Attributes:\n    haoda_type: str, type of the tensor element.\n    parents: Dict from str of name of Tensor to Tensor.\n    children: Dict from str of name of Tensor to Tensor.\n    st_ref: Ref, name, index, and latency stored.\n    offset: int, shift offset in terms of data elements\n    lets: Lets of computation.\n    expr: Expr of computation.\n    ld_refs: Dict from str of name to dict of Ref loaded.\n\n  Property:\n    name: str, unique in each SODA program.\n    st_offset: int, stencil offset in terms of data elements.\n    st_idx, Tuple of int, the index referenced by its parent stage.\n    ld_indices: Dict from str of name to dict of accessed indices of the input.\n    ld_offsets: Dict from str of name to dict of offsets of the input.\n  '

    def __init__(self, stmt, tile_size):
        self.haoda_type = stmt.haoda_type
        self._tile_size = tile_size
        if isinstance(stmt, grammar.LocalStmtOrOutputStmt):
            self.st_ref = copy.copy(stmt.ref)
            self.st_ref.parent = self
            self.lets = stmt.let
            self.expr = stmt.expr
        else:
            if isinstance(stmt, grammar.InputStmt):
                self._name = stmt.name
                self.st_ref = None
                self.lets = []
                self.expr = None
            else:
                raise util.InternalError('cannot initialize a Tensor from %s' % type(stmt))
        _logger.debug('tensor initialized from stmt `%s`', stmt)
        _logger.debug('                   at tx position %d', stmt._tx_position)
        self.parents = collections.OrderedDict()
        self.children = collections.OrderedDict()
        self.ld_refs = collections.OrderedDict()

    @property
    def name(self):
        if self.st_ref is not None:
            return self.st_ref.name
        else:
            return self._name

    @property
    def st_idx(self):
        if self.st_ref is not None:
            return self.st_ref.idx
        else:
            return (0, ) * len(self._tile_size)

    @property
    def st_offset(self):
        return soda.util.serialize(self.st_idx, self._tile_size)

    @cached_property.cached_property
    def ld_indices(self):
        return collections.OrderedDict((name,
         collections.OrderedDict((ref.idx, ref) for ref in refs)) for name, refs in self.ld_refs.items())

    @cached_property.cached_property
    def ld_offsets(self):
        return collections.OrderedDict((name,
         collections.OrderedDict((soda.util.serialize(ref.idx, self._tile_size), ref) for ref in refs)) for name, refs in self.ld_refs.items())

    @property
    def c_type(self):
        return self.haoda_type.c_type

    def propagate_type(self):
        if self.expr is None:
            return
        var_types = {}
        for let in self.lets:
            var_types[let.name] = let.haoda_type

        def visit_haoda_type(obj, args):
            if obj.haoda_type is None:
                if isinstance(obj, ir.Var):
                    obj.haoda_type = var_types[obj.name]
            return obj

        self.lets = tuple(_.visit(visit_haoda_type) for _ in self.lets)
        self.expr = self.expr.visit(visit_haoda_type)
        self.st_ref = self.st_ref.visit(visit_haoda_type)

    def mutate(self, callback, args=None):
        self.lets = tuple(_.visit(callback, args) for _ in self.lets)
        self.expr = self.expr.visit(callback, args)
        self.st_ref = self.st_ref.visit(callback, args)

    def visit_loads(self, callback, args=None):
        for let in self.lets:
            let.visit(callback, args)

        self.expr.visit(callback, args)

    def __str__(self):
        return 'Tensor\n  {haoda_type}: {name} = {expr}\n  store: {st_ref}\n  parents: {parents}\n  children: {children}'.format(name=(self.name),
          haoda_type=(self.haoda_type),
          expr=(self.expr),
          parents=(util.idx2str(self.parents)),
          children=(util.idx2str(self.children)),
          st_ref=(str(self.st_ref)))

    def is_output(self):
        return len(self.children) == 0

    def is_input(self):
        return len(self.parents) == 0

    def is_producer(self):
        return not self.is_output()

    def is_consumer(self):
        return not self.is_input()