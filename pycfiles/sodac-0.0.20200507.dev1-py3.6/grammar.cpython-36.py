# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soda/grammar.py
# Compiled at: 2020-05-07 15:50:46
# Size of source mod 2**32: 7272 bytes
from typing import Dict, Tuple
import logging, toposort
from haoda import ir, util
from haoda.ir.arithmetic import base
_logger = logging.getLogger().getChild(__name__)
GRAMMAR = "\nSodaProgram:\n(\n  ('border' ':' border=BorderStrategies)?\n  ('burst' 'width' ':' burst_width=INT)\n  ('cluster' ':' cluster=ClusterStrategies)?\n  ('iterate' ':' iterate=INT)\n  ('kernel' ':' app_name=ID)\n  ('unroll' 'factor' ':' unroll_factor=INT)\n  (input_stmts=InputStmt)+\n  (param_stmts=ParamStmt)*\n  (local_stmts=LocalStmt)*\n  (output_stmts=OutputStmt)+\n)#;\n\nYesOrNo: 'yes'|'no';\n\nBorderStrategies: 'ignore'|'preserve';\nClusterStrategies: 'none'|'fine'|'coarse'|'full';\n\nComment: /\\s*#.*$/;\n\nInputStmt: 'input' ('dram' dram=INT ('.' dram=INT)*)? haoda_type=Type ':' name=ID ('(' (tile_size=INT ',')* '*' ')')?;\nLocalStmt: 'local' haoda_type=Type ':' (let=Let)* ref=Ref '=' expr=Expr;\nOutputStmt: 'output' ('dram' dram=INT ('.' dram=INT)*)? haoda_type=Type ':' (let=Let)* ref=Ref '=' expr=Expr;\n\nParamStmt: 'param' ('dram' dram=INT ('.' dram=INT)*)? haoda_type=Type (',' attr=ParamAttr)* ':' name=ID ('[' size=INT ']')*;\nParamAttr: 'dup' dup=Int | partitioning=Partitioning;\nPartitioning:\n  'partition' strategy='complete' ('dim' '=' dim=Int)? |\n  'partition' strategy='cyclic' 'factor' '=' factor=Int ('dim' '=' dim=Int)?;\n" + ir.GRAMMAR

class InputStmt(ir.Node):
    __doc__ = 'Node for input statement, represents a tiled input tensor.\n\n  Attributes:\n    haoda_type: Type of this input tensor.\n    dram: [int], dram id used to read this input\n    name: str, name of this input tensor.\n    tile_size: list of tile sizes. The last dimension should be 0.\n  '
    SCALAR_ATTRS = ('haoda_type', 'name')
    LINEAR_ATTRS = ('tile_size', 'dram')

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        if not self.dram:
            self.dram = (0, )
        self.tile_size += (0, )

    def __str__(self):
        result = 'input {}: {}'.format(self.haoda_type, self.name)
        if self.tile_size[:-1]:
            result += '({}, *)'.format(', '.join(map(str, self.tile_size[:-1])))
        return result


class LocalStmtOrOutputStmt(ir.Node):
    SCALAR_ATTRS: Tuple[(str, ...)]
    LINEAR_ATTRS: Tuple[(str, ...)]
    SCALAR_ATTRS = ('haoda_type', 'ref', 'expr')
    LINEAR_ATTRS = ('let', )

    def __init__(self, **kwargs):
        self.haoda_type = None
        self.ref = None
        self.expr = None
        self.let = ()
        (super().__init__)(**kwargs)
        var_types = {}
        for let in self.let:
            var_types[let.name] = let.haoda_type

        def set_var_type(obj, var_types):
            if isinstance(obj, ir.Var):
                if obj.name in var_types:
                    obj.haoda_type = var_types[obj.name]
            return obj

        self.let = tuple(_.visit(set_var_type, var_types) for _ in self.let)
        self.expr = self.expr.visit(set_var_type, var_types)
        self.stencil = kwargs.pop('stencil', None)

    @property
    def name(self):
        return self.ref.name

    def __str__(self):
        if self.let:
            let = '\n  {}\n '.format('\n  '.join(map(str, self.let)))
        else:
            let = ''
        return '{} {}:{} {} = {}'.format(type(self).__name__[:-4].lower(), self.haoda_type, let, self.ref, ir.unparenthesize(self.expr))

    @property
    def symbol_table(self) -> Dict[(str, str)]:
        symbol_table = self.stencil.symbol_table.copy()
        lets = {let.name:let for let in self.let}
        for var in toposort.toposort_flatten({let.name:{var.name for var in ir.visitor.get_vars(let)} for let in self.let}):
            symbol_table[var] = base.propagate_type(lets[var], symbol_table).haoda_type

        return symbol_table

    def propagate_type(self, dummy=None) -> None:
        """Propagate haoda type of the nodes in this statement.

    Args:
      symbol_table: A dict mapping input or local tensor names to haoda types.

    Returns:
      None.
    """
        symbol_table = self.symbol_table
        self.expr = base.propagate_type(self.expr, symbol_table)
        if self.expr.haoda_type != self.haoda_type:
            self.expr = ir.Cast(expr=(self.expr), haoda_type=(self.haoda_type))
        self.let = tuple(base.propagate_type(let, symbol_table) for let in self.let)


class LocalStmt(LocalStmtOrOutputStmt):
    pass


class OutputStmt(LocalStmtOrOutputStmt):
    LINEAR_ATTRS = LocalStmtOrOutputStmt.LINEAR_ATTRS + ('dram', )

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        if not self.dram:
            self.dram = (0, )


class ParamStmt(ir.Node):
    SCALAR_ATTRS = ('haoda_type', 'attr', 'name', 'size')
    LINEAR_ATTRS = ('dram', )

    def __str__(self):
        return 'param {}{}: {}{}'.format(self.haoda_type, ''.join(map(', {}'.format, self.attr)), self.name, ''.join(map('[{}]'.format, self.size)))


class ParamAttr(ir.Node):
    SCALAR_ATTRS = ('dup', 'partitioning')

    def __str__(self):
        if self.dup is not None:
            return 'dup {}'.format(self.dup)
        else:
            result = 'partition {0.strategy}'.format(self.partitioning)
            if self.partitioning.strategy == 'cyclic':
                result += ' factor={}'.format(self.partitioning.factor)
            if self.partitioning.dim is not None:
                result += ' dim={}'.format(self.partitioning.dim)
            return result


class SodaProgram(ir.Node):
    SCALAR_ATTRS = ('border', 'burst_width', 'cluster', 'iterate', 'app_name', 'unroll_factor',
                    'input_stmts', 'param_stmts', 'local_stmts', 'output_stmts')

    def __init__(self, **kwargs):
        (super().__init__)(**kwargs)
        for node in self.input_stmts:
            if hasattr(self, 'tile_size'):
                if self.tile_size != node.tile_size:
                    msg = "tile size %s doesn't match previous one %s" % (
                     node.tile_size, self.tile_size)
                    raise util.SemanticError(msg)
                else:
                    if node.tile_size[:-1]:
                        self.tile_size = node.tile_size
                        self.dim = len(self.tile_size)

        if not hasattr(self, 'tile_size'):
            self.tile_size = node.tile_size
            self.dim = len(self.tile_size)

    def __str__(self):
        return '\n'.join(filter(None, (
         'border: {}'.format(self.border),
         'burst width: {}'.format(self.burst_width),
         'cluster: {}'.format(self.cluster),
         'iterate: {}'.format(self.iterate),
         'kernel: {}'.format(self.app_name),
         'unroll factor: {}'.format(self.unroll_factor),
         '\n'.join(map(str, self.input_stmts)),
         '\n'.join(map(str, self.param_stmts)),
         '\n'.join(map(str, self.local_stmts)),
         '\n'.join(map(str, self.output_stmts)))))


CLASSES = (
 InputStmt,
 LocalStmt,
 OutputStmt,
 ir.Let,
 ir.Ref,
 ir.Expr,
 ir.LogicAnd,
 ir.BinaryOr,
 ir.Xor,
 ir.BinaryAnd,
 ir.EqCmp,
 ir.LtCmp,
 ir.AddSub,
 ir.MulDiv,
 ir.Unary,
 ir.Operand,
 ir.Cast,
 ir.Call,
 ir.Var,
 ParamStmt,
 ParamAttr,
 SodaProgram)