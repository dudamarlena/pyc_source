# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/gutz/init.py
# Compiled at: 2019-02-26 10:13:54
# Size of source mod 2**32: 2499 bytes
import sys
import pygrisb.gutz.init_magnet_conf as init_magnet_conf

def initialize():
    """
    Initialization for the Gutzwiller-Slave-Boson solver.
    Store all the relevant information in GPARAM.5 file.
    """
    log_file = open('init_ga.slog', 'w')
    print(' The executed commant line is:', file=log_file)
    print(('    ' + ' '.join(sys.argv[:])), file=log_file)
    from pygrisb.gutz.structure import get_gatoms, check_material
    from pygrisb.gutz.gatom import h5calc_save_lrot
    material = get_gatoms()
    material.set_modify_mode()
    from pygrisb.gutz.usrqa import h5save_usr_qa_setup
    h5save_usr_qa_setup(material, log=log_file)
    material.h5set()
    material.set_SelfEnergy()
    material.set_LieParameters()
    material.set_one_particle_rotation_list()
    material.set_v2e_list()
    material.set_SL_vector_list()
    check_material(material, log_file)
    from pygrisb.gutz.ginput import save_gparam
    save_gparam(iso=(material.iso), ispin=(material.ispin), ityp_list=(material.ityp_list),
      imap_list=(material.imap_list),
      na2_list=(material.na2_list),
      imix=(material.gimix),
      iembeddiag=(material.giembeddiag),
      sigma_list=(material.sigma_list),
      v2e_list=(material.v2e_list),
      sx_list=(material.sx_list),
      sy_list=(material.sy_list),
      sz_list=(material.sz_list),
      lx_list=(material.lx_list),
      ly_list=(material.ly_list),
      lz_list=(material.lz_list),
      utrans_list=(material.utrans_list),
      ldc=(material.ldc),
      u_avg_list=(material.u_avg_list),
      j_avg_list=(material.j_avg_list),
      nelf_list=(material.nelf_list),
      rotations_list=(material.rotations_list),
      lie_odd_params_list=(material.Lie_Jodd_list),
      lie_even_params_list=(material.Lie_Jeven_list),
      jgenerator_list=(material.jgenerator_list),
      sp_rotations_list=(material.sp_rotations_list),
      nval_bot_list=(material.nval_bot_list),
      nval_top_list=(material.nval_top_list))
    h5calc_save_lrot(material)
    log_file.close()


if __name__ == '__main__':
    initialize()