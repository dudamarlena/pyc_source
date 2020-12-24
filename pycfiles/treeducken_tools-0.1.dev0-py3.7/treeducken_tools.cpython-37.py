# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/treeducken_tools/treeducken_tools.py
# Compiled at: 2019-09-09 16:05:39
# Size of source mod 2**32: 7789 bytes
import os, subprocess, math

def install_treeducken(path_to_install_dir):
    check_name = path_to_install_dir
    check_install = False
    git_repo = 'http://github.com/wadedismukes/treeducken.git'
    install_cmd = ['make', 'install']
    if not os.path.exists(check_name):
        subprocess.call(['git', 'clone', '--depth=1', git_repo, check_name])
    os.chdir(check_name + 'src/')
    install_process = subprocess.Popen(install_cmd, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
    out, err = install_process.communicate()
    errcode = install_process.returncode
    treeducken_exe = 'treeducken'
    check_install = os.path.isfile(treeducken_exe)
    return check_install


def choose(n, k):
    """
    A fast way to calculate binomial coefficients by Andrew Dalke (contrib).
    """
    if 0 <= k <= n:
        ntok = 1
        ktok = 1
        for t in range(1, min(k, n - k) + 1):
            ntok *= n
            ktok *= t
            n -= 1

        return ntok // ktok
    return 0


def calculate_expected_birth_rate(number_taxa, k, rel_ext, tre_dep):
    if rel_ext != 0:
        sum_val_i = 0.0
        sum_val_j = 0.0
        br = (k + 1) / tre_dep * choose(number_taxa, k + 1) * (-1) ** k
        for i in range(0, number_taxa - k - 1):
            temp = choose(number_taxa - k - 1, i)
            temp *= 1 / ((k + i + 1) * rel_ext)
            temp *= (1 / rel_ext - 1) ** (k + i)
            for j in range(1, k + i + 1):
                temp_j = choose(k + i, j)
                temp_j *= (-1) ** j / j
                temp_j *= 1 - (1 / (1 - rel_ext)) ** j
                sum_val_j += temp_j

            sum_val_i += temp * (math.log(1 / (1 - rel_ext)) - sum_val_j)

        br *= sum_val_i
    else:
        sum_val = 0.0
        for i in range(k + 1, number_taxa + 1):
            sum_val += 1 / (i * tre_dep)

        br = abs(2.0 * sum_val)
    return br


def calculate_expected_pbtree_length(lamda, ntips, k=1):
    exp_tree_length = 0
    for i in range(k + 1, ntips):
        exp_tree_length = exp_tree_length + (lamda * i) ** (-1)

    return exp_tree_length


def calculate_expected_bdtree_length(birth_rate, death_rate, ntips, k=1):
    if death_rate > 0.0001 and death_rate != birth_rate:
        rho = death_rate / birth_rate
        outer_prod = (k + 1) / birth_rate * choose(ntips, k + 1) * (-1) ** k
        outer_sum = 0
        ntips_for_loop_indx = ntips - k - 1
        for i in range(0, ntips_for_loop_indx + 1):
            index = k + i
            sum_terms = choose(ntips_for_loop_indx, i) * (1 / (rho * (k + i + 1))) * (1 / rho - 1) ** index
            inner_sum = 0
            for j in range(1, index + 1):
                inner_sum_terms = choose(index, j) * (1 / j) * (-1) ** j * (1 - (1 / (1 - rho)) ** j)
                inner_sum += inner_sum_terms

            sum_terms *= math.log(1 / (1 - rho)) - inner_sum
            outer_sum += sum_terms

        exp_tree_length = outer_sum * outer_prod
    else:
        if death_rate > 0.0001 and death_rate == birth_rate:
            exp_tree_length = (ntips - k) / (birth_rate * k)
        else:
            exp_tree_length = calculate_expected_pbtree_length(birth_rate, ntips)
    return exp_tree_length


def calculate_expected_time_spec_event(b_rate, d_rate, ntips, k):
    return calculate_expected_bdtree_length(b_rate, d_rate, ntips, k)


def write_settings_file(settings_dict, settings_file_prefix):
    settings_fn = settings_file_prefix + '_settings.txt'
    with open(settings_fn, 'w') as (f):
        for setting in settings_dict:
            print(setting, (settings_dict[setting]), file=f)


def create_settings_dictionary(sbr, sdr, ntax, reps, gbr=0.0, gdr=0.0, lgtr=0.0, num_loci=1, ipp=1, ne=1, num_genes=1, ofn='', screen_out=0, sd1=0, sd2=0):
    sett_dict = {'-r':reps, 
     '-sbr':sbr, 
     '-sdr':sdr, 
     '-nt':ntax, 
     '-gdr':gdr, 
     '-gbr':gbr, 
     '-nl':num_loci, 
     '-lgtr':lgtr, 
     '-ng':num_genes, 
     '-ipp':ipp, 
     '-sout':screen_out, 
     '-ne':ne, 
     '-o':ofn, 
     '-sd1':sd1, 
     '-sd2':sd2}
    return sett_dict


def run_treeducken_simulation(path_to_exe, settings_filename, data_dir):
    subprocess.call([path_to_exe + 'treeducken', '-i', settings_filename], shell=True)


def run_seqgen(model, seq_length, newick_tree, output_file='sequences.dat', of_format='p', num_reps=1, scale_brlen=0.0, scale_tree=0.0, gamma_rate_het=0.0, gamma_cats=1, prop_invariant=0.0, rel_state_freq=None, tstv_ratio=0.5, gtr_mat=None, rng_seed=None):
    line_write = 'seq-gen '
    if model in ('GTR', 'HKY', 'F84'):
        line_write += '-m' + model
    else:
        throw_seqgen_error()
    line_write += ' -l' + str(seq_length)
    if of_format in ('r', 'p', 'n'):
        line_write += ' -p' + of_format
    else:
        throw_seqgen_error()
    line_write += ' -n' + str(num_reps)
    if scale_brlen > 0.0:
        line_write += ' -s' + str(scale_brlen)
    else:
        if scale_brlen == 0.0:
            pass
        else:
            throw_seqgen_error()
        if scale_tree > 0:
            line_write += ' -d' + str(scale_tree)
        else:
            if scale_tree == 0.0:
                pass
            else:
                throw_seqgen_error()
            if gamma_rate_het > 0.0:
                line_write += ' -g' + str(gamma_rate_het)
            else:
                if gamma_rate_het == 0.0:
                    pass
                else:
                    throw_seqgen_error()
                if gamma_cats > 0:
                    line_write += ' -g' + str(gamma_cats)
                else:
                    if gamma_cats == 0:
                        pass
                    else:
                        throw_seqgen_error()
                    if prop_invariant > 0.0:
                        line_write += ' -i' + str(prop_invariant)
                    else:
                        if prop_invariant == 0.0:
                            pass
                        else:
                            throw_seqgen_error()
                        if rel_state_freq is not None:
                            if sum(rel_state_freq) != 1:
                                throw_seqgen_error()
                            else:
                                line_write += '-f' + ','.join(str(rel_state_freq))
                        else:
                            line_write += ' -fe'
                        if tstv_ratio > 0.0:
                            line_write += ' -t' + str(tstv_ratio)
                        else:
                            throw_seqgen_error()
                        if gtr_mat is not None:
                            if model is 'GTR':
                                line_write += ' -r' + ','.join(str(gtr_mat))
                        if rng_seed is not None:
                            if rng_seed.is_integer():
                                line_write += ' -z' + str(rng_seed)
                            else:
                                throw_seqgen_error()
                        line_write += ' ' + str(newick_tree) + ' ' + output_file
                        cmd = line_write
                        proc = subprocess.Popen(cmd, stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
                        o, e = proc.communicate()
                        print('Output: ' + o.decode('ascii'))
                        print('Error: ' + e.decode('ascii'))
                        print('code: ' + str(proc.returncode))


def throw_seqgen_error():
    print('It appears that you input one of the Seq-Gen parameters\n')
    print('Incorrectly, please check the Seq-Gen manual for more info!\n')