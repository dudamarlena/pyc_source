# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ykent/GitLab/pygrisb/pygrisb/pygrisb/gutz/usrqa.py
# Compiled at: 2019-03-05 11:19:39
# Size of source mod 2**32: 3622 bytes
import sys, h5py

class usrqa(object):
    __doc__ = 'class to handle a list of questions for user input,\n    to guide the set up of gutzwiller calculation.\n    final results can also be stored in hdf5 file\n    to be referenced later.\n    '

    def __init__(self, material, log=sys.stdout, ginit_file='ginit.h5'):
        self.material = material
        self.log = log
        self.ginit_file = ginit_file
        self.done = False
        self.spin_polarization = 'n'
        self.orbital_polarization = 'n'
        self.spin_orbit_coup = 'n'
        self.crystal_field = 'n'
        self.u_matrix_type = 1
        self.dc_type = 12
        self.unique_u_list = []
        self.unique_f_list = []
        self.newton_type = 0
        self.embeddiag_type = -1

    def check_done_previously(self):
        with h5py.File('ginit.h5', 'r') as (f):
            if '/usrqa' in f:
                self.done = True

    def h5save_input(self):
        """save user inputs to hdf5 file to be referenced later.
        """
        with h5py.File(self.ginit_file, 'a') as (f):
            f['/usrqa/dist_cut'] = self.dist_cut
            f['/usrqa/unit'] = self.unit
            f['/usrqa/spin_polarization'] = self.spin_polarization
            f['/usrqa/full_orbital_polarization'] = self.orbital_polarization
            f['/usrqa/spin_orbit_coup'] = self.spin_orbit_coup
            f['/usrqa/crystal_field'] = self.crystal_field
            f['/usrqa/u_matrix_type'] = self.u_matrix_type
            f['/usrqa/ldc'] = self.dc_type
            f['/usrqa/idx_equivalent_atoms'] = self.idx_equivalent_atoms
            f['/usrqa/unique_corr_symbol_list'] = self.unique_corr_symbol_list
            f['/usrqa/unique_df_list'] = [df.encode() for df in self.unique_df_list]
            if len(self.unique_u_list) > 0:
                f['/usrqa/unique_u_list_ev'] = self.unique_u_list
                f['/usrqa/unique_j_list_ev'] = self.unique_j_list
            if len(self.unique_f_list) > 0:
                f['/usrqa/unique_f_list_ev'] = self.unique_f_list
            if self.dc_type == 2:
                f['/usrqa/unique_nf_list'] = self.unique_nf_list
            f['/usrqa/lnewton'] = self.newton_type
            f['/usrqa/iembeddiag'] = self.embeddiag_type


def get_usr_input(message, accept_list):
    while True:
        answer = input(message + ' \n Pick one from [' + ', '.join((item for item in accept_list)) + ']...')
        if answer not in accept_list:
            print(' Please pick an answer in the list! Make your choice again.')
        else:
            break

    return answer


def get_usr_input_combo(message, accept_list):
    while 1:
        answer = input(message + ' \n Pick one or combinations separated by blank space' + ' \n from [' + ', '.join((item for item in accept_list)) + ']...')
        if answer_valid(answer, accept_list):
            break

    return answer


def answer_valid(answer, accept_list):
    answer_list = answer.split()
    for ans in answer_list:
        if ans not in accept_list:
            return False

    return True