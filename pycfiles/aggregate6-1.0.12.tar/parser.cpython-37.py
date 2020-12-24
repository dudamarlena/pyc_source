# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aggregate\parser.py
# Compiled at: 2019-12-26 00:23:45
# Size of source mod 2**32: 28751 bytes
__doc__ = '\nlexer and parser specification for aggregate\n============================================\n\nOverview\n    Implements the ``agg`` programming lanaguage\n\nExample program\n    The following short program replicates Thought Experiemnt 1 from Neil Bodoff\'s\n    paper Capital Allocation by Percentile Layer\n\n    ::\n\n        port BODOFF1 note{Bodoff Thought Experiment No. 1}\n            agg wind  1 claim sev dhistogram xps [0,  99] [0.80, 0.20] fixed\n            agg quake 1 claim sev dhistogram xps [0, 100] [0.95, 0.05] fixed\n\nPreprocessing\n    tab or four spaces needed and are replaced with space (program is on one line)\n\n\nIgnored characters\n    colon, comma, ( ) |\n\n\nLanguage Specification\n----------------------\n\nThe ```agg``` Language Grammar:\n\n::\n\n    answer              \t:: sev_out\n                        \t | agg_out\n                        \t | port_out\n\n    port_out            \t:: port_name note agg_list\n\n    agg_list            \t:: agg_list agg_out\n                        \t | agg_out\n\n    agg_out             \t:: agg_name builtin_aggregate note\n                        \t | agg_name exposures layers SEV sev freq note\n\n    sev_out             \t:: sev_out sev_name sev note\n                        \t | sev_name sev note\n\n    freq                \t:: MIXED ID snumber snumber\n                        \t | MIXED ID snumber\n                        \t | FREQ snumber\n                        \t | FREQ\n\n    snumber             \t:: NUMBER\n                        \t | MINUS NUMBER %prec UMINUS\n\n    sev                 \t:: sev PLUS numbers\n                        \t | sev MINUS numbers\n                        \t | numbers TIMES sev\n                        \t | ids numbers CV numbers weights\n                        \t | ids numbers weights\n                        \t | ids numbers numbers weights xps\n                        \t | ids xps\n                        \t | builtinids numbers numbers\n                        \t | builtinids\n\n    xps                 \t:: XPS numbers numbers\n                        \t |\n\n    weights             \t:: WEIGHTS EQUAL_WEIGHT NUMBER\n                        \t | WEIGHTS numbers\n                        \t |\n\n    layers              \t:: numbers XS numbers\n                        \t |\n\n    note                \t:: NOTE\n                        \t |\n\n    exposures           \t:: numbers CLAIMS\n                        \t | numbers LOSS\n                        \t | numbers PREMIUM AT numbers LR\n                        \t | numbers PREMIUM AT numbers\n\n    builtinids          \t:: BUILTINID\n\n    ids                 \t:: "[" idl "]"\n                        \t | ID\n\n    idl                 \t:: idl ID\n                        \t | ID\n\n    numbers             \t:: "[" numberl "]"\n                        \t | NUMBER\n\n    numberl             \t:: numberl NUMBER\n                        \t | NUMBER\n\n    builtin_aggregate   \t:: builtin_aggregate_dist TIMES NUMBER\n                        \t | NUMBER TIMES builtin_aggregate_dist\n                        \t | builtin_aggregate_dist\n\n    builtin_aggregate_dist\t:: BUILTINID\n\n    sev_name            \t:: SEV ID\n\n    agg_name            \t:: AGG ID\n\n    port_name           \t:: PORT ID\n\nparser.out parser debug information\n-----------------------------------\n\nLexer term definition\n---------------------\n\n::\n\n    tokens = {ID, BUILTINID, NOTE,\n              SEV, AGG, PORT,\n              PLUS, MINUS, TIMES, NUMBER,\n              LOSS, PREMIUM, AT, LR, CLAIMS,\n              XS,\n              CV, WEIGHTS, EQUAL_WEIGHT, XPS,\n              MIXED, FREQ\n              }\n    ignore = \' \t,\\:\\(\\)|\'\n    literals = {\'[\', \']\'}\n\n    # per manual, need to list longer tokens before shorter ones\n    # NOTE = r\'note\\{[0-9a-zA-Z,\\.\\(\\)\\-=\\+!\\s]*\\}\'  # r\'[^\\}]+\'\n    NOTE = r\'note\\{[^\\}]*\\}\'  # r\'[^\\}]+\'\n    BUILTINID = r\'(sev|agg|port|meta)\\.[a-zA-Z][a-zA-Z0-9_]*\'\n    FREQ = r\'binomial|poisson|bernoulli|fixed\'\n    ID = r\'[a-zA-Z][\\.a-zA-Z0-9~]*\'  # do not allow _ in line names, use ~ instead: BECAUSE p_ etc. makes _ special\n    PLUS = r\'\\+\'\n    MINUS = r\'\\-\'\n    TIMES = r\'\\*\'\n    EQUAL_WEIGHT = r\'=\'\n    ID[\'loss\'] = LOSS\n    ID[\'at\'] = AT\n    ID[\'cv\'] = CV\n    ID[\'premium\'] = PREMIUM\n    ID[\'prem\'] = PREMIUM\n    ID[\'lr\'] = LR\n    ID[\'claims\'] = CLAIMS\n    ID[\'claim\'] = CLAIMS\n    ID[\'x\'] = XS\n    ID[\'xs\'] = XS\n    ID[\'wts\'] = WEIGHTS\n    ID[\'wt\'] = WEIGHTS\n    ID[\'xps\'] = XPS\n    ID[\'mixed\'] = MIXED\n    ID[\'inf\'] = NUMBER\n    ID[\'sev\'] = SEV\n    ID[\'on\'] = SEV\n    ID[\'agg\'] = AGG\n    ID[\'port\'] = PORT\n\n\nExample Code\n------------\n\n    ::\n\n        port Complex~Portfolio~Mixed\n            agg LineA  50  claims           sev lognorm 12 cv [2, 3, 4] wt [.3 .5 .2] mixed gamma 0.4\n            agg LineB  24  claims 10 x 5    sev lognorm 12 cv [{\', \'.join([str(i) for i in np.linspace(2,5, 20)])}] wt=20 mixed gamma 0.35\n            agg LineC 124  claims 120 x 5   sev lognorm 16 cv 3.4                     mixed gamma 0.45\n\n        port Complex~Portfolio\n            agg Line3  50  claims [5 10 15] x 0         sev lognorm 12 cv [1, 2, 3]        mixed gamma 0.25\n            agg Line9  24  claims [5 10 15] x 5         sev lognorm 12 cv [1, 2, 3] wt=3   mixed gamma 0.25\n\n        port Portfolio~2\n            agg CA 500 prem at .5 lr 15 x 12  sev gamma 12 cv [2 3 4] wt [.3 .5 .2] mixed gamma 0.4\n            agg FL 1.7 claims 100 x 5         sev 10000 * pareto 1.3 - 10000        poisson\n            agg IL 1e-8 * agg.CMP\n            agg OH agg.CMP * 1e-8\n            agg NY 500 prem at .5 lr 15 x 12  sev [20 30 40 10] * gamma [9 10 11 12] cv [1 2 3 4] wt =4 mixed gamma 0.4\n\n        sev proda 30000 * lognorm 2\n        sev prodc:   50000 * lognorm(3)\n        sev weird    50000 * beta(1, 4) + 10000\n        sev premsop1 25000 * lognorm 2.3; sev premsop2 35000 * lognorm 2.4;\n        sev premsop3 45000 * lognorm 2.8\n\n        agg Agg1     20 claims 10 x 2 sev lognorm 12 cv 0.2 mixed gamma 0.8\n        agg Agg2     20 claims 10 x 2 sev 15 * lognorm 2.5  poisson;\n        sev premsop1 25000 * lognorm 2.3;\n        agg Agg3     20 claims 10 x 2 on 25 * lognorm 2 fixed;\n\n        port MyFirstPortfolio\n            agg A1: 50  claims          sev gamma 12 cv .30 (mixed gamma 0.014)\n            agg A2: 50  claims 30 xs 10 sev gamma 12 cv .30 (mixed gamma 0.014)\n            agg A3: 50  claims          sev gamma 12 cv 1.30 (mixed gamma 0.014)\n            agg A4: 50  claims 30 xs 20 sev gamma 12 cv 1.30 (mixed gamma 0.14)\n            agg B 15 claims 15 xs 15 sev lognorm 12 cv 1.5 + 2 mixed gamma 4.8\n            agg Cat 1.7 claims 25 xs 5  sev 25 * pareto 1.3 0 - 25 poisson\n            agg ppa: 1e-8 * agg.PPAL\n\n        port distortionTest\n            agg mix    50 claims              [50, 100, 150, 200] xs 0  sev lognorm 12 cv [1,2,3,4]    poisson\n            agg low    500 premium at 0.5     5 xs 5                    sev gamma 12 cv .30            mixed gamma 0.2\n            agg med    500 premium at 0.5 lr  15 xs 10                  sev gamma 12 cv .30            mixed gamma 0.4\n            agg xsa    50  claims             30 xs 10                  sev gamma 12 cv .30            mixed gamma 1.2\n            agg hcmp   1e-8 * agg.CMP\n            agg ihmp   agg.PPAL * 1e-8\n\nReferences\n----------\n\nhttps://sly.readthedocs.io/en/latest/sly.html\n\n'
from sly import Lexer, Parser
import logging, numpy as np, warnings
logger = logging.getLogger('aggregate')

class UnderwritingLexer(Lexer):
    tokens = {
     ID, BUILTINID, NOTE,
     SEV, AGG, PORT,
     PLUS, MINUS, TIMES, NUMBER,
     LOSS, PREMIUM, AT, LR, CLAIMS,
     XS,
     CV, WEIGHTS, EQUAL_WEIGHT, XPS,
     MIXED, FREQ}
    ignore = ' \t,\\:\\(\\)|'
    literals = {'[', ']'}
    NOTE = 'note\\{[^\\}]*\\}'
    BUILTINID = '(sev|agg|port|meta)\\.[a-zA-Z][a-zA-Z0-9_]*'
    FREQ = 'binomial|poisson|bernoulli|pascal|fixed'
    ID = '[a-zA-Z][\\.:~_a-zA-Z0-9]*'
    PLUS = '\\+'
    MINUS = '\\-'
    TIMES = '\\*'
    EQUAL_WEIGHT = '='
    ID['loss'] = LOSS
    ID['at'] = AT
    ID['cv'] = CV
    ID['premium'] = PREMIUM
    ID['prem'] = PREMIUM
    ID['lr'] = LR
    ID['claims'] = CLAIMS
    ID['claim'] = CLAIMS
    ID['x'] = XS
    ID['xs'] = XS
    ID['wts'] = WEIGHTS
    ID['wt'] = WEIGHTS
    ID['xps'] = XPS
    ID['mixed'] = MIXED
    ID['inf'] = NUMBER
    ID['sev'] = SEV
    ID['agg'] = AGG
    ID['port'] = PORT

    @_('\\-?(\\d+\\.?\\d*|\\d*\\.\\d+)([eE](\\+|\\-)?\\d+)?')
    def NUMBER(self, t):
        if t.value == 'INF' or t.value == 'inf':
            t.value = np.inf
        else:
            t.value = float(t.value)
        return t

    @_('\\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]:s}'")
        self.index += 1


class UnderwritingParser(Parser):
    tokens = UnderwritingLexer.tokens
    precedence = (('left', PLUS, MINUS), ('left', TIMES), ('right', UMINUS))

    def __init__(self, safe_lookup_function, debug=False):
        self.arg_dict = None
        self.sev_out_dict = None
        self.agg_out_dict = None
        self.port_out_dict = None
        self.reset()
        self._safe_lookup = safe_lookup_function
        if debug:

            def _print(message):
                print(message)

            self.log = _print
        else:

            def _print(message):
                logger.info('UnderwritingParser | ' + message)

            self.log = _print

    def reset(self):
        self.sev_out_dict = {}
        self.agg_out_dict = {}
        self.port_out_dict = {}

    @staticmethod
    def _check_vectorizable(value):
        """
        check the if value can be vectorized

        """
        if isinstance(value, float) or isinstance(value, int) or isinstance(value, np.ndarray):
            return value
        return np.array(value)

    @_('sev_out')
    def answer(self, p):
        self.log(f"\t\tExiting through sev_out, created severity {p.sev_out}")

    @_('agg_out')
    def answer(self, p):
        self.log(f"\t\tExiting through agg_out, created aggregate {p.agg_out}")

    @_('port_out')
    def answer(self, p):
        self.log(f"\t\tExiting through port_out, created portfolio {p.port_out} with {len(self.port_out_dict[p.port_out]['spec'])} aggregates")

    @_('port_name note agg_list')
    def port_out(self, p):
        self.log(f"\tADDING port_name note ({p.note[:10]}...) agg_list to port_out {p.port_name}")
        self.port_out_dict[p.port_name] = {'spec':p.agg_list,  'note':p.note}
        return p.port_name

    @_('agg_list agg_out')
    def agg_list(self, p):
        if p.agg_list is None:
            raise ValueError('ODD agg list is empty')
        p.agg_list.append(p.agg_out)
        self.log(f"\tADDED agg_out {p.agg_out} to agg_list {p.agg_list}")
        return p.agg_list

    @_('agg_out')
    def agg_list(self, p):
        self.log(f"\tADDING agg_out {p.agg_out} to new agg_list")
        return [
         p.agg_out]

    @_('agg_name builtin_aggregate note')
    def agg_out(self, p):
        self.log(f"ADDING agg_name builtin_aggregate note {p.builtin_aggregate} to agg_out")
        if 'name' in p.builtin_aggregate:
            del p.builtin_aggregate['name']
        self.agg_out_dict[p.agg_name] = {**{'name': p.agg_name}, **(p.builtin_aggregate), **{'note': p.note}}
        return p.agg_name

    @_('agg_name exposures layers SEV sev freq note')
    def agg_out(self, p):
        self.log(f"ADDING agg_name exposures layers SEV sev freq note to agg_out {p.agg_name}")
        self.agg_out_dict[p.agg_name] = {**{'name': p.agg_name}, **(p.exposures), **(p.layers), **(p.sev), **(p.freq), **{'note': p.note}}
        return p.agg_name

    @_('sev_out sev_name sev note')
    def sev_out(self, p):
        self.log(f"ADDING sev_out sev_name {p.sev_name} sev note to sev_out, appending to sev_out_dict")
        p.sev['note'] = p.note
        self.sev_out_dict[p.sev_name] = p.sev

    @_('sev_name sev note')
    def sev_out(self, p):
        self.log(f"ADDING sev_name sev note resolving to sev_part {p.sev_name}, adding to sev_out_dict")
        p.sev['note'] = p.note
        self.sev_out_dict[p.sev_name] = p.sev

    @_('MIXED ID snumber snumber')
    def freq(self, p):
        self.log(f"MIXED ID snumber snumber {p.ID}, {p[2]}, {p[3]} to two param freq, snumber.1=CV")
        return {'freq_name':p.ID, 
         'freq_a':p[2],  'freq_b':p[3]}

    @_('MIXED ID snumber')
    def freq(self, p):
        self.log(f"MIXED ID snumber {p.ID}, {p.snumber} to single param freq, snumber=CVs")
        return {'freq_name':p.ID, 
         'freq_a':p.snumber}

    @_('FREQ snumber snumber')
    def freq(self, p):
        self.log(f"resolving named frequency distribution {p.FREQ} parameters {p[1]}, {p[2]} to freq")
        if p.FREQ != 'pascal':
            warnings.warn(f"Illogical choice of frequency {p.FREQ}, expected pascal")
        return {'freq_name':p.FREQ,  'freq_a':p[1],  'freq_b':p[2]}

    @_('FREQ snumber')
    def freq(self, p):
        self.log(f"resolving named frequency distribution {p.FREQ} parameter {p.snumber} to freq")
        if p.FREQ != 'binomial':
            warnings.warn(f"Illogical choice of frequency {p.FREQ}, expected binomial")
        return {'freq_name':p.FREQ,  'freq_a':p.snumber}

    @_('FREQ')
    def freq(self, p):
        self.log(f"resolving named frequency distribution {p.FREQ} to freq")
        if p.FREQ not in ('poisson', 'bernoulli', 'fixed'):
            warnings.warn(f"Illogical choice for FREQ {p.FREQ}, should be poisson, bernoulli or fixed")
        return {'freq_name': p.FREQ}

    @_('NUMBER')
    def snumber(self, p):
        self.log(f"NUMBER {p.NUMBER} to signed number")
        return p.NUMBER

    @_('MINUS NUMBER %prec UMINUS')
    def snumber(self, p):
        self.log(f"-NUMBER {p.NUMBER} to signed number")
        return -p.NUMBER

    @_('sev PLUS numbers')
    def sev(self, p):
        self.log(f"resolving sev PLUS numbers to sev {p.numbers}")
        p.sev['sev_loc'] = UnderwritingParser._check_vectorizable(p.sev.get('sev_loc', 0))
        p.numbers = UnderwritingParser._check_vectorizable(p.numbers)
        p.sev['sev_loc'] += p.numbers
        return p.sev

    @_('sev MINUS numbers')
    def sev(self, p):
        self.log(f"resolving sev MINUS numbers to sev {p.numbers}")
        p.sev['sev_loc'] = p.sev.get('sev_loc', 0) - p.numbers
        return p.sev

    @_('numbers TIMES sev')
    def sev(self, p):
        self.log(f"resolving numbers TIMES sev to sev {p.numbers}")
        p.numbers = UnderwritingParser._check_vectorizable(p.numbers)
        if 'sev_mean' in p.sev:
            p.sev['sev_mean'] = UnderwritingParser._check_vectorizable(p.sev.get('sev_mean', 0))
            p.sev['sev_mean'] *= p.numbers
        if 'sev_scale' in p.sev:
            p.sev['sev_scale'] = UnderwritingParser._check_vectorizable(p.sev.get('sev_scale', 0))
            p.sev['sev_scale'] *= p.numbers
        if 'sev_mean' not in p.sev:
            p.sev['sev_scale'] = p.numbers
        if 'sev_loc' in p.sev:
            p.sev['sev_loc'] = UnderwritingParser._check_vectorizable(p.sev['sev_loc'])
            p.sev['sev_loc'] *= p.numbers
        return p.sev

    @_('ids numbers CV numbers weights')
    def sev(self, p):
        self.log(f"resolving ids {p.ids} numbers CV numbers weights {p[1]}, {p[3]}, {p.weights}")
        return {'sev_name':p.ids, 
         'sev_mean':p[1],  'sev_cv':p[3],  'sev_wt':p.weights}

    @_('ids numbers weights')
    def sev(self, p):
        self.log(f"resolving ids {p.ids} numbers {p[1]} to sev (one param dist)")
        return {'sev_name':p.ids, 
         'sev_a':p[1],  'sev_wt':p.weights}

    @_('ids numbers numbers weights')
    def sev(self, p):
        self.log(f"resolving ids {p.ids} numbers numbers {p[1]}, {p[2]} to sev (two param sev dist)")
        return {'sev_name':p.ids, 
         'sev_a':p[1],  'sev_b':p[2],  'sev_wt':p.weights}

    @_('ids xps')
    def sev(self, p):
        self.log(f"resolving ids {p.ids} xps {p.xps} to sev (fixed or histogram type)")
        return {**{'sev_name': p.ids}, **(p.xps)}

    @_('XPS numbers numbers')
    def xps(self, p):
        self.log(f"XPS numbers numbers resolving to xs and ps {p[1]}, {p[2]}")
        return {'sev_xs':p[1], 
         'sev_ps':p[2]}

    @_('')
    def xps(self, p):
        self.log('missing xps term')
        return {}

    @_('WEIGHTS EQUAL_WEIGHT NUMBER')
    def weights(self, p):
        self.log(f"WEIGHTS EQUAL_WEIGHTS {p.NUMBER} resolving to equal weights")
        return np.ones(int(p.NUMBER)) / p.NUMBER

    @_('WEIGHTS numbers')
    def weights(self, p):
        self.log(f"WEIGHTS numbers resolving to weights {p.numbers}")
        return p.numbers

    @_('')
    def weights(self, p):
        self.log('missing weights term')
        return 1

    @_('builtinids numbers numbers')
    def sev(self, p):
        self.log(f"builtinds {p.builtinids} numbers numbers log2={p[1]}, bs={p[2]} to sev")
        requested_type = p.builtinids.split('.')[0]
        if requested_type == 'meta':
            return {'sev_name':p.builtinids,  'sev_a':p[1],  'sev_b':p[2]}
        raise ValueError(f"Only meta type can be used with arguments, not {p.builtinids}")

    @_('builtinids')
    def sev(self, p):
        self.log(f"builtinds {p.builtinids} to sev")
        requested_type = p.builtinids.split('.')[0]
        if requested_type not in ('sev', 'meta'):
            raise ValueError(f"built in type must be sev or meta, not {p.builtinids}")
        if requested_type == 'meta':
            return {'sev_name': p.builtinids}
        return self._safe_lookup(p.builtinids)

    @_('numbers XS numbers')
    def layers(self, p):
        self.log(f"resolving numbers XS numbers to layers {p[0]} xs {p[2]}")
        return {'exp_attachment':p[2], 
         'exp_limit':p[0]}

    @_('')
    def layers(self, p):
        self.log('missing layer term')
        return {}

    @_('NOTE')
    def note(self, p):
        self.log(f"NOTE to note: {p.NOTE[5:-1]}")
        return p.NOTE[5:-1]

    @_('')
    def note(self, p):
        self.log('Empty note term')
        return ''

    @_('numbers CLAIMS')
    def exposures(self, p):
        self.log(f"resolving numbers CLAIMS to exposures {p.numbers}")
        return {'exp_en': p.numbers}

    @_('numbers LOSS')
    def exposures(self, p):
        self.log(f"resolving numbers LOSS to exposures {p.numbers}")
        return {'exp_el': p.numbers}

    @_('numbers PREMIUM AT numbers LR')
    def exposures(self, p):
        self.log(f"resolving numbers PREMIUM AT numbers LR to exposures {p[0]} at {p[3]}")
        return {'exp_premium':p[0], 
         'exp_lr':p[3],  'exp_el':p[0] * p[3]}

    @_('numbers PREMIUM AT numbers')
    def exposures(self, p):
        self.log(f"resolving numbers PREMIUM AT numbers to exposures {p[0]} at {p[3]}")
        return {'exp_premium':p[0], 
         'exp_lr':p[3],  'exp_el':p[0] * p[3]}

    @_('BUILTINID')
    def builtinids(self, p):
        self.log(f"resolving BUILTINID to builtinids {p.BUILTINID}")
        return p.BUILTINID

    @_('"[" idl "]"')
    def ids(self, p):
        self.log(f"resolving [id1] to ids {p.idl}")
        return p.idl

    @_('idl ID')
    def idl(self, p):
        s1 = f"resolving idl ID {p.idl}, {p.ID} --> "
        p.idl.append(p.ID)
        s1 += (f"{p.idl}")
        self.log(s1)
        return p.idl

    @_('ID')
    def idl(self, p):
        ans = [p.ID]
        self.log(f"resolving ID to idl {p.ID} --> {ans}")
        return ans

    @_('ID')
    def ids(self, p):
        self.log(f"resolving ID to ids {p.ID}")
        return p.ID

    @_('"[" numberl "]"')
    def numbers(self, p):
        self.log(f"resolving [number1] to numbers {p.numberl}")
        return p.numberl

    @_('numberl NUMBER')
    def numberl(self, p):
        s1 = f"resolving numberl NUMBER {p.numberl}, {p.NUMBER} --> "
        p.numberl.append(p.NUMBER)
        s1 += (f"{p.numberl}")
        self.log(s1)
        return p.numberl

    @_('NUMBER')
    def numberl(self, p):
        ans = [p.NUMBER]
        self.log(f"resolving NUMBER to numberl {p.NUMBER} --> {ans}")
        return ans

    @_('NUMBER')
    def numbers(self, p):
        self.log(f"resolving NUMBER to numbers {p.NUMBER}")
        return p.NUMBER

    @_('builtin_aggregate_dist TIMES NUMBER')
    def builtin_aggregate(self, p):
        """  inhomogeneous change of scale """
        self.log(f"builtin_aggregate_dist TIMES NUMBER {p.NUMBER}")
        bid = p.builtin_aggregate_dist
        bid['exp_en'] = bid.get('exp_en', 0) * p.NUMBER
        bid['exp_el'] = bid.get('exp_el', 0) * p.NUMBER
        bid['exp_premium'] = bid.get('exp_premium', 0) * p.NUMBER
        return bid

    @_('NUMBER TIMES builtin_aggregate_dist')
    def builtin_aggregate(self, p):
        """
        homogeneous change of scale

        :param p:
        :return:
        """
        self.log(f"NUMBER {p.NUMBER} TIMES builtin_aggregate_dist")
        bid = p.builtin_aggregate_dist
        if 'sev_mean' in bid:
            bid['sev_mean'] = bid['sev_mean'] * p.NUMBER
        if 'sev_scale' in bid:
            bid['sev_scale'] = bid['sev_scale'] * p.NUMBER
        if 'sev_loc' in bid:
            bid['sev_loc'] = bid['sev_loc'] * p.NUMBER
        bid['exp_attachment'] = bid.get('exp_attachment', 0) * p.NUMBER
        bid['exp_limit'] = bid.get('exp_limit', np.inf) * p.NUMBER
        bid['exp_el'] = bid.get('exp_el', 0) * p.NUMBER
        bid['exp_premium'] = bid.get('exp_premium', 0) * p.NUMBER
        return bid

    @_('builtin_aggregate_dist')
    def builtin_aggregate(self, p):
        self.log('builtin_aggregate_dist becomese builtin_aggregate')
        return p.builtin_aggregate_dist

    @_('BUILTINID')
    def builtin_aggregate_dist(self, p):
        self.log(f"Lookup BUILTINID {p.BUILTINID}")
        built_in_dict = self._safe_lookup(p.BUILTINID)
        return built_in_dict

    @_('SEV ID')
    def sev_name(self, p):
        self.log(f"SEV ID resolves to sev_name {p.ID}")
        return p.ID

    @_('AGG ID')
    def agg_name(self, p):
        self.log(f"AGG ID resolves to agg_name {p.ID}")
        return p.ID

    @_('PORT ID')
    def port_name(self, p):
        self.log(f"PORT ID note resolves to port_name {p.ID}")
        return p.ID

    def error(self, p):
        if p:
            raise ValueError(p)
        else:
            raise ValueError('Unexpected end of file')


if __name__ == '__main__':
    start_string = 'Language Specification\n----------------------\n\nThe ```agg``` Language Grammar:\n\n::\n\n'
    end_string = 'parser.out parser debug information'
    with open(__file__, 'r') as (f):
        txt = f.read()
    stxt = txt.split('@_')
    ans = {}
    for it in stxt[3:-2]:
        if it.find('# def') >= 0:
            continue
        b = it.split('def')
        b0 = b[0].strip()[2:-2]
        b1 = b[1].split('(self, p):')[0].strip()
        if b1 in ans:
            ans[b1] += [b0]
        else:
            ans[b1] = [
             b0]

    s = ''
    for k, v in ans.items():
        s += f"{k:<20s}\t:: {v[0]:<s}\n"
        for rhs in v[1:]:
            s += f"{'                    '}\t | {rhs:<s}\n"

        s += '\n'

    print(s)
    st = txt.find(start_string) + len(start_string)
    end = txt.find(end_string)
    txt = txt[0:st] + s + txt[end:]
    with open(__file__, 'w') as (f):
        f.write(txt)