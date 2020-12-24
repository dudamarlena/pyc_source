# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington/__main__.py
# Compiled at: 2020-04-04 13:10:47
# Size of source mod 2**32: 2459 bytes
from eddington.app_util import split_function_and_parameters, load_func
from eddington_matplotlib import plot_all, PlotConfiguration, OutputConfiguration
from eddington.arguments.parser import LabUtilParser
from eddington.consts import LIST, SYNTAX
from eddington_core import FitData, FitFunctionsRegistry, fit_to_data
from eddington.input.get import get_data_dict_from_args
from eddington.input.util import get_a0

def main():
    args = LabUtilParser.parse_and_validate()
    func_name, func_parameters = split_function_and_parameters(args.func)
    if func_name == LIST:
        print(FitFunctionsRegistry.list())
        exit(0)
    if func_name == SYNTAX:
        print(FitFunctionsRegistry.syntax(func_parameters))
        exit(0)
    func = load_func(func_name=func_name,
      func_parameters=func_parameters,
      costumed=(args.costumed))
    if func is None:
        LabUtilParser.print_help()
        exit(0)
    data_dict = get_data_dict_from_args(func=func, args=args)
    if data_dict is None:
        LabUtilParser.print_help()
        exit(0)
    data = FitData.build_from_data_dict(data_dict=data_dict)
    a0 = get_a0(n=(func.n), a0=(args.a0))
    print(f"Fitting {func.name} ({func.syntax})")
    res = fit_to_data(data=data, func=func, a0=a0)
    print(res)
    if args.output_dir is not None:
        with open((args.output_dir / f"{func.name}_fitting_results.txt"),
          mode='w') as (result_file):
            result_file.write(str(res))
    if args.plot:
        xmin, xmax = PlotConfiguration.get_plot_borders(data.x)
        columns = list(data_dict.keys())
        plot_configuration = PlotConfiguration.build(func_name=(func.title_name),
          xmin=xmin,
          xmax=xmax,
          title=(args.title),
          residuals_title=(args.residuals_title),
          xcolumn=(columns[0]),
          ycolumn=(columns[2]),
          xlabel=(args.xlabel),
          ylabel=(args.ylabel),
          grid=(args.grid),
          plot_data=(args.plot_data))
        output_configuration = OutputConfiguration.build(func_name=(func.title_name),
          output_dir=(args.output_dir))
        print('Plotting...')
        plot_all(func=func,
          data=data,
          plot_configuration=plot_configuration,
          a=(res.a),
          output_configuration=output_configuration)
    print('Done!')


if __name__ == '__main__':
    main()