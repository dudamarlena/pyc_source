# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/Pygments/pygments/lexers/theorem.py
# Compiled at: 2020-01-10 16:25:35
# Size of source mod 2**32: 18902 bytes
"""
    pygments.lexers.theorem
    ~~~~~~~~~~~~~~~~~~~~~~~

    Lexers for theorem-proving languages.

    :copyright: Copyright 2006-2019 by the Pygments team, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
import re
from pygments.lexer import RegexLexer, default, words
from pygments.token import Text, Comment, Operator, Keyword, Name, String, Number, Punctuation, Generic
__all__ = [
 'CoqLexer', 'IsabelleLexer', 'LeanLexer']

class CoqLexer(RegexLexer):
    __doc__ = '\n    For the `Coq <http://coq.inria.fr/>`_ theorem prover.\n\n    .. versionadded:: 1.5\n    '
    name = 'Coq'
    aliases = ['coq']
    filenames = ['*.v']
    mimetypes = ['text/x-coq']
    keywords1 = ('Section', 'Module', 'End', 'Require', 'Import', 'Export', 'Variable',
                 'Variables', 'Parameter', 'Parameters', 'Axiom', 'Hypothesis', 'Hypotheses',
                 'Notation', 'Local', 'Tactic', 'Reserved', 'Scope', 'Open', 'Close',
                 'Bind', 'Delimit', 'Definition', 'Let', 'Ltac', 'Fixpoint', 'CoFixpoint',
                 'Morphism', 'Relation', 'Implicit', 'Arguments', 'Set', 'Unset',
                 'Contextual', 'Strict', 'Prenex', 'Implicits', 'Inductive', 'CoInductive',
                 'Record', 'Structure', 'Canonical', 'Coercion', 'Theorem', 'Lemma',
                 'Corollary', 'Proposition', 'Fact', 'Remark', 'Example', 'Proof',
                 'Goal', 'Save', 'Qed', 'Defined', 'Hint', 'Resolve', 'Rewrite',
                 'View', 'Search', 'Show', 'Print', 'Printing', 'All', 'Graph', 'Projections',
                 'inside', 'outside', 'Check', 'Global', 'Instance', 'Class', 'Existing',
                 'Universe', 'Polymorphic', 'Monomorphic', 'Context')
    keywords2 = ('forall', 'exists', 'exists2', 'fun', 'fix', 'cofix', 'struct', 'match',
                 'end', 'in', 'return', 'let', 'if', 'is', 'then', 'else', 'for',
                 'of', 'nosimpl', 'with', 'as')
    keywords3 = ('Type', 'Prop')
    keywords4 = ('pose', 'set', 'move', 'case', 'elim', 'apply', 'clear', 'hnf', 'intro',
                 'intros', 'generalize', 'rename', 'pattern', 'after', 'destruct',
                 'induction', 'using', 'refine', 'inversion', 'injection', 'rewrite',
                 'congr', 'unlock', 'compute', 'ring', 'field', 'replace', 'fold',
                 'unfold', 'change', 'cutrewrite', 'simpl', 'have', 'suff', 'wlog',
                 'suffices', 'without', 'loss', 'nat_norm', 'assert', 'cut', 'trivial',
                 'revert', 'bool_congr', 'nat_congr', 'symmetry', 'transitivity',
                 'auto', 'split', 'left', 'right', 'autorewrite', 'tauto', 'setoid_rewrite',
                 'intuition', 'eauto', 'eapply', 'econstructor', 'etransitivity',
                 'constructor', 'erewrite', 'red', 'cbv', 'lazy', 'vm_compute', 'native_compute',
                 'subst')
    keywords5 = ('by', 'done', 'exact', 'reflexivity', 'tauto', 'romega', 'omega',
                 'assumption', 'solve', 'contradiction', 'discriminate', 'congruence')
    keywords6 = ('do', 'last', 'first', 'try', 'idtac', 'repeat')
    keyopts = ('!=', '#', '&', '&&', '\\(', '\\)', '\\*', '\\+', ',', '-', '-\\.',
               '->', '\\.', '\\.\\.', ':', '::', ':=', ':>', ';', ';;', '<', '<-',
               '<->', '=', '>', '>]', '>\\}', '\\?', '\\?\\?', '\\[', '\\[<', '\\[>',
               '\\[\\|', ']', '_', '`', '\\{', '\\{<', '\\|', '\\|]', '\\}', '~',
               '=>', '/\\\\', '\\\\/', '\\{\\|', '\\|\\}', 'Π', 'λ')
    operators = '[!$%&*+\\./:<=>?@^|~-]'
    prefix_syms = '[!?~]'
    infix_syms = '[=<>@^|&+\\*/$%-]'
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       'false|true|\\(\\)|\\[\\]', Name.Builtin.Pseudo),
      (
       '\\(\\*', Comment, 'comment'),
      (
       words(keywords1, prefix='\\b', suffix='\\b'), Keyword.Namespace),
      (
       words(keywords2, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keywords3, prefix='\\b', suffix='\\b'), Keyword.Type),
      (
       words(keywords4, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keywords5, prefix='\\b', suffix='\\b'), Keyword.Pseudo),
      (
       words(keywords6, prefix='\\b', suffix='\\b'), Keyword.Reserved),
      (
       "\\b([A-Z][\\w\\']*)", Name),
      (
       '(%s)' % '|'.join(keyopts[::-1]), Operator),
      (
       '(%s|%s)?%s' % (infix_syms, prefix_syms, operators), Operator),
      (
       "[^\\W\\d][\\w']*", Name),
      (
       '\\d[\\d_]*', Number.Integer),
      (
       '0[xX][\\da-fA-F][\\da-fA-F_]*', Number.Hex),
      (
       '0[oO][0-7][0-7_]*', Number.Oct),
      (
       '0[bB][01][01_]*', Number.Bin),
      (
       '-?\\d[\\d_]*(.[\\d_]*)?([eE][+\\-]?\\d[\\d_]*)', Number.Float),
      (
       '\'(?:(\\\\[\\\\\\"\'ntbr ])|(\\\\[0-9]{3})|(\\\\x[0-9a-fA-F]{2}))\'',
       String.Char),
      (
       "'.'", String.Char),
      (
       "'", Keyword),
      (
       '"', String.Double, 'string'),
      (
       "[~?][a-z][\\w\\']*:", Name)], 
     'comment':[
      (
       '[^(*)]+', Comment),
      (
       '\\(\\*', Comment, '#push'),
      (
       '\\*\\)', Comment, '#pop'),
      (
       '[(*)]', Comment)], 
     'string':[
      (
       '[^"]+', String.Double),
      (
       '""', String.Double),
      (
       '"', String.Double, '#pop')], 
     'dotted':[
      (
       '\\s+', Text),
      (
       '\\.', Punctuation),
      (
       "[A-Z][\\w\\']*(?=\\s*\\.)", Name.Namespace),
      (
       "[A-Z][\\w\\']*", Name.Class, '#pop'),
      (
       "[a-z][a-z0-9_\\']*", Name, '#pop'),
      default('#pop')]}

    def analyse_text(text):
        if text.startswith('(*'):
            return True


class IsabelleLexer(RegexLexer):
    __doc__ = '\n    For the `Isabelle <http://isabelle.in.tum.de/>`_ proof assistant.\n\n    .. versionadded:: 2.0\n    '
    name = 'Isabelle'
    aliases = ['isabelle']
    filenames = ['*.thy']
    mimetypes = ['text/x-isabelle']
    keyword_minor = ('and', 'assumes', 'attach', 'avoids', 'binder', 'checking', 'class_instance',
                     'class_relation', 'code_module', 'congs', 'constant', 'constrains',
                     'datatypes', 'defines', 'file', 'fixes', 'for', 'functions',
                     'hints', 'identifier', 'if', 'imports', 'in', 'includes', 'infix',
                     'infixl', 'infixr', 'is', 'keywords', 'lazy', 'module_name',
                     'monos', 'morphisms', 'no_discs_sels', 'notes', 'obtains', 'open',
                     'output', 'overloaded', 'parametric', 'permissive', 'pervasive',
                     'rep_compat', 'shows', 'structure', 'type_class', 'type_constructor',
                     'unchecked', 'unsafe', 'where')
    keyword_diag = ('ML_command', 'ML_val', 'class_deps', 'code_deps', 'code_thms',
                    'display_drafts', 'find_consts', 'find_theorems', 'find_unused_assms',
                    'full_prf', 'help', 'locale_deps', 'nitpick', 'pr', 'prf', 'print_abbrevs',
                    'print_antiquotations', 'print_attributes', 'print_binds', 'print_bnfs',
                    'print_bundles', 'print_case_translations', 'print_cases', 'print_claset',
                    'print_classes', 'print_codeproc', 'print_codesetup', 'print_coercions',
                    'print_commands', 'print_context', 'print_defn_rules', 'print_dependencies',
                    'print_facts', 'print_induct_rules', 'print_inductives', 'print_interps',
                    'print_locale', 'print_locales', 'print_methods', 'print_options',
                    'print_orders', 'print_quot_maps', 'print_quotconsts', 'print_quotients',
                    'print_quotientsQ3', 'print_quotmapsQ3', 'print_rules', 'print_simpset',
                    'print_state', 'print_statement', 'print_syntax', 'print_theorems',
                    'print_theory', 'print_trans_rules', 'prop', 'pwd', 'quickcheck',
                    'refute', 'sledgehammer', 'smt_status', 'solve_direct', 'spark_status',
                    'term', 'thm', 'thm_deps', 'thy_deps', 'try', 'try0', 'typ',
                    'unused_thms', 'value', 'values', 'welcome', 'print_ML_antiquotations',
                    'print_term_bindings', 'values_prolog')
    keyword_thy = ('theory', 'begin', 'end')
    keyword_section = ('header', 'chapter')
    keyword_subsection = ('section', 'subsection', 'subsubsection', 'sect', 'subsect',
                          'subsubsect')
    keyword_theory_decl = ('ML', 'ML_file', 'abbreviation', 'adhoc_overloading', 'arities',
                           'atom_decl', 'attribute_setup', 'axiomatization', 'bundle',
                           'case_of_simps', 'class', 'classes', 'classrel', 'codatatype',
                           'code_abort', 'code_class', 'code_const', 'code_datatype',
                           'code_identifier', 'code_include', 'code_instance', 'code_modulename',
                           'code_monad', 'code_printing', 'code_reflect', 'code_reserved',
                           'code_type', 'coinductive', 'coinductive_set', 'consts',
                           'context', 'datatype', 'datatype_new', 'datatype_new_compat',
                           'declaration', 'declare', 'default_sort', 'defer_recdef',
                           'definition', 'defs', 'domain', 'domain_isomorphism',
                           'domaindef', 'equivariance', 'export_code', 'extract',
                           'extract_type', 'fixrec', 'fun', 'fun_cases', 'hide_class',
                           'hide_const', 'hide_fact', 'hide_type', 'import_const_map',
                           'import_file', 'import_tptp', 'import_type_map', 'inductive',
                           'inductive_set', 'instantiation', 'judgment', 'lemmas',
                           'lifting_forget', 'lifting_update', 'local_setup', 'locale',
                           'method_setup', 'nitpick_params', 'no_adhoc_overloading',
                           'no_notation', 'no_syntax', 'no_translations', 'no_type_notation',
                           'nominal_datatype', 'nonterminal', 'notation', 'notepad',
                           'oracle', 'overloading', 'parse_ast_translation', 'parse_translation',
                           'partial_function', 'primcorec', 'primrec', 'primrec_new',
                           'print_ast_translation', 'print_translation', 'quickcheck_generator',
                           'quickcheck_params', 'realizability', 'realizers', 'recdef',
                           'record', 'refute_params', 'setup', 'setup_lifting', 'simproc_setup',
                           'simps_of_case', 'sledgehammer_params', 'spark_end', 'spark_open',
                           'spark_open_siv', 'spark_open_vcg', 'spark_proof_functions',
                           'spark_types', 'statespace', 'syntax', 'syntax_declaration',
                           'text', 'text_raw', 'theorems', 'translations', 'type_notation',
                           'type_synonym', 'typed_print_translation', 'typedecl',
                           'hoarestate', 'install_C_file', 'install_C_types', 'wpc_setup',
                           'c_defs', 'c_types', 'memsafe', 'SML_export', 'SML_file',
                           'SML_import', 'approximate', 'bnf_axiomatization', 'cartouche',
                           'datatype_compat', 'free_constructors', 'functor', 'nominal_function',
                           'nominal_termination', 'permanent_interpretation', 'binds',
                           'defining', 'smt2_status', 'term_cartouche', 'boogie_file',
                           'text_cartouche')
    keyword_theory_script = ('inductive_cases', 'inductive_simps')
    keyword_theory_goal = ('ax_specification', 'bnf', 'code_pred', 'corollary', 'cpodef',
                           'crunch', 'crunch_ignore', 'enriched_type', 'function',
                           'instance', 'interpretation', 'lemma', 'lift_definition',
                           'nominal_inductive', 'nominal_inductive2', 'nominal_primrec',
                           'pcpodef', 'primcorecursive', 'quotient_definition', 'quotient_type',
                           'recdef_tc', 'rep_datatype', 'schematic_corollary', 'schematic_lemma',
                           'schematic_theorem', 'spark_vc', 'specification', 'subclass',
                           'sublocale', 'termination', 'theorem', 'typedef', 'wrap_free_constructors')
    keyword_qed = ('by', 'done', 'qed')
    keyword_abandon_proof = ('sorry', 'oops')
    keyword_proof_goal = ('have', 'hence', 'interpret')
    keyword_proof_block = ('next', 'proof')
    keyword_proof_chain = ('finally', 'from', 'then', 'ultimately', 'with')
    keyword_proof_decl = ('ML_prf', 'also', 'include', 'including', 'let', 'moreover',
                          'note', 'txt', 'txt_raw', 'unfolding', 'using', 'write')
    keyword_proof_asm = ('assume', 'case', 'def', 'fix', 'presume')
    keyword_proof_asm_goal = ('guess', 'obtain', 'show', 'thus')
    keyword_proof_script = ('apply', 'apply_end', 'apply_trace', 'back', 'defer', 'prefer')
    operators = ('::', ':', '(', ')', '[', ']', '_', '=', ',', '|', '+', '-', '!',
                 '?')
    proof_operators = ('{', '}', '.', '..')
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '\\(\\*', Comment, 'comment'),
      (
       '\\{\\*', Comment, 'text'),
      (
       words(operators), Operator),
      (
       words(proof_operators), Operator.Word),
      (
       words(keyword_minor, prefix='\\b', suffix='\\b'), Keyword.Pseudo),
      (
       words(keyword_diag, prefix='\\b', suffix='\\b'), Keyword.Type),
      (
       words(keyword_thy, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_theory_decl, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_section, prefix='\\b', suffix='\\b'), Generic.Heading),
      (
       words(keyword_subsection, prefix='\\b', suffix='\\b'), Generic.Subheading),
      (
       words(keyword_theory_goal, prefix='\\b', suffix='\\b'), Keyword.Namespace),
      (
       words(keyword_theory_script, prefix='\\b', suffix='\\b'), Keyword.Namespace),
      (
       words(keyword_abandon_proof, prefix='\\b', suffix='\\b'), Generic.Error),
      (
       words(keyword_qed, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_goal, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_block, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_decl, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_chain, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_asm, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_asm_goal, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keyword_proof_script, prefix='\\b', suffix='\\b'), Keyword.Pseudo),
      (
       '\\\\<\\w*>', Text.Symbol),
      (
       "[^\\W\\d][.\\w']*", Name),
      (
       "\\?[^\\W\\d][.\\w']*", Name),
      (
       "'[^\\W\\d][.\\w']*", Name.Type),
      (
       '\\d[\\d_]*', Name),
      (
       '0[xX][\\da-fA-F][\\da-fA-F_]*', Number.Hex),
      (
       '0[oO][0-7][0-7_]*', Number.Oct),
      (
       '0[bB][01][01_]*', Number.Bin),
      (
       '"', String, 'string'),
      (
       '`', String.Other, 'fact')], 
     'comment':[
      (
       '[^(*)]+', Comment),
      (
       '\\(\\*', Comment, '#push'),
      (
       '\\*\\)', Comment, '#pop'),
      (
       '[(*)]', Comment)], 
     'text':[
      (
       '[^*}]+', Comment),
      (
       '\\*\\}', Comment, '#pop'),
      (
       '\\*', Comment),
      (
       '\\}', Comment)], 
     'string':[
      (
       '[^"\\\\]+', String),
      (
       '\\\\<\\w*>', String.Symbol),
      (
       '\\\\"', String),
      (
       '\\\\', String),
      (
       '"', String, '#pop')], 
     'fact':[
      (
       '[^`\\\\]+', String.Other),
      (
       '\\\\<\\w*>', String.Symbol),
      (
       '\\\\`', String.Other),
      (
       '\\\\', String.Other),
      (
       '`', String.Other, '#pop')]}


class LeanLexer(RegexLexer):
    __doc__ = '\n    For the `Lean <https://github.com/leanprover/lean>`_\n    theorem prover.\n\n    .. versionadded:: 2.0\n    '
    name = 'Lean'
    aliases = ['lean']
    filenames = ['*.lean']
    mimetypes = ['text/x-lean']
    flags = re.MULTILINE | re.UNICODE
    keywords1 = ('import', 'abbreviation', 'opaque_hint', 'tactic_hint', 'definition',
                 'renaming', 'inline', 'hiding', 'exposing', 'parameter', 'parameters',
                 'conjecture', 'hypothesis', 'lemma', 'corollary', 'variable', 'variables',
                 'theorem', 'axiom', 'inductive', 'structure', 'universe', 'alias',
                 'help', 'options', 'precedence', 'postfix', 'prefix', 'calc_trans',
                 'calc_subst', 'calc_refl', 'infix', 'infixl', 'infixr', 'notation',
                 'eval', 'check', 'exit', 'coercion', 'end', 'private', 'using',
                 'namespace', 'including', 'instance', 'section', 'context', 'protected',
                 'expose', 'export', 'set_option', 'add_rewrite', 'extends', 'open',
                 'example', 'constant', 'constants', 'print', 'opaque', 'reducible',
                 'irreducible')
    keywords2 = ('forall', 'fun', 'Pi', 'obtain', 'from', 'have', 'show', 'assume',
                 'take', 'let', 'if', 'else', 'then', 'by', 'in', 'with', 'begin',
                 'proof', 'qed', 'calc', 'match')
    keywords3 = ('Type', 'Prop')
    operators = ('!=', '#', '&', '&&', '*', '+', '-', '/', '@', '!', '`', '-.', '->',
                 '.', '..', '...', '::', ':>', ';', ';;', '<', '<-', '=', '==', '>',
                 '_', '|', '||', '~', '=>', '<=', '>=', '/\\', '\\/', '∀', 'Π', 'λ',
                 '↔', '∧', '∨', '≠', '≤', '≥', '¬', '⁻¹', '⬝', '▸', '→', '∃', 'ℕ',
                 'ℤ', '≈', '×', '⌞', '⌟', '≡', '⟨', '⟩')
    punctuation = ('(', ')', ':', '{', '}', '[', ']', '⦃', '⦄', ':=', ',')
    tokens = {'root':[
      (
       '\\s+', Text),
      (
       '/-', Comment, 'comment'),
      (
       '--.*?$', Comment.Single),
      (
       words(keywords1, prefix='\\b', suffix='\\b'), Keyword.Namespace),
      (
       words(keywords2, prefix='\\b', suffix='\\b'), Keyword),
      (
       words(keywords3, prefix='\\b', suffix='\\b'), Keyword.Type),
      (
       words(operators), Name.Builtin.Pseudo),
      (
       words(punctuation), Operator),
      (
       "[A-Za-z_α-κμ-ϻἀ-῾℀-⅏][A-Za-z_'α-κμ-ϻἀ-῾⁰-⁹ⁿ-₉ₐ-ₜ℀-⅏0-9]*",
       Name),
      (
       '\\d+', Number.Integer),
      (
       '"', String.Double, 'string'),
      (
       "[~?][a-z][\\w\\']*:", Name.Variable)], 
     'comment':[
      (
       '[^/-]', Comment.Multiline),
      (
       '/-', Comment.Multiline, '#push'),
      (
       '-/', Comment.Multiline, '#pop'),
      (
       '[/-]', Comment.Multiline)], 
     'string':[
      (
       '[^\\\\"]+', String.Double),
      (
       '\\\\[n"\\\\]', String.Escape),
      (
       '"', String.Double, '#pop')]}