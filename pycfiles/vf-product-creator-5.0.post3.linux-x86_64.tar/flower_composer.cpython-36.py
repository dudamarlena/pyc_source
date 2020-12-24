# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/miranda/.virtualenvs/vf_utils/lib/python3.6/site-packages/vf_createproducts_core/composers/flower_composer.py
# Compiled at: 2018-10-05 17:13:25
# Size of source mod 2**32: 4641 bytes
"""
Copyright (2018) Raydel Miranda

This file is part of "VillaFlores Product Creator".

    "VillaFlores Product Creator" is free software: you can redistribute it and/or 1wmodify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    "VillaFlores Product Creator" is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with "VillaFlores Product Creator".  If not, see <http://www.gnu.org/licenses/>.
"""
import os, queue
from vf_createproducts_core.build_paths import build_combinations, compute_output
from vf_createproducts_core.composers.common_defs import WorkerParams
from vf_createproducts_core.json_templates import FABRIC_JSON
from vf_createproducts_core.workers import CopyWorker, ConverterWorker

def compose_flowers(cli_args, settings):
    copy_workers = []
    copy_queue = queue.Queue()
    convert_queue = queue.Queue()
    for i in range(cli_args.num_threads):
        cw = CopyWorker(copy_queue)
        cw.setDaemon(True)
        copy_workers.append(cw)
        cv = ConverterWorker(convert_queue)
        cv.setDaemon(True)
        copy_workers.append(cv)
        cv.start()
        cw.start()

    last_image_params = None
    current_flower_and_background = None
    generated_image_params = None
    for fb in build_combinations(path_to_backgrounds=(cli_args.background_root_folder),
      path_to_flowers=(cli_args.flowers_root_folder),
      path_to_bundles=(cli_args.bundles_folder),
      bundles_number=(cli_args.bundles_number)):
        folder, output_name = compute_output(*fb, background_code_pattern=cli_args.background_code_pattern, 
         flower_code_pattern=cli_args.flower_code_pattern, 
         bundle_code_pattern=cli_args.bundles_code_pattern, 
         extension=cli_args.format)
        worker_params = WorkerParams(*fb)
        if current_flower_and_background is None:
            current_flower_and_background = worker_params[:2]
            generated_image_params = []
        elif current_flower_and_background != worker_params[:2]:
            current_flower_and_background = worker_params[:2]
            del generated_image_params
            generated_image_params = []
        else:
            full_path = os.path.join(cli_args.output, folder)
            if not os.path.exists(full_path):
                os.makedirs(full_path)
            bundles_layer_slot_names = settings.bundle_layers
            images = [
             (
              worker_params.flower,
              cli_args.flower_layer_id)]

            def filter_bundles(bundle_path_slot_name):
                bundle_path, slot_name = bundle_path_slot_name
                dir = os.path.dirname(bundle_path)
                dir = os.path.split(dir)[1]
                try:
                    return slot_name in settings.bundle_layer_selection[dir]
                except KeyError:
                    return True

            if worker_params.bundles:
                bundles = zip(worker_params.bundles, bundles_layer_slot_names)
                bundles = list(filter(filter_bundles, bundles))
                images.extend(bundles)
            if last_image_params is None:
                last_image_params = images
            else:
                if last_image_params != images:
                    last_image_params = images
                else:
                    continue
        if images in generated_image_params:
            pass
        else:
            generated_image_params.append(images)
            convert_queue.put((
             images, worker_params.background,
             os.path.join(full_path, output_name),
             cli_args.verbose))
            flower_file_name = os.path.split(worker_params.flower)[1]
            background_file_name = os.path.split(worker_params.background)[1]
            copy_queue.put((
             worker_params.flower,
             os.path.join(full_path, flower_file_name)))
            copy_queue.put((
             worker_params.background,
             os.path.join(full_path, background_file_name)))

    convert_queue.join()
    copy_queue.join()