# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/eddington_matplotlib/output_configuration.py
# Compiled at: 2020-04-02 13:21:11
# Size of source mod 2**32: 1313 bytes
from dataclasses import dataclass
from pathlib import Path
from typing import Union

@dataclass
class OutputConfiguration:
    data_output_path = None
    data_output_path: Union[(Path, None)]
    fitting_output_path = None
    fitting_output_path: Union[(Path, None)]
    residuals_output_path = None
    residuals_output_path: Union[(Path, None)]

    @classmethod
    def build(cls, func_name: str, output_dir: Path=None):
        data_output_path, fitting_output_path, residuals_output_path = cls._OutputConfiguration__get_output_paths(func_name=func_name, output_dir=output_dir)
        return OutputConfiguration(data_output_path=data_output_path,
          fitting_output_path=fitting_output_path,
          residuals_output_path=residuals_output_path)

    @classmethod
    def __get_output_paths(cls, func_name: str, output_dir: Path):
        if output_dir is None:
            return (None, None, None)
        underscore_func_name = func_name.lower().replace(' ', '_')
        data_output_path = output_dir / f"{underscore_func_name}_data.png"
        fitting_output_path = output_dir / f"{underscore_func_name}_fitting.png"
        residuals_output_path = output_dir / f"{underscore_func_name}_fitting_residuals.png"
        return (
         data_output_path, fitting_output_path, residuals_output_path)