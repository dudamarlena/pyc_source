# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/bin/clients/qbit/qbit_pb2.py
# Compiled at: 2019-02-28 19:10:53
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf.internal import enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from google.protobuf import empty_pb2 as google_dot_protobuf_dot_empty__pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2
from google.api import annotations_pb2 as google_dot_api_dot_annotations__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='qbit.proto', package='qbit.services', syntax='proto3', serialized_options=None, serialized_pb=_b(b'\n\nqbit.proto\x12\rqbit.services\x1a\x1bgoogle/protobuf/empty.proto\x1a\x1cgoogle/protobuf/struct.proto\x1a\x1cgoogle/api/annotations.proto"\xea\x02\n\x0eCompareRequest\x12\x0e\n\x06smiles\x18\x01 \x03(\t\x12-\n\x04tabu\x18\x02 \x01(\x0b2\x1d.qbit.services.Tabu1OptSolverH\x00\x127\n\tmultitabu\x18\x03 \x01(\x0b2".qbit.services.MultiTabu1OptSolverH\x00\x12;\n\rpathrelinking\x18\x04 \x01(\x0b2".qbit.services.PathRelinkingSolverH\x00\x12\'\n\x03sqa\x18\x05 \x01(\x0b2\x18.qbit.services.SQASolverH\x00\x12+\n\x05pticm\x18\x06 \x01(\x0b2\x1a.qbit.services.PTICMSolverH\x00\x12\x18\n\x10should_visualize\x18\x07 \x01(\x08\x12)\n\x08criteria\x18\x08 \x01(\x0b2\x17.google.protobuf.StructB\x08\n\x06solver"\x84\x03\n\x11CompareRequestSDF\x12\x11\n\tsdf_first\x18\x01 \x01(\t\x12\x12\n\nsdf_second\x18\x02 \x01(\t\x12-\n\x04tabu\x18\x03 \x01(\x0b2\x1d.qbit.services.Tabu1OptSolverH\x00\x127\n\tmultitabu\x18\x04 \x01(\x0b2".qbit.services.MultiTabu1OptSolverH\x00\x12;\n\rpathrelinking\x18\x05 \x01(\x0b2".qbit.services.PathRelinkingSolverH\x00\x12\'\n\x03sqa\x18\x06 \x01(\x0b2\x18.qbit.services.SQASolverH\x00\x12+\n\x05pticm\x18\x07 \x01(\x0b2\x1a.qbit.services.PTICMSolverH\x00\x12\x18\n\x10should_visualize\x18\x08 \x01(\x08\x12)\n\x08criteria\x18\t \x01(\x0b2\x17.google.protobuf.StructB\x08\n\x06solver"\x93\x01\n\x10ComparisonResult\x12\x17\n\x0fcan_use_quantum\x18\x01 \x01(\x08\x12\n\n\x02ok\x18\x02 \x01(\x08\x12\x16\n\x0evisualizations\x18\x03 \x03(\t\x12.\n\rshared_traits\x18\x04 \x01(\x0b2\x17.google.protobuf.Struct\x12\x12\n\nsimilarity\x18\x05 \x01(\x01"p\n\nQuboMatrix\x121\n\x04qubo\x18\x01 \x03(\x0b2#.qbit.services.QuboMatrix.QuboArray\x12\x10\n\x08constant\x18\x02 \x01(\x01\x1a\x1d\n\tQuboArray\x12\x10\n\x08qubo_row\x18\x01 \x03(\x01"y\n\x10BinaryPolynomial\x123\n\x05terms\x18\x01 \x03(\x0b2$.qbit.services.BinaryPolynomial.Term\x1a0\n\x04Term\x12\x13\n\x0bcoefficient\x18\x01 \x01(\x01\x12\x13\n\x0bpolynomials\x18\x02 \x03(\r"\xb7\x01\n\x0eTabu1OptSolver\x12\x1c\n\x12improvement_cutoff\x18\x01 \x01(\rH\x00\x12\x1f\n\x15improvement_tolerance\x18\x02 \x01(\x01H\x01\x12\x15\n\x0btabu_tenure\x18\x03 \x01(\rH\x02\x12\x1e\n\x14tabu_tenure_rand_max\x18\x04 \x01(\rH\x03\x12\x11\n\x07timeout\x18\x05 \x01(\rH\x04B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5"E\n\x0eTabuSolverList\x123\n\x0ctabu_solvers\x18\x01 \x03(\x0b2\x1d.qbit.services.Tabu1OptSolver"\x90\x02\n\x13MultiTabu1OptSolver\x12\x1c\n\x12improvement_cutoff\x18\x01 \x01(\rH\x00\x12\x1f\n\x15improvement_tolerance\x18\x02 \x01(\x01H\x01\x12\x15\n\x0btabu_tenure\x18\x03 \x01(\rH\x02\x12\x1e\n\x14tabu_tenure_rand_max\x18\x04 \x01(\rH\x03\x12\x16\n\x0csolver_count\x18\x05 \x01(\rH\x04\x124\n\x0bsolver_list\x18\x07 \x01(\x0b2\x1d.qbit.services.TabuSolverListH\x04\x12\x11\n\x07timeout\x18\x06 \x01(\rH\x05B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x04\n\x02v6"\x8c\x01\n\x13PathRelinkingSolver\x12\x18\n\x0edistance_scale\x18\x01 \x01(\x01H\x00\x12\x1d\n\x15greedy_path_relinking\x18\x02 \x01(\x08\x12\x11\n\x07timeout\x18\x03 \x01(\rH\x01\x12\x17\n\rref_set_count\x18\x04 \x01(\rH\x02B\x04\n\x02v1B\x04\n\x02v3B\x04\n\x02v4"\xc1\x02\n\tSQASolver\x12\x0e\n\x04beta\x18\x01 \x01(\x01H\x00\x123\n\x0benergy_type\x18\x02 \x01(\x0e2\x1e.qbit.services.sqa_energy_type\x12\x17\n\rgamma_initial\x18\x03 \x01(\x01H\x01\x12\x15\n\x0bgamma_final\x18\x04 \x01(\x01H\x02\x12\x13\n\tnum_reads\x18\x05 \x01(\rH\x03\x12\x16\n\x0cnum_replicas\x18\x06 \x01(\rH\x04\x12\x14\n\nnum_sweeps\x18\x07 \x01(\rH\x05\x12\x11\n\x07timeout\x18\x08 \x01(\rH\x06\x129\n\rschedule_type\x18\t \x01(\x0e2 .qbit.services.sqa_schedule_typeH\x07B\x04\n\x02v1B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x04\n\x02v6B\x04\n\x02v7B\x04\n\x02v8B\x04\n\x02v9"\xe7\x05\n\x0bPTICMSolver\x12\x13\n\thigh_temp\x18\x01 \x01(\x01H\x00\x12\x12\n\x08low_temp\x18\x02 \x01(\x01H\x01\x12\x16\n\x0cnum_replicas\x18\x03 \x01(\rH\x02\x12\x1c\n\x12num_sweeps_per_run\x18\x04 \x01(\rH\x03\x12\x13\n\tnum_temps\x18\x05 \x01(\rH\x04\x12\x1b\n\x13manual_temperatures\x18\x0b \x03(\x01\x12\x1f\n\x15auto_set_temperatures\x18\x0c \x01(\x08H\x05\x12\x19\n\x0felite_threshold\x18\r \x01(\x01H\x06\x12!\n\x17frac_icm_thermal_layers\x18\x0e \x01(\x01H\x07\x12\x1c\n\x12frac_sweeps_fixing\x18\x0f \x01(\x01H\x08\x12\x1a\n\x10frac_sweeps_idle\x18\x10 \x01(\x01H\t\x12 \n\x16frac_sweeps_stagnation\x18\x11 \x01(\x01H\n\x12\x1f\n\x15max_samples_per_layer\x18\x12 \x01(\rH\x0b\x12\x1a\n\x10max_total_sweeps\x18\x13 \x01(\rH\x0c\x12\x19\n\x0fnum_elite_temps\x18\x14 \x01(\rH\r\x12\x15\n\x0bperform_icm\x18\x15 \x01(\x08H\x0e\x12\'\n\x04goal\x18\x16 \x01(\x0e2\x19.qbit.services.pticm_goal\x127\n\x0cscaling_type\x18\x17 \x01(\x0e2!.qbit.services.pticm_scaling_type\x12=\n\x0fvar_fixing_type\x18\x18 \x01(\x0e2$.qbit.services.pticm_var_fixing_type\x12\x11\n\x07timeout\x18\x19 \x01(\rH\x0fB\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x05\n\x03v12B\x05\n\x03v13B\x05\n\x03v14B\x05\n\x03v15B\x05\n\x03v16B\x05\n\x03v17B\x05\n\x03v18B\x05\n\x03v19B\x05\n\x03v20B\x05\n\x03v21B\x05\n\x03v25"\xd7\x04\n\x0fFujitsuDASolver\x125\n\x0bnoise_model\x18\x01 \x01(\x0e2\x1e.qbit.services.fuj_noise_modelH\x00\x12\x1b\n\x11number_iterations\x18\x02 \x01(\rH\x01\x12\x15\n\x0bnumber_runs\x18\x03 \x01(\rH\x02\x12\x1e\n\x14offset_increase_rate\x18\x04 \x01(\rH\x03\x12\x1b\n\x11temperature_decay\x18\x05 \x01(\x01H\x04\x12\x1e\n\x14temperature_interval\x18\x06 \x01(\rH\x05\x128\n\x10temperature_mode\x18\x07 \x01(\x0e2\x1c.qbit.services.fuj_temp_modeH\x06\x12\x1b\n\x11temperature_start\x18\x08 \x01(\x01H\x07\x122\n\rsolution_mode\x18\t \x01(\x0e2\x1b.qbit.services.fuj_sol_mode\x12\x13\n\x0bexpert_mode\x18\n \x01(\x08\x12K\n\x0fguidance_config\x18\x0b \x03(\x0b22.qbit.services.FujitsuDASolver.GuidanceConfigEntry\x12\x0e\n\x06job_id\x18\x0c \x01(\t\x12\x11\n\x07timeout\x18\r \x01(\rH\x08\x1a5\n\x13GuidanceConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x04\n\x02v6B\x04\n\x02v7B\x04\n\x02v8B\x05\n\x03v13"\xd4\x04\n\x18FujitsuDAMixedModeSolver\x125\n\x0bnoise_model\x18\x01 \x01(\x0e2\x1e.qbit.services.fuj_noise_modelH\x00\x12\x1b\n\x11number_iterations\x18\x02 \x01(\rH\x01\x12\x15\n\x0bnumber_runs\x18\x03 \x01(\rH\x02\x12\x1e\n\x14offset_increase_rate\x18\x04 \x01(\rH\x03\x12\x1b\n\x11temperature_decay\x18\x05 \x01(\x01H\x04\x12\x1e\n\x14temperature_interval\x18\x06 \x01(\rH\x05\x128\n\x10temperature_mode\x18\x07 \x01(\x0e2\x1c.qbit.services.fuj_temp_modeH\x06\x12\x1b\n\x11temperature_start\x18\x08 \x01(\x01H\x07\x122\n\rsolution_mode\x18\t \x01(\x0e2\x1b.qbit.services.fuj_sol_mode\x12T\n\x0fguidance_config\x18\x0b \x03(\x0b2;.qbit.services.FujitsuDAMixedModeSolver.GuidanceConfigEntry\x12\x0e\n\x06job_id\x18\x0c \x01(\t\x12\x11\n\x07timeout\x18\r \x01(\rH\x08\x1a5\n\x13GuidanceConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x04\n\x02v6B\x04\n\x02v7B\x04\n\x02v8B\x05\n\x03v13"\xe0\x02\n\x11FujitsuDAPTSolver\x12\x1b\n\x11number_iterations\x18\x01 \x01(\rH\x00\x12\x1e\n\x14offset_increase_rate\x18\x02 \x01(\rH\x01\x122\n\rsolution_mode\x18\x03 \x01(\x0e2\x1b.qbit.services.fuj_sol_mode\x12\x19\n\x0fnumber_replicas\x18\x04 \x01(\rH\x02\x12M\n\x0fguidance_config\x18\x05 \x03(\x0b24.qbit.services.FujitsuDAPTSolver.GuidanceConfigEntry\x12\x0e\n\x06job_id\x18\x06 \x01(\t\x12\x11\n\x07timeout\x18\x07 \x01(\rH\x03\x1a5\n\x13GuidanceConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v4B\x04\n\x02v7"\x9c\x04\n\x10FujitsuDA2Solver\x12\x1b\n\x11number_iterations\x18\x01 \x01(\rH\x00\x12\x15\n\x0bnumber_runs\x18\x02 \x01(\rH\x01\x12\x1e\n\x14offset_increase_rate\x18\x03 \x01(\x02H\x02\x12\x1b\n\x11temperature_decay\x18\x04 \x01(\x01H\x03\x12\x1e\n\x14temperature_interval\x18\x05 \x01(\rH\x04\x128\n\x10temperature_mode\x18\x06 \x01(\x0e2\x1c.qbit.services.fuj_temp_modeH\x05\x12\x1b\n\x11temperature_start\x18\x07 \x01(\x01H\x06\x122\n\rsolution_mode\x18\x08 \x01(\x0e2\x1b.qbit.services.fuj_sol_mode\x12\x13\n\x0bexpert_mode\x18\t \x01(\x08\x12L\n\x0fguidance_config\x18\n \x03(\x0b23.qbit.services.FujitsuDA2Solver.GuidanceConfigEntry\x12\x0e\n\x06job_id\x18\x0b \x01(\t\x12\x11\n\x07timeout\x18\x0c \x01(\rH\x07\x1a5\n\x13GuidanceConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x04\n\x02v6B\x04\n\x02v7B\x05\n\x03v12"\xe2\x02\n\x12FujitsuDA2PTSolver\x12\x1b\n\x11number_iterations\x18\x01 \x01(\rH\x00\x12\x19\n\x0fnumber_replicas\x18\x02 \x01(\rH\x01\x12\x1e\n\x14offset_increase_rate\x18\x03 \x01(\x02H\x02\x122\n\rsolution_mode\x18\x04 \x01(\x0e2\x1b.qbit.services.fuj_sol_mode\x12N\n\x0fguidance_config\x18\x05 \x03(\x0b25.qbit.services.FujitsuDA2PTSolver.GuidanceConfigEntry\x12\x0e\n\x06job_id\x18\x06 \x01(\t\x12\x11\n\x07timeout\x18\x07 \x01(\rH\x03\x1a5\n\x13GuidanceConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v7"\x99\x04\n\x19FujitsuDA2MixedModeSolver\x12\x1b\n\x11number_iterations\x18\x01 \x01(\rH\x00\x12\x15\n\x0bnumber_runs\x18\x02 \x01(\rH\x01\x12\x1e\n\x14offset_increase_rate\x18\x03 \x01(\x02H\x02\x12\x1b\n\x11temperature_decay\x18\x04 \x01(\x01H\x03\x12\x1e\n\x14temperature_interval\x18\x05 \x01(\rH\x04\x128\n\x10temperature_mode\x18\x06 \x01(\x0e2\x1c.qbit.services.fuj_temp_modeH\x05\x12\x1b\n\x11temperature_start\x18\x07 \x01(\x01H\x06\x122\n\rsolution_mode\x18\x08 \x01(\x0e2\x1b.qbit.services.fuj_sol_mode\x12U\n\x0fguidance_config\x18\t \x03(\x0b2<.qbit.services.FujitsuDA2MixedModeSolver.GuidanceConfigEntry\x12\x0e\n\x06job_id\x18\n \x01(\t\x12\x11\n\x07timeout\x18\x0b \x01(\rH\x07\x1a5\n\x13GuidanceConfigEntry\x12\x0b\n\x03key\x18\x01 \x01(\r\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01B\x04\n\x02v1B\x04\n\x02v2B\x04\n\x02v3B\x04\n\x02v4B\x04\n\x02v5B\x04\n\x02v6B\x04\n\x02v7B\x05\n\x03v11"\xaf\x06\n\x0bQuboRequest\x12(\n\x08run_type\x18\x01 \x01(\x0e2\x16.qbit.services.runType\x12<\n\x11binary_polynomial\x18\x02 \x01(\x0b2\x1f.qbit.services.BinaryPolynomialH\x00\x120\n\x0bqubo_matrix\x18\x03 \x01(\x0b2\x19.qbit.services.QuboMatrixH\x00\x12-\n\x04tabu\x18\x05 \x01(\x0b2\x1d.qbit.services.Tabu1OptSolverH\x01\x127\n\tmultitabu\x18\x06 \x01(\x0b2".qbit.services.MultiTabu1OptSolverH\x01\x12;\n\rpathrelinking\x18\x07 \x01(\x0b2".qbit.services.PathRelinkingSolverH\x01\x12\'\n\x03sqa\x18\x08 \x01(\x0b2\x18.qbit.services.SQASolverH\x01\x12+\n\x05pticm\x18\t \x01(\x0b2\x1a.qbit.services.PTICMSolverH\x01\x123\n\tfujitsuDA\x18\n \x01(\x0b2\x1e.qbit.services.FujitsuDASolverH\x01\x127\n\x0bfujitsuDAPT\x18\x0b \x01(\x0b2 .qbit.services.FujitsuDAPTSolverH\x01\x12E\n\x12fujitsuDAMixedMode\x18\x0c \x01(\x0b2\'.qbit.services.FujitsuDAMixedModeSolverH\x01\x125\n\nfujitsuDA2\x18\r \x01(\x0b2\x1f.qbit.services.FujitsuDA2SolverH\x01\x129\n\x0cfujitsuDA2PT\x18\x0e \x01(\x0b2!.qbit.services.FujitsuDA2PTSolverH\x01\x12G\n\x13fujitsuDA2MixedMode\x18\x0f \x01(\x0b2(.qbit.services.FujitsuDA2MixedModeSolverH\x01B\x06\n\x04quboB\x13\n\x11solver_parameters"\xae\x01\n\x0cQuboSolution\x12\x0e\n\x06energy\x18\x01 \x01(\x01\x12\x11\n\tfrequency\x18\x02 \x01(\x01\x12E\n\rconfiguration\x18\x03 \x03(\x0b2..qbit.services.QuboSolution.ConfigurationEntry\x1a4\n\x12ConfigurationEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\x08:\x028\x01"\xd2\x01\n\x0cSolverTiming\x12\x10\n\x08cpu_time\x18\x01 \x01(\x04\x12\x12\n\nqueue_time\x18\x02 \x01(\x04\x12\x12\n\nsolve_time\x18\x03 \x01(\x04\x12\x1a\n\x12total_elapsed_time\x18\x05 \x01(\x04\x12;\n\x08detailed\x18\x06 \x03(\x0b2).qbit.services.SolverTiming.DetailedEntry\x1a/\n\rDetailedEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\x04:\x028\x01"\x86\x01\n\x10QuboSolutionList\x12\x15\n\rresult_status\x18\x01 \x01(\x08\x12.\n\tsolutions\x18\x02 \x03(\x0b2\x1b.qbit.services.QuboSolution\x12+\n\x06timing\x18\x03 \x01(\x0b2\x1b.qbit.services.SolverTiming"\xeb\x01\n\x0cQuboResponse\x128\n\rqubo_solution\x18\x01 \x01(\x0b2\x1f.qbit.services.QuboSolutionListH\x00\x12W\n\x17solver_input_parameters\x18\x02 \x03(\x0b26.qbit.services.QuboResponse.SolverInputParametersEntry\x1a<\n\x1aSolverInputParametersEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x028\x01B\n\n\x08response"\xc7\x02\n\x0fKnapsackRequest\x12-\n\x04tabu\x18\x01 \x01(\x0b2\x1d.qbit.services.Tabu1OptSolverH\x00\x127\n\tmultitabu\x18\x02 \x01(\x0b2".qbit.services.MultiTabu1OptSolverH\x00\x12;\n\rpathrelinking\x18\x03 \x01(\x0b2".qbit.services.PathRelinkingSolverH\x00\x12\'\n\x03sqa\x18\x04 \x01(\x0b2\x18.qbit.services.SQASolverH\x00\x12+\n\x05pticm\x18\x05 \x01(\x0b2\x1a.qbit.services.PTICMSolverH\x00\x12/\n\x07problem\x18\x07 \x01(\x0b2\x1e.qbit.services.KnapsackProblemB\x08\n\x06solver"O\n\x0fKnapsackProblem\x12\x10\n\x08capacity\x18\x01 \x01(\r\x12*\n\x05items\x18\x02 \x03(\x0b2\x1b.qbit.services.KnapsackItem"<\n\x0cKnapsackItem\x12\r\n\x05index\x18\x01 \x01(\r\x12\x0e\n\x06weight\x18\x02 \x01(\r\x12\r\n\x05value\x18\x03 \x01(\x01"F\n\x10KnapsackResponse\x122\n\tsolutions\x18\x01 \x03(\x0b2\x1f.qbit.services.KnapsackSolution"\x81\x01\n\x10KnapsackSolution\x12\x10\n\x08feasible\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\x01\x12\x0e\n\x06weight\x18\x03 \x01(\r\x12<\n\x0econfigurations\x18\x04 \x03(\x0b2$.qbit.services.KnapsackConfiguration"8\n\x15KnapsackConfiguration\x12\r\n\x05index\x18\x01 \x01(\r\x12\x10\n\x08selected\x18\x02 \x01(\x08"\xbb\x02\n\x0eMinKCutRequest\x12-\n\x04tabu\x18\x01 \x01(\x0b2\x1d.qbit.services.Tabu1OptSolverH\x00\x127\n\tmultitabu\x18\x02 \x01(\x0b2".qbit.services.MultiTabu1OptSolverH\x00\x12;\n\rpathrelinking\x18\x03 \x01(\x0b2".qbit.services.PathRelinkingSolverH\x00\x12\'\n\x03sqa\x18\x04 \x01(\x0b2\x18.qbit.services.SQASolverH\x00\x12+\n\x05pticm\x18\x05 \x01(\x0b2\x1a.qbit.services.PTICMSolverH\x00\x12$\n\x06graphs\x18\x07 \x03(\x0b2\x14.qbit.services.GraphB\x08\n\x06solver"5\n\x05Graph\x12\r\n\x05node1\x18\x01 \x01(\r\x12\r\n\x05node2\x18\x02 \x01(\r\x12\x0e\n\x06weight\x18\x03 \x01(\x01"D\n\x0fMinKCutResponse\x121\n\tsolutions\x18\x01 \x03(\x0b2\x1e.qbit.services.MinKCutSolution"b\n\x0fMinKCutSolution\x12\x10\n\x08feasible\x18\x01 \x01(\x08\x12\r\n\x05value\x18\x02 \x01(\x01\x12.\n\x07mapping\x18\x03 \x03(\x0b2\x1d.qbit.services.MinKCutMapping"?\n\x0eMinKCutMapping\x12\x17\n\x0fpartition_index\x18\x01 \x01(\r\x12\x14\n\x0cvertex_index\x18\x02 \x03(\r"\x14\n\x12HealthCheckRequest*$\n\x0fsqa_energy_type\x12\x08\n\x04BEST\x10\x00\x12\x07\n\x03ALL\x10\x01*\x1f\n\x11sqa_schedule_type\x12\n\n\x06LINEAR\x10\x00*&\n\npticm_goal\x12\x0c\n\x08OPTIMIZE\x10\x00\x12\n\n\x06SAMPLE\x10\x01*0\n\x12pticm_scaling_type\x12\n\n\x06MEDIAN\x10\x00\x12\x0e\n\nNO_SCALING\x10\x01*B\n\x15pticm_var_fixing_type\x12\r\n\tNO_FIXING\x10\x00\x12\x0f\n\x0bPERSISTENCY\x10\x01\x12\t\n\x05SPVAR\x10\x02*,\n\x0ffuj_noise_model\x12\x0e\n\nMETROPOLIS\x10\x00\x12\t\n\x05GIBBS\x10\x01*?\n\rfuj_temp_mode\x12\x0f\n\x0bEXPONENTIAL\x10\x00\x12\x0b\n\x07INVERSE\x10\x01\x12\x10\n\x0cINVERSE_ROOT\x10\x02*\'\n\x0cfuj_sol_mode\x12\x0c\n\x08COMPLETE\x10\x00\x12\t\n\x05QUICK\x10\x01*8\n\x10fuj_scaling_mode\x12\r\n\tAUTOMATIC\x10\x00\x12\n\n\x06EXPERT\x10\x01\x12\t\n\x05MIXED\x10\x02*,\n\x07runType\x12\x0f\n\x0bSYNCHRONOUS\x10\x00\x12\x10\n\x0cASYNCHRONOUS\x10\x012\xd3\x08\n\x04Qbit\x12m\n\x0fCompareMolecule\x12\x1d.qbit.services.CompareRequest\x1a\x1f.qbit.services.ComparisonResult"\x1a\x82\xd3\xe4\x93\x02\x14"\x0f/v1/gms/compare:\x01*\x12{\n\x18CompareMoleculeBenchmark\x12\x1d.qbit.services.CompareRequest\x1a\x1f.qbit.services.ComparisonResult"\x1f\x82\xd3\xe4\x93\x02\x19"\x14/v1/gms/comparebench:\x01*\x12l\n\tHobo2Qubo\x12\x1f.qbit.services.BinaryPolynomial\x1a\x1f.qbit.services.BinaryPolynomial"\x1d\x82\xd3\xe4\x93\x02\x17"\x12/v1/qubo/hobo2qubo:\x01*\x12_\n\tSolveQubo\x12\x1a.qbit.services.QuboRequest\x1a\x1b.qbit.services.QuboResponse"\x19\x82\xd3\xe4\x93\x02\x13"\x0e/v1/qubo/solve:\x01*\x12t\n\x13SolveQuboFujitsuDA2\x12\x1a.qbit.services.QuboRequest\x1a\x1b.qbit.services.QuboResponse"$\x82\xd3\xe4\x93\x02\x1e"\x19/v1/qubo/solve/fujitsuda2:\x01*\x12x\n\x15SolveQuboFujitsuDA2PT\x12\x1a.qbit.services.QuboRequest\x1a\x1b.qbit.services.QuboResponse"&\x82\xd3\xe4\x93\x02 "\x1b/v1/qubo/solve/fujitsuda2pt:\x01*\x12d\n\x08Knapsack\x12\x1e.qbit.services.KnapsackRequest\x1a\x1f.qbit.services.KnapsackResponse"\x17\x82\xd3\xe4\x93\x02\x11"\x0c/v1/knapsack:\x01*\x12x\n\x13MinKCutPartitioning\x12\x1d.qbit.services.MinKCutRequest\x1a\x1e.qbit.services.MinKCutResponse""\x82\xd3\xe4\x93\x02\x1c"\x17/v1/MinKCutPartitioning:\x01*\x12a\n\x0bHealthCheck\x12!.qbit.services.HealthCheckRequest\x1a\x16.google.protobuf.Empty"\x17\x82\xd3\xe4\x93\x02\x11\x12\x0f/v1/healthcheck\x12]\n\tAuthCheck\x12!.qbit.services.HealthCheckRequest\x1a\x16.google.protobuf.Empty"\x15\x82\xd3\xe4\x93\x02\x0f\x12\r/v1/authcheckb\x06proto3'), dependencies=[
 google_dot_protobuf_dot_empty__pb2.DESCRIPTOR, google_dot_protobuf_dot_struct__pb2.DESCRIPTOR, google_dot_api_dot_annotations__pb2.DESCRIPTOR])
_SQA_ENERGY_TYPE = _descriptor.EnumDescriptor(name='sqa_energy_type', full_name='qbit.services.sqa_energy_type', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='BEST', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='ALL', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=8950, serialized_end=8986)
_sym_db.RegisterEnumDescriptor(_SQA_ENERGY_TYPE)
sqa_energy_type = enum_type_wrapper.EnumTypeWrapper(_SQA_ENERGY_TYPE)
_SQA_SCHEDULE_TYPE = _descriptor.EnumDescriptor(name='sqa_schedule_type', full_name='qbit.services.sqa_schedule_type', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='LINEAR', index=0, number=0, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=8988, serialized_end=9019)
_sym_db.RegisterEnumDescriptor(_SQA_SCHEDULE_TYPE)
sqa_schedule_type = enum_type_wrapper.EnumTypeWrapper(_SQA_SCHEDULE_TYPE)
_PTICM_GOAL = _descriptor.EnumDescriptor(name='pticm_goal', full_name='qbit.services.pticm_goal', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='OPTIMIZE', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SAMPLE', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9021, serialized_end=9059)
_sym_db.RegisterEnumDescriptor(_PTICM_GOAL)
pticm_goal = enum_type_wrapper.EnumTypeWrapper(_PTICM_GOAL)
_PTICM_SCALING_TYPE = _descriptor.EnumDescriptor(name='pticm_scaling_type', full_name='qbit.services.pticm_scaling_type', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='MEDIAN', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='NO_SCALING', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9061, serialized_end=9109)
_sym_db.RegisterEnumDescriptor(_PTICM_SCALING_TYPE)
pticm_scaling_type = enum_type_wrapper.EnumTypeWrapper(_PTICM_SCALING_TYPE)
_PTICM_VAR_FIXING_TYPE = _descriptor.EnumDescriptor(name='pticm_var_fixing_type', full_name='qbit.services.pticm_var_fixing_type', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='NO_FIXING', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='PERSISTENCY', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='SPVAR', index=2, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9111, serialized_end=9177)
_sym_db.RegisterEnumDescriptor(_PTICM_VAR_FIXING_TYPE)
pticm_var_fixing_type = enum_type_wrapper.EnumTypeWrapper(_PTICM_VAR_FIXING_TYPE)
_FUJ_NOISE_MODEL = _descriptor.EnumDescriptor(name='fuj_noise_model', full_name='qbit.services.fuj_noise_model', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='METROPOLIS', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='GIBBS', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9179, serialized_end=9223)
_sym_db.RegisterEnumDescriptor(_FUJ_NOISE_MODEL)
fuj_noise_model = enum_type_wrapper.EnumTypeWrapper(_FUJ_NOISE_MODEL)
_FUJ_TEMP_MODE = _descriptor.EnumDescriptor(name='fuj_temp_mode', full_name='qbit.services.fuj_temp_mode', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='EXPONENTIAL', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INVERSE', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='INVERSE_ROOT', index=2, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9225, serialized_end=9288)
_sym_db.RegisterEnumDescriptor(_FUJ_TEMP_MODE)
fuj_temp_mode = enum_type_wrapper.EnumTypeWrapper(_FUJ_TEMP_MODE)
_FUJ_SOL_MODE = _descriptor.EnumDescriptor(name='fuj_sol_mode', full_name='qbit.services.fuj_sol_mode', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='COMPLETE', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='QUICK', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9290, serialized_end=9329)
_sym_db.RegisterEnumDescriptor(_FUJ_SOL_MODE)
fuj_sol_mode = enum_type_wrapper.EnumTypeWrapper(_FUJ_SOL_MODE)
_FUJ_SCALING_MODE = _descriptor.EnumDescriptor(name='fuj_scaling_mode', full_name='qbit.services.fuj_scaling_mode', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='AUTOMATIC', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='EXPERT', index=1, number=1, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='MIXED', index=2, number=2, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9331, serialized_end=9387)
_sym_db.RegisterEnumDescriptor(_FUJ_SCALING_MODE)
fuj_scaling_mode = enum_type_wrapper.EnumTypeWrapper(_FUJ_SCALING_MODE)
_RUNTYPE = _descriptor.EnumDescriptor(name='runType', full_name='qbit.services.runType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='SYNCHRONOUS', index=0, number=0, serialized_options=None, type=None),
 _descriptor.EnumValueDescriptor(name='ASYNCHRONOUS', index=1, number=1, serialized_options=None, type=None)], containing_type=None, serialized_options=None, serialized_start=9389, serialized_end=9433)
_sym_db.RegisterEnumDescriptor(_RUNTYPE)
runType = enum_type_wrapper.EnumTypeWrapper(_RUNTYPE)
BEST = 0
ALL = 1
LINEAR = 0
OPTIMIZE = 0
SAMPLE = 1
MEDIAN = 0
NO_SCALING = 1
NO_FIXING = 0
PERSISTENCY = 1
SPVAR = 2
METROPOLIS = 0
GIBBS = 1
EXPONENTIAL = 0
INVERSE = 1
INVERSE_ROOT = 2
COMPLETE = 0
QUICK = 1
AUTOMATIC = 0
EXPERT = 1
MIXED = 2
SYNCHRONOUS = 0
ASYNCHRONOUS = 1
_COMPAREREQUEST = _descriptor.Descriptor(name='CompareRequest', full_name='qbit.services.CompareRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='smiles', full_name='qbit.services.CompareRequest.smiles', index=0, number=1, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu', full_name='qbit.services.CompareRequest.tabu', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='multitabu', full_name='qbit.services.CompareRequest.multitabu', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pathrelinking', full_name='qbit.services.CompareRequest.pathrelinking', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='sqa', full_name='qbit.services.CompareRequest.sqa', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pticm', full_name='qbit.services.CompareRequest.pticm', index=5, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='should_visualize', full_name='qbit.services.CompareRequest.should_visualize', index=6, number=7, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='criteria', full_name='qbit.services.CompareRequest.criteria', index=7, number=8, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='solver', full_name='qbit.services.CompareRequest.solver', index=0, containing_type=None, fields=[])], serialized_start=119, serialized_end=481)
_COMPAREREQUESTSDF = _descriptor.Descriptor(name='CompareRequestSDF', full_name='qbit.services.CompareRequestSDF', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='sdf_first', full_name='qbit.services.CompareRequestSDF.sdf_first', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='sdf_second', full_name='qbit.services.CompareRequestSDF.sdf_second', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu', full_name='qbit.services.CompareRequestSDF.tabu', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='multitabu', full_name='qbit.services.CompareRequestSDF.multitabu', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pathrelinking', full_name='qbit.services.CompareRequestSDF.pathrelinking', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='sqa', full_name='qbit.services.CompareRequestSDF.sqa', index=5, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pticm', full_name='qbit.services.CompareRequestSDF.pticm', index=6, number=7, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='should_visualize', full_name='qbit.services.CompareRequestSDF.should_visualize', index=7, number=8, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='criteria', full_name='qbit.services.CompareRequestSDF.criteria', index=8, number=9, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='solver', full_name='qbit.services.CompareRequestSDF.solver', index=0, containing_type=None, fields=[])], serialized_start=484, serialized_end=872)
_COMPARISONRESULT = _descriptor.Descriptor(name='ComparisonResult', full_name='qbit.services.ComparisonResult', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='can_use_quantum', full_name='qbit.services.ComparisonResult.can_use_quantum', index=0, number=1, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='ok', full_name='qbit.services.ComparisonResult.ok', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='visualizations', full_name='qbit.services.ComparisonResult.visualizations', index=2, number=3, type=9, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='shared_traits', full_name='qbit.services.ComparisonResult.shared_traits', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='similarity', full_name='qbit.services.ComparisonResult.similarity', index=4, number=5, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=875, serialized_end=1022)
_QUBOMATRIX_QUBOARRAY = _descriptor.Descriptor(name='QuboArray', full_name='qbit.services.QuboMatrix.QuboArray', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='qubo_row', full_name='qbit.services.QuboMatrix.QuboArray.qubo_row', index=0, number=1, type=1, cpp_type=5, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1107, serialized_end=1136)
_QUBOMATRIX = _descriptor.Descriptor(name='QuboMatrix', full_name='qbit.services.QuboMatrix', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='qubo', full_name='qbit.services.QuboMatrix.qubo', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='constant', full_name='qbit.services.QuboMatrix.constant', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _QUBOMATRIX_QUBOARRAY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1024, serialized_end=1136)
_BINARYPOLYNOMIAL_TERM = _descriptor.Descriptor(name='Term', full_name='qbit.services.BinaryPolynomial.Term', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='coefficient', full_name='qbit.services.BinaryPolynomial.Term.coefficient', index=0, number=1, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='polynomials', full_name='qbit.services.BinaryPolynomial.Term.polynomials', index=1, number=2, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1211, serialized_end=1259)
_BINARYPOLYNOMIAL = _descriptor.Descriptor(name='BinaryPolynomial', full_name='qbit.services.BinaryPolynomial', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='terms', full_name='qbit.services.BinaryPolynomial.terms', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _BINARYPOLYNOMIAL_TERM], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1138, serialized_end=1259)
_TABU1OPTSOLVER = _descriptor.Descriptor(name='Tabu1OptSolver', full_name='qbit.services.Tabu1OptSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='improvement_cutoff', full_name='qbit.services.Tabu1OptSolver.improvement_cutoff', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='improvement_tolerance', full_name='qbit.services.Tabu1OptSolver.improvement_tolerance', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu_tenure', full_name='qbit.services.Tabu1OptSolver.tabu_tenure', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu_tenure_rand_max', full_name='qbit.services.Tabu1OptSolver.tabu_tenure_rand_max', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.Tabu1OptSolver.timeout', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.Tabu1OptSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.Tabu1OptSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.Tabu1OptSolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.Tabu1OptSolver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.Tabu1OptSolver.v5', index=4, containing_type=None, fields=[])], serialized_start=1262, serialized_end=1445)
_TABUSOLVERLIST = _descriptor.Descriptor(name='TabuSolverList', full_name='qbit.services.TabuSolverList', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='tabu_solvers', full_name='qbit.services.TabuSolverList.tabu_solvers', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=1447, serialized_end=1516)
_MULTITABU1OPTSOLVER = _descriptor.Descriptor(name='MultiTabu1OptSolver', full_name='qbit.services.MultiTabu1OptSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='improvement_cutoff', full_name='qbit.services.MultiTabu1OptSolver.improvement_cutoff', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='improvement_tolerance', full_name='qbit.services.MultiTabu1OptSolver.improvement_tolerance', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu_tenure', full_name='qbit.services.MultiTabu1OptSolver.tabu_tenure', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu_tenure_rand_max', full_name='qbit.services.MultiTabu1OptSolver.tabu_tenure_rand_max', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solver_count', full_name='qbit.services.MultiTabu1OptSolver.solver_count', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solver_list', full_name='qbit.services.MultiTabu1OptSolver.solver_list', index=5, number=7, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.MultiTabu1OptSolver.timeout', index=6, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.MultiTabu1OptSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.MultiTabu1OptSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.MultiTabu1OptSolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.MultiTabu1OptSolver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.MultiTabu1OptSolver.v5', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v6', full_name='qbit.services.MultiTabu1OptSolver.v6', index=5, containing_type=None, fields=[])], serialized_start=1519, serialized_end=1791)
_PATHRELINKINGSOLVER = _descriptor.Descriptor(name='PathRelinkingSolver', full_name='qbit.services.PathRelinkingSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='distance_scale', full_name='qbit.services.PathRelinkingSolver.distance_scale', index=0, number=1, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='greedy_path_relinking', full_name='qbit.services.PathRelinkingSolver.greedy_path_relinking', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.PathRelinkingSolver.timeout', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='ref_set_count', full_name='qbit.services.PathRelinkingSolver.ref_set_count', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.PathRelinkingSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.PathRelinkingSolver.v3', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.PathRelinkingSolver.v4', index=2, containing_type=None, fields=[])], serialized_start=1794, serialized_end=1934)
_SQASOLVER = _descriptor.Descriptor(name='SQASolver', full_name='qbit.services.SQASolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='beta', full_name='qbit.services.SQASolver.beta', index=0, number=1, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='energy_type', full_name='qbit.services.SQASolver.energy_type', index=1, number=2, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='gamma_initial', full_name='qbit.services.SQASolver.gamma_initial', index=2, number=3, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='gamma_final', full_name='qbit.services.SQASolver.gamma_final', index=3, number=4, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_reads', full_name='qbit.services.SQASolver.num_reads', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_replicas', full_name='qbit.services.SQASolver.num_replicas', index=5, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_sweeps', full_name='qbit.services.SQASolver.num_sweeps', index=6, number=7, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.SQASolver.timeout', index=7, number=8, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='schedule_type', full_name='qbit.services.SQASolver.schedule_type', index=8, number=9, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.SQASolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.SQASolver.v3', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.SQASolver.v4', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.SQASolver.v5', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v6', full_name='qbit.services.SQASolver.v6', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.SQASolver.v7', index=5, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v8', full_name='qbit.services.SQASolver.v8', index=6, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v9', full_name='qbit.services.SQASolver.v9', index=7, containing_type=None, fields=[])], serialized_start=1937, serialized_end=2258)
_PTICMSOLVER = _descriptor.Descriptor(name='PTICMSolver', full_name='qbit.services.PTICMSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='high_temp', full_name='qbit.services.PTICMSolver.high_temp', index=0, number=1, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='low_temp', full_name='qbit.services.PTICMSolver.low_temp', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_replicas', full_name='qbit.services.PTICMSolver.num_replicas', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_sweeps_per_run', full_name='qbit.services.PTICMSolver.num_sweeps_per_run', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_temps', full_name='qbit.services.PTICMSolver.num_temps', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='manual_temperatures', full_name='qbit.services.PTICMSolver.manual_temperatures', index=5, number=11, type=1, cpp_type=5, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='auto_set_temperatures', full_name='qbit.services.PTICMSolver.auto_set_temperatures', index=6, number=12, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='elite_threshold', full_name='qbit.services.PTICMSolver.elite_threshold', index=7, number=13, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='frac_icm_thermal_layers', full_name='qbit.services.PTICMSolver.frac_icm_thermal_layers', index=8, number=14, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='frac_sweeps_fixing', full_name='qbit.services.PTICMSolver.frac_sweeps_fixing', index=9, number=15, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='frac_sweeps_idle', full_name='qbit.services.PTICMSolver.frac_sweeps_idle', index=10, number=16, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='frac_sweeps_stagnation', full_name='qbit.services.PTICMSolver.frac_sweeps_stagnation', index=11, number=17, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='max_samples_per_layer', full_name='qbit.services.PTICMSolver.max_samples_per_layer', index=12, number=18, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='max_total_sweeps', full_name='qbit.services.PTICMSolver.max_total_sweeps', index=13, number=19, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_elite_temps', full_name='qbit.services.PTICMSolver.num_elite_temps', index=14, number=20, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='perform_icm', full_name='qbit.services.PTICMSolver.perform_icm', index=15, number=21, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='goal', full_name='qbit.services.PTICMSolver.goal', index=16, number=22, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='scaling_type', full_name='qbit.services.PTICMSolver.scaling_type', index=17, number=23, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='var_fixing_type', full_name='qbit.services.PTICMSolver.var_fixing_type', index=18, number=24, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.PTICMSolver.timeout', index=19, number=25, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.PTICMSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.PTICMSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.PTICMSolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.PTICMSolver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.PTICMSolver.v5', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v12', full_name='qbit.services.PTICMSolver.v12', index=5, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v13', full_name='qbit.services.PTICMSolver.v13', index=6, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v14', full_name='qbit.services.PTICMSolver.v14', index=7, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v15', full_name='qbit.services.PTICMSolver.v15', index=8, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v16', full_name='qbit.services.PTICMSolver.v16', index=9, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v17', full_name='qbit.services.PTICMSolver.v17', index=10, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v18', full_name='qbit.services.PTICMSolver.v18', index=11, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v19', full_name='qbit.services.PTICMSolver.v19', index=12, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v20', full_name='qbit.services.PTICMSolver.v20', index=13, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v21', full_name='qbit.services.PTICMSolver.v21', index=14, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v25', full_name='qbit.services.PTICMSolver.v25', index=15, containing_type=None, fields=[])], serialized_start=2261, serialized_end=3004)
_FUJITSUDASOLVER_GUIDANCECONFIGENTRY = _descriptor.Descriptor(name='GuidanceConfigEntry', full_name='qbit.services.FujitsuDASolver.GuidanceConfigEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.FujitsuDASolver.GuidanceConfigEntry.key', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.FujitsuDASolver.GuidanceConfigEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3498, serialized_end=3551)
_FUJITSUDASOLVER = _descriptor.Descriptor(name='FujitsuDASolver', full_name='qbit.services.FujitsuDASolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='noise_model', full_name='qbit.services.FujitsuDASolver.noise_model', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_iterations', full_name='qbit.services.FujitsuDASolver.number_iterations', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_runs', full_name='qbit.services.FujitsuDASolver.number_runs', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='offset_increase_rate', full_name='qbit.services.FujitsuDASolver.offset_increase_rate', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_decay', full_name='qbit.services.FujitsuDASolver.temperature_decay', index=4, number=5, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_interval', full_name='qbit.services.FujitsuDASolver.temperature_interval', index=5, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_mode', full_name='qbit.services.FujitsuDASolver.temperature_mode', index=6, number=7, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_start', full_name='qbit.services.FujitsuDASolver.temperature_start', index=7, number=8, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solution_mode', full_name='qbit.services.FujitsuDASolver.solution_mode', index=8, number=9, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='expert_mode', full_name='qbit.services.FujitsuDASolver.expert_mode', index=9, number=10, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='guidance_config', full_name='qbit.services.FujitsuDASolver.guidance_config', index=10, number=11, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='job_id', full_name='qbit.services.FujitsuDASolver.job_id', index=11, number=12, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.FujitsuDASolver.timeout', index=12, number=13, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _FUJITSUDASOLVER_GUIDANCECONFIGENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.FujitsuDASolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.FujitsuDASolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.FujitsuDASolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.FujitsuDASolver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.FujitsuDASolver.v5', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v6', full_name='qbit.services.FujitsuDASolver.v6', index=5, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.FujitsuDASolver.v7', index=6, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v8', full_name='qbit.services.FujitsuDASolver.v8', index=7, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v13', full_name='qbit.services.FujitsuDASolver.v13', index=8, containing_type=None, fields=[])], serialized_start=3007, serialized_end=3606)
_FUJITSUDAMIXEDMODESOLVER_GUIDANCECONFIGENTRY = _descriptor.Descriptor(name='GuidanceConfigEntry', full_name='qbit.services.FujitsuDAMixedModeSolver.GuidanceConfigEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.FujitsuDAMixedModeSolver.GuidanceConfigEntry.key', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.FujitsuDAMixedModeSolver.GuidanceConfigEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3498, serialized_end=3551)
_FUJITSUDAMIXEDMODESOLVER = _descriptor.Descriptor(name='FujitsuDAMixedModeSolver', full_name='qbit.services.FujitsuDAMixedModeSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='noise_model', full_name='qbit.services.FujitsuDAMixedModeSolver.noise_model', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_iterations', full_name='qbit.services.FujitsuDAMixedModeSolver.number_iterations', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_runs', full_name='qbit.services.FujitsuDAMixedModeSolver.number_runs', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='offset_increase_rate', full_name='qbit.services.FujitsuDAMixedModeSolver.offset_increase_rate', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_decay', full_name='qbit.services.FujitsuDAMixedModeSolver.temperature_decay', index=4, number=5, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_interval', full_name='qbit.services.FujitsuDAMixedModeSolver.temperature_interval', index=5, number=6, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_mode', full_name='qbit.services.FujitsuDAMixedModeSolver.temperature_mode', index=6, number=7, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_start', full_name='qbit.services.FujitsuDAMixedModeSolver.temperature_start', index=7, number=8, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solution_mode', full_name='qbit.services.FujitsuDAMixedModeSolver.solution_mode', index=8, number=9, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='guidance_config', full_name='qbit.services.FujitsuDAMixedModeSolver.guidance_config', index=9, number=11, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='job_id', full_name='qbit.services.FujitsuDAMixedModeSolver.job_id', index=10, number=12, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.FujitsuDAMixedModeSolver.timeout', index=11, number=13, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _FUJITSUDAMIXEDMODESOLVER_GUIDANCECONFIGENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.FujitsuDAMixedModeSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.FujitsuDAMixedModeSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.FujitsuDAMixedModeSolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.FujitsuDAMixedModeSolver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.FujitsuDAMixedModeSolver.v5', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v6', full_name='qbit.services.FujitsuDAMixedModeSolver.v6', index=5, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.FujitsuDAMixedModeSolver.v7', index=6, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v8', full_name='qbit.services.FujitsuDAMixedModeSolver.v8', index=7, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v13', full_name='qbit.services.FujitsuDAMixedModeSolver.v13', index=8, containing_type=None, fields=[])], serialized_start=3609, serialized_end=4205)
_FUJITSUDAPTSOLVER_GUIDANCECONFIGENTRY = _descriptor.Descriptor(name='GuidanceConfigEntry', full_name='qbit.services.FujitsuDAPTSolver.GuidanceConfigEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.FujitsuDAPTSolver.GuidanceConfigEntry.key', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.FujitsuDAPTSolver.GuidanceConfigEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3498, serialized_end=3551)
_FUJITSUDAPTSOLVER = _descriptor.Descriptor(name='FujitsuDAPTSolver', full_name='qbit.services.FujitsuDAPTSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='number_iterations', full_name='qbit.services.FujitsuDAPTSolver.number_iterations', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='offset_increase_rate', full_name='qbit.services.FujitsuDAPTSolver.offset_increase_rate', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solution_mode', full_name='qbit.services.FujitsuDAPTSolver.solution_mode', index=2, number=3, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_replicas', full_name='qbit.services.FujitsuDAPTSolver.number_replicas', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='guidance_config', full_name='qbit.services.FujitsuDAPTSolver.guidance_config', index=4, number=5, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='job_id', full_name='qbit.services.FujitsuDAPTSolver.job_id', index=5, number=6, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.FujitsuDAPTSolver.timeout', index=6, number=7, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _FUJITSUDAPTSOLVER_GUIDANCECONFIGENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.FujitsuDAPTSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.FujitsuDAPTSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.FujitsuDAPTSolver.v4', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.FujitsuDAPTSolver.v7', index=3, containing_type=None, fields=[])], serialized_start=4208, serialized_end=4560)
_FUJITSUDA2SOLVER_GUIDANCECONFIGENTRY = _descriptor.Descriptor(name='GuidanceConfigEntry', full_name='qbit.services.FujitsuDA2Solver.GuidanceConfigEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.FujitsuDA2Solver.GuidanceConfigEntry.key', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.FujitsuDA2Solver.GuidanceConfigEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3498, serialized_end=3551)
_FUJITSUDA2SOLVER = _descriptor.Descriptor(name='FujitsuDA2Solver', full_name='qbit.services.FujitsuDA2Solver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='number_iterations', full_name='qbit.services.FujitsuDA2Solver.number_iterations', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_runs', full_name='qbit.services.FujitsuDA2Solver.number_runs', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='offset_increase_rate', full_name='qbit.services.FujitsuDA2Solver.offset_increase_rate', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_decay', full_name='qbit.services.FujitsuDA2Solver.temperature_decay', index=3, number=4, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_interval', full_name='qbit.services.FujitsuDA2Solver.temperature_interval', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_mode', full_name='qbit.services.FujitsuDA2Solver.temperature_mode', index=5, number=6, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_start', full_name='qbit.services.FujitsuDA2Solver.temperature_start', index=6, number=7, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solution_mode', full_name='qbit.services.FujitsuDA2Solver.solution_mode', index=7, number=8, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='expert_mode', full_name='qbit.services.FujitsuDA2Solver.expert_mode', index=8, number=9, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='guidance_config', full_name='qbit.services.FujitsuDA2Solver.guidance_config', index=9, number=10, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='job_id', full_name='qbit.services.FujitsuDA2Solver.job_id', index=10, number=11, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.FujitsuDA2Solver.timeout', index=11, number=12, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _FUJITSUDA2SOLVER_GUIDANCECONFIGENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.FujitsuDA2Solver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.FujitsuDA2Solver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.FujitsuDA2Solver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.FujitsuDA2Solver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.FujitsuDA2Solver.v5', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v6', full_name='qbit.services.FujitsuDA2Solver.v6', index=5, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.FujitsuDA2Solver.v7', index=6, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v12', full_name='qbit.services.FujitsuDA2Solver.v12', index=7, containing_type=None, fields=[])], serialized_start=4563, serialized_end=5103)
_FUJITSUDA2PTSOLVER_GUIDANCECONFIGENTRY = _descriptor.Descriptor(name='GuidanceConfigEntry', full_name='qbit.services.FujitsuDA2PTSolver.GuidanceConfigEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.FujitsuDA2PTSolver.GuidanceConfigEntry.key', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.FujitsuDA2PTSolver.GuidanceConfigEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3498, serialized_end=3551)
_FUJITSUDA2PTSOLVER = _descriptor.Descriptor(name='FujitsuDA2PTSolver', full_name='qbit.services.FujitsuDA2PTSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='number_iterations', full_name='qbit.services.FujitsuDA2PTSolver.number_iterations', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_replicas', full_name='qbit.services.FujitsuDA2PTSolver.number_replicas', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='offset_increase_rate', full_name='qbit.services.FujitsuDA2PTSolver.offset_increase_rate', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solution_mode', full_name='qbit.services.FujitsuDA2PTSolver.solution_mode', index=3, number=4, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='guidance_config', full_name='qbit.services.FujitsuDA2PTSolver.guidance_config', index=4, number=5, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='job_id', full_name='qbit.services.FujitsuDA2PTSolver.job_id', index=5, number=6, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.FujitsuDA2PTSolver.timeout', index=6, number=7, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _FUJITSUDA2PTSOLVER_GUIDANCECONFIGENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.FujitsuDA2PTSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.FujitsuDA2PTSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.FujitsuDA2PTSolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.FujitsuDA2PTSolver.v7', index=3, containing_type=None, fields=[])], serialized_start=5106, serialized_end=5460)
_FUJITSUDA2MIXEDMODESOLVER_GUIDANCECONFIGENTRY = _descriptor.Descriptor(name='GuidanceConfigEntry', full_name='qbit.services.FujitsuDA2MixedModeSolver.GuidanceConfigEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.FujitsuDA2MixedModeSolver.GuidanceConfigEntry.key', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.FujitsuDA2MixedModeSolver.GuidanceConfigEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=3498, serialized_end=3551)
_FUJITSUDA2MIXEDMODESOLVER = _descriptor.Descriptor(name='FujitsuDA2MixedModeSolver', full_name='qbit.services.FujitsuDA2MixedModeSolver', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='number_iterations', full_name='qbit.services.FujitsuDA2MixedModeSolver.number_iterations', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='number_runs', full_name='qbit.services.FujitsuDA2MixedModeSolver.number_runs', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='offset_increase_rate', full_name='qbit.services.FujitsuDA2MixedModeSolver.offset_increase_rate', index=2, number=3, type=2, cpp_type=6, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_decay', full_name='qbit.services.FujitsuDA2MixedModeSolver.temperature_decay', index=3, number=4, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_interval', full_name='qbit.services.FujitsuDA2MixedModeSolver.temperature_interval', index=4, number=5, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_mode', full_name='qbit.services.FujitsuDA2MixedModeSolver.temperature_mode', index=5, number=6, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='temperature_start', full_name='qbit.services.FujitsuDA2MixedModeSolver.temperature_start', index=6, number=7, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solution_mode', full_name='qbit.services.FujitsuDA2MixedModeSolver.solution_mode', index=7, number=8, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='guidance_config', full_name='qbit.services.FujitsuDA2MixedModeSolver.guidance_config', index=8, number=9, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='job_id', full_name='qbit.services.FujitsuDA2MixedModeSolver.job_id', index=9, number=10, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timeout', full_name='qbit.services.FujitsuDA2MixedModeSolver.timeout', index=10, number=11, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _FUJITSUDA2MIXEDMODESOLVER_GUIDANCECONFIGENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='v1', full_name='qbit.services.FujitsuDA2MixedModeSolver.v1', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v2', full_name='qbit.services.FujitsuDA2MixedModeSolver.v2', index=1, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v3', full_name='qbit.services.FujitsuDA2MixedModeSolver.v3', index=2, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v4', full_name='qbit.services.FujitsuDA2MixedModeSolver.v4', index=3, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v5', full_name='qbit.services.FujitsuDA2MixedModeSolver.v5', index=4, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v6', full_name='qbit.services.FujitsuDA2MixedModeSolver.v6', index=5, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v7', full_name='qbit.services.FujitsuDA2MixedModeSolver.v7', index=6, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='v11', full_name='qbit.services.FujitsuDA2MixedModeSolver.v11', index=7, containing_type=None, fields=[])], serialized_start=5463, serialized_end=6000)
_QUBOREQUEST = _descriptor.Descriptor(name='QuboRequest', full_name='qbit.services.QuboRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='run_type', full_name='qbit.services.QuboRequest.run_type', index=0, number=1, type=14, cpp_type=8, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='binary_polynomial', full_name='qbit.services.QuboRequest.binary_polynomial', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='qubo_matrix', full_name='qbit.services.QuboRequest.qubo_matrix', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='tabu', full_name='qbit.services.QuboRequest.tabu', index=3, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='multitabu', full_name='qbit.services.QuboRequest.multitabu', index=4, number=6, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pathrelinking', full_name='qbit.services.QuboRequest.pathrelinking', index=5, number=7, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='sqa', full_name='qbit.services.QuboRequest.sqa', index=6, number=8, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pticm', full_name='qbit.services.QuboRequest.pticm', index=7, number=9, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fujitsuDA', full_name='qbit.services.QuboRequest.fujitsuDA', index=8, number=10, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fujitsuDAPT', full_name='qbit.services.QuboRequest.fujitsuDAPT', index=9, number=11, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fujitsuDAMixedMode', full_name='qbit.services.QuboRequest.fujitsuDAMixedMode', index=10, number=12, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fujitsuDA2', full_name='qbit.services.QuboRequest.fujitsuDA2', index=11, number=13, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fujitsuDA2PT', full_name='qbit.services.QuboRequest.fujitsuDA2PT', index=12, number=14, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='fujitsuDA2MixedMode', full_name='qbit.services.QuboRequest.fujitsuDA2MixedMode', index=13, number=15, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='qubo', full_name='qbit.services.QuboRequest.qubo', index=0, containing_type=None, fields=[]),
 _descriptor.OneofDescriptor(name='solver_parameters', full_name='qbit.services.QuboRequest.solver_parameters', index=1, containing_type=None, fields=[])], serialized_start=6003, serialized_end=6818)
_QUBOSOLUTION_CONFIGURATIONENTRY = _descriptor.Descriptor(name='ConfigurationEntry', full_name='qbit.services.QuboSolution.ConfigurationEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.QuboSolution.ConfigurationEntry.key', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.QuboSolution.ConfigurationEntry.value', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=6943, serialized_end=6995)
_QUBOSOLUTION = _descriptor.Descriptor(name='QuboSolution', full_name='qbit.services.QuboSolution', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='energy', full_name='qbit.services.QuboSolution.energy', index=0, number=1, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='frequency', full_name='qbit.services.QuboSolution.frequency', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='configuration', full_name='qbit.services.QuboSolution.configuration', index=2, number=3, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _QUBOSOLUTION_CONFIGURATIONENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=6821, serialized_end=6995)
_SOLVERTIMING_DETAILEDENTRY = _descriptor.Descriptor(name='DetailedEntry', full_name='qbit.services.SolverTiming.DetailedEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.SolverTiming.DetailedEntry.key', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.SolverTiming.DetailedEntry.value', index=1, number=2, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=7161, serialized_end=7208)
_SOLVERTIMING = _descriptor.Descriptor(name='SolverTiming', full_name='qbit.services.SolverTiming', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='cpu_time', full_name='qbit.services.SolverTiming.cpu_time', index=0, number=1, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='queue_time', full_name='qbit.services.SolverTiming.queue_time', index=1, number=2, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solve_time', full_name='qbit.services.SolverTiming.solve_time', index=2, number=3, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='total_elapsed_time', full_name='qbit.services.SolverTiming.total_elapsed_time', index=3, number=5, type=4, cpp_type=4, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='detailed', full_name='qbit.services.SolverTiming.detailed', index=4, number=6, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _SOLVERTIMING_DETAILEDENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=6998, serialized_end=7208)
_QUBOSOLUTIONLIST = _descriptor.Descriptor(name='QuboSolutionList', full_name='qbit.services.QuboSolutionList', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='result_status', full_name='qbit.services.QuboSolutionList.result_status', index=0, number=1, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solutions', full_name='qbit.services.QuboSolutionList.solutions', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='timing', full_name='qbit.services.QuboSolutionList.timing', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=7211, serialized_end=7345)
_QUBORESPONSE_SOLVERINPUTPARAMETERSENTRY = _descriptor.Descriptor(name='SolverInputParametersEntry', full_name='qbit.services.QuboResponse.SolverInputParametersEntry', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='key', full_name='qbit.services.QuboResponse.SolverInputParametersEntry.key', index=0, number=1, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.QuboResponse.SolverInputParametersEntry.value', index=1, number=2, type=9, cpp_type=9, label=1, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=_b('8\x01'), is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=7511, serialized_end=7571)
_QUBORESPONSE = _descriptor.Descriptor(name='QuboResponse', full_name='qbit.services.QuboResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='qubo_solution', full_name='qbit.services.QuboResponse.qubo_solution', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='solver_input_parameters', full_name='qbit.services.QuboResponse.solver_input_parameters', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[
 _QUBORESPONSE_SOLVERINPUTPARAMETERSENTRY], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='response', full_name='qbit.services.QuboResponse.response', index=0, containing_type=None, fields=[])], serialized_start=7348, serialized_end=7583)
_KNAPSACKREQUEST = _descriptor.Descriptor(name='KnapsackRequest', full_name='qbit.services.KnapsackRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='tabu', full_name='qbit.services.KnapsackRequest.tabu', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='multitabu', full_name='qbit.services.KnapsackRequest.multitabu', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pathrelinking', full_name='qbit.services.KnapsackRequest.pathrelinking', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='sqa', full_name='qbit.services.KnapsackRequest.sqa', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pticm', full_name='qbit.services.KnapsackRequest.pticm', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='problem', full_name='qbit.services.KnapsackRequest.problem', index=5, number=7, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='solver', full_name='qbit.services.KnapsackRequest.solver', index=0, containing_type=None, fields=[])], serialized_start=7586, serialized_end=7913)
_KNAPSACKPROBLEM = _descriptor.Descriptor(name='KnapsackProblem', full_name='qbit.services.KnapsackProblem', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='capacity', full_name='qbit.services.KnapsackProblem.capacity', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='items', full_name='qbit.services.KnapsackProblem.items', index=1, number=2, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=7915, serialized_end=7994)
_KNAPSACKITEM = _descriptor.Descriptor(name='KnapsackItem', full_name='qbit.services.KnapsackItem', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='index', full_name='qbit.services.KnapsackItem.index', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='weight', full_name='qbit.services.KnapsackItem.weight', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.KnapsackItem.value', index=2, number=3, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=7996, serialized_end=8056)
_KNAPSACKRESPONSE = _descriptor.Descriptor(name='KnapsackResponse', full_name='qbit.services.KnapsackResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='solutions', full_name='qbit.services.KnapsackResponse.solutions', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8058, serialized_end=8128)
_KNAPSACKSOLUTION = _descriptor.Descriptor(name='KnapsackSolution', full_name='qbit.services.KnapsackSolution', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='feasible', full_name='qbit.services.KnapsackSolution.feasible', index=0, number=1, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.KnapsackSolution.value', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='weight', full_name='qbit.services.KnapsackSolution.weight', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='configurations', full_name='qbit.services.KnapsackSolution.configurations', index=3, number=4, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8131, serialized_end=8260)
_KNAPSACKCONFIGURATION = _descriptor.Descriptor(name='KnapsackConfiguration', full_name='qbit.services.KnapsackConfiguration', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='index', full_name='qbit.services.KnapsackConfiguration.index', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='selected', full_name='qbit.services.KnapsackConfiguration.selected', index=1, number=2, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8262, serialized_end=8318)
_MINKCUTREQUEST = _descriptor.Descriptor(name='MinKCutRequest', full_name='qbit.services.MinKCutRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='tabu', full_name='qbit.services.MinKCutRequest.tabu', index=0, number=1, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='multitabu', full_name='qbit.services.MinKCutRequest.multitabu', index=1, number=2, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pathrelinking', full_name='qbit.services.MinKCutRequest.pathrelinking', index=2, number=3, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='sqa', full_name='qbit.services.MinKCutRequest.sqa', index=3, number=4, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='pticm', full_name='qbit.services.MinKCutRequest.pticm', index=4, number=5, type=11, cpp_type=10, label=1, has_default_value=False, default_value=None, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='graphs', full_name='qbit.services.MinKCutRequest.graphs', index=5, number=7, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[
 _descriptor.OneofDescriptor(name='solver', full_name='qbit.services.MinKCutRequest.solver', index=0, containing_type=None, fields=[])], serialized_start=8321, serialized_end=8636)
_GRAPH = _descriptor.Descriptor(name='Graph', full_name='qbit.services.Graph', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='node1', full_name='qbit.services.Graph.node1', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='node2', full_name='qbit.services.Graph.node2', index=1, number=2, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='weight', full_name='qbit.services.Graph.weight', index=2, number=3, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8638, serialized_end=8691)
_MINKCUTRESPONSE = _descriptor.Descriptor(name='MinKCutResponse', full_name='qbit.services.MinKCutResponse', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='solutions', full_name='qbit.services.MinKCutResponse.solutions', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8693, serialized_end=8761)
_MINKCUTSOLUTION = _descriptor.Descriptor(name='MinKCutSolution', full_name='qbit.services.MinKCutSolution', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='feasible', full_name='qbit.services.MinKCutSolution.feasible', index=0, number=1, type=8, cpp_type=7, label=1, has_default_value=False, default_value=False, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='value', full_name='qbit.services.MinKCutSolution.value', index=1, number=2, type=1, cpp_type=5, label=1, has_default_value=False, default_value=float(0), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='mapping', full_name='qbit.services.MinKCutSolution.mapping', index=2, number=3, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8763, serialized_end=8861)
_MINKCUTMAPPING = _descriptor.Descriptor(name='MinKCutMapping', full_name='qbit.services.MinKCutMapping', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='partition_index', full_name='qbit.services.MinKCutMapping.partition_index', index=0, number=1, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='vertex_index', full_name='qbit.services.MinKCutMapping.vertex_index', index=1, number=2, type=13, cpp_type=3, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, serialized_options=None, file=DESCRIPTOR)], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8863, serialized_end=8926)
_HEALTHCHECKREQUEST = _descriptor.Descriptor(name='HealthCheckRequest', full_name='qbit.services.HealthCheckRequest', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], serialized_options=None, is_extendable=False, syntax='proto3', extension_ranges=[], oneofs=[], serialized_start=8928, serialized_end=8948)
_COMPAREREQUEST.fields_by_name['tabu'].message_type = _TABU1OPTSOLVER
_COMPAREREQUEST.fields_by_name['multitabu'].message_type = _MULTITABU1OPTSOLVER
_COMPAREREQUEST.fields_by_name['pathrelinking'].message_type = _PATHRELINKINGSOLVER
_COMPAREREQUEST.fields_by_name['sqa'].message_type = _SQASOLVER
_COMPAREREQUEST.fields_by_name['pticm'].message_type = _PTICMSOLVER
_COMPAREREQUEST.fields_by_name['criteria'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_COMPAREREQUEST.oneofs_by_name['solver'].fields.append(_COMPAREREQUEST.fields_by_name['tabu'])
_COMPAREREQUEST.fields_by_name['tabu'].containing_oneof = _COMPAREREQUEST.oneofs_by_name['solver']
_COMPAREREQUEST.oneofs_by_name['solver'].fields.append(_COMPAREREQUEST.fields_by_name['multitabu'])
_COMPAREREQUEST.fields_by_name['multitabu'].containing_oneof = _COMPAREREQUEST.oneofs_by_name['solver']
_COMPAREREQUEST.oneofs_by_name['solver'].fields.append(_COMPAREREQUEST.fields_by_name['pathrelinking'])
_COMPAREREQUEST.fields_by_name['pathrelinking'].containing_oneof = _COMPAREREQUEST.oneofs_by_name['solver']
_COMPAREREQUEST.oneofs_by_name['solver'].fields.append(_COMPAREREQUEST.fields_by_name['sqa'])
_COMPAREREQUEST.fields_by_name['sqa'].containing_oneof = _COMPAREREQUEST.oneofs_by_name['solver']
_COMPAREREQUEST.oneofs_by_name['solver'].fields.append(_COMPAREREQUEST.fields_by_name['pticm'])
_COMPAREREQUEST.fields_by_name['pticm'].containing_oneof = _COMPAREREQUEST.oneofs_by_name['solver']
_COMPAREREQUESTSDF.fields_by_name['tabu'].message_type = _TABU1OPTSOLVER
_COMPAREREQUESTSDF.fields_by_name['multitabu'].message_type = _MULTITABU1OPTSOLVER
_COMPAREREQUESTSDF.fields_by_name['pathrelinking'].message_type = _PATHRELINKINGSOLVER
_COMPAREREQUESTSDF.fields_by_name['sqa'].message_type = _SQASOLVER
_COMPAREREQUESTSDF.fields_by_name['pticm'].message_type = _PTICMSOLVER
_COMPAREREQUESTSDF.fields_by_name['criteria'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_COMPAREREQUESTSDF.oneofs_by_name['solver'].fields.append(_COMPAREREQUESTSDF.fields_by_name['tabu'])
_COMPAREREQUESTSDF.fields_by_name['tabu'].containing_oneof = _COMPAREREQUESTSDF.oneofs_by_name['solver']
_COMPAREREQUESTSDF.oneofs_by_name['solver'].fields.append(_COMPAREREQUESTSDF.fields_by_name['multitabu'])
_COMPAREREQUESTSDF.fields_by_name['multitabu'].containing_oneof = _COMPAREREQUESTSDF.oneofs_by_name['solver']
_COMPAREREQUESTSDF.oneofs_by_name['solver'].fields.append(_COMPAREREQUESTSDF.fields_by_name['pathrelinking'])
_COMPAREREQUESTSDF.fields_by_name['pathrelinking'].containing_oneof = _COMPAREREQUESTSDF.oneofs_by_name['solver']
_COMPAREREQUESTSDF.oneofs_by_name['solver'].fields.append(_COMPAREREQUESTSDF.fields_by_name['sqa'])
_COMPAREREQUESTSDF.fields_by_name['sqa'].containing_oneof = _COMPAREREQUESTSDF.oneofs_by_name['solver']
_COMPAREREQUESTSDF.oneofs_by_name['solver'].fields.append(_COMPAREREQUESTSDF.fields_by_name['pticm'])
_COMPAREREQUESTSDF.fields_by_name['pticm'].containing_oneof = _COMPAREREQUESTSDF.oneofs_by_name['solver']
_COMPARISONRESULT.fields_by_name['shared_traits'].message_type = google_dot_protobuf_dot_struct__pb2._STRUCT
_QUBOMATRIX_QUBOARRAY.containing_type = _QUBOMATRIX
_QUBOMATRIX.fields_by_name['qubo'].message_type = _QUBOMATRIX_QUBOARRAY
_BINARYPOLYNOMIAL_TERM.containing_type = _BINARYPOLYNOMIAL
_BINARYPOLYNOMIAL.fields_by_name['terms'].message_type = _BINARYPOLYNOMIAL_TERM
_TABU1OPTSOLVER.oneofs_by_name['v1'].fields.append(_TABU1OPTSOLVER.fields_by_name['improvement_cutoff'])
_TABU1OPTSOLVER.fields_by_name['improvement_cutoff'].containing_oneof = _TABU1OPTSOLVER.oneofs_by_name['v1']
_TABU1OPTSOLVER.oneofs_by_name['v2'].fields.append(_TABU1OPTSOLVER.fields_by_name['improvement_tolerance'])
_TABU1OPTSOLVER.fields_by_name['improvement_tolerance'].containing_oneof = _TABU1OPTSOLVER.oneofs_by_name['v2']
_TABU1OPTSOLVER.oneofs_by_name['v3'].fields.append(_TABU1OPTSOLVER.fields_by_name['tabu_tenure'])
_TABU1OPTSOLVER.fields_by_name['tabu_tenure'].containing_oneof = _TABU1OPTSOLVER.oneofs_by_name['v3']
_TABU1OPTSOLVER.oneofs_by_name['v4'].fields.append(_TABU1OPTSOLVER.fields_by_name['tabu_tenure_rand_max'])
_TABU1OPTSOLVER.fields_by_name['tabu_tenure_rand_max'].containing_oneof = _TABU1OPTSOLVER.oneofs_by_name['v4']
_TABU1OPTSOLVER.oneofs_by_name['v5'].fields.append(_TABU1OPTSOLVER.fields_by_name['timeout'])
_TABU1OPTSOLVER.fields_by_name['timeout'].containing_oneof = _TABU1OPTSOLVER.oneofs_by_name['v5']
_TABUSOLVERLIST.fields_by_name['tabu_solvers'].message_type = _TABU1OPTSOLVER
_MULTITABU1OPTSOLVER.fields_by_name['solver_list'].message_type = _TABUSOLVERLIST
_MULTITABU1OPTSOLVER.oneofs_by_name['v1'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['improvement_cutoff'])
_MULTITABU1OPTSOLVER.fields_by_name['improvement_cutoff'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v1']
_MULTITABU1OPTSOLVER.oneofs_by_name['v2'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['improvement_tolerance'])
_MULTITABU1OPTSOLVER.fields_by_name['improvement_tolerance'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v2']
_MULTITABU1OPTSOLVER.oneofs_by_name['v3'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['tabu_tenure'])
_MULTITABU1OPTSOLVER.fields_by_name['tabu_tenure'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v3']
_MULTITABU1OPTSOLVER.oneofs_by_name['v4'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['tabu_tenure_rand_max'])
_MULTITABU1OPTSOLVER.fields_by_name['tabu_tenure_rand_max'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v4']
_MULTITABU1OPTSOLVER.oneofs_by_name['v5'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['solver_count'])
_MULTITABU1OPTSOLVER.fields_by_name['solver_count'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v5']
_MULTITABU1OPTSOLVER.oneofs_by_name['v5'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['solver_list'])
_MULTITABU1OPTSOLVER.fields_by_name['solver_list'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v5']
_MULTITABU1OPTSOLVER.oneofs_by_name['v6'].fields.append(_MULTITABU1OPTSOLVER.fields_by_name['timeout'])
_MULTITABU1OPTSOLVER.fields_by_name['timeout'].containing_oneof = _MULTITABU1OPTSOLVER.oneofs_by_name['v6']
_PATHRELINKINGSOLVER.oneofs_by_name['v1'].fields.append(_PATHRELINKINGSOLVER.fields_by_name['distance_scale'])
_PATHRELINKINGSOLVER.fields_by_name['distance_scale'].containing_oneof = _PATHRELINKINGSOLVER.oneofs_by_name['v1']
_PATHRELINKINGSOLVER.oneofs_by_name['v3'].fields.append(_PATHRELINKINGSOLVER.fields_by_name['timeout'])
_PATHRELINKINGSOLVER.fields_by_name['timeout'].containing_oneof = _PATHRELINKINGSOLVER.oneofs_by_name['v3']
_PATHRELINKINGSOLVER.oneofs_by_name['v4'].fields.append(_PATHRELINKINGSOLVER.fields_by_name['ref_set_count'])
_PATHRELINKINGSOLVER.fields_by_name['ref_set_count'].containing_oneof = _PATHRELINKINGSOLVER.oneofs_by_name['v4']
_SQASOLVER.fields_by_name['energy_type'].enum_type = _SQA_ENERGY_TYPE
_SQASOLVER.fields_by_name['schedule_type'].enum_type = _SQA_SCHEDULE_TYPE
_SQASOLVER.oneofs_by_name['v1'].fields.append(_SQASOLVER.fields_by_name['beta'])
_SQASOLVER.fields_by_name['beta'].containing_oneof = _SQASOLVER.oneofs_by_name['v1']
_SQASOLVER.oneofs_by_name['v3'].fields.append(_SQASOLVER.fields_by_name['gamma_initial'])
_SQASOLVER.fields_by_name['gamma_initial'].containing_oneof = _SQASOLVER.oneofs_by_name['v3']
_SQASOLVER.oneofs_by_name['v4'].fields.append(_SQASOLVER.fields_by_name['gamma_final'])
_SQASOLVER.fields_by_name['gamma_final'].containing_oneof = _SQASOLVER.oneofs_by_name['v4']
_SQASOLVER.oneofs_by_name['v5'].fields.append(_SQASOLVER.fields_by_name['num_reads'])
_SQASOLVER.fields_by_name['num_reads'].containing_oneof = _SQASOLVER.oneofs_by_name['v5']
_SQASOLVER.oneofs_by_name['v6'].fields.append(_SQASOLVER.fields_by_name['num_replicas'])
_SQASOLVER.fields_by_name['num_replicas'].containing_oneof = _SQASOLVER.oneofs_by_name['v6']
_SQASOLVER.oneofs_by_name['v7'].fields.append(_SQASOLVER.fields_by_name['num_sweeps'])
_SQASOLVER.fields_by_name['num_sweeps'].containing_oneof = _SQASOLVER.oneofs_by_name['v7']
_SQASOLVER.oneofs_by_name['v8'].fields.append(_SQASOLVER.fields_by_name['timeout'])
_SQASOLVER.fields_by_name['timeout'].containing_oneof = _SQASOLVER.oneofs_by_name['v8']
_SQASOLVER.oneofs_by_name['v9'].fields.append(_SQASOLVER.fields_by_name['schedule_type'])
_SQASOLVER.fields_by_name['schedule_type'].containing_oneof = _SQASOLVER.oneofs_by_name['v9']
_PTICMSOLVER.fields_by_name['goal'].enum_type = _PTICM_GOAL
_PTICMSOLVER.fields_by_name['scaling_type'].enum_type = _PTICM_SCALING_TYPE
_PTICMSOLVER.fields_by_name['var_fixing_type'].enum_type = _PTICM_VAR_FIXING_TYPE
_PTICMSOLVER.oneofs_by_name['v1'].fields.append(_PTICMSOLVER.fields_by_name['high_temp'])
_PTICMSOLVER.fields_by_name['high_temp'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v1']
_PTICMSOLVER.oneofs_by_name['v2'].fields.append(_PTICMSOLVER.fields_by_name['low_temp'])
_PTICMSOLVER.fields_by_name['low_temp'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v2']
_PTICMSOLVER.oneofs_by_name['v3'].fields.append(_PTICMSOLVER.fields_by_name['num_replicas'])
_PTICMSOLVER.fields_by_name['num_replicas'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v3']
_PTICMSOLVER.oneofs_by_name['v4'].fields.append(_PTICMSOLVER.fields_by_name['num_sweeps_per_run'])
_PTICMSOLVER.fields_by_name['num_sweeps_per_run'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v4']
_PTICMSOLVER.oneofs_by_name['v5'].fields.append(_PTICMSOLVER.fields_by_name['num_temps'])
_PTICMSOLVER.fields_by_name['num_temps'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v5']
_PTICMSOLVER.oneofs_by_name['v12'].fields.append(_PTICMSOLVER.fields_by_name['auto_set_temperatures'])
_PTICMSOLVER.fields_by_name['auto_set_temperatures'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v12']
_PTICMSOLVER.oneofs_by_name['v13'].fields.append(_PTICMSOLVER.fields_by_name['elite_threshold'])
_PTICMSOLVER.fields_by_name['elite_threshold'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v13']
_PTICMSOLVER.oneofs_by_name['v14'].fields.append(_PTICMSOLVER.fields_by_name['frac_icm_thermal_layers'])
_PTICMSOLVER.fields_by_name['frac_icm_thermal_layers'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v14']
_PTICMSOLVER.oneofs_by_name['v15'].fields.append(_PTICMSOLVER.fields_by_name['frac_sweeps_fixing'])
_PTICMSOLVER.fields_by_name['frac_sweeps_fixing'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v15']
_PTICMSOLVER.oneofs_by_name['v16'].fields.append(_PTICMSOLVER.fields_by_name['frac_sweeps_idle'])
_PTICMSOLVER.fields_by_name['frac_sweeps_idle'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v16']
_PTICMSOLVER.oneofs_by_name['v17'].fields.append(_PTICMSOLVER.fields_by_name['frac_sweeps_stagnation'])
_PTICMSOLVER.fields_by_name['frac_sweeps_stagnation'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v17']
_PTICMSOLVER.oneofs_by_name['v18'].fields.append(_PTICMSOLVER.fields_by_name['max_samples_per_layer'])
_PTICMSOLVER.fields_by_name['max_samples_per_layer'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v18']
_PTICMSOLVER.oneofs_by_name['v19'].fields.append(_PTICMSOLVER.fields_by_name['max_total_sweeps'])
_PTICMSOLVER.fields_by_name['max_total_sweeps'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v19']
_PTICMSOLVER.oneofs_by_name['v20'].fields.append(_PTICMSOLVER.fields_by_name['num_elite_temps'])
_PTICMSOLVER.fields_by_name['num_elite_temps'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v20']
_PTICMSOLVER.oneofs_by_name['v21'].fields.append(_PTICMSOLVER.fields_by_name['perform_icm'])
_PTICMSOLVER.fields_by_name['perform_icm'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v21']
_PTICMSOLVER.oneofs_by_name['v25'].fields.append(_PTICMSOLVER.fields_by_name['timeout'])
_PTICMSOLVER.fields_by_name['timeout'].containing_oneof = _PTICMSOLVER.oneofs_by_name['v25']
_FUJITSUDASOLVER_GUIDANCECONFIGENTRY.containing_type = _FUJITSUDASOLVER
_FUJITSUDASOLVER.fields_by_name['noise_model'].enum_type = _FUJ_NOISE_MODEL
_FUJITSUDASOLVER.fields_by_name['temperature_mode'].enum_type = _FUJ_TEMP_MODE
_FUJITSUDASOLVER.fields_by_name['solution_mode'].enum_type = _FUJ_SOL_MODE
_FUJITSUDASOLVER.fields_by_name['guidance_config'].message_type = _FUJITSUDASOLVER_GUIDANCECONFIGENTRY
_FUJITSUDASOLVER.oneofs_by_name['v1'].fields.append(_FUJITSUDASOLVER.fields_by_name['noise_model'])
_FUJITSUDASOLVER.fields_by_name['noise_model'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v1']
_FUJITSUDASOLVER.oneofs_by_name['v2'].fields.append(_FUJITSUDASOLVER.fields_by_name['number_iterations'])
_FUJITSUDASOLVER.fields_by_name['number_iterations'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v2']
_FUJITSUDASOLVER.oneofs_by_name['v3'].fields.append(_FUJITSUDASOLVER.fields_by_name['number_runs'])
_FUJITSUDASOLVER.fields_by_name['number_runs'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v3']
_FUJITSUDASOLVER.oneofs_by_name['v4'].fields.append(_FUJITSUDASOLVER.fields_by_name['offset_increase_rate'])
_FUJITSUDASOLVER.fields_by_name['offset_increase_rate'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v4']
_FUJITSUDASOLVER.oneofs_by_name['v5'].fields.append(_FUJITSUDASOLVER.fields_by_name['temperature_decay'])
_FUJITSUDASOLVER.fields_by_name['temperature_decay'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v5']
_FUJITSUDASOLVER.oneofs_by_name['v6'].fields.append(_FUJITSUDASOLVER.fields_by_name['temperature_interval'])
_FUJITSUDASOLVER.fields_by_name['temperature_interval'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v6']
_FUJITSUDASOLVER.oneofs_by_name['v7'].fields.append(_FUJITSUDASOLVER.fields_by_name['temperature_mode'])
_FUJITSUDASOLVER.fields_by_name['temperature_mode'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v7']
_FUJITSUDASOLVER.oneofs_by_name['v8'].fields.append(_FUJITSUDASOLVER.fields_by_name['temperature_start'])
_FUJITSUDASOLVER.fields_by_name['temperature_start'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v8']
_FUJITSUDASOLVER.oneofs_by_name['v13'].fields.append(_FUJITSUDASOLVER.fields_by_name['timeout'])
_FUJITSUDASOLVER.fields_by_name['timeout'].containing_oneof = _FUJITSUDASOLVER.oneofs_by_name['v13']
_FUJITSUDAMIXEDMODESOLVER_GUIDANCECONFIGENTRY.containing_type = _FUJITSUDAMIXEDMODESOLVER
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['noise_model'].enum_type = _FUJ_NOISE_MODEL
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_mode'].enum_type = _FUJ_TEMP_MODE
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['solution_mode'].enum_type = _FUJ_SOL_MODE
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['guidance_config'].message_type = _FUJITSUDAMIXEDMODESOLVER_GUIDANCECONFIGENTRY
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v1'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['noise_model'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['noise_model'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v1']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v2'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['number_iterations'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['number_iterations'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v2']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v3'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['number_runs'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['number_runs'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v3']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v4'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['offset_increase_rate'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['offset_increase_rate'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v4']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v5'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_decay'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_decay'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v5']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v6'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_interval'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_interval'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v6']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v7'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_mode'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_mode'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v7']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v8'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_start'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['temperature_start'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v8']
_FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v13'].fields.append(_FUJITSUDAMIXEDMODESOLVER.fields_by_name['timeout'])
_FUJITSUDAMIXEDMODESOLVER.fields_by_name['timeout'].containing_oneof = _FUJITSUDAMIXEDMODESOLVER.oneofs_by_name['v13']
_FUJITSUDAPTSOLVER_GUIDANCECONFIGENTRY.containing_type = _FUJITSUDAPTSOLVER
_FUJITSUDAPTSOLVER.fields_by_name['solution_mode'].enum_type = _FUJ_SOL_MODE
_FUJITSUDAPTSOLVER.fields_by_name['guidance_config'].message_type = _FUJITSUDAPTSOLVER_GUIDANCECONFIGENTRY
_FUJITSUDAPTSOLVER.oneofs_by_name['v1'].fields.append(_FUJITSUDAPTSOLVER.fields_by_name['number_iterations'])
_FUJITSUDAPTSOLVER.fields_by_name['number_iterations'].containing_oneof = _FUJITSUDAPTSOLVER.oneofs_by_name['v1']
_FUJITSUDAPTSOLVER.oneofs_by_name['v2'].fields.append(_FUJITSUDAPTSOLVER.fields_by_name['offset_increase_rate'])
_FUJITSUDAPTSOLVER.fields_by_name['offset_increase_rate'].containing_oneof = _FUJITSUDAPTSOLVER.oneofs_by_name['v2']
_FUJITSUDAPTSOLVER.oneofs_by_name['v4'].fields.append(_FUJITSUDAPTSOLVER.fields_by_name['number_replicas'])
_FUJITSUDAPTSOLVER.fields_by_name['number_replicas'].containing_oneof = _FUJITSUDAPTSOLVER.oneofs_by_name['v4']
_FUJITSUDAPTSOLVER.oneofs_by_name['v7'].fields.append(_FUJITSUDAPTSOLVER.fields_by_name['timeout'])
_FUJITSUDAPTSOLVER.fields_by_name['timeout'].containing_oneof = _FUJITSUDAPTSOLVER.oneofs_by_name['v7']
_FUJITSUDA2SOLVER_GUIDANCECONFIGENTRY.containing_type = _FUJITSUDA2SOLVER
_FUJITSUDA2SOLVER.fields_by_name['temperature_mode'].enum_type = _FUJ_TEMP_MODE
_FUJITSUDA2SOLVER.fields_by_name['solution_mode'].enum_type = _FUJ_SOL_MODE
_FUJITSUDA2SOLVER.fields_by_name['guidance_config'].message_type = _FUJITSUDA2SOLVER_GUIDANCECONFIGENTRY
_FUJITSUDA2SOLVER.oneofs_by_name['v1'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['number_iterations'])
_FUJITSUDA2SOLVER.fields_by_name['number_iterations'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v1']
_FUJITSUDA2SOLVER.oneofs_by_name['v2'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['number_runs'])
_FUJITSUDA2SOLVER.fields_by_name['number_runs'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v2']
_FUJITSUDA2SOLVER.oneofs_by_name['v3'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['offset_increase_rate'])
_FUJITSUDA2SOLVER.fields_by_name['offset_increase_rate'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v3']
_FUJITSUDA2SOLVER.oneofs_by_name['v4'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['temperature_decay'])
_FUJITSUDA2SOLVER.fields_by_name['temperature_decay'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v4']
_FUJITSUDA2SOLVER.oneofs_by_name['v5'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['temperature_interval'])
_FUJITSUDA2SOLVER.fields_by_name['temperature_interval'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v5']
_FUJITSUDA2SOLVER.oneofs_by_name['v6'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['temperature_mode'])
_FUJITSUDA2SOLVER.fields_by_name['temperature_mode'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v6']
_FUJITSUDA2SOLVER.oneofs_by_name['v7'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['temperature_start'])
_FUJITSUDA2SOLVER.fields_by_name['temperature_start'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v7']
_FUJITSUDA2SOLVER.oneofs_by_name['v12'].fields.append(_FUJITSUDA2SOLVER.fields_by_name['timeout'])
_FUJITSUDA2SOLVER.fields_by_name['timeout'].containing_oneof = _FUJITSUDA2SOLVER.oneofs_by_name['v12']
_FUJITSUDA2PTSOLVER_GUIDANCECONFIGENTRY.containing_type = _FUJITSUDA2PTSOLVER
_FUJITSUDA2PTSOLVER.fields_by_name['solution_mode'].enum_type = _FUJ_SOL_MODE
_FUJITSUDA2PTSOLVER.fields_by_name['guidance_config'].message_type = _FUJITSUDA2PTSOLVER_GUIDANCECONFIGENTRY
_FUJITSUDA2PTSOLVER.oneofs_by_name['v1'].fields.append(_FUJITSUDA2PTSOLVER.fields_by_name['number_iterations'])
_FUJITSUDA2PTSOLVER.fields_by_name['number_iterations'].containing_oneof = _FUJITSUDA2PTSOLVER.oneofs_by_name['v1']
_FUJITSUDA2PTSOLVER.oneofs_by_name['v2'].fields.append(_FUJITSUDA2PTSOLVER.fields_by_name['number_replicas'])
_FUJITSUDA2PTSOLVER.fields_by_name['number_replicas'].containing_oneof = _FUJITSUDA2PTSOLVER.oneofs_by_name['v2']
_FUJITSUDA2PTSOLVER.oneofs_by_name['v3'].fields.append(_FUJITSUDA2PTSOLVER.fields_by_name['offset_increase_rate'])
_FUJITSUDA2PTSOLVER.fields_by_name['offset_increase_rate'].containing_oneof = _FUJITSUDA2PTSOLVER.oneofs_by_name['v3']
_FUJITSUDA2PTSOLVER.oneofs_by_name['v7'].fields.append(_FUJITSUDA2PTSOLVER.fields_by_name['timeout'])
_FUJITSUDA2PTSOLVER.fields_by_name['timeout'].containing_oneof = _FUJITSUDA2PTSOLVER.oneofs_by_name['v7']
_FUJITSUDA2MIXEDMODESOLVER_GUIDANCECONFIGENTRY.containing_type = _FUJITSUDA2MIXEDMODESOLVER
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_mode'].enum_type = _FUJ_TEMP_MODE
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['solution_mode'].enum_type = _FUJ_SOL_MODE
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['guidance_config'].message_type = _FUJITSUDA2MIXEDMODESOLVER_GUIDANCECONFIGENTRY
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v1'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['number_iterations'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['number_iterations'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v1']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v2'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['number_runs'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['number_runs'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v2']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v3'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['offset_increase_rate'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['offset_increase_rate'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v3']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v4'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_decay'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_decay'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v4']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v5'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_interval'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_interval'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v5']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v6'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_mode'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_mode'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v6']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v7'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_start'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['temperature_start'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v7']
_FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v11'].fields.append(_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['timeout'])
_FUJITSUDA2MIXEDMODESOLVER.fields_by_name['timeout'].containing_oneof = _FUJITSUDA2MIXEDMODESOLVER.oneofs_by_name['v11']
_QUBOREQUEST.fields_by_name['run_type'].enum_type = _RUNTYPE
_QUBOREQUEST.fields_by_name['binary_polynomial'].message_type = _BINARYPOLYNOMIAL
_QUBOREQUEST.fields_by_name['qubo_matrix'].message_type = _QUBOMATRIX
_QUBOREQUEST.fields_by_name['tabu'].message_type = _TABU1OPTSOLVER
_QUBOREQUEST.fields_by_name['multitabu'].message_type = _MULTITABU1OPTSOLVER
_QUBOREQUEST.fields_by_name['pathrelinking'].message_type = _PATHRELINKINGSOLVER
_QUBOREQUEST.fields_by_name['sqa'].message_type = _SQASOLVER
_QUBOREQUEST.fields_by_name['pticm'].message_type = _PTICMSOLVER
_QUBOREQUEST.fields_by_name['fujitsuDA'].message_type = _FUJITSUDASOLVER
_QUBOREQUEST.fields_by_name['fujitsuDAPT'].message_type = _FUJITSUDAPTSOLVER
_QUBOREQUEST.fields_by_name['fujitsuDAMixedMode'].message_type = _FUJITSUDAMIXEDMODESOLVER
_QUBOREQUEST.fields_by_name['fujitsuDA2'].message_type = _FUJITSUDA2SOLVER
_QUBOREQUEST.fields_by_name['fujitsuDA2PT'].message_type = _FUJITSUDA2PTSOLVER
_QUBOREQUEST.fields_by_name['fujitsuDA2MixedMode'].message_type = _FUJITSUDA2MIXEDMODESOLVER
_QUBOREQUEST.oneofs_by_name['qubo'].fields.append(_QUBOREQUEST.fields_by_name['binary_polynomial'])
_QUBOREQUEST.fields_by_name['binary_polynomial'].containing_oneof = _QUBOREQUEST.oneofs_by_name['qubo']
_QUBOREQUEST.oneofs_by_name['qubo'].fields.append(_QUBOREQUEST.fields_by_name['qubo_matrix'])
_QUBOREQUEST.fields_by_name['qubo_matrix'].containing_oneof = _QUBOREQUEST.oneofs_by_name['qubo']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['tabu'])
_QUBOREQUEST.fields_by_name['tabu'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['multitabu'])
_QUBOREQUEST.fields_by_name['multitabu'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['pathrelinking'])
_QUBOREQUEST.fields_by_name['pathrelinking'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['sqa'])
_QUBOREQUEST.fields_by_name['sqa'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['pticm'])
_QUBOREQUEST.fields_by_name['pticm'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['fujitsuDA'])
_QUBOREQUEST.fields_by_name['fujitsuDA'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['fujitsuDAPT'])
_QUBOREQUEST.fields_by_name['fujitsuDAPT'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['fujitsuDAMixedMode'])
_QUBOREQUEST.fields_by_name['fujitsuDAMixedMode'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['fujitsuDA2'])
_QUBOREQUEST.fields_by_name['fujitsuDA2'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['fujitsuDA2PT'])
_QUBOREQUEST.fields_by_name['fujitsuDA2PT'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOREQUEST.oneofs_by_name['solver_parameters'].fields.append(_QUBOREQUEST.fields_by_name['fujitsuDA2MixedMode'])
_QUBOREQUEST.fields_by_name['fujitsuDA2MixedMode'].containing_oneof = _QUBOREQUEST.oneofs_by_name['solver_parameters']
_QUBOSOLUTION_CONFIGURATIONENTRY.containing_type = _QUBOSOLUTION
_QUBOSOLUTION.fields_by_name['configuration'].message_type = _QUBOSOLUTION_CONFIGURATIONENTRY
_SOLVERTIMING_DETAILEDENTRY.containing_type = _SOLVERTIMING
_SOLVERTIMING.fields_by_name['detailed'].message_type = _SOLVERTIMING_DETAILEDENTRY
_QUBOSOLUTIONLIST.fields_by_name['solutions'].message_type = _QUBOSOLUTION
_QUBOSOLUTIONLIST.fields_by_name['timing'].message_type = _SOLVERTIMING
_QUBORESPONSE_SOLVERINPUTPARAMETERSENTRY.containing_type = _QUBORESPONSE
_QUBORESPONSE.fields_by_name['qubo_solution'].message_type = _QUBOSOLUTIONLIST
_QUBORESPONSE.fields_by_name['solver_input_parameters'].message_type = _QUBORESPONSE_SOLVERINPUTPARAMETERSENTRY
_QUBORESPONSE.oneofs_by_name['response'].fields.append(_QUBORESPONSE.fields_by_name['qubo_solution'])
_QUBORESPONSE.fields_by_name['qubo_solution'].containing_oneof = _QUBORESPONSE.oneofs_by_name['response']
_KNAPSACKREQUEST.fields_by_name['tabu'].message_type = _TABU1OPTSOLVER
_KNAPSACKREQUEST.fields_by_name['multitabu'].message_type = _MULTITABU1OPTSOLVER
_KNAPSACKREQUEST.fields_by_name['pathrelinking'].message_type = _PATHRELINKINGSOLVER
_KNAPSACKREQUEST.fields_by_name['sqa'].message_type = _SQASOLVER
_KNAPSACKREQUEST.fields_by_name['pticm'].message_type = _PTICMSOLVER
_KNAPSACKREQUEST.fields_by_name['problem'].message_type = _KNAPSACKPROBLEM
_KNAPSACKREQUEST.oneofs_by_name['solver'].fields.append(_KNAPSACKREQUEST.fields_by_name['tabu'])
_KNAPSACKREQUEST.fields_by_name['tabu'].containing_oneof = _KNAPSACKREQUEST.oneofs_by_name['solver']
_KNAPSACKREQUEST.oneofs_by_name['solver'].fields.append(_KNAPSACKREQUEST.fields_by_name['multitabu'])
_KNAPSACKREQUEST.fields_by_name['multitabu'].containing_oneof = _KNAPSACKREQUEST.oneofs_by_name['solver']
_KNAPSACKREQUEST.oneofs_by_name['solver'].fields.append(_KNAPSACKREQUEST.fields_by_name['pathrelinking'])
_KNAPSACKREQUEST.fields_by_name['pathrelinking'].containing_oneof = _KNAPSACKREQUEST.oneofs_by_name['solver']
_KNAPSACKREQUEST.oneofs_by_name['solver'].fields.append(_KNAPSACKREQUEST.fields_by_name['sqa'])
_KNAPSACKREQUEST.fields_by_name['sqa'].containing_oneof = _KNAPSACKREQUEST.oneofs_by_name['solver']
_KNAPSACKREQUEST.oneofs_by_name['solver'].fields.append(_KNAPSACKREQUEST.fields_by_name['pticm'])
_KNAPSACKREQUEST.fields_by_name['pticm'].containing_oneof = _KNAPSACKREQUEST.oneofs_by_name['solver']
_KNAPSACKPROBLEM.fields_by_name['items'].message_type = _KNAPSACKITEM
_KNAPSACKRESPONSE.fields_by_name['solutions'].message_type = _KNAPSACKSOLUTION
_KNAPSACKSOLUTION.fields_by_name['configurations'].message_type = _KNAPSACKCONFIGURATION
_MINKCUTREQUEST.fields_by_name['tabu'].message_type = _TABU1OPTSOLVER
_MINKCUTREQUEST.fields_by_name['multitabu'].message_type = _MULTITABU1OPTSOLVER
_MINKCUTREQUEST.fields_by_name['pathrelinking'].message_type = _PATHRELINKINGSOLVER
_MINKCUTREQUEST.fields_by_name['sqa'].message_type = _SQASOLVER
_MINKCUTREQUEST.fields_by_name['pticm'].message_type = _PTICMSOLVER
_MINKCUTREQUEST.fields_by_name['graphs'].message_type = _GRAPH
_MINKCUTREQUEST.oneofs_by_name['solver'].fields.append(_MINKCUTREQUEST.fields_by_name['tabu'])
_MINKCUTREQUEST.fields_by_name['tabu'].containing_oneof = _MINKCUTREQUEST.oneofs_by_name['solver']
_MINKCUTREQUEST.oneofs_by_name['solver'].fields.append(_MINKCUTREQUEST.fields_by_name['multitabu'])
_MINKCUTREQUEST.fields_by_name['multitabu'].containing_oneof = _MINKCUTREQUEST.oneofs_by_name['solver']
_MINKCUTREQUEST.oneofs_by_name['solver'].fields.append(_MINKCUTREQUEST.fields_by_name['pathrelinking'])
_MINKCUTREQUEST.fields_by_name['pathrelinking'].containing_oneof = _MINKCUTREQUEST.oneofs_by_name['solver']
_MINKCUTREQUEST.oneofs_by_name['solver'].fields.append(_MINKCUTREQUEST.fields_by_name['sqa'])
_MINKCUTREQUEST.fields_by_name['sqa'].containing_oneof = _MINKCUTREQUEST.oneofs_by_name['solver']
_MINKCUTREQUEST.oneofs_by_name['solver'].fields.append(_MINKCUTREQUEST.fields_by_name['pticm'])
_MINKCUTREQUEST.fields_by_name['pticm'].containing_oneof = _MINKCUTREQUEST.oneofs_by_name['solver']
_MINKCUTRESPONSE.fields_by_name['solutions'].message_type = _MINKCUTSOLUTION
_MINKCUTSOLUTION.fields_by_name['mapping'].message_type = _MINKCUTMAPPING
DESCRIPTOR.message_types_by_name['CompareRequest'] = _COMPAREREQUEST
DESCRIPTOR.message_types_by_name['CompareRequestSDF'] = _COMPAREREQUESTSDF
DESCRIPTOR.message_types_by_name['ComparisonResult'] = _COMPARISONRESULT
DESCRIPTOR.message_types_by_name['QuboMatrix'] = _QUBOMATRIX
DESCRIPTOR.message_types_by_name['BinaryPolynomial'] = _BINARYPOLYNOMIAL
DESCRIPTOR.message_types_by_name['Tabu1OptSolver'] = _TABU1OPTSOLVER
DESCRIPTOR.message_types_by_name['TabuSolverList'] = _TABUSOLVERLIST
DESCRIPTOR.message_types_by_name['MultiTabu1OptSolver'] = _MULTITABU1OPTSOLVER
DESCRIPTOR.message_types_by_name['PathRelinkingSolver'] = _PATHRELINKINGSOLVER
DESCRIPTOR.message_types_by_name['SQASolver'] = _SQASOLVER
DESCRIPTOR.message_types_by_name['PTICMSolver'] = _PTICMSOLVER
DESCRIPTOR.message_types_by_name['FujitsuDASolver'] = _FUJITSUDASOLVER
DESCRIPTOR.message_types_by_name['FujitsuDAMixedModeSolver'] = _FUJITSUDAMIXEDMODESOLVER
DESCRIPTOR.message_types_by_name['FujitsuDAPTSolver'] = _FUJITSUDAPTSOLVER
DESCRIPTOR.message_types_by_name['FujitsuDA2Solver'] = _FUJITSUDA2SOLVER
DESCRIPTOR.message_types_by_name['FujitsuDA2PTSolver'] = _FUJITSUDA2PTSOLVER
DESCRIPTOR.message_types_by_name['FujitsuDA2MixedModeSolver'] = _FUJITSUDA2MIXEDMODESOLVER
DESCRIPTOR.message_types_by_name['QuboRequest'] = _QUBOREQUEST
DESCRIPTOR.message_types_by_name['QuboSolution'] = _QUBOSOLUTION
DESCRIPTOR.message_types_by_name['SolverTiming'] = _SOLVERTIMING
DESCRIPTOR.message_types_by_name['QuboSolutionList'] = _QUBOSOLUTIONLIST
DESCRIPTOR.message_types_by_name['QuboResponse'] = _QUBORESPONSE
DESCRIPTOR.message_types_by_name['KnapsackRequest'] = _KNAPSACKREQUEST
DESCRIPTOR.message_types_by_name['KnapsackProblem'] = _KNAPSACKPROBLEM
DESCRIPTOR.message_types_by_name['KnapsackItem'] = _KNAPSACKITEM
DESCRIPTOR.message_types_by_name['KnapsackResponse'] = _KNAPSACKRESPONSE
DESCRIPTOR.message_types_by_name['KnapsackSolution'] = _KNAPSACKSOLUTION
DESCRIPTOR.message_types_by_name['KnapsackConfiguration'] = _KNAPSACKCONFIGURATION
DESCRIPTOR.message_types_by_name['MinKCutRequest'] = _MINKCUTREQUEST
DESCRIPTOR.message_types_by_name['Graph'] = _GRAPH
DESCRIPTOR.message_types_by_name['MinKCutResponse'] = _MINKCUTRESPONSE
DESCRIPTOR.message_types_by_name['MinKCutSolution'] = _MINKCUTSOLUTION
DESCRIPTOR.message_types_by_name['MinKCutMapping'] = _MINKCUTMAPPING
DESCRIPTOR.message_types_by_name['HealthCheckRequest'] = _HEALTHCHECKREQUEST
DESCRIPTOR.enum_types_by_name['sqa_energy_type'] = _SQA_ENERGY_TYPE
DESCRIPTOR.enum_types_by_name['sqa_schedule_type'] = _SQA_SCHEDULE_TYPE
DESCRIPTOR.enum_types_by_name['pticm_goal'] = _PTICM_GOAL
DESCRIPTOR.enum_types_by_name['pticm_scaling_type'] = _PTICM_SCALING_TYPE
DESCRIPTOR.enum_types_by_name['pticm_var_fixing_type'] = _PTICM_VAR_FIXING_TYPE
DESCRIPTOR.enum_types_by_name['fuj_noise_model'] = _FUJ_NOISE_MODEL
DESCRIPTOR.enum_types_by_name['fuj_temp_mode'] = _FUJ_TEMP_MODE
DESCRIPTOR.enum_types_by_name['fuj_sol_mode'] = _FUJ_SOL_MODE
DESCRIPTOR.enum_types_by_name['fuj_scaling_mode'] = _FUJ_SCALING_MODE
DESCRIPTOR.enum_types_by_name['runType'] = _RUNTYPE
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
CompareRequest = _reflection.GeneratedProtocolMessageType('CompareRequest', (_message.Message,), dict(DESCRIPTOR=_COMPAREREQUEST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(CompareRequest)
CompareRequestSDF = _reflection.GeneratedProtocolMessageType('CompareRequestSDF', (_message.Message,), dict(DESCRIPTOR=_COMPAREREQUESTSDF, __module__='qbit_pb2'))
_sym_db.RegisterMessage(CompareRequestSDF)
ComparisonResult = _reflection.GeneratedProtocolMessageType('ComparisonResult', (_message.Message,), dict(DESCRIPTOR=_COMPARISONRESULT, __module__='qbit_pb2'))
_sym_db.RegisterMessage(ComparisonResult)
QuboMatrix = _reflection.GeneratedProtocolMessageType('QuboMatrix', (_message.Message,), dict(QuboArray=_reflection.GeneratedProtocolMessageType('QuboArray', (_message.Message,), dict(DESCRIPTOR=_QUBOMATRIX_QUBOARRAY, __module__='qbit_pb2')), DESCRIPTOR=_QUBOMATRIX, __module__='qbit_pb2'))
_sym_db.RegisterMessage(QuboMatrix)
_sym_db.RegisterMessage(QuboMatrix.QuboArray)
BinaryPolynomial = _reflection.GeneratedProtocolMessageType('BinaryPolynomial', (_message.Message,), dict(Term=_reflection.GeneratedProtocolMessageType('Term', (_message.Message,), dict(DESCRIPTOR=_BINARYPOLYNOMIAL_TERM, __module__='qbit_pb2')), DESCRIPTOR=_BINARYPOLYNOMIAL, __module__='qbit_pb2'))
_sym_db.RegisterMessage(BinaryPolynomial)
_sym_db.RegisterMessage(BinaryPolynomial.Term)
Tabu1OptSolver = _reflection.GeneratedProtocolMessageType('Tabu1OptSolver', (_message.Message,), dict(DESCRIPTOR=_TABU1OPTSOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(Tabu1OptSolver)
TabuSolverList = _reflection.GeneratedProtocolMessageType('TabuSolverList', (_message.Message,), dict(DESCRIPTOR=_TABUSOLVERLIST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(TabuSolverList)
MultiTabu1OptSolver = _reflection.GeneratedProtocolMessageType('MultiTabu1OptSolver', (_message.Message,), dict(DESCRIPTOR=_MULTITABU1OPTSOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(MultiTabu1OptSolver)
PathRelinkingSolver = _reflection.GeneratedProtocolMessageType('PathRelinkingSolver', (_message.Message,), dict(DESCRIPTOR=_PATHRELINKINGSOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(PathRelinkingSolver)
SQASolver = _reflection.GeneratedProtocolMessageType('SQASolver', (_message.Message,), dict(DESCRIPTOR=_SQASOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(SQASolver)
PTICMSolver = _reflection.GeneratedProtocolMessageType('PTICMSolver', (_message.Message,), dict(DESCRIPTOR=_PTICMSOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(PTICMSolver)
FujitsuDASolver = _reflection.GeneratedProtocolMessageType('FujitsuDASolver', (_message.Message,), dict(GuidanceConfigEntry=_reflection.GeneratedProtocolMessageType('GuidanceConfigEntry', (_message.Message,), dict(DESCRIPTOR=_FUJITSUDASOLVER_GUIDANCECONFIGENTRY, __module__='qbit_pb2')), DESCRIPTOR=_FUJITSUDASOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(FujitsuDASolver)
_sym_db.RegisterMessage(FujitsuDASolver.GuidanceConfigEntry)
FujitsuDAMixedModeSolver = _reflection.GeneratedProtocolMessageType('FujitsuDAMixedModeSolver', (_message.Message,), dict(GuidanceConfigEntry=_reflection.GeneratedProtocolMessageType('GuidanceConfigEntry', (_message.Message,), dict(DESCRIPTOR=_FUJITSUDAMIXEDMODESOLVER_GUIDANCECONFIGENTRY, __module__='qbit_pb2')), DESCRIPTOR=_FUJITSUDAMIXEDMODESOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(FujitsuDAMixedModeSolver)
_sym_db.RegisterMessage(FujitsuDAMixedModeSolver.GuidanceConfigEntry)
FujitsuDAPTSolver = _reflection.GeneratedProtocolMessageType('FujitsuDAPTSolver', (_message.Message,), dict(GuidanceConfigEntry=_reflection.GeneratedProtocolMessageType('GuidanceConfigEntry', (_message.Message,), dict(DESCRIPTOR=_FUJITSUDAPTSOLVER_GUIDANCECONFIGENTRY, __module__='qbit_pb2')), DESCRIPTOR=_FUJITSUDAPTSOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(FujitsuDAPTSolver)
_sym_db.RegisterMessage(FujitsuDAPTSolver.GuidanceConfigEntry)
FujitsuDA2Solver = _reflection.GeneratedProtocolMessageType('FujitsuDA2Solver', (_message.Message,), dict(GuidanceConfigEntry=_reflection.GeneratedProtocolMessageType('GuidanceConfigEntry', (_message.Message,), dict(DESCRIPTOR=_FUJITSUDA2SOLVER_GUIDANCECONFIGENTRY, __module__='qbit_pb2')), DESCRIPTOR=_FUJITSUDA2SOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(FujitsuDA2Solver)
_sym_db.RegisterMessage(FujitsuDA2Solver.GuidanceConfigEntry)
FujitsuDA2PTSolver = _reflection.GeneratedProtocolMessageType('FujitsuDA2PTSolver', (_message.Message,), dict(GuidanceConfigEntry=_reflection.GeneratedProtocolMessageType('GuidanceConfigEntry', (_message.Message,), dict(DESCRIPTOR=_FUJITSUDA2PTSOLVER_GUIDANCECONFIGENTRY, __module__='qbit_pb2')), DESCRIPTOR=_FUJITSUDA2PTSOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(FujitsuDA2PTSolver)
_sym_db.RegisterMessage(FujitsuDA2PTSolver.GuidanceConfigEntry)
FujitsuDA2MixedModeSolver = _reflection.GeneratedProtocolMessageType('FujitsuDA2MixedModeSolver', (_message.Message,), dict(GuidanceConfigEntry=_reflection.GeneratedProtocolMessageType('GuidanceConfigEntry', (_message.Message,), dict(DESCRIPTOR=_FUJITSUDA2MIXEDMODESOLVER_GUIDANCECONFIGENTRY, __module__='qbit_pb2')), DESCRIPTOR=_FUJITSUDA2MIXEDMODESOLVER, __module__='qbit_pb2'))
_sym_db.RegisterMessage(FujitsuDA2MixedModeSolver)
_sym_db.RegisterMessage(FujitsuDA2MixedModeSolver.GuidanceConfigEntry)
QuboRequest = _reflection.GeneratedProtocolMessageType('QuboRequest', (_message.Message,), dict(DESCRIPTOR=_QUBOREQUEST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(QuboRequest)
QuboSolution = _reflection.GeneratedProtocolMessageType('QuboSolution', (_message.Message,), dict(ConfigurationEntry=_reflection.GeneratedProtocolMessageType('ConfigurationEntry', (_message.Message,), dict(DESCRIPTOR=_QUBOSOLUTION_CONFIGURATIONENTRY, __module__='qbit_pb2')), DESCRIPTOR=_QUBOSOLUTION, __module__='qbit_pb2'))
_sym_db.RegisterMessage(QuboSolution)
_sym_db.RegisterMessage(QuboSolution.ConfigurationEntry)
SolverTiming = _reflection.GeneratedProtocolMessageType('SolverTiming', (_message.Message,), dict(DetailedEntry=_reflection.GeneratedProtocolMessageType('DetailedEntry', (_message.Message,), dict(DESCRIPTOR=_SOLVERTIMING_DETAILEDENTRY, __module__='qbit_pb2')), DESCRIPTOR=_SOLVERTIMING, __module__='qbit_pb2'))
_sym_db.RegisterMessage(SolverTiming)
_sym_db.RegisterMessage(SolverTiming.DetailedEntry)
QuboSolutionList = _reflection.GeneratedProtocolMessageType('QuboSolutionList', (_message.Message,), dict(DESCRIPTOR=_QUBOSOLUTIONLIST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(QuboSolutionList)
QuboResponse = _reflection.GeneratedProtocolMessageType('QuboResponse', (_message.Message,), dict(SolverInputParametersEntry=_reflection.GeneratedProtocolMessageType('SolverInputParametersEntry', (_message.Message,), dict(DESCRIPTOR=_QUBORESPONSE_SOLVERINPUTPARAMETERSENTRY, __module__='qbit_pb2')), DESCRIPTOR=_QUBORESPONSE, __module__='qbit_pb2'))
_sym_db.RegisterMessage(QuboResponse)
_sym_db.RegisterMessage(QuboResponse.SolverInputParametersEntry)
KnapsackRequest = _reflection.GeneratedProtocolMessageType('KnapsackRequest', (_message.Message,), dict(DESCRIPTOR=_KNAPSACKREQUEST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(KnapsackRequest)
KnapsackProblem = _reflection.GeneratedProtocolMessageType('KnapsackProblem', (_message.Message,), dict(DESCRIPTOR=_KNAPSACKPROBLEM, __module__='qbit_pb2'))
_sym_db.RegisterMessage(KnapsackProblem)
KnapsackItem = _reflection.GeneratedProtocolMessageType('KnapsackItem', (_message.Message,), dict(DESCRIPTOR=_KNAPSACKITEM, __module__='qbit_pb2'))
_sym_db.RegisterMessage(KnapsackItem)
KnapsackResponse = _reflection.GeneratedProtocolMessageType('KnapsackResponse', (_message.Message,), dict(DESCRIPTOR=_KNAPSACKRESPONSE, __module__='qbit_pb2'))
_sym_db.RegisterMessage(KnapsackResponse)
KnapsackSolution = _reflection.GeneratedProtocolMessageType('KnapsackSolution', (_message.Message,), dict(DESCRIPTOR=_KNAPSACKSOLUTION, __module__='qbit_pb2'))
_sym_db.RegisterMessage(KnapsackSolution)
KnapsackConfiguration = _reflection.GeneratedProtocolMessageType('KnapsackConfiguration', (_message.Message,), dict(DESCRIPTOR=_KNAPSACKCONFIGURATION, __module__='qbit_pb2'))
_sym_db.RegisterMessage(KnapsackConfiguration)
MinKCutRequest = _reflection.GeneratedProtocolMessageType('MinKCutRequest', (_message.Message,), dict(DESCRIPTOR=_MINKCUTREQUEST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(MinKCutRequest)
Graph = _reflection.GeneratedProtocolMessageType('Graph', (_message.Message,), dict(DESCRIPTOR=_GRAPH, __module__='qbit_pb2'))
_sym_db.RegisterMessage(Graph)
MinKCutResponse = _reflection.GeneratedProtocolMessageType('MinKCutResponse', (_message.Message,), dict(DESCRIPTOR=_MINKCUTRESPONSE, __module__='qbit_pb2'))
_sym_db.RegisterMessage(MinKCutResponse)
MinKCutSolution = _reflection.GeneratedProtocolMessageType('MinKCutSolution', (_message.Message,), dict(DESCRIPTOR=_MINKCUTSOLUTION, __module__='qbit_pb2'))
_sym_db.RegisterMessage(MinKCutSolution)
MinKCutMapping = _reflection.GeneratedProtocolMessageType('MinKCutMapping', (_message.Message,), dict(DESCRIPTOR=_MINKCUTMAPPING, __module__='qbit_pb2'))
_sym_db.RegisterMessage(MinKCutMapping)
HealthCheckRequest = _reflection.GeneratedProtocolMessageType('HealthCheckRequest', (_message.Message,), dict(DESCRIPTOR=_HEALTHCHECKREQUEST, __module__='qbit_pb2'))
_sym_db.RegisterMessage(HealthCheckRequest)
_FUJITSUDASOLVER_GUIDANCECONFIGENTRY._options = None
_FUJITSUDAMIXEDMODESOLVER_GUIDANCECONFIGENTRY._options = None
_FUJITSUDAPTSOLVER_GUIDANCECONFIGENTRY._options = None
_FUJITSUDA2SOLVER_GUIDANCECONFIGENTRY._options = None
_FUJITSUDA2PTSOLVER_GUIDANCECONFIGENTRY._options = None
_FUJITSUDA2MIXEDMODESOLVER_GUIDANCECONFIGENTRY._options = None
_QUBOSOLUTION_CONFIGURATIONENTRY._options = None
_SOLVERTIMING_DETAILEDENTRY._options = None
_QUBORESPONSE_SOLVERINPUTPARAMETERSENTRY._options = None
_QBIT = _descriptor.ServiceDescriptor(name='Qbit', full_name='qbit.services.Qbit', file=DESCRIPTOR, index=0, serialized_options=None, serialized_start=9436, serialized_end=10543, methods=[
 _descriptor.MethodDescriptor(name='CompareMolecule', full_name='qbit.services.Qbit.CompareMolecule', index=0, containing_service=None, input_type=_COMPAREREQUEST, output_type=_COMPARISONRESULT, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x14"\x0f/v1/gms/compare:\x01*')),
 _descriptor.MethodDescriptor(name='CompareMoleculeBenchmark', full_name='qbit.services.Qbit.CompareMoleculeBenchmark', index=1, containing_service=None, input_type=_COMPAREREQUEST, output_type=_COMPARISONRESULT, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x19"\x14/v1/gms/comparebench:\x01*')),
 _descriptor.MethodDescriptor(name='Hobo2Qubo', full_name='qbit.services.Qbit.Hobo2Qubo', index=2, containing_service=None, input_type=_BINARYPOLYNOMIAL, output_type=_BINARYPOLYNOMIAL, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x17"\x12/v1/qubo/hobo2qubo:\x01*')),
 _descriptor.MethodDescriptor(name='SolveQubo', full_name='qbit.services.Qbit.SolveQubo', index=3, containing_service=None, input_type=_QUBOREQUEST, output_type=_QUBORESPONSE, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x13"\x0e/v1/qubo/solve:\x01*')),
 _descriptor.MethodDescriptor(name='SolveQuboFujitsuDA2', full_name='qbit.services.Qbit.SolveQuboFujitsuDA2', index=4, containing_service=None, input_type=_QUBOREQUEST, output_type=_QUBORESPONSE, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x1e"\x19/v1/qubo/solve/fujitsuda2:\x01*')),
 _descriptor.MethodDescriptor(name='SolveQuboFujitsuDA2PT', full_name='qbit.services.Qbit.SolveQuboFujitsuDA2PT', index=5, containing_service=None, input_type=_QUBOREQUEST, output_type=_QUBORESPONSE, serialized_options=_b(b'\x82\xd3\xe4\x93\x02 "\x1b/v1/qubo/solve/fujitsuda2pt:\x01*')),
 _descriptor.MethodDescriptor(name='Knapsack', full_name='qbit.services.Qbit.Knapsack', index=6, containing_service=None, input_type=_KNAPSACKREQUEST, output_type=_KNAPSACKRESPONSE, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x11"\x0c/v1/knapsack:\x01*')),
 _descriptor.MethodDescriptor(name='MinKCutPartitioning', full_name='qbit.services.Qbit.MinKCutPartitioning', index=7, containing_service=None, input_type=_MINKCUTREQUEST, output_type=_MINKCUTRESPONSE, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x1c"\x17/v1/MinKCutPartitioning:\x01*')),
 _descriptor.MethodDescriptor(name='HealthCheck', full_name='qbit.services.Qbit.HealthCheck', index=8, containing_service=None, input_type=_HEALTHCHECKREQUEST, output_type=google_dot_protobuf_dot_empty__pb2._EMPTY, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x11\x12\x0f/v1/healthcheck')),
 _descriptor.MethodDescriptor(name='AuthCheck', full_name='qbit.services.Qbit.AuthCheck', index=9, containing_service=None, input_type=_HEALTHCHECKREQUEST, output_type=google_dot_protobuf_dot_empty__pb2._EMPTY, serialized_options=_b(b'\x82\xd3\xe4\x93\x02\x0f\x12\r/v1/authcheck'))])
_sym_db.RegisterServiceDescriptor(_QBIT)
DESCRIPTOR.services_by_name['Qbit'] = _QBIT