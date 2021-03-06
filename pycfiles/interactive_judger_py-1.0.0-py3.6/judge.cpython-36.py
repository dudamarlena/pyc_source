# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/interactive_judger/judge.py
# Compiled at: 2018-08-03 01:03:40
# Size of source mod 2**32: 7178 bytes
import json, os, contextlib
from .tester import Tester
from .conf_generator import ConfigKeys
from .test_case_loader import Loader
WELCOME = "\n==========================================================================================\n//   ___       _                      _   _               _           _                  //\n//  |_ _|_ __ | |_ ___ _ __ __ _  ___| |_(___   _____    (_)_   _  __| | __ _  ___ _ __  //\n//   | || '_ \\| __/ _ | '__/ _` |/ __| __| \\ \\ / / _ \\   | | | | |/ _` |/ _` |/ _ | '__| //\n//   | || | | | ||  __| | | (_| | (__| |_| |\\ V |  __/   | | |_| | (_| | (_| |  __| |    //\n//  |___|_| |_|\\__\\___|_|  \\__,_|\\___|\\__|_| \\_/ \\___|  _/ |\\__,_|\\__,_|\\__, |\\___|_|    //\n//                                                     |__/             |___/            //\n=========================================================================================== \n                                || Version: 1.0.0           ||\n                                || Target Language: Python3 ||\n                                || Revision: 0              ||\n                                || Author: AD1024           ||\n                                ==============================\n"

def configuration_check(conf_dict):
    """
        Check whether the configuration file contains all the necessary parameters
        and whether files are required in the judgement exist
    :param conf_dict: configuration
    :return: Whether it can be used to perform a judgement
    """
    attrs = list(filter(lambda x: not x.startswith('__'), dir(ConfigKeys)))
    for e in attrs:
        if eval('ConfigKeys.{}'.format(e)) not in conf_dict:
            return False

    if not os.path.exists(os.path.join(get_data_path(conf_dict), conf_dict[ConfigKeys.TEST_CASE_FILE])):
        print('[WARN] Test case file {} not found.'.format(conf_dict[ConfigKeys.TEST_CASE_FILE]))
        return False
    else:
        return True


def get_conf_path():
    return os.path.join(os.environ['HOME'], 'conf')


def get_src_path(conf):
    return conf[ConfigKeys.SRC_DIR]


def get_data_path(conf):
    return conf[ConfigKeys.DATA_DIR]


def get_result_path(conf):
    return conf[ConfigKeys.RESULT_DIR]


def main():
    print(WELCOME + '\n\n')
    print('Configuration files: ')
    conf_files = list(filter(lambda x: x.endswith('.json'), os.listdir(get_conf_path())))
    for i, conf in enumerate(conf_files):
        print('[{}]\t{}'.format(i, conf))

    if not len(conf_files):
        print('No configuration found. Please run <conf_generator.py> first.')
        exit(-2)

    def load_conf():
        try:
            selection = input('Select a configuration file(input id): ')
            while not selection.isdigit() or int(selection) >= len(conf_files):
                selection = input('Select a configuration file(*input id* less than {}): '.format(len(conf_files)))

            return int(selection)
        except EOFError:
            print('\nHave a nice day~\n')
            exit(0)

    continue_flag = 'n'
    conf = 0
    while continue_flag != '' and continue_flag.lower() != 'y':
        conf = load_conf()
        continue_flag = input('Your choice is: {}, proceed judgement?[Y]/n: '.format(conf_files[conf]))

    try:
        configuration = json.load(open(os.path.join(get_conf_path(), conf_files[conf]), 'r'))
        if configuration_check(configuration):
            src_files = list(filter(lambda x: configuration[ConfigKeys.PROGRAM_NAME_PREFIX] in x, os.listdir(get_src_path(configuration))))
            src_files += configuration[ConfigKeys.UNIQUE_PROGRAM_LIST]
            src_files = list(map(lambda x: x if not x.endswith('.py') else x[:-3], src_files))
            if len(src_files) == 0:
                print('No target source file found. Stop judging')
                exit(-2)
            data_loader = Loader(configuration[ConfigKeys.NUMBER_OF_TEST_CASES], configuration[ConfigKeys.NUMBER_OF_TARGET_METHOD_PARAMETERS])
            test_cases = data_loader.load_cases(os.path.join(get_data_path(configuration), configuration[ConfigKeys.TEST_CASE_FILE]))
            answers = data_loader.load_answers(os.path.join(get_data_path(configuration), configuration[ConfigKeys.ANSWER_FILE]))
            judge_client = Tester('', (get_src_path(configuration)), (configuration[ConfigKeys.TARGET_METHOD_NAME]), time_limit=(configuration[ConfigKeys.TIME_LIMIT]))
            from .judge_result import Result
            judge_result_summary = ''
            for program in src_files:
                judge_client.set_program(program)
                result = list()
                judge_result = ''
                for case, ans in zip(test_cases, answers):
                    result.append(judge_client.run_test(case, ans[0]))

                judge_result += '==============================\n'
                judge_result += 'Result for {}.py: \n'.format(program)
                num_correct = 0
                for i, r in enumerate(result):
                    judge_result += 'Case #{}: {}\n'.format(i + 1, r.value)
                    if r == Result.AC:
                        num_correct += 1

                judge_result += '--------\n ' + 'Score: {}\n'.format(100.0 / configuration[ConfigKeys.NUMBER_OF_TEST_CASES] * num_correct)
                judge_result += '================================\n'
                print(judge_result)
                judge_result_summary += judge_result

            store_result = input('Store result for this judgement?[Y]/n: ')
            if store_result in ('', 'Y', 'y'):
                result_name = input('Name of result file: ')
                while os.path.exists(os.path.join(get_result_path(configuration), result_name)):
                    prompt = input('*{}.json* found, overwrite? [Y/n]: '.format(result_name))
                    if prompt.lower() == 'y':
                        break
                    else:
                        result_name = input('Name of result file: ')

                with contextlib.closing(open(os.path.join(get_result_path(configuration), result_name), 'w')) as (fp):
                    fp.write(judge_result_summary)
            print('Judgement Finished! Have a nice day~')
        else:
            raise Exception('Missing attribute(s)')
    except json.decoder.JSONDecodeError:
        print('[Error] Malformat json file. Stop judging')
        exit(-1)


if __name__ == '__main__':
    main()