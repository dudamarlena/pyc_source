# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\aggregate\underwriter.py
# Compiled at: 2020-01-13 09:06:16
# Size of source mod 2**32: 35918 bytes
__doc__ = "\n=================\nUnderwriter Class\n=================\n\nThe Underwriter is an easy to use interface into the computational functionality of aggregate.\n\nThe Underwriter\n---------------\n\n* Maintains a default library of severity curves\n* Maintains a default library of aggregate distributions corresponding to industry losses in\n  major classes of business, total catastrophe losses from major perils, and other useful constructs\n* Maintains a default library of portfolios, including several example instances and examples used in\n  papers on risk theory (e.g. the Bodoff examples)\n\n\nThe library functions can be listed using\n\n::\n\n        uw.list()\n\nor, for more detail\n\n::\n\n        uw.describe()\n\nA given example can be inspected using ``uw['cmp']`` which returns the defintion of the database\nobject cmp (an aggregate representing industry losses from the line Commercial Multiperil). It can\nbe created as an Aggregate class using ``ag = uw('cmp')``. The Aggregate class can then be updated,\nplotted and various reports run on it. In iPython or Jupyter ``ag`` returns an informative HTML\ndescription.\n\nThe real power of Underwriter is access to the agg scripting language (see parser module). The scripting\nlanguage allows severities, aggregates and portfolios to be created using more-or-less natural language.\nFor example\n\n::\n\n        pf = uw('''\n        port MyCompanyBook\n            agg LineA 100 claims 100000 xs 0 sev lognorm 30000 cv 1.25\n            agg LineB 150 claims 250000 xs 5000 sev lognorm 50000 cv 0.9\n            agg Cat 2 claims 100000000 xs 0 sev 500000 * pareto 1.8 - 500000\n        ''')\n\ncreates a portfolio with three sublines, LineA, LineB and Cat. LineA is 100 (expected) claims, each pulled\nfrom a lognormal distribution with mean of 30000 and coefficient of variation 1.25 within the layer\n100000 xs 0 (i.e. limited at 100000). The frequency distribution is Poisson. LineB is similar. Cat is jsut\n2 claims from the indicated limit, with severity given by a Pareto distribution with shape parameter 1.8,\nscale 500000, shifted left by 500000. This corresponds to the usual Pareto with survival function\nS(x) = (lambda / (lambda + x))^1.8, x >= 0.\n\nThe portfolio can be approximated using FFTs to convolve the aggregates and add the lines. The severities\nare first discretized using a certain bucket-size (bs). The port object has a port.recommend_bucket() to\nsuggest reasonable buckets:\n\n>> pf.recommend_bucket()\n\n+-------+---------+--------+--------+--------+-------+-------+-------+------+------+\n|       | bs10    | bs11   | bs12   | bs13   | bs14  | bs15  | bs16  | bs18 | bs20 |\n+=======+=========+========+========+========+=======+=======+=======+======+======+\n| LineA | 3,903   | 1,951  | 976    | 488    | 244   | 122   | 61.0  | 15.2 | 3.8  |\n+-------+---------+--------+--------+--------+-------+-------+-------+------+------+\n| LineB | 8,983   | 4,491  | 2,245  | 1,122  | 561   | 280   | 140   | 35.1 | 8.8  |\n+-------+---------+--------+--------+--------+-------+-------+-------+------+------+\n| Cat   | 97,656  | 48,828 | 24,414 | 12,207 | 6,103 | 3,051 | 1,525 | 381  | 95.4 |\n+-------+---------+--------+--------+--------+-------+-------+-------+------+------+\n| total | 110,543 | 55,271 | 27,635 | 13,817 | 6,908 | 3,454 | 1,727 | 431  | 108  |\n+-------+---------+--------+--------+--------+-------+-------+-------+------+------+\n\nThe column bsNcorrespond to discretizing with 2**N buckets. The rows show suggested bucket sizes for each\nline and in total. For example with N=13 (i.e. 8196 buckets) the suggestion is 13817. It is best the bucket\nsize is a divisor of any limits or attachment points, so we select 10000.\n\nUpdating can then be run as\n\n::\n\n    bs = 10000\n    pf.update(13, bs)\n    pf.report('quick')\n    pf.plot('density')\n    pf.plot('density', logy=True)\n    print(pf)\n\n    Portfolio name           MyCompanyBook\n    Theoretic expected loss     10,684,541.2\n    Actual expected loss        10,657,381.1\n    Error                          -0.002542\n    Discretization size                   13\n    Bucket size                     10000.00\n    <aggregate.port.Portfolio object at 0x0000023950683CF8>\n\n\nEtc. etc.\n\n"
import os, numpy as np
import IPython.core.display as display
import logging, pandas as pd
from collections import Iterable
from .port import Portfolio
from .utils import html_title
from .distr import Aggregate, Severity
from .parser import UnderwritingLexer, UnderwritingParser
import re, warnings
logger = logging.getLogger('aggregate')

class Underwriter(object):
    """Underwriter"""
    data_types = [
     'portfolio', 'aggregate', 'severity']

    def __init__(self, dir_name='', name='Rory', databases=None, glob=None, store_mode=True, update=False, verbose=False, log2=10, debug=False, create_all=False):
        """

        :param dir_name:
        :param name:
        :param databases:
        :param glob: reference, e.g. to globals(), used to resolve meta.XX references
        :param store_mode: add newly created aggregates to the database?
        :param update:
        :param verbose:
        :param log2:
        :param debug: run parser in debug mode
        :param create_all: by default write only creates portfolios.
        """
        self.last_spec = None
        self.name = name
        self.update = update
        self.log2 = log2
        self.debug = debug
        self.verbose = verbose
        self.glob = glob
        self.lexer = UnderwritingLexer()
        self.parser = UnderwritingParser(self._safe_lookup, debug)
        self.severity = {}
        self.aggregate = {}
        self.portfolio = {}
        if databases is None:
            databases = [
             'site.agg', 'user.agg']
        self.dir_name = dir_name
        if self.dir_name == '':
            self.dir_name = os.path.split(__file__)[0]
            self.dir_name = os.path.join(self.dir_name, 'agg')
        self.store_mode = True
        for fn in databases:
            with open(os.path.join(self.dir_name, fn), 'r') as (f):
                program = f.read()
            self._runner(program)

        self.store_mode = store_mode
        self.create_all = create_all

    def __getitem__(self, item):
        """
        handles self[item]

        subscriptable: try user portfolios, b/in portfolios, line, severity
        to access specifically use severity or line methods

        :param item:
        :return:
        """
        obj = self.portfolio.get(item, None)
        if obj is not None:
            logger.info(f"Underwriter.__getitem__ | found {item} of type port")
            return (
             'port', obj)
        obj = self.aggregate.get(item, None)
        if obj is not None:
            logger.info(f"Underwriter.__getitem__ | found {item} of type agg")
            return (
             'agg', obj)
        obj = self.severity.get(item, None)
        if obj is not None:
            logger.info(f"Underwriter.__getitem__ | found {item} of type sev")
            return (
             'sev', obj)
        raise LookupError(f"Item {item} not found in any database")

    def _repr_html_(self):
        s = [
         f"<h1>Underwriter {self.name}</h1>"]
        s.append(f"Underwriter expert in all classes including {len(self.severity)} severities, {len(self.aggregate)} aggregates and {len(self.portfolio)} portfolios<br>")
        for what in ('severity', 'aggregate', 'portfolio'):
            s.append(f"<b>{what.title()}</b>: ")
            s.append(', '.join([k for k in sorted(getattr(self, what).keys())]))
            s.append('<br>')

        s.append('<h3>Settings</h3>')
        for k in ('update', 'log2', 'store_mode', 'verbose', 'last_spec', 'create_all'):
            s.append(f'<span style="color: red;">{k}</span>: {getattr(self, k)}; ')

        return '\n'.join(s)

    def __call__(self, portfolio_program, **kwargs):
        """
        make the Underwriter object callable; pass through to write

        :param portfolio_program:
        :return:
        """
        return (self.write)(portfolio_program, **kwargs)

    def list(self):
        """
        list all available databases

        :return:
        """
        sers = dict()
        for k in Underwriter.data_types:
            d = sorted(list(self.__getattribute__(k).keys()))
            sers[k.title()] = pd.Series(d, index=(range(len(d))), name=k)

        df = pd.DataFrame(data=sers)
        df = df.fillna('')
        return df

    def describe(self, item_type='', pretty_print=False):
        """
        more informative version of list
        Pull notes for type items

        :return:
        """

        def deal_with_sequences(x):
            """
            pandas can't have a field set as a sequence
            need to check if x is a sequence and if so return something suitable...

            :param x:
            :return:
            """
            if isinstance(x, Iterable):
                return str(x)
            return x

        df = pd.DataFrame(columns=['Name', 'Type', 'Severity', 'ESev', 'Sev_a', 'Sev_b',
         'EN', 'Freq_a',
         'ELoss', 'Notes'])
        df = df.set_index('Name')
        df['ELoss'] = np.maximum(df.ELoss, df.ESev * df.EN)
        if item_type == '':
            item_type = Underwriter.data_types
        else:
            item_type = [
             item_type.lower()]
        for k in item_type:
            for kk, vv in self.__getattribute__(k).items():
                _data_fields = [
                 vv.get('sev_name', ''), vv.get('sev_mean', 0), vv.get('sev_a', 0),
                 vv.get('sev_b', 0), vv.get('exp_en', 0), vv.get('freq_a', 0),
                 vv.get('exp_el', 0), vv.get('note', '')]
                try:
                    df.loc[kk, :] = [
                     k] + _data_fields
                except ValueError as e:
                    try:
                        if e.args[0] == 'setting an array element with a sequence':
                            df.loc[kk, :] = [
                             k] + list(map(deal_with_sequences, _data_fields))
                        else:
                            raise e
                    finally:
                        e = None
                        del e

        df = df.fillna('')
        if pretty_print:
            for t, egs in df.groupby('Type'):
                html_title(t, 2)
                display(egs.style)

        return df

    def parse_portfolio_program(self, portfolio_program, output='spec'):
        """
        Utility routine to parse the program and return the spec suitable to pass to Portfolio to
        create the object.
        Initially just for a single portfolio program (which it checks!)
        No argument of default conniptions

        To write program in testing mode use output='df':

        * dictionary definitions are added to uw but no objects are created
        * returns data frame description of added severity/aggregate/portfolios
        * the dataframe of aggregates can be used to create a portfolio (with all the aggregates) by calling

        ```Portfolio.from_DataFrame(name df)```

        To parse and get dictionary definitions use output='spec'.
        Aggregate and severity objects are also returned though they could be
        accessed directly using wu['name']. May be convenient...we'll see.

        Output has form that an Aggregate can be created from Aggregate(**x['name'])
        etc. which is a bit easier than uw['name'] which returns the type.

        TODO make more robust

        :param portfolio_program:
        :param output:  'spec' output a spec (assumes only one portfolio),
                        or a dictionary {name: spec_list} if multiple
                        'df' or 'dataframe' output as pandas data frame
                        'dict' output as dictionary of pandas data frames (old write_test output)
        :return:
        """
        self._runner(portfolio_program)
        if self.glob is not None:
            for a in list(self.parser.agg_out_dict.values()) + list(self.parser.sev_out_dict.values()):
                if a['sev_name'][0:4] == 'meta':
                    obj_name = a['sev_name'][5:]
                    try:
                        obj = self.glob[obj_name]
                    except NameError as e:
                        try:
                            print(f"Object {obj_name} passed as a proto-severity cannot be found")
                            raise e
                        finally:
                            e = None
                            del e

                    a['sev_name'] = obj
                    logger.info(f"Underwriter.write | {a['sev_name']} ({type(a)} reference to {obj_name} replaced with object {obj.name} from glob")

        elif output == 'spec':
            if len(self.parser.port_out_dict) == 1:
                nm = ''
                spec_list = None
                for nm in self.parser.port_out_dict.keys():
                    spec_list = [self[v][1] for v in self.portfolio[nm]['spec']]

                return (nm, spec_list)
            if len(self.parser.port_out_dict) > 1 or len(self.parser.agg_out_dict) or len(self.parser.sev_out_dict):
                ans = {}
                for nm in self.parser.port_out_dict.keys():
                    spec_list = [self[v][1] for v in self.portfolio[nm]['spec']]
                    ans[nm] = dict(name=nm, spec_list=spec_list)

                for nm in self.parser.agg_out_dict.keys():
                    ans[nm] = self.aggregate[nm]

                for nm in self.parser.sev_out_dict.keys():
                    ans[nm] = self.severity[nm]

                return ans
            logger.warning('Underwriter.parse_portfolio_program | program has no Portfolio outputs. Nothing returned. ')
            return
        else:
            if output == 'df' or output.lower() == 'dataframe':
                logger.info(f"Runner.write_test | Executing program\n{portfolio_program[:500]}\n\n")
                ans = {}
                if len(self.parser.sev_out_dict) > 0:
                    for v in self.parser.sev_out_dict.values():
                        Underwriter._add_defaults(v, 'sev')

                    ans['sev'] = pd.DataFrame((list(self.parser.sev_out_dict.values())), index=(self.parser.sev_out_dict.keys()))
                if len(self.parser.agg_out_dict) > 0:
                    for v in self.parser.agg_out_dict.values():
                        Underwriter._add_defaults(v)

                    ans['agg'] = pd.DataFrame((list(self.parser.agg_out_dict.values())), index=(self.parser.agg_out_dict.keys()))
                if len(self.parser.port_out_dict) > 0:
                    ans['port'] = pd.DataFrame((list(self.parser.port_out_dict.values())), index=(self.parser.port_out_dict.keys()))
                return ans
            raise ValueError(f"Inadmissible output type {output}  passed to parse_portfolio_program. Expecting spec or df/dataframe.")

    def write(self, portfolio_program, **kwargs):
        """
        Write a natural language program. Write carries out the following steps.

        1. Read in the program and cleans it (e.g. punctuation, parens etc. are
        removed and ignored, replace ; with new line etc.)
        2. Parse line by line to create a dictioonary definition of sev, agg or port objects
        3. If glob set, pull in objects
        4. replace sev.name, agg.name and port.name references with their objects
        5. If create_all set, create all objects and return in dictionary. If not set only create the port objects
        6. If update set, update all created objects.

        Sample input

        ::

            port MY_PORTFOLIO
                agg Line1 20  loss 3 x 2 sev gamma 5 cv 0.30 mixed gamma 0.4
                agg Line2 10  claims 3 x 2 sevgamma 12 cv 0.30 mixed gamma 1.2
                agg Line 3100  premium at 0.4 3 x 2 sev 4 * lognormal 3 cv 0.8 fixed 1

        The indents are required...

        See parser for full language spec! See Aggregate class for many examples.

        Reasonable kwargs:

        * bs
        * log2
        * verbose
        * update overrides class default
        * add_exa should port.add_exa add the exa related columns to the output?
        * create_all: create all objects, default just portfolios. You generally
                     don't want to create underlying sevs and aggs in a portfolio.

        :param portfolio_program:
        :param kwargs:
        :return: single created object or dictionary name: object
        """
        create_all = kwargs.get('create_all', self.create_all)
        update = kwargs.get('update', self.update)
        if update:
            if 'log2' in kwargs:
                log2 = kwargs.get('log2')
                del kwargs['log2']
            else:
                log2 = self.log2
            if 'bs' in kwargs:
                bs = kwargs.get('bs')
                del kwargs['bs']
            else:
                bs = 0
            if 'verbose' in kwargs:
                verbose = kwargs.get('verbose')
                del kwargs['verbose']
            else:
                verbose = self.verbose
            if 'add_exa' in kwargs:
                add_exa = kwargs.get('add_exa')
                del kwargs['add_exa']
            else:
                add_exa = False

        def _update(s, k):
            if update:
                if bs > 0 and log2 > 0:
                    _bs = bs
                    _log2 = log2
                elif bs == 0:
                    _bs = s.recommend_bucket().iloc[(-1, 0)]
                    _log2 = log2
                    _bs *= 2 ** (10 - _log2)
                else:
                    logger.warning('Underwriter.write | nonsensical options bs > 0 and log2 = 0')
                    _bs = bs
                    _log2 = 10
                logger.info(f"Underwriter.write | updating Portfolio {k} log2={_log2}, bs={_bs}")
                (s.update)(log2=_log2, bs=_bs, verbose=verbose, add_exa=add_exa, **kwargs)

        lookup_success = True
        _type = ''
        obj = None
        try:
            _type, obj = self.__getitem__(portfolio_program)
        except LookupError:
            lookup_success = False
            logger.info(f"underwriter.write | object {portfolio_program[:500]} not found, will process as program")

        if lookup_success:
            logger.info(f"underwriter.write | object {portfolio_program[:500]} found, returning object...")
            if _type == 'agg':
                _name = obj.get('name', portfolio_program)
                obj = Aggregate(_name, **)
                if update:
                    obj.easy_update(log2, bs)
                return obj
            if _type == 'port':
                obj = Portfolio(portfolio_program, [self[v][1] for v in obj['spec']])
                _update(obj, portfolio_program)
                return obj
            if _type == 'sev':
                if 'sev_wt' in obj:
                    del obj['sev_wt']
                return Severity(**obj)
            ValueError(f"Cannot build {_type} objects")
            return obj
        self._runner(portfolio_program)
        if self.glob is not None:
            logger.info('Underwriter.write | Resolving globals')
            for a in list(self.parser.agg_out_dict.values()) + list(self.parser.sev_out_dict.values()):
                if a['sev_name'][0:4] == 'meta':
                    logger.info(f"Underwriter.write | Resolving {a['sev_name']}")
                    obj_name = a['sev_name'][5:]
                    try:
                        obj = self.glob[obj_name]
                    except NameError as e:
                        try:
                            print(f"Object {obj_name} passed as a proto-severity cannot be found")
                            raise e
                        finally:
                            e = None
                            del e

                    a['sev_name'] = obj
                    logger.info(f"Underwriter.write | {a['sev_name']} ({type(a)} reference to {obj_name} replaced with object {obj.name} from glob")

            logger.info('Underwriter.write | Done resolving globals')
        else:
            rv = None
            if len(self.parser.port_out_dict) > 0:
                rv = {}
                for k in self.parser.port_out_dict.keys():
                    s = Portfolio(k, [self[v][1] for v in self.portfolio[k]['spec']])
                    s.program = 'unknown'
                    _update(s, k)
                    rv[k] = s

                if len(self.parser.port_out_dict) == 1:
                    s.program = portfolio_program
            if len(self.parser.agg_out_dict) > 0 and create_all:
                if rv is None:
                    rv = {}
                for k, v in self.parser.agg_out_dict.items():
                    s = Aggregate(k, **)
                    if update:
                        s.easy_update((self.log2), verbose=verbose)
                    rv[k] = s

        if len(self.parser.sev_out_dict) > 0:
            if create_all:
                if rv is None:
                    rv = {}
                for v in self.parser.sev_out_dict.values():
                    if 'sev_wt' in v:
                        del v['sev_wt']
                    s = Severity(**v)
                    rv[f"sev_{s.__repr__()[38:54]}"] = s

            if rv is None:
                print('WARNING: Program did not contain any output...')
                logger.warning(f"Underwriter.write | Program {portfolio_program} did not contain any output")
        elif len(rv):
            logger.info(f"Underwriter.write | Program created {len(rv)} objects and defined {len(self.parser.port_out_dict)} Portfolio(s), {len(self.parser.agg_out_dict)} Aggregate(s), and {len(self.parser.sev_out_dict)} Severity(ies)")
        if len(rv) == 1:
            rv = rv.popitem()[1]
        return rv

    def write_from_file(self, file_name, **kwargs):
        """
        read program from file. delegates to write

        :param file_name:
        :param update:
        :param verbose:
        :param log2:
        :param bs:
        :param kwargs:
        :return:
        """
        with open(file_name, 'r', encoding='utf-8') as (f):
            portfolio_program = f.read()
        return (self.write)(portfolio_program, **kwargs)

    def write_test(self, portfolio_program):
        """
        write programs in testing mode

        dictionary definitions are added to uw but no objects are created

        returns data frame description of added severity/aggregate/portfolios

        the dataframe of aggregates can be used to create a portfolio (with all the aggregates) by calling

        ```Portfolio.from_DataFrame(name df)```

        TODO rationalize with parse_portfolio_program

        :param portfolio_program:
        :return: dictionary with keys sev agg port and assoicated dataframes
        """
        print('write_test deprecated...use parse_portfolio_porgram with output="dict".')
        raise RuntimeError

    def _runner(self, portfolio_program):
        """
        preprocessing:
            remove 
 in [] (vectors) e.g. put by f{np.linspace} TODO only works for 1d vectors
            ; mapped to newline
            backslash (line continuation) mapped to space
            split on newlines
            parse one line at a time
            PIPE format no longer supported

        error handling and piping through parser

        :param portfolio_program:
        :return:
        """
        portfolio_program = re.sub('\\s*#[^\\n]*\\n', '\\n', portfolio_program)
        out_in = re.split('\\[|\\]', portfolio_program)
        assert len(out_in) % 2
        odd = [t.replace('\n', ' ') for t in out_in[1::2]]
        even = out_in[0::2]
        portfolio_program = ' '.join([even[0]] + [f"[{o}] {e}" for o, e in zip(odd, even[1:])])
        portfolio_program = [i.strip() for i in portfolio_program.replace('\\\n', ' ').replace('\n\t', ' ').replace('\n    ', ' ').replace(';', '\n').split('\n') if len(i.strip()) > 0]
        self.parser.reset()
        for program_line in portfolio_program:
            try:
                if len(program_line) > 0:
                    self.parser.parse(self.lexer.tokenize(program_line))
            except ValueError as e:
                try:
                    if isinstance(e.args[0], str):
                        print(e)
                        raise e
                    else:
                        t = e.args[0].type
                        v = e.args[0].value
                        i = e.args[0].index
                        txt2 = program_line[0:i] + '>>>' + program_line[i:]
                        print(f'Parse error in input "{txt2}"\nValue {v} of type {t} not expected')
                        raise e
                finally:
                    e = None
                    del e

        if self.store_mode:
            if len(self.parser.sev_out_dict) > 0:
                self.severity.update(self.parser.sev_out_dict)
                logger.info(f"Underwriter._runner | saving {self.parser.sev_out_dict.keys()} severity/ies")
            if len(self.parser.agg_out_dict) > 0:
                self.aggregate.update(self.parser.agg_out_dict)
                logger.info(f"Underwriter._runner | saving {self.parser.agg_out_dict.keys()} aggregate(s)")
            if len(self.parser.port_out_dict) > 0:
                for k, v in self.parser.port_out_dict.items():
                    logger.info(f"Underwriter._runner | saving {k} portfolio")
                    self.portfolio[k] = {'spec':v['spec'],  'arg_dict':{}}

    @staticmethod
    def _add_defaults--- This code section failed: ---

 L. 744         0  LOAD_GLOBAL              dict
                2  LOAD_STR                 ''
                4  LOAD_CONST               0
                6  LOAD_CONST               0
                8  LOAD_CONST               0
               10  LOAD_CONST               0
               12  LOAD_CONST               0
               14  LOAD_GLOBAL              np
               16  LOAD_ATTR                inf

 L. 745        18  LOAD_STR                 ''
               20  LOAD_CONST               0
               22  LOAD_CONST               0
               24  LOAD_CONST               0
               26  LOAD_CONST               0
               28  LOAD_CONST               0
               30  LOAD_CONST               0
               32  LOAD_CONST               1

 L. 746        34  LOAD_STR                 'poisson'
               36  LOAD_CONST               0
               38  LOAD_CONST               0
               40  LOAD_CONST               ('name', 'exp_el', 'exp_premium', 'exp_lr', 'exp_en', 'exp_attachment', 'exp_limit', 'sev_name', 'sev_a', 'sev_b', 'sev_mean', 'sev_cv', 'sev_scale', 'sev_loc', 'sev_wt', 'freq_name', 'freq_a', 'freq_b')
               42  CALL_FUNCTION_KW_18    18  '18 total positional and keyword args'
               44  STORE_FAST               'defaults'

 L. 747        46  LOAD_FAST                'kind'
               48  LOAD_STR                 'agg'
               50  COMPARE_OP               ==
               52  POP_JUMP_IF_FALSE    94  'to 94'

 L. 748        54  SETUP_LOOP          164  'to 164'
               56  LOAD_FAST                'defaults'
               58  LOAD_METHOD              items
               60  CALL_METHOD_0         0  ''
               62  GET_ITER         
             64_0  COME_FROM            78  '78'
               64  FOR_ITER             90  'to 90'
               66  UNPACK_SEQUENCE_2     2 
               68  STORE_FAST               'k'
               70  STORE_FAST               'v'

 L. 749        72  LOAD_FAST                'k'
               74  LOAD_FAST                'dict_'
               76  COMPARE_OP               not-in
               78  POP_JUMP_IF_FALSE    64  'to 64'

 L. 750        80  LOAD_FAST                'v'
               82  LOAD_FAST                'dict_'
               84  LOAD_FAST                'k'
               86  STORE_SUBSCR     
               88  JUMP_BACK            64  'to 64'
               90  POP_BLOCK        
               92  JUMP_FORWARD        164  'to 164'
             94_0  COME_FROM            52  '52'

 L. 751        94  LOAD_FAST                'kind'
               96  LOAD_STR                 'sev'
               98  COMPARE_OP               ==
              100  POP_JUMP_IF_FALSE   164  'to 164'

 L. 752       102  SETUP_LOOP          164  'to 164'
              104  LOAD_FAST                'defaults'
              106  LOAD_METHOD              items
              108  CALL_METHOD_0         0  ''
              110  GET_ITER         
            112_0  COME_FROM           150  '150'
            112_1  COME_FROM           142  '142'
            112_2  COME_FROM           134  '134'
              112  FOR_ITER            162  'to 162'
              114  UNPACK_SEQUENCE_2     2 
              116  STORE_FAST               'k'
              118  STORE_FAST               'v'

 L. 753       120  LOAD_FAST                'k'
              122  LOAD_CONST               0
              124  LOAD_CONST               3
              126  BUILD_SLICE_2         2 
              128  BINARY_SUBSCR    
              130  LOAD_STR                 'sev'
              132  COMPARE_OP               ==
              134  POP_JUMP_IF_FALSE   112  'to 112'
              136  LOAD_FAST                'k'
              138  LOAD_FAST                'dict_'
              140  COMPARE_OP               not-in
              142  POP_JUMP_IF_FALSE   112  'to 112'
              144  LOAD_FAST                'k'
              146  LOAD_STR                 'sev_wt'
              148  COMPARE_OP               !=
              150  POP_JUMP_IF_FALSE   112  'to 112'

 L. 754       152  LOAD_FAST                'v'
              154  LOAD_FAST                'dict_'
              156  LOAD_FAST                'k'
              158  STORE_SUBSCR     
              160  JUMP_BACK           112  'to 112'
              162  POP_BLOCK        
            164_0  COME_FROM_LOOP      102  '102'
            164_1  COME_FROM           100  '100'
            164_2  COME_FROM            92  '92'
            164_3  COME_FROM_LOOP       54  '54'

Parse error at or near `COME_FROM' instruction at offset 164_2

    def _safe_lookup(self, full_uw_id):
        """
        lookup uw_id in uw of expected type and merge safely into self.arg_dict
        delete name and note if appropriate

        :param full_uw_id:  type.name format
        :return:
        """
        expected_type, uw_id = full_uw_id.split('.')
        try:
            found_type, found_dict = self[uw_id]
        except LookupError as e:
            try:
                print(f"ERROR id {expected_type}.{uw_id} not found")
                raise e
            finally:
                e = None
                del e

        logger.info(f"UnderwritingParser._safe_lookup | retrieved {uw_id} as type {found_type}")
        if found_type != expected_type:
            raise ValueError(f"Error: type of {uw_id} is  {found_type}, not expected {expected_type}")
        return found_dict.copy()

    @staticmethod
    def obj_to_agg(obj):
        """
        convert an object into an agg language specification, used for saving
        :param obj: a dictionary, Aggregate, Severity or Portfolio object
        :return:
        """
        pass