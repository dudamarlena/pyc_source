# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/fdasrsf/pcr_regression.py
# Compiled at: 2019-10-14 10:32:19
# Size of source mod 2**32: 25493 bytes
"""
Warping Invariant PCR Regression using SRSF

moduleauthor:: Derek Tucker <jdtuck@sandia.gov>

"""
import numpy as np, fdasrsf as fs
import fdasrsf.utility_functions as uf
import fdasrsf.fPCA as fpca
import fdasrsf.regression as rg
import fdasrsf.geometry as geo
from scipy import dot
from scipy.linalg import inv, norm
from scipy.integrate import trapz, cumtrapz
from scipy.optimize import fmin_l_bfgs_b
import collections

class elastic_pcr_regression:
    __doc__ = '\n    This class provides elastic pcr regression for functional data using the\n    SRVF framework accounting for warping\n    \n    Usage:  obj = elastic_pcr_regression(f,y,time)\n    \n    :param f: (M,N) % matrix defining N functions of M samples\n    :param y: response vector of length N\n    :param warp_data: fdawarp object of alignment\n    :param pca: class dependent on fPCA method used object of fPCA\n    :param alpha: intercept\n    :param b: coefficient vector\n    :param SSE: sum of squared errors\n\n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  18-Mar-2018\n    '

    def __init__(self, f, y, time):
        """
        Construct an instance of the elastic_pcr_regression class
        :param f: numpy ndarray of shape (M,N) of N functions with M samples
        :param y: response vector
        :param time: vector of size M describing the sample points
        """
        a = time.shape[0]
        if f.shape[0] != a:
            raise Exception('Columns of f and time must be equal')
        self.f = f
        self.y = y
        self.time = time

    def calc_model(self, pca_method='combined', no=5, smooth_data=False, sparam=25, parallel=False, C=None):
        """
        This function identifies a regression model with phase-variability
        using elastic pca

        :param pca_method: string specifing pca method (options = "combined",
                        "vert", or "horiz", default = "combined")
        :param no: scalar specify number of principal components (default=5)
        :param smooth_data: smooth data using box filter (default = F)
        :param sparam: number of times to apply box filter (default = 25)
        :param parallel: run in parallel (default = F)
        :param C: scale balance parameter for combined method (default = None)
        """
        if smooth_data:
            self.f = fs.smooth_data(self.f, sparam)
        else:
            N1 = self.f.shape[1]
            self.warp_data = fs.fdawarp(self.f, self.time)
            self.warp_data.srsf_align(parallel=parallel)
            if pca_method == 'combined':
                out_pca = fpca.fdajpca(self.warp_data)
            else:
                if pca_method == 'vert':
                    out_pca = fpca.fdavpca(self.warp_data)
                else:
                    if pca_method == 'horiz':
                        out_pca = fpca.fdahpca(self.warp_data)
                    else:
                        raise Exception('Invalid fPCA Method')
        out_pca.calc_fpca(no)
        lam = 0
        R = 0
        Phi = np.ones((N1, no + 1))
        Phi[:, 1:no + 1] = out_pca.coef
        xx = dot(Phi.T, Phi)
        inv_xx = inv(xx + lam * R)
        xy = dot(Phi.T, self.y)
        b = dot(inv_xx, xy)
        alpha = b[0]
        b = b[1:no + 1]
        int_X = np.zeros(N1)
        for ii in range(0, N1):
            int_X[ii] = np.sum(out_pca.coef * b)

        SSE = np.sum((self.y - alpha - int_X) ** 2)
        self.alpha = alpha
        self.b = b
        self.pca = out_pca
        self.SSE = SSE
        self.pca_method = pca_method

    def predict(self, newdata=None):
        """
        This function performs prediction on regression model on new data if available or current stored data in object
        Usage:  obj.predict()
                obj.predict(newdata)

        :param newdata: dict containing new data for prediction (needs the keys below, if None predicts on training data)
        :type newdata: dict
        :param f: (M,N) matrix of functions
        :param time: vector of time points
        :param y: truth if available
        :param smooth: smooth data if needed
        :param sparam: number of times to run filter
        """
        omethod = self.warp_data.method
        lam = self.warp_data.lam
        M = self.time.shape[0]
        if newdata != None:
            f = newdata['f']
            time = newdata['time']
            y = newdata['y']
            sparam = newdata['sparam']
            if newdata['smooth']:
                f = fs.smooth_data(f, sparam)
            else:
                q1 = fs.f_to_srsf(f, time)
                n = q1.shape[1]
                self.y_pred = np.zeros(n)
                mq = self.warp_data.mqn
                fn = np.zeros((M, n))
                qn = np.zeros((M, n))
                gam = np.zeros((M, n))
                for ii in range(0, n):
                    gam[:, ii] = uf.optimum_reparam(mq, time, q1[:, ii], omethod)
                    fn[:, ii] = uf.warp_f_gamma(time, f[:, ii], gam[:, ii])
                    qn[:, ii] = uf.f_to_srsf(fn[:, ii], time)

                m_new = np.sign(fn[self.pca.id, :]) * np.sqrt(np.abs(fn[self.pca.id, :]))
                qn1 = np.vstack((qn, m_new))
                U = self.pca.U
                no = U.shape[1]
                if self.pca.__class__.__name__ == 'fdajpca':
                    C = self.pca.C
                    TT = self.time.shape[0]
                    mu_g = self.pca.mu_g
                    mu_psi = self.pca.mu_psi
                    vec = np.zeros((M, n))
                    psi = np.zeros((TT, n))
                    binsize = np.mean(np.diff(self.time))
                    for i in range(0, n):
                        psi[:, i] = np.sqrt(np.gradient(gam[:, i], binsize))
                        vec[:, i] = geo.inv_exp_map(mu_psi, psi[:, i])

                    g = np.vstack((qn1, C * vec))
                    a = np.zeros((n, no))
                    for i in range(0, n):
                        for j in range(0, no):
                            tmp = g[:, i] - mu_g
                            a[(i, j)] = dot(tmp.T, U[:, j])

                else:
                    if self.pca.__class__.__name__ == 'fdavpca':
                        a = np.zeros((n, no))
                        for i in range(0, n):
                            for j in range(0, no):
                                tmp = qn1[:, i] - self.pca.mqn
                                a[(i, j)] = dot(tmp.T, U[:, j])

                    else:
                        if self.pca.__class__.__name__ == 'fdahpca':
                            a = np.zeros((n, no))
                            mu_psi = self.pca.psi_mu
                            vec = np.zeros((M, n))
                            TT = self.time.shape[0]
                            psi = np.zeros((TT, n))
                            binsize = np.mean(np.diff(self.time))
                            for i in range(0, n):
                                psi[:, i] = np.sqrt(np.gradient(gam[:, i], binsize))
                                vec[:, i] = geo.inv_exp_map(mu_psi, psi[:, i])

                            vm = self.pca.vec.mean(axis=1)
                            for i in range(0, n):
                                for j in range(0, no):
                                    a[(i, j)] = np.sum(dot(vec[:, i] - vm, U[:, j]))

                        else:
                            raise Exception('Invalid fPCA Method')
                for ii in range(0, n):
                    self.y_pred[ii] = self.alpha + np.sum(a[ii, :] * self.b)

                if y == None:
                    self.SSE = np.nan
                else:
                    self.SSE = np.sum((y - self.y_pred) ** 2)
        else:
            n = self.pca.coef.shape[1]
            self.y_pred = np.zeros(n)
            for ii in range(0, n):
                self.y_pred[ii] = self.alpha + np.dot(self.pca.coef[ii, :], self.b)

            self.SSE = np.sum((self.y - self.y_pred) ** 2)
            return


class elastic_lpcr_regression:
    __doc__ = '\n    This class provides elastic logistic pcr regression for functional \n    data using the SRVF framework accounting for warping\n    \n    Usage:  obj = elastic_lpcr_regression(f,y,time)\n\n    :param f: (M,N) % matrix defining N functions of M samples\n    :param y: response vector of length N (-1/1)\n    :param warp_data: fdawarp object of alignment\n    :param pca: class dependent on fPCA method used object of fPCA\n    :param information\n    :param alpha: intercept\n    :param b: coefficient vector\n    :param Loss: logistic loss\n    :param PC: probability of classification\n    :param ylabels: predicted labels\n    \n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  18-Mar-2018\n    '

    def __init__(self, f, y, time):
        """
        Construct an instance of the elastic_lpcr_regression class
        :param f: numpy ndarray of shape (M,N) of N functions with M samples
        :param y: response vector
        :param time: vector of size M describing the sample points
        """
        a = time.shape[0]
        if f.shape[0] != a:
            raise Exception('Columns of f and time must be equal')
        self.f = f
        self.y = y
        self.time = time

    def calc_model(self, pca_method='combined', no=5, smooth_data=False, sparam=25, parallel=False):
        """
        This function identifies a logistic regression model with phase-variability
        using elastic pca

        :param pca_method: string specifing pca method (options = "combined",
                        "vert", or "horiz", default = "combined")
        :param no: scalar specify number of principal components (default=5)
        :param smooth_data: smooth data using box filter (default = F)
        :param sparam: number of times to apply box filter (default = 25)
        :param parallel: calculate in parallel (default = F)
        :type f: np.ndarray
        :type time: np.ndarray
        """
        if smooth_data:
            self.f = fs.smooth_data(self.f, sparam)
        else:
            N1 = self.f.shape[1]
            self.warp_data = fs.fdawarp(self.f, self.time)
            self.warp_data.srsf_align(parallel=parallel)
            if pca_method == 'combined':
                out_pca = fpca.fdajpca(self.warp_data)
            else:
                if pca_method == 'vert':
                    out_pca = fpca.fdavpca(self.warp_data)
                else:
                    if pca_method == 'horiz':
                        out_pca = fpca.fdahpca(self.warp_data)
                    else:
                        raise Exception('Invalid fPCA Method')
        out_pca.calc_fpca(no)
        lam = 0
        R = 0
        Phi = np.ones((N1, no + 1))
        Phi[:, 1:no + 1] = out_pca.coef
        b0 = np.zeros(no + 1)
        out = fmin_l_bfgs_b((rg.logit_loss), b0, fprime=(rg.logit_gradient), args=(
         Phi, self.y),
          pgtol=1e-10,
          maxiter=200,
          maxfun=250,
          factr=1e-30)
        b = out[0]
        alpha = b[0]
        LL = rg.logit_loss(b, Phi, self.y)
        b = b[1:no + 1]
        self.alpha = alpha
        self.b = b
        self.pca = out_pca
        self.LL = LL
        self.pca_method = pca_method

    def predict--- This code section failed: ---

 L. 341         0  LOAD_FAST                'self'
                2  LOAD_ATTR                warp_data
                4  LOAD_ATTR                method
                6  STORE_FAST               'omethod'

 L. 342         8  LOAD_FAST                'self'
               10  LOAD_ATTR                warp_data
               12  LOAD_ATTR                lam
               14  STORE_FAST               'lam'

 L. 343        16  LOAD_FAST                'self'
               18  LOAD_ATTR                time
               20  LOAD_ATTR                shape
               22  LOAD_CONST               0
               24  BINARY_SUBSCR    
               26  STORE_FAST               'M'

 L. 345        28  LOAD_FAST                'newdata'
               30  LOAD_CONST               None
               32  COMPARE_OP               !=
            34_36  POP_JUMP_IF_FALSE  1484  'to 1484'

 L. 346        38  LOAD_FAST                'newdata'
               40  LOAD_STR                 'f'
               42  BINARY_SUBSCR    
               44  STORE_FAST               'f'

 L. 347        46  LOAD_FAST                'newdata'
               48  LOAD_STR                 'time'
               50  BINARY_SUBSCR    
               52  STORE_FAST               'time'

 L. 348        54  LOAD_FAST                'newdata'
               56  LOAD_STR                 'y'
               58  BINARY_SUBSCR    
               60  STORE_FAST               'y'

 L. 349        62  LOAD_FAST                'newdata'
               64  LOAD_STR                 'sparam'
               66  BINARY_SUBSCR    
               68  STORE_FAST               'sparam'

 L. 350        70  LOAD_FAST                'newdata'
               72  LOAD_STR                 'smooth'
               74  BINARY_SUBSCR    
               76  POP_JUMP_IF_FALSE    90  'to 90'

 L. 351        78  LOAD_GLOBAL              fs
               80  LOAD_METHOD              smooth_data
               82  LOAD_FAST                'f'
               84  LOAD_FAST                'sparam'
               86  CALL_METHOD_2         2  '2 positional arguments'
               88  STORE_FAST               'f'
             90_0  COME_FROM            76  '76'

 L. 353        90  LOAD_GLOBAL              fs
               92  LOAD_METHOD              f_to_srsf
               94  LOAD_FAST                'f'
               96  LOAD_FAST                'time'
               98  CALL_METHOD_2         2  '2 positional arguments'
              100  STORE_FAST               'q1'

 L. 354       102  LOAD_FAST                'q1'
              104  LOAD_ATTR                shape
              106  LOAD_CONST               1
              108  BINARY_SUBSCR    
              110  STORE_FAST               'n'

 L. 355       112  LOAD_GLOBAL              np
              114  LOAD_METHOD              zeros
              116  LOAD_FAST                'n'
              118  CALL_METHOD_1         1  '1 positional argument'
              120  LOAD_FAST                'self'
              122  STORE_ATTR               y_pred

 L. 356       124  LOAD_FAST                'self'
              126  LOAD_ATTR                warp_data
              128  LOAD_ATTR                mqn
              130  STORE_FAST               'mq'

 L. 357       132  LOAD_GLOBAL              np
              134  LOAD_METHOD              zeros
              136  LOAD_FAST                'M'
              138  LOAD_FAST                'n'
              140  BUILD_TUPLE_2         2 
              142  CALL_METHOD_1         1  '1 positional argument'
              144  STORE_FAST               'fn'

 L. 358       146  LOAD_GLOBAL              np
              148  LOAD_METHOD              zeros
              150  LOAD_FAST                'M'
              152  LOAD_FAST                'n'
              154  BUILD_TUPLE_2         2 
              156  CALL_METHOD_1         1  '1 positional argument'
              158  STORE_FAST               'qn'

 L. 359       160  LOAD_GLOBAL              np
              162  LOAD_METHOD              zeros
              164  LOAD_FAST                'M'
              166  LOAD_FAST                'n'
              168  BUILD_TUPLE_2         2 
              170  CALL_METHOD_1         1  '1 positional argument'
              172  STORE_FAST               'gam'

 L. 360       174  SETUP_LOOP          320  'to 320'
              176  LOAD_GLOBAL              range
              178  LOAD_CONST               0
              180  LOAD_FAST                'n'
              182  CALL_FUNCTION_2       2  '2 positional arguments'
              184  GET_ITER         
              186  FOR_ITER            318  'to 318'
              188  STORE_FAST               'ii'

 L. 361       190  LOAD_GLOBAL              uf
              192  LOAD_METHOD              optimum_reparam
              194  LOAD_FAST                'mq'
              196  LOAD_FAST                'time'
              198  LOAD_FAST                'q1'
              200  LOAD_CONST               None
              202  LOAD_CONST               None
              204  BUILD_SLICE_2         2 
              206  LOAD_FAST                'ii'
              208  BUILD_TUPLE_2         2 
              210  BINARY_SUBSCR    
              212  LOAD_FAST                'omethod'
              214  CALL_METHOD_4         4  '4 positional arguments'
              216  LOAD_FAST                'gam'
              218  LOAD_CONST               None
              220  LOAD_CONST               None
              222  BUILD_SLICE_2         2 
              224  LOAD_FAST                'ii'
              226  BUILD_TUPLE_2         2 
              228  STORE_SUBSCR     

 L. 362       230  LOAD_GLOBAL              uf
              232  LOAD_METHOD              warp_f_gamma
              234  LOAD_FAST                'time'
              236  LOAD_FAST                'f'
              238  LOAD_CONST               None
              240  LOAD_CONST               None
              242  BUILD_SLICE_2         2 
              244  LOAD_FAST                'ii'
              246  BUILD_TUPLE_2         2 
              248  BINARY_SUBSCR    
              250  LOAD_FAST                'gam'
              252  LOAD_CONST               None
              254  LOAD_CONST               None
              256  BUILD_SLICE_2         2 
              258  LOAD_FAST                'ii'
              260  BUILD_TUPLE_2         2 
              262  BINARY_SUBSCR    
              264  CALL_METHOD_3         3  '3 positional arguments'
              266  LOAD_FAST                'fn'
              268  LOAD_CONST               None
              270  LOAD_CONST               None
              272  BUILD_SLICE_2         2 
              274  LOAD_FAST                'ii'
              276  BUILD_TUPLE_2         2 
              278  STORE_SUBSCR     

 L. 363       280  LOAD_GLOBAL              uf
              282  LOAD_METHOD              f_to_srsf
              284  LOAD_FAST                'fn'
              286  LOAD_CONST               None
              288  LOAD_CONST               None
              290  BUILD_SLICE_2         2 
              292  LOAD_FAST                'ii'
              294  BUILD_TUPLE_2         2 
              296  BINARY_SUBSCR    
              298  LOAD_FAST                'time'
              300  CALL_METHOD_2         2  '2 positional arguments'
              302  LOAD_FAST                'qn'
              304  LOAD_CONST               None
              306  LOAD_CONST               None
              308  BUILD_SLICE_2         2 
              310  LOAD_FAST                'ii'
              312  BUILD_TUPLE_2         2 
              314  STORE_SUBSCR     
              316  JUMP_BACK           186  'to 186'
              318  POP_BLOCK        
            320_0  COME_FROM_LOOP      174  '174'

 L. 365       320  LOAD_GLOBAL              np
              322  LOAD_METHOD              sign
              324  LOAD_FAST                'fn'
              326  LOAD_FAST                'self'
              328  LOAD_ATTR                pca
              330  LOAD_ATTR                id
              332  LOAD_CONST               None
              334  LOAD_CONST               None
              336  BUILD_SLICE_2         2 
              338  BUILD_TUPLE_2         2 
              340  BINARY_SUBSCR    
              342  CALL_METHOD_1         1  '1 positional argument'
              344  LOAD_GLOBAL              np
              346  LOAD_METHOD              sqrt
              348  LOAD_GLOBAL              np
              350  LOAD_METHOD              abs
              352  LOAD_FAST                'fn'
              354  LOAD_FAST                'self'
              356  LOAD_ATTR                pca
              358  LOAD_ATTR                id
              360  LOAD_CONST               None
              362  LOAD_CONST               None
              364  BUILD_SLICE_2         2 
              366  BUILD_TUPLE_2         2 
              368  BINARY_SUBSCR    
              370  CALL_METHOD_1         1  '1 positional argument'
              372  CALL_METHOD_1         1  '1 positional argument'
              374  BINARY_MULTIPLY  
              376  STORE_FAST               'm_new'

 L. 366       378  LOAD_GLOBAL              np
              380  LOAD_METHOD              vstack
              382  LOAD_FAST                'qn'
              384  LOAD_FAST                'm_new'
              386  BUILD_TUPLE_2         2 
              388  CALL_METHOD_1         1  '1 positional argument'
              390  STORE_FAST               'qn1'

 L. 367       392  LOAD_FAST                'self'
              394  LOAD_ATTR                pca
              396  LOAD_ATTR                U
              398  STORE_FAST               'U'

 L. 368       400  LOAD_FAST                'U'
              402  LOAD_ATTR                shape
              404  LOAD_CONST               1
              406  BINARY_SUBSCR    
              408  STORE_FAST               'no'

 L. 370       410  LOAD_FAST                'self'
              412  LOAD_ATTR                pca
              414  LOAD_ATTR                __class__
              416  LOAD_ATTR                __name__
              418  LOAD_STR                 'fdajpca'
              420  COMPARE_OP               ==
          422_424  POP_JUMP_IF_FALSE   740  'to 740'

 L. 371       426  LOAD_FAST                'self'
              428  LOAD_ATTR                pca
              430  LOAD_ATTR                C
              432  STORE_FAST               'C'

 L. 372       434  LOAD_FAST                'self'
              436  LOAD_ATTR                time
              438  LOAD_ATTR                shape
              440  LOAD_CONST               0
              442  BINARY_SUBSCR    
              444  STORE_FAST               'TT'

 L. 373       446  LOAD_FAST                'self'
              448  LOAD_ATTR                pca
              450  LOAD_ATTR                mu_g
              452  STORE_FAST               'mu_g'

 L. 374       454  LOAD_FAST                'self'
              456  LOAD_ATTR                pca
              458  LOAD_ATTR                mu_psi
              460  STORE_FAST               'mu_psi'

 L. 375       462  LOAD_GLOBAL              np
              464  LOAD_METHOD              zeros
              466  LOAD_FAST                'M'
              468  LOAD_FAST                'n'
              470  BUILD_TUPLE_2         2 
              472  CALL_METHOD_1         1  '1 positional argument'
              474  STORE_FAST               'vec'

 L. 376       476  LOAD_GLOBAL              np
              478  LOAD_METHOD              zeros
              480  LOAD_FAST                'TT'
              482  LOAD_FAST                'n'
              484  BUILD_TUPLE_2         2 
              486  CALL_METHOD_1         1  '1 positional argument'
              488  STORE_FAST               'psi'

 L. 377       490  LOAD_GLOBAL              np
              492  LOAD_METHOD              mean
              494  LOAD_GLOBAL              np
              496  LOAD_METHOD              diff
              498  LOAD_FAST                'self'
              500  LOAD_ATTR                time
              502  CALL_METHOD_1         1  '1 positional argument'
              504  CALL_METHOD_1         1  '1 positional argument'
              506  STORE_FAST               'binsize'

 L. 378       508  SETUP_LOOP          608  'to 608'
              510  LOAD_GLOBAL              range
              512  LOAD_CONST               0
              514  LOAD_FAST                'n'
              516  CALL_FUNCTION_2       2  '2 positional arguments'
              518  GET_ITER         
              520  FOR_ITER            606  'to 606'
              522  STORE_FAST               'i'

 L. 379       524  LOAD_GLOBAL              np
              526  LOAD_METHOD              sqrt
              528  LOAD_GLOBAL              np
              530  LOAD_METHOD              gradient
              532  LOAD_FAST                'gam'
              534  LOAD_CONST               None
              536  LOAD_CONST               None
              538  BUILD_SLICE_2         2 
              540  LOAD_FAST                'i'
              542  BUILD_TUPLE_2         2 
              544  BINARY_SUBSCR    
              546  LOAD_FAST                'binsize'
              548  CALL_METHOD_2         2  '2 positional arguments'
              550  CALL_METHOD_1         1  '1 positional argument'
              552  LOAD_FAST                'psi'
              554  LOAD_CONST               None
              556  LOAD_CONST               None
              558  BUILD_SLICE_2         2 
              560  LOAD_FAST                'i'
              562  BUILD_TUPLE_2         2 
              564  STORE_SUBSCR     

 L. 380       566  LOAD_GLOBAL              geo
              568  LOAD_METHOD              inv_exp_map
              570  LOAD_FAST                'mu_psi'
              572  LOAD_FAST                'psi'
              574  LOAD_CONST               None
              576  LOAD_CONST               None
              578  BUILD_SLICE_2         2 
              580  LOAD_FAST                'i'
              582  BUILD_TUPLE_2         2 
              584  BINARY_SUBSCR    
              586  CALL_METHOD_2         2  '2 positional arguments'
              588  LOAD_FAST                'vec'
              590  LOAD_CONST               None
              592  LOAD_CONST               None
              594  BUILD_SLICE_2         2 
              596  LOAD_FAST                'i'
              598  BUILD_TUPLE_2         2 
              600  STORE_SUBSCR     
          602_604  JUMP_BACK           520  'to 520'
              606  POP_BLOCK        
            608_0  COME_FROM_LOOP      508  '508'

 L. 382       608  LOAD_GLOBAL              np
              610  LOAD_METHOD              vstack
              612  LOAD_FAST                'qn1'
              614  LOAD_FAST                'C'
              616  LOAD_FAST                'vec'
              618  BINARY_MULTIPLY  
              620  BUILD_TUPLE_2         2 
              622  CALL_METHOD_1         1  '1 positional argument'
              624  STORE_FAST               'g'

 L. 383       626  LOAD_GLOBAL              np
              628  LOAD_METHOD              zeros
              630  LOAD_FAST                'n'
              632  LOAD_FAST                'no'
              634  BUILD_TUPLE_2         2 
              636  CALL_METHOD_1         1  '1 positional argument'
              638  STORE_FAST               'a'

 L. 384       640  SETUP_LOOP          736  'to 736'
              642  LOAD_GLOBAL              range
              644  LOAD_CONST               0
              646  LOAD_FAST                'n'
              648  CALL_FUNCTION_2       2  '2 positional arguments'
              650  GET_ITER         
              652  FOR_ITER            734  'to 734'
              654  STORE_FAST               'i'

 L. 385       656  SETUP_LOOP          730  'to 730'
              658  LOAD_GLOBAL              range
              660  LOAD_CONST               0
              662  LOAD_FAST                'no'
              664  CALL_FUNCTION_2       2  '2 positional arguments'
              666  GET_ITER         
              668  FOR_ITER            728  'to 728'
              670  STORE_FAST               'j'

 L. 386       672  LOAD_FAST                'g'
              674  LOAD_CONST               None
              676  LOAD_CONST               None
              678  BUILD_SLICE_2         2 
              680  LOAD_FAST                'i'
              682  BUILD_TUPLE_2         2 
              684  BINARY_SUBSCR    
              686  LOAD_FAST                'mu_g'
              688  BINARY_SUBTRACT  
              690  STORE_FAST               'tmp'

 L. 387       692  LOAD_GLOBAL              dot
              694  LOAD_FAST                'tmp'
              696  LOAD_ATTR                T
              698  LOAD_FAST                'U'
              700  LOAD_CONST               None
              702  LOAD_CONST               None
              704  BUILD_SLICE_2         2 
              706  LOAD_FAST                'j'
              708  BUILD_TUPLE_2         2 
              710  BINARY_SUBSCR    
              712  CALL_FUNCTION_2       2  '2 positional arguments'
              714  LOAD_FAST                'a'
              716  LOAD_FAST                'i'
              718  LOAD_FAST                'j'
              720  BUILD_TUPLE_2         2 
              722  STORE_SUBSCR     
          724_726  JUMP_BACK           668  'to 668'
              728  POP_BLOCK        
            730_0  COME_FROM_LOOP      656  '656'
          730_732  JUMP_BACK           652  'to 652'
              734  POP_BLOCK        
            736_0  COME_FROM_LOOP      640  '640'
          736_738  JUMP_FORWARD       1192  'to 1192'
            740_0  COME_FROM           422  '422'

 L. 389       740  LOAD_FAST                'self'
              742  LOAD_ATTR                pca
              744  LOAD_ATTR                __class__
              746  LOAD_ATTR                __name__
              748  LOAD_STR                 'fdavpca'
              750  COMPARE_OP               ==
          752_754  POP_JUMP_IF_FALSE   874  'to 874'

 L. 390       756  LOAD_GLOBAL              np
              758  LOAD_METHOD              zeros
              760  LOAD_FAST                'n'
              762  LOAD_FAST                'no'
              764  BUILD_TUPLE_2         2 
              766  CALL_METHOD_1         1  '1 positional argument'
              768  STORE_FAST               'a'

 L. 391       770  SETUP_LOOP          870  'to 870'
              772  LOAD_GLOBAL              range
              774  LOAD_CONST               0
              776  LOAD_FAST                'n'
              778  CALL_FUNCTION_2       2  '2 positional arguments'
              780  GET_ITER         
              782  FOR_ITER            868  'to 868'
              784  STORE_FAST               'i'

 L. 392       786  SETUP_LOOP          864  'to 864'
              788  LOAD_GLOBAL              range
              790  LOAD_CONST               0
              792  LOAD_FAST                'no'
              794  CALL_FUNCTION_2       2  '2 positional arguments'
              796  GET_ITER         
              798  FOR_ITER            862  'to 862'
              800  STORE_FAST               'j'

 L. 393       802  LOAD_FAST                'qn1'
              804  LOAD_CONST               None
              806  LOAD_CONST               None
              808  BUILD_SLICE_2         2 
              810  LOAD_FAST                'i'
              812  BUILD_TUPLE_2         2 
              814  BINARY_SUBSCR    
              816  LOAD_FAST                'self'
              818  LOAD_ATTR                pca
              820  LOAD_ATTR                mqn
              822  BINARY_SUBTRACT  
              824  STORE_FAST               'tmp'

 L. 394       826  LOAD_GLOBAL              dot
              828  LOAD_FAST                'tmp'
              830  LOAD_ATTR                T
              832  LOAD_FAST                'U'
              834  LOAD_CONST               None
              836  LOAD_CONST               None
              838  BUILD_SLICE_2         2 
              840  LOAD_FAST                'j'
              842  BUILD_TUPLE_2         2 
              844  BINARY_SUBSCR    
              846  CALL_FUNCTION_2       2  '2 positional arguments'
              848  LOAD_FAST                'a'
              850  LOAD_FAST                'i'
              852  LOAD_FAST                'j'
              854  BUILD_TUPLE_2         2 
              856  STORE_SUBSCR     
          858_860  JUMP_BACK           798  'to 798'
              862  POP_BLOCK        
            864_0  COME_FROM_LOOP      786  '786'
          864_866  JUMP_BACK           782  'to 782'
              868  POP_BLOCK        
            870_0  COME_FROM_LOOP      770  '770'
          870_872  JUMP_FORWARD       1192  'to 1192'
            874_0  COME_FROM           752  '752'

 L. 396       874  LOAD_FAST                'self'
              876  LOAD_ATTR                pca
              878  LOAD_ATTR                __class__
              880  LOAD_ATTR                __name__
              882  LOAD_STR                 'fdahpca'
              884  COMPARE_OP               ==
          886_888  POP_JUMP_IF_FALSE  1184  'to 1184'

 L. 397       890  LOAD_GLOBAL              np
              892  LOAD_METHOD              zeros
              894  LOAD_FAST                'n'
              896  LOAD_FAST                'no'
              898  BUILD_TUPLE_2         2 
              900  CALL_METHOD_1         1  '1 positional argument'
              902  STORE_FAST               'a'

 L. 398       904  LOAD_FAST                'self'
              906  LOAD_ATTR                pca
              908  LOAD_ATTR                psi_mu
              910  STORE_FAST               'mu_psi'

 L. 399       912  LOAD_GLOBAL              np
              914  LOAD_METHOD              zeros
              916  LOAD_FAST                'M'
              918  LOAD_FAST                'n'
              920  BUILD_TUPLE_2         2 
              922  CALL_METHOD_1         1  '1 positional argument'
              924  STORE_FAST               'vec'

 L. 400       926  LOAD_FAST                'self'
              928  LOAD_ATTR                time
              930  LOAD_ATTR                shape
              932  LOAD_CONST               0
              934  BINARY_SUBSCR    
              936  STORE_FAST               'TT'

 L. 401       938  LOAD_GLOBAL              np
              940  LOAD_METHOD              zeros
              942  LOAD_FAST                'TT'
              944  LOAD_FAST                'n'
              946  BUILD_TUPLE_2         2 
              948  CALL_METHOD_1         1  '1 positional argument'
              950  STORE_FAST               'psi'

 L. 402       952  LOAD_GLOBAL              np
              954  LOAD_METHOD              mean
              956  LOAD_GLOBAL              np
              958  LOAD_METHOD              diff
              960  LOAD_FAST                'self'
              962  LOAD_ATTR                time
              964  CALL_METHOD_1         1  '1 positional argument'
              966  CALL_METHOD_1         1  '1 positional argument'
              968  STORE_FAST               'binsize'

 L. 403       970  SETUP_LOOP         1070  'to 1070'
              972  LOAD_GLOBAL              range
              974  LOAD_CONST               0
              976  LOAD_FAST                'n'
              978  CALL_FUNCTION_2       2  '2 positional arguments'
              980  GET_ITER         
              982  FOR_ITER           1068  'to 1068'
              984  STORE_FAST               'i'

 L. 404       986  LOAD_GLOBAL              np
              988  LOAD_METHOD              sqrt
              990  LOAD_GLOBAL              np
              992  LOAD_METHOD              gradient
              994  LOAD_FAST                'gam'
              996  LOAD_CONST               None
              998  LOAD_CONST               None
             1000  BUILD_SLICE_2         2 
             1002  LOAD_FAST                'i'
             1004  BUILD_TUPLE_2         2 
             1006  BINARY_SUBSCR    
             1008  LOAD_FAST                'binsize'
             1010  CALL_METHOD_2         2  '2 positional arguments'
             1012  CALL_METHOD_1         1  '1 positional argument'
             1014  LOAD_FAST                'psi'
             1016  LOAD_CONST               None
             1018  LOAD_CONST               None
             1020  BUILD_SLICE_2         2 
             1022  LOAD_FAST                'i'
             1024  BUILD_TUPLE_2         2 
             1026  STORE_SUBSCR     

 L. 405      1028  LOAD_GLOBAL              geo
             1030  LOAD_METHOD              inv_exp_map
             1032  LOAD_FAST                'mu_psi'
             1034  LOAD_FAST                'psi'
             1036  LOAD_CONST               None
             1038  LOAD_CONST               None
             1040  BUILD_SLICE_2         2 
             1042  LOAD_FAST                'i'
             1044  BUILD_TUPLE_2         2 
             1046  BINARY_SUBSCR    
             1048  CALL_METHOD_2         2  '2 positional arguments'
             1050  LOAD_FAST                'vec'
             1052  LOAD_CONST               None
             1054  LOAD_CONST               None
             1056  BUILD_SLICE_2         2 
             1058  LOAD_FAST                'i'
             1060  BUILD_TUPLE_2         2 
             1062  STORE_SUBSCR     
         1064_1066  JUMP_BACK           982  'to 982'
             1068  POP_BLOCK        
           1070_0  COME_FROM_LOOP      970  '970'

 L. 407      1070  LOAD_FAST                'self'
             1072  LOAD_ATTR                pca
             1074  LOAD_ATTR                vec
             1076  LOAD_ATTR                mean
             1078  LOAD_CONST               1
             1080  LOAD_CONST               ('axis',)
             1082  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
             1084  STORE_FAST               'vm'

 L. 409      1086  SETUP_LOOP         1192  'to 1192'
             1088  LOAD_GLOBAL              range
             1090  LOAD_CONST               0
             1092  LOAD_FAST                'n'
             1094  CALL_FUNCTION_2       2  '2 positional arguments'
             1096  GET_ITER         
             1098  FOR_ITER           1180  'to 1180'
             1100  STORE_FAST               'i'

 L. 410      1102  SETUP_LOOP         1176  'to 1176'
             1104  LOAD_GLOBAL              range
             1106  LOAD_CONST               0
             1108  LOAD_FAST                'no'
             1110  CALL_FUNCTION_2       2  '2 positional arguments'
             1112  GET_ITER         
             1114  FOR_ITER           1174  'to 1174'
             1116  STORE_FAST               'j'

 L. 411      1118  LOAD_GLOBAL              np
             1120  LOAD_METHOD              sum
             1122  LOAD_GLOBAL              dot
             1124  LOAD_FAST                'vec'
             1126  LOAD_CONST               None
             1128  LOAD_CONST               None
             1130  BUILD_SLICE_2         2 
             1132  LOAD_FAST                'i'
             1134  BUILD_TUPLE_2         2 
             1136  BINARY_SUBSCR    
             1138  LOAD_FAST                'vm'
             1140  BINARY_SUBTRACT  
             1142  LOAD_FAST                'U'
             1144  LOAD_CONST               None
             1146  LOAD_CONST               None
             1148  BUILD_SLICE_2         2 
             1150  LOAD_FAST                'j'
             1152  BUILD_TUPLE_2         2 
             1154  BINARY_SUBSCR    
             1156  CALL_FUNCTION_2       2  '2 positional arguments'
             1158  CALL_METHOD_1         1  '1 positional argument'
             1160  LOAD_FAST                'a'
             1162  LOAD_FAST                'i'
             1164  LOAD_FAST                'j'
             1166  BUILD_TUPLE_2         2 
             1168  STORE_SUBSCR     
         1170_1172  JUMP_BACK          1114  'to 1114'
             1174  POP_BLOCK        
           1176_0  COME_FROM_LOOP     1102  '1102'
         1176_1178  JUMP_BACK          1098  'to 1098'
             1180  POP_BLOCK        
             1182  JUMP_FORWARD       1192  'to 1192'
           1184_0  COME_FROM           886  '886'

 L. 413      1184  LOAD_GLOBAL              Exception
             1186  LOAD_STR                 'Invalid fPCA Method'
             1188  CALL_FUNCTION_1       1  '1 positional argument'
             1190  RAISE_VARARGS_1       1  'exception instance'
           1192_0  COME_FROM          1182  '1182'
           1192_1  COME_FROM_LOOP     1086  '1086'
           1192_2  COME_FROM           870  '870'
           1192_3  COME_FROM           736  '736'

 L. 415      1192  SETUP_LOOP         1254  'to 1254'
             1194  LOAD_GLOBAL              range
             1196  LOAD_CONST               0
             1198  LOAD_FAST                'n'
             1200  CALL_FUNCTION_2       2  '2 positional arguments'
             1202  GET_ITER         
             1204  FOR_ITER           1252  'to 1252'
             1206  STORE_FAST               'ii'

 L. 416      1208  LOAD_FAST                'self'
             1210  LOAD_ATTR                alpha
             1212  LOAD_GLOBAL              np
             1214  LOAD_METHOD              sum
             1216  LOAD_FAST                'a'
             1218  LOAD_FAST                'ii'
             1220  LOAD_CONST               None
             1222  LOAD_CONST               None
             1224  BUILD_SLICE_2         2 
             1226  BUILD_TUPLE_2         2 
             1228  BINARY_SUBSCR    
             1230  LOAD_FAST                'self'
             1232  LOAD_ATTR                b
             1234  BINARY_MULTIPLY  
             1236  CALL_METHOD_1         1  '1 positional argument'
             1238  BINARY_ADD       
             1240  LOAD_FAST                'self'
             1242  LOAD_ATTR                y_pred
             1244  LOAD_FAST                'ii'
             1246  STORE_SUBSCR     
         1248_1250  JUMP_BACK          1204  'to 1204'
             1252  POP_BLOCK        
           1254_0  COME_FROM_LOOP     1192  '1192'

 L. 418      1254  LOAD_FAST                'y'
             1256  LOAD_CONST               None
             1258  COMPARE_OP               ==
         1260_1262  POP_JUMP_IF_FALSE  1316  'to 1316'

 L. 419      1264  LOAD_GLOBAL              rg
             1266  LOAD_METHOD              phi
             1268  LOAD_FAST                'self'
             1270  LOAD_ATTR                y_pred
             1272  CALL_METHOD_1         1  '1 positional argument'
             1274  LOAD_FAST                'self'
             1276  STORE_ATTR               y_pred

 L. 420      1278  LOAD_GLOBAL              np
             1280  LOAD_METHOD              ones
             1282  LOAD_FAST                'n'
             1284  CALL_METHOD_1         1  '1 positional argument'
             1286  LOAD_FAST                'self'
             1288  STORE_ATTR               y_labels

 L. 421      1290  LOAD_CONST               -1
             1292  LOAD_FAST                'self'
             1294  LOAD_ATTR                y_labels
             1296  LOAD_FAST                'self'
             1298  LOAD_ATTR                y_pred
             1300  LOAD_CONST               0.5
             1302  COMPARE_OP               <
             1304  STORE_SUBSCR     

 L. 422      1306  LOAD_GLOBAL              np
             1308  LOAD_ATTR                nan
             1310  LOAD_FAST                'self'
             1312  STORE_ATTR               PC
             1314  JUMP_FORWARD       1750  'to 1750'
           1316_0  COME_FROM          1260  '1260'

 L. 424      1316  LOAD_GLOBAL              rg
             1318  LOAD_METHOD              phi
             1320  LOAD_FAST                'self'
             1322  LOAD_ATTR                y_pred
             1324  CALL_METHOD_1         1  '1 positional argument'
             1326  LOAD_FAST                'self'
             1328  STORE_ATTR               y_pred

 L. 425      1330  LOAD_GLOBAL              np
             1332  LOAD_METHOD              ones
             1334  LOAD_FAST                'n'
             1336  CALL_METHOD_1         1  '1 positional argument'
             1338  LOAD_FAST                'self'
             1340  STORE_ATTR               y_labels

 L. 426      1342  LOAD_CONST               -1
             1344  LOAD_FAST                'self'
             1346  LOAD_ATTR                y_labels
             1348  LOAD_FAST                'self'
             1350  LOAD_ATTR                y_pred
             1352  LOAD_CONST               0.5
             1354  COMPARE_OP               <
             1356  STORE_SUBSCR     

 L. 427      1358  LOAD_GLOBAL              np
             1360  LOAD_METHOD              sum
             1362  LOAD_FAST                'y'
             1364  LOAD_FAST                'self'
             1366  LOAD_ATTR                y_labels
             1368  LOAD_CONST               1
             1370  COMPARE_OP               ==
             1372  BINARY_SUBSCR    
             1374  LOAD_CONST               1
             1376  COMPARE_OP               ==
             1378  CALL_METHOD_1         1  '1 positional argument'
             1380  STORE_FAST               'TP'

 L. 428      1382  LOAD_GLOBAL              np
             1384  LOAD_METHOD              sum
             1386  LOAD_FAST                'y'
             1388  LOAD_FAST                'self'
             1390  LOAD_ATTR                y_labels
             1392  LOAD_CONST               -1
             1394  COMPARE_OP               ==
             1396  BINARY_SUBSCR    
             1398  LOAD_CONST               1
             1400  COMPARE_OP               ==
             1402  CALL_METHOD_1         1  '1 positional argument'
             1404  STORE_FAST               'FP'

 L. 429      1406  LOAD_GLOBAL              np
             1408  LOAD_METHOD              sum
             1410  LOAD_FAST                'y'
             1412  LOAD_FAST                'self'
             1414  LOAD_ATTR                y_labels
             1416  LOAD_CONST               -1
             1418  COMPARE_OP               ==
             1420  BINARY_SUBSCR    
             1422  LOAD_CONST               -1
             1424  COMPARE_OP               ==
             1426  CALL_METHOD_1         1  '1 positional argument'
             1428  STORE_FAST               'TN'

 L. 430      1430  LOAD_GLOBAL              np
             1432  LOAD_METHOD              sum
             1434  LOAD_FAST                'y'
             1436  LOAD_FAST                'self'
             1438  LOAD_ATTR                y_labels
             1440  LOAD_CONST               1
             1442  COMPARE_OP               ==
             1444  BINARY_SUBSCR    
             1446  LOAD_CONST               -1
             1448  COMPARE_OP               ==
             1450  CALL_METHOD_1         1  '1 positional argument'
             1452  STORE_FAST               'FN'

 L. 431      1454  LOAD_FAST                'TP'
             1456  LOAD_FAST                'TN'
             1458  BINARY_ADD       
             1460  LOAD_FAST                'TP'
             1462  LOAD_FAST                'FP'
             1464  BINARY_ADD       
             1466  LOAD_FAST                'FN'
             1468  BINARY_ADD       
             1470  LOAD_FAST                'TN'
             1472  BINARY_ADD       
             1474  BINARY_TRUE_DIVIDE
             1476  LOAD_FAST                'self'
             1478  STORE_ATTR               PC
         1480_1482  JUMP_FORWARD       1750  'to 1750'
           1484_0  COME_FROM            34  '34'

 L. 433      1484  LOAD_FAST                'self'
             1486  LOAD_ATTR                pca
             1488  LOAD_ATTR                coef
             1490  LOAD_ATTR                shape
             1492  LOAD_CONST               1
             1494  BINARY_SUBSCR    
             1496  STORE_FAST               'n'

 L. 434      1498  LOAD_GLOBAL              np
             1500  LOAD_METHOD              zeros
             1502  LOAD_FAST                'n'
             1504  CALL_METHOD_1         1  '1 positional argument'
             1506  LOAD_FAST                'self'
             1508  STORE_ATTR               y_pred

 L. 435      1510  SETUP_LOOP         1574  'to 1574'
             1512  LOAD_GLOBAL              range
             1514  LOAD_CONST               0
             1516  LOAD_FAST                'n'
             1518  CALL_FUNCTION_2       2  '2 positional arguments'
             1520  GET_ITER         
             1522  FOR_ITER           1572  'to 1572'
             1524  STORE_FAST               'ii'

 L. 436      1526  LOAD_FAST                'self'
             1528  LOAD_ATTR                alpha
             1530  LOAD_GLOBAL              np
             1532  LOAD_METHOD              dot
             1534  LOAD_FAST                'self'
             1536  LOAD_ATTR                pca
             1538  LOAD_ATTR                coef
             1540  LOAD_FAST                'ii'
             1542  LOAD_CONST               None
             1544  LOAD_CONST               None
             1546  BUILD_SLICE_2         2 
             1548  BUILD_TUPLE_2         2 
             1550  BINARY_SUBSCR    
             1552  LOAD_FAST                'self'
             1554  LOAD_ATTR                b
             1556  CALL_METHOD_2         2  '2 positional arguments'
             1558  BINARY_ADD       
             1560  LOAD_FAST                'self'
             1562  LOAD_ATTR                y_pred
             1564  LOAD_FAST                'ii'
             1566  STORE_SUBSCR     
         1568_1570  JUMP_BACK          1522  'to 1522'
             1572  POP_BLOCK        
           1574_0  COME_FROM_LOOP     1510  '1510'

 L. 438      1574  LOAD_GLOBAL              rg
             1576  LOAD_METHOD              phi
             1578  LOAD_FAST                'self'
             1580  LOAD_ATTR                y_pred
           1582_0  COME_FROM          1314  '1314'
             1582  CALL_METHOD_1         1  '1 positional argument'
             1584  LOAD_FAST                'self'
             1586  STORE_ATTR               y_pred

 L. 439      1588  LOAD_GLOBAL              np
             1590  LOAD_METHOD              ones
             1592  LOAD_FAST                'n'
             1594  CALL_METHOD_1         1  '1 positional argument'
             1596  LOAD_FAST                'self'
             1598  STORE_ATTR               y_labels

 L. 440      1600  LOAD_CONST               -1
             1602  LOAD_FAST                'self'
             1604  LOAD_ATTR                y_labels
             1606  LOAD_FAST                'self'
             1608  LOAD_ATTR                y_pred
             1610  LOAD_CONST               0.5
             1612  COMPARE_OP               <
             1614  STORE_SUBSCR     

 L. 441      1616  LOAD_GLOBAL              np
             1618  LOAD_METHOD              sum
             1620  LOAD_FAST                'self'
             1622  LOAD_ATTR                y
             1624  LOAD_FAST                'self'
             1626  LOAD_ATTR                y_labels
             1628  LOAD_CONST               1
             1630  COMPARE_OP               ==
             1632  BINARY_SUBSCR    
             1634  LOAD_CONST               1
             1636  COMPARE_OP               ==
             1638  CALL_METHOD_1         1  '1 positional argument'
             1640  STORE_FAST               'TP'

 L. 442      1642  LOAD_GLOBAL              np
             1644  LOAD_METHOD              sum
             1646  LOAD_FAST                'self'
             1648  LOAD_ATTR                y
             1650  LOAD_FAST                'self'
             1652  LOAD_ATTR                y_labels
             1654  LOAD_CONST               -1
             1656  COMPARE_OP               ==
             1658  BINARY_SUBSCR    
             1660  LOAD_CONST               1
             1662  COMPARE_OP               ==
             1664  CALL_METHOD_1         1  '1 positional argument'
             1666  STORE_FAST               'FP'

 L. 443      1668  LOAD_GLOBAL              np
             1670  LOAD_METHOD              sum
             1672  LOAD_FAST                'self'
             1674  LOAD_ATTR                y
             1676  LOAD_FAST                'self'
             1678  LOAD_ATTR                y_labels
             1680  LOAD_CONST               -1
             1682  COMPARE_OP               ==
             1684  BINARY_SUBSCR    
             1686  LOAD_CONST               -1
             1688  COMPARE_OP               ==
             1690  CALL_METHOD_1         1  '1 positional argument'
             1692  STORE_FAST               'TN'

 L. 444      1694  LOAD_GLOBAL              np
             1696  LOAD_METHOD              sum
             1698  LOAD_FAST                'self'
             1700  LOAD_ATTR                y
             1702  LOAD_FAST                'self'
             1704  LOAD_ATTR                y_labels
             1706  LOAD_CONST               1
             1708  COMPARE_OP               ==
             1710  BINARY_SUBSCR    
             1712  LOAD_CONST               -1
             1714  COMPARE_OP               ==
             1716  CALL_METHOD_1         1  '1 positional argument'
             1718  STORE_FAST               'FN'

 L. 445      1720  LOAD_FAST                'TP'
             1722  LOAD_FAST                'TN'
             1724  BINARY_ADD       
             1726  LOAD_FAST                'TP'
             1728  LOAD_FAST                'FP'
             1730  BINARY_ADD       
             1732  LOAD_FAST                'FN'
             1734  BINARY_ADD       
             1736  LOAD_FAST                'TN'
             1738  BINARY_ADD       
             1740  BINARY_TRUE_DIVIDE
             1742  LOAD_FAST                'self'
             1744  STORE_ATTR               PC

 L. 447      1746  LOAD_CONST               None
             1748  RETURN_VALUE     
           1750_0  COME_FROM          1480  '1480'

Parse error at or near `COME_FROM' instruction at offset 1582_0


class elastic_mlpcr_regression:
    __doc__ = '\n    This class provides elastic multinomial logistic pcr regression for functional\n    data using the SRVF framework accounting for warping\n    \n    Usage:  obj = elastic_mlpcr_regression(f,y,time)\n\n    :param f: (M,N) % matrix defining N functions of M samples\n    :param y: response vector of length N\n    :param Y: coded label matrix\n    :param warp_data: fdawarp object of alignment\n    :param pca: class dependent on fPCA method used object of fPCA\n    :param information\n    :param alpha: intercept\n    :param b: coefficient vector\n    :param Loss: logistic loss\n    :param PC: probability of classification\n    :param ylabels: predicted labels\n    :param \n\n    Author :  J. D. Tucker (JDT) <jdtuck AT sandia.gov>\n    Date   :  18-Mar-2018\n    '

    def __init__(self, f, y, time):
        """
        Construct an instance of the elastic_mlpcr_regression class
        :param f: numpy ndarray of shape (M,N) of N functions with M samples
        :param y: response vector
        :param time: vector of size M describing the sample points
        """
        a = time.shape[0]
        if f.shape[0] != a:
            raise Exception('Columns of f and time must be equal')
        self.f = f
        self.y = y
        self.time = time
        N1 = f.shape[1]
        m = y.max()
        self.n_classes = m
        self.Y = np.zeros((N1, m), dtype=int)
        for ii in range(0, N1):
            self.Y[(ii, y[ii] - 1)] = 1

    def calc_model(self, pca_method='combined', no=5, smooth_data=False, sparam=25, parallel=False):
        """
        This function identifies a logistic regression model with phase-variability
        using elastic pca

        :param f: numpy ndarray of shape (M,N) of N functions with M samples
        :param y: numpy array of N responses
        :param time: vector of size M describing the sample points
        :param pca_method: string specifing pca method (options = "combined",
                        "vert", or "horiz", default = "combined")
        :param no: scalar specify number of principal components (default=5)
        :param smooth_data: smooth data using box filter (default = F)
        :param sparam: number of times to apply box filter (default = 25)
        :param parallel: run model in parallel (default = F)
        :type f: np.ndarray
        :type time: np.ndarray
        """
        if smooth_data:
            self.f = fs.smooth_data(self.f, sparam)
        else:
            N1 = self.f.shape[1]
            self.warp_data = fs.fdawarp(self.f, self.time)
            self.warp_data.srsf_align(parallel=parallel)
            if pca_method == 'combined':
                out_pca = fpca.fdajpca(self.warp_data)
            else:
                if pca_method == 'vert':
                    out_pca = fpca.fdavpca(self.warp_data)
                else:
                    if pca_method == 'horiz':
                        out_pca = fpca.fdahpca(self.warp_data)
                    else:
                        raise Exception('Invalid fPCA Method')
        out_pca.calc_fpca(no)
        lam = 0
        R = 0
        Phi = np.ones((N1, no + 1))
        Phi[:, 1:no + 1] = out_pca.coef
        b0 = np.zeros(self.n_classes * (no + 1))
        out = fmin_l_bfgs_b((rg.mlogit_loss), b0, fprime=(rg.mlogit_gradient), args=(
         Phi, self.Y),
          pgtol=1e-10,
          maxiter=200,
          maxfun=250,
          factr=1e-30)
        b = out[0]
        B0 = b.reshape(no + 1, self.n_classes)
        alpha = B0[0, :]
        LL = rg.mlogit_loss(b, Phi, self.y)
        b = B0[1:no + 1, :]
        self.alpha = alpha
        self.b = b
        self.pca = out_pca
        self.LL = LL
        self.pca_method = pca_method

    def predict(self, newdata=None):
        """
        This function performs prediction on regression model on new data if available or current stored data in object
        Usage:  obj.predict()
                obj.predict(newdata)

        :param newdata: dict containing new data for prediction (needs the keys below, if None predicts on training data)
        :type newdata: dict
        :param f: (M,N) matrix of functions
        :param time: vector of time points
        :param y: truth if available
        :param smooth: smooth data if needed
        :param sparam: number of times to run filter
        """
        omethod = self.warp_data.method
        lam = self.warp_data.lam
        m = self.n_classes
        M = self.time.shape[0]
        if newdata != None:
            f = newdata['f']
            time = newdata['time']
            y = newdata['y']
            sparam = newdata['sparam']
            if newdata['smooth']:
                f = fs.smooth_data(f, sparam)
            else:
                q1 = fs.f_to_srsf(f, time)
                n = q1.shape[1]
                self.y_pred = np.zeros((n, m))
                mq = self.warp_data.mqn
                fn = np.zeros((M, n))
                qn = np.zeros((M, n))
                gam = np.zeros((M, n))
                for ii in range(0, n):
                    gam[:, ii] = uf.optimum_reparam(mq, time, q1[:, ii], omethod)
                    fn[:, ii] = uf.warp_f_gamma(time, f[:, ii], gam[:, ii])
                    qn[:, ii] = uf.f_to_srsf(fn[:, ii], time)

                m_new = np.sign(fn[self.pca.id, :]) * np.sqrt(np.abs(fn[self.pca.id, :]))
                qn1 = np.vstack((qn, m_new))
                U = self.pca.U
                no = U.shape[1]
                if self.pca.__class__.__name__ == 'fdajpca':
                    C = self.pca.C
                    TT = self.time.shape[0]
                    mu_g = self.pca.mu_g
                    mu_psi = self.pca.mu_psi
                    vec = np.zeros((M, n))
                    psi = np.zeros((TT, n))
                    binsize = np.mean(np.diff(self.time))
                    for i in range(0, n):
                        psi[:, i] = np.sqrt(np.gradient(gam[:, i], binsize))
                        vec[:, i] = geo.inv_exp_map(mu_psi, psi[:, i])

                    g = np.vstack((qn1, C * vec))
                    a = np.zeros((n, no))
                    for i in range(0, n):
                        for j in range(0, no):
                            tmp = g[:, i] - mu_g
                            a[(i, j)] = dot(tmp.T, U[:, j])

                else:
                    if self.pca.__class__.__name__ == 'fdavpca':
                        a = np.zeros((n, no))
                        for i in range(0, n):
                            for j in range(0, no):
                                tmp = qn1[:, i] - self.pca.mqn
                                a[(i, j)] = dot(tmp.T, U[:, j])

                    else:
                        if self.pca.__class__.__name__ == 'fdahpca':
                            a = np.zeros((n, no))
                            mu_psi = self.pca.psi_mu
                            vec = np.zeros((M, n))
                            TT = self.time.shape[0]
                            psi = np.zeros((TT, n))
                            binsize = np.mean(np.diff(self.time))
                            for i in range(0, n):
                                psi[:, i] = np.sqrt(np.gradient(gam[:, i], binsize))
                                vec[:, i] = geo.inv_exp_map(mu_psi, psi[:, i])

                            vm = self.pca.vec.mean(axis=1)
                            for i in range(0, n):
                                for j in range(0, no):
                                    a[(i, j)] = np.sum(dot(vec[:, i] - vm, U[:, j]))

                        else:
                            raise Exception('Invalid fPCA Method')
            for ii in range(0, n):
                for jj in range(0, m):
                    self.y_pred[(ii, jj)] = self.alpha[jj] + np.sum(a[ii, :] * self.b[:, jj])

            if y == None:
                self.y_pred = rg.phi(self.y_pred.reshape((1, n * m)))
                self.y_pred = self.y_pred.reshape((n, m))
                self.y_labels = np.argmax((self.y_pred), axis=1)
                self.PC = np.nan
            else:
                self.y_pred = rg.phi(self.y_pred.reshape((1, n * m)))
                self.y_pred = self.y_pred.reshape((n, m))
                self.y_labels = np.argmax((self.y_pred), axis=1)
                self.PC = np.zeros(m)
                cls_set = np.arange(0, m)
                for ii in range(0, m):
                    cls_sub = np.setdiff1d(cls_set, ii)
                    TP = np.sum(y[(self.y_labels == ii)] == ii)
                    FP = np.sum(y[np.in1d(self.y_labels, cls_sub)] == ii)
                    TN = np.sum(y[np.in1d(self.y_labels, cls_sub)] == self.y_labels[np.in1d(self.y_labels, cls_sub)])
                    FN = np.sum(np.in1d(y[(self.y_labels == ii)], cls_sub))
                    self.PC[ii] = (TP + TN) / (TP + FP + FN + TN)

                self.PCo = np.sum(y == self.y_labels) / self.y_labels.shape[0]
        else:
            n = self.pca.coef.shape[1]
            self.y_pred = np.zeros((n, m))
            for ii in range(0, n):
                for jj in range(0, m):
                    self.y_pred[(ii, jj)] = self.alpha[jj] + np.sum(self.pca.coef[ii, :] * self.b[:, jj])

            self.y_pred = rg.phi(self.y_pred.reshape((1, n * m)))
            self.y_pred = self.y_pred.reshape((n, m))
            self.y_labels = np.argmax((self.y_pred), axis=1)
            self.PC = np.zeros(m)
            cls_set = np.arange(0, m)
            for ii in range(0, m):
                cls_sub = np.setdiff1d(cls_set, ii)
                TP = np.sum(self.y[(self.y_labels == ii)] == ii)
                FP = np.sum(self.y[np.in1d(self.y_labels, cls_sub)] == ii)
                TN = np.sum(self.y[np.in1d(self.y_labels, cls_sub)] == self.y_labels[np.in1d(self.y_labels, cls_sub)])
                FN = np.sum(np.in1d(y[(self.y_labels == ii)], cls_sub))
                self.PC[ii] = (TP + TN) / (TP + FP + FN + TN)

            self.PCo = np.sum(y == self.y_labels) / self.y_labels.shape[0]
            return