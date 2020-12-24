# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/cruisecontrolclient/client/cccli.py
# Compiled at: 2020-03-16 12:46:21
# Size of source mod 2**32: 10754 bytes
import argparse
import cruisecontrolclient.client.ExecutionContext as ExecutionContext
import cruisecontrolclient.client.Endpoint as Endpoint
from cruisecontrolclient.client.Responder import CruiseControlResponder

def get_endpoint(args: argparse.Namespace, execution_context: ExecutionContext) -> Endpoint.AbstractEndpoint:
    arg_dict = vars(args).copy()
    if 'brokers' in arg_dict:
        comma_broker_id_list = ','.join(args.brokers)
        endpoint = execution_context.dest_to_Endpoint[args.endpoint_subparser](comma_broker_id_list)
        del arg_dict['brokers']
    else:
        endpoint = execution_context.dest_to_Endpoint[args.endpoint_subparser]()
    for flag in arg_dict:
        if flag in execution_context.non_parameter_flags:
            continue
        if arg_dict[flag] is not None:
            param_name = execution_context.flag_to_parameter_name[flag]
            if endpoint.has_param(param_name):
                if not isinstance(endpoint, Endpoint.StateEndpoint):
                    existing_value = endpoint.get_value(param_name)
                    raise ValueError(f"Parameter {param_name}={existing_value} already exists in this endpoint.\nUnclear whether it's safe to remap to {param_name}={arg_dict[flag]}")
            if flag == 'destination_broker':
                comma_broker_id_list = ','.join(arg_dict[flag])
                endpoint.add_param(param_name, comma_broker_id_list)
            else:
                endpoint.add_param(param_name, arg_dict[flag])

    if 'destination_broker' in arg_dict:
        del arg_dict['destination_broker']
    adding_parameter = 'add_parameter' in arg_dict and arg_dict['add_parameter']
    if adding_parameter:
        parameters_to_add = {}
        for item in arg_dict['add_parameter']:
            if '=' not in item:
                raise ValueError('Expected "=" in the given parameter')
            else:
                split_item = item.split('=')
                if len(split_item) != 2:
                    raise ValueError('Expected only one "=" in the given parameter')
                if not split_item[0]:
                    raise ValueError('Expected parameter preceding "="')
                assert split_item[1], 'Expected value after "=" in the given parameter'
            parameter, value = split_item
            parameters_to_add[parameter] = value

    removing_parameter = 'remove_parameter' in arg_dict and arg_dict['remove_parameter']
    if removing_parameter:
        parameters_to_remove = set()
        for item in arg_dict['remove_parameter']:
            parameters_to_remove.add(item)

    if adding_parameter:
        if removing_parameter:
            if set(parameters_to_add) & parameters_to_remove:
                raise ValueError('Parameter present in --add-parameter and in --remove-parameter; unclear how to proceed')
    if adding_parameter:
        for parameter, value in parameters_to_add.items():
            endpoint.add_param(parameter, value)

    if removing_parameter:
        for parameter in parameters_to_remove:
            endpoint.remove_param(parameter)

    return endpoint


def build_argument_parser(execution_context: ExecutionContext) -> argparse.ArgumentParser:
    """
    Builds and returns an argument parser for interacting with cruise-control via CLI.

    It is expected that you can substitute another function for this function
    that returns a parser which is decorated similarly.

    :return:
    """

    def add_add_parameter_argument(p):
        """
        This should be used with all cruise-control endpoint parsers, to provide
        forward compatibility and greater operational flexibility.
        :param p:
        :return:
        """
        p.add_argument('--add-parameter', '--add-parameters', metavar='PARAM=VALUE', help="Manually specify one or more parameter and its value in the cruise-control endpoint, like 'param=value'",
          nargs='+')
        execution_context.non_parameter_flags.add('add_parameter')

    def add_remove_parameter_argument(p):
        """
        Adds the ability to manually specify parameters to remove from the cruise-control
        endpoint, of the form 'parameter'.

        This should be used with all cruise-control endpoint parsers, to provide
        forward compatibility and greater operational flexibility.

        :param p:
        :return:
        """
        p.add_argument('--remove-parameter', '--remove-parameters', metavar='PARAM', help="Manually remove one or more parameter from the cruise-control endpoint, like 'param'",
          nargs='+')
        execution_context.non_parameter_flags.add('remove_parameter')

    parser = argparse.ArgumentParser()
    parser.add_argument('-a', '--socket-address', help='The hostname[:port] of the cruise-control to interact with', required=True)
    execution_context.non_parameter_flags.add('socket_address')
    endpoint_subparser = parser.add_subparsers(title='endpoint', description='Which cruise-control endpoint to interact with',
      dest='endpoint_subparser')
    execution_context.non_parameter_flags.add('endpoint_subparser')
    endpoint_to_parser_instance = {}
    for endpoint in execution_context.available_endpoints:
        endpoint_parser = (endpoint_subparser.add_parser)(*endpoint.argparse_properties['args'], **endpoint.argparse_properties['kwargs'])
        endpoint_to_parser_instance[endpoint.name] = endpoint_parser
        for parameter in endpoint.available_Parameters:
            (endpoint_parser.add_argument)(*parameter.argparse_properties['args'], **parameter.argparse_properties['kwargs'])

        add_add_parameter_argument(endpoint_parser)
        add_remove_parameter_argument(endpoint_parser)

    return parser


def main():
    e = ExecutionContext()
    parser = build_argument_parser(e)
    args = parser.parse_args()
    endpoint = get_endpoint(args=args, execution_context=e)
    cc_socket_address = args.socket_address
    json_responder = CruiseControlResponder()
    response = json_responder.retrieve_response_from_Endpoint(cc_socket_address, endpoint)
    print(response.text)


if __name__ == '__main__':
    main()