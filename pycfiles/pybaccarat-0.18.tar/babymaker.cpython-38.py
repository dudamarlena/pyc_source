# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyBabyMaker/babymaker.py
# Compiled at: 2020-05-01 05:18:06
# Size of source mod 2**32: 4441 bytes
from pyBabyMaker.base import BaseCppGenerator, BaseConfigParser, BaseMaker

class BabyCppGenerator(BaseCppGenerator):

    def gen(self):
        result = ''
        result += self.gen_timestamp()
        result += self.gen_headers()
        result += self.gen_preamble()
        result += self.gen_body()
        return result

    def gen_preamble(self):
        result = ''
        for data_store in self.instructions:
            result += self.gen_preamble_single_output_tree(data_store)

        return result

    def gen_body(self):
        function_calls = ''.join(['generator_{}(input_file, output_file);\n'.format(self.cpp_make_var(i.output_tree)) for i in self.instructions])
        body = '\nTFile *input_file = new TFile(argv[1], "read");\nTFile *output_file = new TFile(argv[2], "recreate");\n\n{}\n\noutput_file->Close();\n\ndelete input_file;\ndelete output_file;\n'.format(function_calls)
        return self.cpp_main(body)

    def gen_preamble_single_output_tree(self, data_store):
        """
        Generate the body of function call for each ``input_tree`` and
        ``output_tree``.
        """
        input_tree = self.cpp_TTreeReader('reader', data_store.input_tree, 'input_file')
        output_tree = self.cpp_TTree('output', data_store.output_tree)
        input_br = ''.join([self.cpp_TTreeReaderValue(v.type, v.name, 'reader', v.name) for v in data_store.input_br])
        output_br = []
        for v in data_store.output_br:
            output_br.append('{} {}_out;\n'.format(v.type, v.name))
            output_br.append('output.Branch("{0}", &{0}_out);\n'.format(v.name))

        output_br = ''.join(output_br)
        transient = ''.join(['{} {} = {};\n'.format(v.type, v.name, self.dereference_variables(v.rvalue, data_store.input_br)) for v in data_store.transient])
        output_vars = ''.join(['{}_out = {};\n'.format(v.name, self.dereference_variables(v.rvalue, data_store.input_br)) for v in data_store.output_br])
        if not data_store.selection:
            loop = '{output_vars}\noutput.Fill();'.format(output_vars=output_vars)
        else:
            loop = 'if ({selection}) {{\n  {output_vars}\n  output.Fill();\n}}'.format(output_vars=output_vars,
              selection=(self.dereference_variables(data_store.selection, data_store.input_br)))
        result = '\nvoid generator_{name}(TFile *input_file, TFile *output_file) {{\n  {input_tree}\n  {output_tree}\n\n  {input_br}\n  {output_br}\n\n  while (reader.Next()) {{\n    {transient}\n    {loop}\n  }}\n\n  output_file->Write();\n}}\n'.format(name=(self.cpp_make_var(data_store.output_tree)),
          input_tree=input_tree,
          output_tree=output_tree,
          input_br=input_br,
          output_br=output_br,
          transient=transient,
          loop=loop)
        return result


class BabyMaker(BaseMaker):
    """BabyMaker"""

    def __init__(self, config_filename, ntuple_filename, use_reformater=True):
        """
        Initialize with path to YAML file and n-tuple file.
        """
        self.config_filename = config_filename
        self.ntuple_filename = ntuple_filename
        self.use_reformater = use_reformater

    def gen--- This code section failed: ---

 L. 121         0  LOAD_FAST                'self'
                2  LOAD_METHOD              read
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                config_filename
                8  CALL_METHOD_1         1  ''
               10  STORE_FAST               'parsed_config'

 L. 122        12  LOAD_FAST                'self'
               14  LOAD_METHOD              dump
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                ntuple_filename
               20  CALL_METHOD_1         1  ''
               22  STORE_FAST               'dumped_ntuple'

 L. 123        24  LOAD_FAST                'self'
               26  LOAD_METHOD              parse_config
               28  LOAD_FAST                'parsed_config'
               30  LOAD_FAST                'dumped_ntuple'
               32  CALL_METHOD_2         2  ''
               34  STORE_FAST               'parser'

 L. 124        36  LOAD_GLOBAL              BabyCppGenerator
               38  LOAD_FAST                'parser'
               40  LOAD_ATTR                instructions

 L. 125        42  LOAD_FAST                'parser'
               44  LOAD_ATTR                system_headers

 L. 126        46  LOAD_FAST                'parser'
               48  LOAD_ATTR                user_headers

 L. 124        50  BUILD_TUPLE_3         3 

 L. 127        52  LOAD_FAST                'kwargs'

 L. 124        54  CALL_FUNCTION_EX_KW     1  'keyword args'
               56  STORE_FAST               'generator'

 L. 128        58  LOAD_FAST                'generator'
               60  LOAD_METHOD              gen
               62  CALL_METHOD_0         0  ''
               64  STORE_FAST               'content'

 L. 130        66  LOAD_GLOBAL              open
               68  LOAD_FAST                'filename'
               70  LOAD_STR                 'w'
               72  CALL_FUNCTION_2       2  ''
               74  SETUP_WITH           92  'to 92'
               76  STORE_FAST               'f'

 L. 131        78  LOAD_FAST                'f'
               80  LOAD_METHOD              write
               82  LOAD_FAST                'content'
               84  CALL_METHOD_1         1  ''
               86  POP_TOP          
               88  POP_BLOCK        
               90  BEGIN_FINALLY    
             92_0  COME_FROM_WITH       74  '74'
               92  WITH_CLEANUP_START
               94  WITH_CLEANUP_FINISH
               96  END_FINALLY      

 L. 132        98  LOAD_FAST                'self'
              100  LOAD_ATTR                use_reformater
              102  POP_JUMP_IF_FALSE   114  'to 114'

 L. 133       104  LOAD_FAST                'self'
              106  LOAD_METHOD              reformat
              108  LOAD_FAST                'filename'
              110  CALL_METHOD_1         1  ''
              112  POP_TOP          
            114_0  COME_FROM           102  '102'

Parse error at or near `BEGIN_FINALLY' instruction at offset 90

    def parse_config(self, parsed_config, dumped_ntuple):
        parser = BaseConfigParserparsed_configdumped_ntuple
        parser.parse()
        return parser