# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/zimpute/zsh.py
# Compiled at: 2020-02-05 06:22:07
# Size of source mod 2**32: 26908 bytes
"""
Created on Wed Nov  6 17:11:23 2019

@author: sihanzhou
"""
import numpy as np
from scipy.fftpack import dctn, idctn
import time, re, math, argparse
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from sklearn.manifold import TSNE
from sklearn import metrics
from sklearn.decomposition import PCA
import random

def Command():
    args = argparse.ArgumentParser(description='======A scRNA imputation method base on low rank complemetion =====', epilog='==============end============ ')
    args.add_argument('infile', type=str, help='the path of inputfile')
    args.add_argument('outfile', type=str, help='the path of outputfile')
    args.add_argument('-r', '--rank', type=int, dest='rank', help='the rank', default=1)
    args.add_argument('-l', '--lambda', type=float, dest='Lambda', help='lambda', default=0.01, choices=[1000, 100, 10, 1, 0.1, 0.01, 0.0001])
    args.add_argument('-f', '--filter', type=str, dest='filter', help='filtering the datamatrix', default='F', choices=['T', 'F'])
    args.add_argument('-n', '--norm', type=str, dest='normalize', help='normalizing the datamatrix', default='F', choices=['T', 'F'])
    args = args.parse_args()
    return args


def Load_Matrix(infile_path):
    path = infile_path
    if re.match('.+\\.csv', infile_path, flags=0) != None:
        print('the format of input file is .csv')
        Data_matrix_M = np.loadtxt((open(path, 'rb')), delimiter=',', skiprows=0)
    else:
        if re.match('.+\\.tsv', infile_path, flags=0) != None:
            print('the format of input file is .tsv')
            Data_matrix_M = np.loadtxt((open(path, 'rb')), delimiter='\t', skiprows=0)
        else:
            print('the format of input file is error')
    Data_matrix_M = Data_matrix_M.transpose(1, 0)
    print('Load the data matrix...')
    return Data_matrix_M


def Data_Filtering(Data_matrix_M):
    m = Data_matrix_M.shape[0]
    n = Data_matrix_M.shape[1]
    Delete_genes = []
    Min_expression_value = 3
    Min_expression_cells = 3
    for j in range(0, n):
        gene_expression_times = 0
        for i in range(0, m):
            if Data_matrix_M[i][j] >= Min_expression_value:
                gene_expression_times += 1

        if gene_expression_times < Min_expression_cells:
            Delete_genes.append(j)

    M_Filtering = np.delete(Data_matrix_M, Delete_genes, axis=1)
    print('Data filtering...')
    return (
     M_Filtering, Delete_genes)


def Data_Normlization(Filtering_M):
    m = Filtering_M.shape[0]
    n = Filtering_M.shape[1]
    Row_sum_list = []
    Row_sum_list_1 = []
    for i in range(0, m):
        Row_sum = 0
        for j in range(0, n):
            Row_sum = Row_sum + Filtering_M[i][j]

        Row_sum_list.append(Row_sum)
        Row_sum_list_1.append(Row_sum)

    Row_sum_list_1.sort()
    half = len(Row_sum_list_1) // 2
    Row_median = (Row_sum_list_1[half] + Row_sum_list_1[(~half)]) / 2
    for i in range(0, m):
        for j in range(0, n):
            if Row_sum_list[i] != 0:
                Filtering_M[i][j] = Filtering_M[i][j] * Row_median / Row_sum_list[i]

    M_Normlization = Filtering_M
    del Filtering_M
    for i in range(0, m):
        for j in range(0, n):
            M_Normlization[i][j] = math.log2(M_Normlization[i][j] + 1)

    print('Data normlization...')
    return (
     M_Normlization, Row_median, Row_sum_list)


def Select_r(Data_matrix_M):
    u, sigma_list, v_T = np.linalg.svd(Data_matrix_M, full_matrices=False)
    sigma_sum = 0
    for i in range(0, len(sigma_list)):
        sigma_sum = sigma_sum + pow(sigma_list[i], 2)

    total = 0
    j = 0
    while 1:
        total = total + pow(sigma_list[j], 2)
        j += 1
        if total > 0.9 * sigma_sum:
            break

    r = j
    return r


def Truncated_QR(X, r):
    Error = 1e-06
    Itmax = 10
    m, n = np.shape(X)
    L = np.eye(m, r)
    S = np.eye(r, r)
    R = np.eye(r, n)
    k = 1
    while 1:
        Q, D = np.linalg.qr(np.dot(X, R.T))
        L = Q[:, :r]
        Q, D = np.linalg.qr(np.dot(X.T, L))
        R = np.transpose(Q)
        D = np.transpose(np.dot(L.T, np.dot(X, Q)))
        S = np.transpose(D[:r, :r])
        k = k + 1
        val = np.linalg.norm(np.dot(L, np.dot(S, R)) - X, 'fro')
        if pow(val, 2) < Error or k > Itmax:
            break

    return (
     L, S, R)


def Impute(M, r=1, lamda=0.01, F_flag='F', N_flag='F'):
    start = time.perf_counter()
    if F_flag == 'T':
        M, dl = Data_Filtering(M)
    if N_flag == 'T':
        M, sum_median, row_sum_list = Data_Normlization(M)
    m, n = np.shape(M)
    X = M
    mu = 1.0 / np.linalg.norm(M, 2)
    Omega = np.count_nonzero(M)
    fraion = float(Omega) / (m * n)
    rho = 1.2 + 1.8 * fraion
    print('Imputation...')
    MAX_ITER = 200
    m, n = np.shape(M)
    W = X
    Y = np.zeros((m, n))
    Z = Y
    E = np.random.random((m, n))
    error = pow(10, -5)
    for k in range(0, MAX_ITER):
        A, sigma, B = Truncated_QR(X, r)
        AB = np.dot(A, B)
        tem = 0.5 * (W - Y / mu + idctn((E + Z / mu), norm='ortho'))
        lastX = X
        u, sigma, v = np.linalg.svd(tem, full_matrices=0)
        ss = sigma - 1 / mu / 2
        s2 = np.clip(ss, 0, max(ss))
        X = np.dot(u, np.dot(np.diag(s2, k=0), v))
        if np.linalg.norm(X - lastX, 'fro') / np.linalg.norm(M, 'fro') < error:
            break
        lastW = W
        W = (AB + Y + mu * X) / mu
        M_observed = np.float64(M > 0)
        M_noobserved = np.ones((m, n)) - M_observed
        W = W * M_noobserved + M * M_observed
        if np.linalg.norm(W - lastW, 'fro') / np.linalg.norm(M, 'fro') < error:
            break
        temp = dctn(X, norm='ortho') - Z / mu
        d_i = []
        for i in range(0, m):
            row_L2_norm = np.linalg.norm((temp[i]), ord=2, keepdims=False)
            if row_L2_norm > lamda / mu:
                d_i.append((row_L2_norm - lamda / mu) / row_L2_norm)
            else:
                d_i.append(0)

        D = np.diag(d_i, k=0)
        E = np.dot(D, temp)
        if np.linalg.norm(X - W, 'fro') / np.linalg.norm(M, 'fro') < error:
            break
        Y = Y + mu * (X - W)
        Z = Z + mu * (E - dctn(X, norm='ortho'))
        val = mu * max(np.linalg.norm(X - lastX, 'fro'), np.linalg.norm(W - lastW, 'fro')) / np.linalg.norm(M, 'fro')
        if val < pow(10, -3):
            mu = rho * mu
        mu = min(mu, pow(10, 10))

    if N_flag == 'T':
        for i in range(0, W.shape[0]):
            for j in range(0, W.shape[1]):
                W[i][j] = (pow(2, W[i][j]) - 1) / sum_median * row_sum_list[i]

    W_nonzero = np.float64(W > 0.5)
    W = W * W_nonzero
    end = time.perf_counter()
    print('Running time: %s Seconds' % (end - start))
    return W


def Save_result(outfile_path, W):
    path = outfile_path
    if re.match('.+\\.csv', path, flags=0) != None:
        np.savetxt(path, (W.T), delimiter=',')
        print('saving result as .csv at' + str(path))
    else:
        if re.match('.+\\.tsv', path, flags=0) != None:
            np.savetxt(path, (W.T), delimiter='\t')
            print('saving result as .tsv at' + str(path))
        else:
            print('the format of input file is error')


def Example_lambda_pic():
    font3 = {'family':'Times New Roman', 
     'weight':'normal', 
     'size':11}
    x = [
     1, 2, 10, 70, 150, 300]
    lamda1 = [
     0.124, 0.124, 0.126, 0.1263, 0.1265, 0.1269]
    lamda2 = [
     0.11, 0.112, 0.113, 0.115, 0.117, 0.152]
    lamda3 = [
     0.1012, 0.1018, 0.1081, 0.109, 0.11, 0.24]
    lamda4 = [
     0.1014, 0.1021, 0.1105, 0.1106, 0.12, 0.3]
    plt.plot(x, lamda1, marker='>', ms=4, label='λ=1')
    plt.plot(x, lamda2, marker='d', ms=4, label='λ=0.1')
    plt.plot(x, lamda3, marker='^', ms=4, label='λ=0.01')
    plt.plot(x, lamda4, marker='X', ms=4, label='λ=0.001')
    plt.legend()
    plt.margins(0)
    plt.subplots_adjust(bottom=0.1)
    plt.xlabel('r', font3)
    plt.ylabel('Relative error', font3)
    plt.xlim(1, 300)
    plt.title('The relative error with different lambda')
    plt.show()


def Example_mu_pic():
    font3 = {'family':'Times New Roman', 
     'weight':'normal', 
     'size':11}
    x = [
     1, 2, 10, 70, 150, 300, 500]
    mu1 = [
     0.4544, 0.4548, 0.4553, 0.4561, 0.4563, 0.4563, 0.4563]
    mu2 = [
     0.4289, 0.4292, 0.4305, 0.4315, 0.4317, 0.4318, 0.4329]
    mu3 = [
     0.3345, 0.3356, 0.3397, 0.3418, 0.3507, 0.3525, 0.3584]
    mu4 = [
     0.1059, 0.1104, 0.1134, 0.1135, 0.1217, 0.1353, 0.1652]
    plt.plot(x, mu1, marker='>', ms=3, label=' μ=0.1')
    plt.plot(x, mu2, marker='d', ms=3, label=' μ=0.01')
    plt.plot(x, mu3, marker='^', ms=3, label=' μ=0.001')
    plt.plot(x, mu4, marker='X', ms=3, label=' μ=0.0001')
    plt.legend()
    plt.margins(0)
    plt.subplots_adjust(bottom=0.1)
    plt.xlabel('r', font3)
    plt.ylabel('Relative error', font3)
    plt.xlim(1, 500)
    plt.ylim(0, 0.7)
    plt.xticks([10, 70, 150, 300, 500])
    plt.title('The relative error with different μ')
    plt.show()


def Relative_error(M_pred, M_obes):
    relative_error = np.linalg.norm(M_pred - M_obes, 'fro') / np.linalg.norm(M_obes, 'fro')
    return relative_error


def tSNE_Visualize(Matrix_raw, Matrix_impute, Target_group, celltype_list, n_components=2):
    font1 = {'family':'Times New Roman', 
     'weight':'normal', 
     'size':11}
    raw, m, l = Data_Normlization(Matrix_raw)
    zim, m, l = Data_Normlization(Matrix_impute)
    estimator = PCA(n_components=n_components)
    raw = estimator.fit_transform(raw)
    estimator = PCA(n_components=n_components)
    zim = estimator.fit_transform(zim)
    X_raw = TSNE(n_components=2, early_exaggeration=12, learning_rate=200, n_iter=2000).fit_transform(raw)
    X_zim = TSNE(n_components=2, early_exaggeration=12, learning_rate=200, n_iter=2000).fit_transform(zim)
    color = [
     'skyblue', 'mediumaquamarine', 'lightseagreen',
     'goldenrod', 'mediumslateblue', 'mediumseagreen',
     'hotpink', 'darkkhaki', 'violet', 'lightcoral',
     'green', 'red', 'yellow', 'black', 'pink', 'blue',
     'skyblue', 'orange', 'lavender', 'lavenderblush',
     'lawngreen', 'lemonchiffon', 'lightblue', 'lightcoral',
     'lightcyan', 'lightgoldenrodyellow', 'lightgreen',
     'lightgray', 'lightpink', 'lightsalmon', 'lightseagreen',
     'lightskyblue', 'lightslategray', 'lightsteelblue',
     'lightyellow', 'lime']
    fig, (ax1, ax2, ax3) = plt.subplots(nrows=1, ncols=3, figsize=(8, 3))
    for i in range(0, X_raw.shape[0]):
        ax1.scatter((X_raw[(i, 0)]), (X_raw[(i, 1)]), s=10, c=(color[int(Target_group[i])]))

    for i in range(0, X_zim.shape[0]):
        ax2.scatter((X_zim[(i, 0)]), (X_zim[(i, 1)]), s=10, c=(color[int(Target_group[i])]))

    s1 = metrics.silhouette_score(X_raw, Target_group, metric='euclidean')
    s2 = metrics.silhouette_score(X_zim, Target_group, metric='euclidean')
    ax1.set_xlabel('tSNE1', size=10)
    ax1.set_ylabel('tSNE2', size=10)
    ax1.set_title('Raw:' + str(round(s1, 3)), font1)
    ax2.set_xlabel('tSNE1', size=10)
    ax2.set_ylabel('tSNE2', size=10)
    ax2.set_title('zimpute:' + str(round(s2, 3)), font1)
    ax3.remove()
    patches = [mpatches.Patch(color=(color[i]), label=('{:s}'.format(celltype_list[i]))) for i in range(0, len(celltype_list))]
    plt.legend(handles=patches, bbox_to_anchor=(1.9, 0.85), ncol=1, prop={'size': 10})
    fig.subplots_adjust(hspace=0.38, wspace=0.38)
    plt.show()


def Example_sigma_pic(Matrix):
    font3 = {'family':'Times New Roman', 
     'weight':'normal', 
     'size':13}
    u, sigma, v = np.linalg.svd(Matrix, full_matrices=False)

    def formatnum1(x, pos):
        return '$%.1f$x$10^{6}$' % (x / max(10000))

    plt.plot((range(1, len(sigma) + 1)), sigma, c='sandybrown', lw=2)
    plt.xlabel('The numbers of singular value', size=12)
    plt.ylabel('The singular value', size=12)
    plt.title('The trend of singular value', font3)
    plt.show()


def Sample(M, sample_rate):
    num = M.shape[0] * M.shape[1]
    zeros = int(num * sample_rate)
    ones = num - zeros
    s = [
     0] * zeros + [1] * ones
    random.shuffle(s)
    ss = np.array(s)
    result = ss.reshape(M.shape[0], M.shape[1])
    result = M * result
    return result


def Show_error_plot():
    font2 = {'family':'times New Roman', 
     'weight':'normal', 
     'size':12}
    dropout_rates = np.array([10, 30, 50, 70])
    dropout_1_error = np.array([0.0785, 0.2044, 0.4677, 0.794])
    zimpute_1_error = np.array([0.0256, 0.0545, 0.1029, 0.1868])
    scimpute_1_error = np.array([0.0485, 0.1223, 0.3098, 0.7188])
    SAVER_1_error = np.array([0.2014, 0.2819, 0.5131, 0.8253])
    MAGIC_1_error = np.array([0.2158, 0.2318, 0.3662, 0.7152])
    ls = '-'
    fig, ax = plt.subplots(nrows=2, ncols=2, figsize=(8, 8))
    ax[(0, 0)].plot(dropout_rates, zimpute_1_error, marker='^', linestyle=ls, label='zimpute')
    ax[(0, 0)].plot(dropout_rates, scimpute_1_error, marker='1', linestyle=ls, label='scimpute')
    ax[(0, 0)].plot(dropout_rates, SAVER_1_error, marker='s', linestyle=ls, label='SAVER')
    ax[(0, 0)].plot(dropout_rates, MAGIC_1_error, marker='x', linestyle=ls, label='MAGIC')
    ax[(0, 0)].plot(dropout_rates, dropout_1_error, marker='2', linestyle=ls, label='dropout')
    ax[(0, 0)].set_xlabel('Dropout rate', size=11)
    ax[(0, 0)].set_ylabel('Relative error', size=11)
    ax[(0, 0)].set_title('mn=2xe5', font2)
    ax[(0, 0)].legend(loc=6, bbox_to_anchor=(0.01, 0.78), prop={'size': 9})
    ax[(0, 0)].set_ylim((0, 1))
    ax[(0, 0)].set_xlim((10, 70))
    dropout_2_error = np.array([0.085, 0.2061, 0.4594, 0.7864])
    zimpute_2_error = np.array([0.0275, 0.0546, 0.1046, 0.1942])
    scimpute_2_error = np.array([0.0595, 0.155, 0.347, 0.7668])
    SAVER_2_error = np.array([0.2245, 0.2999, 0.5142, 0.8174])
    MAGIC_2_error = np.array([0.1997, 0.2232, 0.3793, 0.7238])
    ax[(0, 1)].plot(dropout_rates, zimpute_2_error, marker='^', linestyle=ls, label='zimpute')
    ax[(0, 1)].plot(dropout_rates, scimpute_2_error, marker='1', linestyle=ls, label='scimpute')
    ax[(0, 1)].plot(dropout_rates, SAVER_2_error, marker='s', linestyle=ls, label='SAVER')
    ax[(0, 1)].plot(dropout_rates, MAGIC_2_error, marker='x', linestyle=ls, label='MAGIC')
    ax[(0, 1)].plot(dropout_rates, dropout_2_error, marker='2', linestyle=ls, label='dropout')
    ax[(0, 1)].set_xlabel('Dropout rate', size=11)
    ax[(0, 1)].set_ylabel('Relative error', size=11)
    ax[(0, 1)].set_title('mn=1xe6', font2)
    ax[(0, 1)].legend(loc=6, bbox_to_anchor=(0.12, 0.78), prop={'size': 9})
    ax[(0, 1)].set_xlim((10, 70))
    ax[(0, 1)].set_ylim((0, 1))
    dropout_3_error = np.array([0.2412, 0.5091, 0.8198, 0.9616])
    zimpute_3_error = np.array([0.1424, 0.2124, 0.314, 0.4689])
    scimpute_3_error = np.array([0.2367, 0.422, 0.7196, 0.957])
    SAVER_3_error = np.array([0.2936, 0.5342, 0.8354, 0.9743])
    MAGIC_3_error = np.array([0.3705, 0.4813, 0.7773, 0.9499])
    ax[(1, 0)].plot(dropout_rates, zimpute_3_error, marker='^', linestyle=ls, label='zimpute')
    ax[(1, 0)].plot(dropout_rates, scimpute_3_error, marker='1', linestyle=ls, label='scimpute')
    ax[(1, 0)].plot(dropout_rates, SAVER_3_error, marker='s', linestyle=ls, label='SAVER')
    ax[(1, 0)].plot(dropout_rates, MAGIC_3_error, marker='x', linestyle=ls, label='MAGIC')
    ax[(1, 0)].plot(dropout_rates, dropout_3_error, marker='2', linestyle=ls, label='dropout')
    ax[(1, 0)].set_xlabel('Dropout rate', size=11)
    ax[(1, 0)].set_ylabel('Relative error', size=11)
    ax[(1, 0)].set_title('mn=2xe6', font2)
    ax[(1, 0)].legend(loc=6, bbox_to_anchor=(0.01, 0.78), prop={'size': 9})
    ax[(1, 0)].set_ylim((0, 1))
    ax[(1, 0)].set_xlim((10, 70))
    dropout_4_error = np.array([0.2456, 0.5203, 0.8282, 0.9661])
    zimpute_4_error = np.array([0.1632, 0.2313, 0.3058, 0.6667])
    scimpute_4_error = np.array([0.255, 0.4994, 0.7943, 0.9592])
    SAVER_4_error = np.array([0.3082, 0.5505, 0.8449, 0.9873])
    MAGIC_4_error = np.array([0.3332, 0.4725, 0.7902, 0.9552])
    ax[(1, 1)].plot(dropout_rates, zimpute_4_error, marker='^', linestyle=ls, label='zimpute')
    ax[(1, 1)].plot(dropout_rates, scimpute_4_error, marker='1', linestyle=ls, label='scimpute')
    ax[(1, 1)].plot(dropout_rates, SAVER_4_error, marker='s', linestyle=ls, label='SAVER')
    ax[(1, 1)].plot(dropout_rates, MAGIC_4_error, marker='x', linestyle=ls, label='MAGIC')
    ax[(1, 1)].plot(dropout_rates, dropout_4_error, marker='2', linestyle=ls, label='dropout')
    ax[(1, 1)].set_xlabel('Dropout rate', size=11)
    ax[(1, 1)].set_ylabel('Relative error', size=11)
    ax[(1, 1)].set_title('mn=2xe7', font2)
    ax[(1, 1)].legend(loc=6, bbox_to_anchor=(0.01, 0.78), prop={'size': 9})
    ax[(1, 1)].set_xlim((10, 70))
    ax[(1, 1)].set_ylim((0, 1))
    x_major_locator = plt.MultipleLocator(10)
    ax[(0, 0)].xaxis.set_major_locator(x_major_locator)
    ax[(0, 1)].xaxis.set_major_locator(x_major_locator)
    ax[(1, 0)].xaxis.set_major_locator(x_major_locator)
    ax[(1, 1)].xaxis.set_major_locator(x_major_locator)
    fig.suptitle('Relative error with different scales', fontsize=13)
    fig.subplots_adjust(hspace=0.35, wspace=0.28)
    plt.show()