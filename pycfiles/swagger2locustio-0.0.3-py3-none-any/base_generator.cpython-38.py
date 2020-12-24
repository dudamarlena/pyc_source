# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dpoliuha/work/opensource/swagger2locustio/swagger2locustio/generators/base_generator.py
# Compiled at: 2020-05-08 14:29:31
# Size of source mod 2**32: 10292 bytes
"""Module: Base Generator"""
import re, logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Dict, Union, Any
import swagger2locustio.templates as l_templates
from swagger2locustio.templates import helpers_templates
from swagger2locustio.templates import auth_templates
from swagger2locustio.templates import constants_templates
LOG = logging.getLogger(__name__)
PATH_PARAMS_PATTERN = re.compile('{.*?}', re.UNICODE)
IDENTIFIER_PATTERN = re.compile('[^\\d\\w/]', re.UNICODE)

@dataclass(frozen=True)
class Constant:
    __doc__ = 'Data Class: Constant'
    name: str
    val: Any
    value_type: str


@dataclass
class TestMethod:
    __doc__ = 'Data Class: Test Method'
    method_data: str
    constants: List[Constant]


@dataclass
class TestClass:
    __doc__ = 'Data Class: Test Class'
    file_path: Path
    file_name: str
    class_name: str
    test_methods = field(default_factory=(lambda : []))
    test_methods: List[TestMethod]


class BaseGenerator:
    __doc__ = 'Class: Base Generator'

    def __init__(self, results_path: Path, strict_level: int):
        self.strict_level = strict_level
        self.test_classes_mapping = {}
        self.results_path = results_path
        self.constants_path = Path('constants')
        self.task_sets_path = Path('tasksets')
        self.tests_path = self.task_sets_path / 'generated_tests'
        (self.results_path / self.constants_path).mkdir(exist_ok=True, parents=True)
        (self.results_path / self.tests_path).mkdir(exist_ok=True, parents=True)

    def generate_locustfiles(self, swagger_data: dict) -> None:
        """Method: generate locustfiles"""
        self.generate_test_classes(swagger_data['paths'])
        security_cases = self.generate_security_cases(swagger_data['security'])
        test_classes_imports = []
        test_classes_inheritance = []
        for test_class in self.test_classes_mapping.values():
            methods_count = len(test_class.test_methods)
            if not methods_count:
                pass
            else:
                class_methods = []
                class_constants = set()

        for test_method in test_class.test_methods:
            class_methods.append(test_method.method_data)
            class_constants.update(test_method.constants)
        else:
            methods_str = ''.join(class_methods)
            class_file_path = self.results_path / self.tests_path / test_class.file_path
            class_file_path.mkdir(parents=True, exist_ok=True)
            file_name = f"{test_class.file_name}.py"
            constants_str = ', '.join([constant.name for constant in class_constants])
            import_path = str(self.tests_path / test_class.file_path / test_class.file_name).replace('/', '.')
            test_classes_imports.append(f"from {import_path} import {test_class.class_name}")
            test_classes_inheritance.append(test_class.class_name)
            (class_file_path / file_name).write_text(l_templates.TEST_CLASS_FILE.render(file_name=(test_class.file_name),
              test_methods=methods_str,
              class_name=(test_class.class_name),
              constants=constants_str))
            if class_constants:
                (self.results_path / self.constants_path / file_name).write_text(constants_templates.CONSTANTS_FILE.render(constants=class_constants))
            (self.results_path / 'locustfile.py').write_text(l_templates.MAIN_LOCUSTFILE.render(host=(swagger_data['host'])))
            (self.results_path / self.task_sets_path / 'base.py').write_text(l_templates.BASE_TASKSET_FILE.render(security_cases=security_cases))
            (self.results_path / self.task_sets_path / 'generated_taskset.py').write_text(l_templates.GENERATED_TASKSET_FILE.render(test_classes_names=test_classes_inheritance,
              test_classes_imports=test_classes_imports))
            (self.results_path / self.task_sets_path / 'helper.py').write_text(helpers_templates.HELPER_CLASS.render())
            (self.results_path / self.constants_path / 'base_constants.py').write_text(constants_templates.CONSTANTS_BASE_FILE.render())
            LOG.info('%s test methods were created successfully', len(test_classes_inheritance))

    def _get_or_create_test_class(self, ulr_path: str) -> TestClass:
        file_path_str = re.sub(PATH_PARAMS_PATTERN, '', ulr_path)
        file_path_str = file_path_str.strip('/')
        file_path_str = re.sub(IDENTIFIER_PATTERN, '_', file_path_str)
        file_path_list = file_path_str.split('/')
        file_name = file_path_list[(-1)]
        file_path = Path(*file_path_list[:-1])
        if not file_name.isidentifier():
            file_name = 'test_' + file_name
        file_name = file_name.replace('_', ' ')
        file_name = file_name.title()
        class_name = file_name.replace(' ', '')
        file_name = file_name.replace(' ', '_')
        test_class = self.test_classes_mapping.get(class_name)
        if test_class is None:
            test_class = TestClass(file_path=file_path, file_name=file_name, class_name=class_name)
            self.test_classes_mapping[class_name] = test_class
        return test_class

    def generate_test_classes--- This code section failed: ---

 L. 135         0  LOAD_FAST                'paths_data'
                2  LOAD_METHOD              items
                4  CALL_METHOD_0         0  ''
                6  GET_ITER         
                8  FOR_ITER            220  'to 220'
               10  UNPACK_SEQUENCE_2     2 
               12  STORE_FAST               'ulr_path'
               14  STORE_FAST               'methods_data'

 L. 136        16  LOAD_FAST                'self'
               18  LOAD_METHOD              _get_or_create_test_class
               20  LOAD_FAST                'ulr_path'
               22  CALL_METHOD_1         1  ''
               24  STORE_FAST               'test_class'

 L. 138        26  LOAD_FAST                'methods_data'
               28  LOAD_METHOD              items
               30  CALL_METHOD_0         0  ''
               32  GET_ITER         
               34  FOR_ITER            218  'to 218'
               36  UNPACK_SEQUENCE_2     2 
               38  STORE_FAST               'method'
               40  STORE_FAST               'method_data'

 L. 140        42  BUILD_LIST_0          0 
               44  STORE_FAST               'constants'

 L. 141        46  SETUP_FINALLY        80  'to 80'

 L. 142        48  LOAD_FAST                'self'
               50  LOAD_METHOD              extract_params
               52  LOAD_FAST                'method_data'
               54  LOAD_METHOD              get
               56  LOAD_STR                 'params'
               58  BUILD_MAP_0           0 
               60  CALL_METHOD_2         2  ''
               62  LOAD_FAST                'constants'
               64  LOAD_GLOBAL              len
               66  LOAD_FAST                'test_class'
               68  LOAD_ATTR                test_methods
               70  CALL_FUNCTION_1       1  ''
               72  CALL_METHOD_3         3  ''
               74  STORE_FAST               'params'
               76  POP_BLOCK        
               78  JUMP_FORWARD        132  'to 132'
             80_0  COME_FROM_FINALLY    46  '46'

 L. 143        80  DUP_TOP          
               82  LOAD_GLOBAL              ValueError
               84  COMPARE_OP               exception-match
               86  POP_JUMP_IF_FALSE   130  'to 130'
               88  POP_TOP          
               90  STORE_FAST               'error'
               92  POP_TOP          
               94  SETUP_FINALLY       118  'to 118'

 L. 144        96  LOAD_GLOBAL              logging
               98  LOAD_METHOD              warning
              100  LOAD_FAST                'error'
              102  CALL_METHOD_1         1  ''
              104  POP_TOP          

 L. 145       106  POP_BLOCK        
              108  POP_EXCEPT       
              110  CALL_FINALLY        118  'to 118'
              112  JUMP_BACK            34  'to 34'
              114  POP_BLOCK        
              116  BEGIN_FINALLY    
            118_0  COME_FROM           110  '110'
            118_1  COME_FROM_FINALLY    94  '94'
              118  LOAD_CONST               None
              120  STORE_FAST               'error'
              122  DELETE_FAST              'error'
              124  END_FINALLY      
              126  POP_EXCEPT       
              128  JUMP_FORWARD        132  'to 132'
            130_0  COME_FROM            86  '86'
              130  END_FINALLY      
            132_0  COME_FROM           128  '128'
            132_1  COME_FROM            78  '78'

 L. 146       132  LOAD_GLOBAL              l_templates
              134  LOAD_ATTR                FUNC
              136  LOAD_ATTR                render

 L. 147       138  LOAD_FAST                'test_class'
              140  LOAD_ATTR                file_name
              142  LOAD_METHOD              lower
              144  CALL_METHOD_0         0  ''
              146  FORMAT_VALUE          0  ''
              148  LOAD_STR                 '_test_'
              150  LOAD_GLOBAL              len
              152  LOAD_FAST                'test_class'
              154  LOAD_ATTR                test_methods
              156  CALL_FUNCTION_1       1  ''
              158  FORMAT_VALUE          0  ''
              160  BUILD_STRING_3        3 

 L. 148       162  LOAD_FAST                'method'

 L. 149       164  LOAD_FAST                'ulr_path'

 L. 150       166  LOAD_FAST                'params'
              168  LOAD_STR                 'path_params'
              170  BINARY_SUBSCR    

 L. 151       172  LOAD_FAST                'params'
              174  LOAD_STR                 'query_params'
              176  BINARY_SUBSCR    

 L. 152       178  LOAD_FAST                'params'
              180  LOAD_STR                 'header_params'
              182  BINARY_SUBSCR    

 L. 153       184  LOAD_FAST                'params'
              186  LOAD_STR                 'cookie_params'
              188  BINARY_SUBSCR    

 L. 146       190  LOAD_CONST               ('func_name', 'method', 'path', 'path_params', 'query_params', 'header_params', 'cookie_params')
              192  CALL_FUNCTION_KW_7     7  '7 total positional and keyword args'
              194  STORE_FAST               'test_method_data'

 L. 155       196  LOAD_FAST                'test_class'
              198  LOAD_ATTR                test_methods
              200  LOAD_METHOD              append
              202  LOAD_GLOBAL              TestMethod
              204  LOAD_FAST                'test_method_data'
              206  LOAD_FAST                'constants'
              208  LOAD_CONST               ('method_data', 'constants')
              210  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              212  CALL_METHOD_1         1  ''
              214  POP_TOP          
              216  JUMP_BACK            34  'to 34'
              218  JUMP_BACK             8  'to 8'

Parse error at or near `CALL_FINALLY' instruction at offset 110

    def extract_params(self, params: dict, constants: List[Constant], method_num: int) -> Dict[(str, Union[(str, dict)])]:
        """Method: extract params"""
        path_params = []
        query_params = []
        header_params = []
        cookie_params = []
        for param, param_config in params.items():
            param_location = param_config.get('in')
            if param_location == 'query':
                target_params = query_params
            else:
                if param_location == 'path':
                    target_params = path_params
                else:
                    if param_location == 'header':
                        target_params = header_params
                    else:
                        if param_location == 'cookie':
                            target_params = cookie_params
                        else:
                            raise ValueError(f"Not valid {param} `in` value: {param_location}", param_config)
            target_params.append(param_config)
        else:
            extracted_params = {'path_params':self._format_params(path_params, 'path', constants, method_num), 
             'query_params':self._format_params(query_params, 'query', constants, method_num), 
             'header_params':self._format_params(header_params, 'header', constants, method_num), 
             'cookie_params':self._format_params(cookie_params, 'cookie', constants, method_num)}
            return extracted_params

    @staticmethod
    def _format_params(raw_params: List[dict], param_type, constants, method_num: int) -> Union[(str, dict)]:
        params = []
        for param in raw_params:
            param_name = param.get('name', '')
            const_name = param_name.upper() + f"__{method_num}"
            param_val = param.get('default')
            param_val_type = param.get('type', '')
            const_val = repr(param_val)
            if param_val is None:
                const_val = helpers_templates.HELPER_MAPPING.get(param_val_type, '')
            param_val = helpers_templates.HELPER_MAPPING['choice'].format(values=const_name)
            constants.append(Constant(name=const_name, val=const_val, value_type=param_val_type))
            if param_type == 'path':
                params.append(l_templates.PATH_PARAM_PAIR.render(key=param_name, val=param_val))
            else:
                params.append(l_templates.DICT_PARAM_PAIR.render(key=param_name, val=param_val))
        else:
            if param_type == 'path':
                formatted_params = ''
                if params:
                    formatted_params = ', ' + ', '.join(params)
            else:
                formatted_params = '{}'
                if params:
                    formatted_params = '{' + ', '.join(params) + '}'
            return formatted_params

    @staticmethod
    def generate_security_cases(security_data: dict) -> str:
        """Method: generate security cases"""
        security_cases = []
        for security_type, security_config in security_data.items():
            if security_type == 'basic':
                security_cases.append(auth_templates.AUTH_BASIC.render(security_config=security_config))
            elif security_type == 'apiKey':
                location = security_config.get('in')
                name = security_config.get('name')
                if location.lower() == 'header' and name:
                    security_cases.append(auth_templates.AUTH_KEY_HEADER.render(name=name, security_config=security_config))
                else:
                    raise ValueError(security_config)
            else:
                security_cases.append(auth_templates.AUTH_UNDEFINED.render(security_config=security_config))
        else:
            return ''.join(security_cases)