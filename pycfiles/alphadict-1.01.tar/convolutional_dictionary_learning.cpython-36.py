# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/tom/.local/miniconda/lib/python3.6/site-packages/alphacsc/convolutional_dictionary_learning.py
# Compiled at: 2019-06-11 08:01:24
# Size of source mod 2**32: 14070 bytes
from sklearn.base import TransformerMixin
from sklearn.exceptions import NotFittedError
from .update_z_multi import update_z_multi
from .utils.dictionary import get_D, get_uv
from .learn_d_z_multi import learn_d_z_multi
from .loss_and_gradient import construct_X_multi
DOC_FMT = "{desc}\n\n    Parameters\n    ----------\n\n    Problem Specs\n\n    n_atoms : int\n        The number of atoms to learn.\n    n_times_atom : int\n        The support of the atom.\n    loss : {{ 'l2' | 'dtw' | 'whitening' }}\n        Loss for the data-fit term. Either the norm l2 or the soft-DTW.\n    loss_params : dict\n        Parameters of the loss.\n    rank1 : boolean\n        If set to True, learn rank 1 dictionary atoms.\n    window : boolean\n        If set to True, re-parametrizes the atoms with a temporal Tukey window.\n    uv_constraint : {{'joint' | 'separate'}}\n        The kind of norm constraint on the atoms:\n\n        - :code:`'joint'`: the constraint is ||[u, v]||_2 <= 1\n        - :code:`'separate'`: the constraint is ||u||_2 <= 1 and ||v||_2 <= 1\n    sort_atoms : boolean\n        If True, the atoms are sorted by explained variances.\n\n\n    Global algorithm\n    {algorithm}\n    n_iter : int\n        The number of alternate steps to perform.\n    eps : float\n        Stopping criterion. If the cost descent after a uv and a z update is\n        smaller than eps, return.\n    reg : float\n        The regularization parameter.\n    lmbd_max : 'fixed' | 'scaled' | 'per_atom' | 'shared'\n        If not fixed, adapt the regularization rate as a ratio of lambda_max:\n\n        - :code:`'scaled'`: the regularization parameter is fixed as a ratio of\n          its maximal value at init *i.e.*\n          :math:`lambda` = reg * lmbd_max(uv_init).\n        - :code:`'shared'`: the regularization parameter is set at each\n          iteration as a ratio of its maximal value for the current dictionary\n          estimate *i.e.* :math:`lambda` = reg * lmbd_max(uv_hat).\n        - :code:`'per_atom'`: the regularization parameter is set per atom and\n          at each iteration as a ratio of its maximal value for this atom\n          *i.e.* :math:`lambda[k]` = reg * lmbd_max(uv_hat[k]).\n\n\n    Z-step parameters\n\n    solver_z : str\n        The solver to use for the z update. Options are\n        {{'l_bfgs' (default) | 'lgcd'}}.\n    solver_z_kwargs : dict\n        Additional keyword arguments to pass to update_z_multi.\n    use_sparse_z : boolean\n        Use sparse lil_matrices to store the activations.\n    unbiased_z_hat : boolean\n        If set to True, the value of the non-zero coefficients in the returned\n        z_hat are recomputed with reg=0 on the frozen support.\n\n\n    D-step parameters\n\n    solver_d : str\n        The solver to use for the d update. Options are\n        'alternate' | 'alternate_adaptive' (default) | 'joint'\n    solver_d_kwargs : dict\n        Additional keyword arguments to provide to update_d\n    D_init : str or array\n        The initial atoms with shape (n_atoms, n_channels + n_times_atoms) or\n        (n_atoms, n_channels, n_times_atom) or an initialization scheme str in\n        {{'kmeans' | 'ssa' | 'chunk' | 'random'}}.\n    D_init_params : dict\n        Dictionnary of parameters for the kmeans init method.\n\n\n    Technical parameters\n\n    n_jobs : int\n        The number of parallel jobs.\n    verbose : int\n        The verbosity level.\n    callback : func\n        A callback function called at the end of each loop of the\n        coordinate descent.\n    random_state : int | None\n        State to seed the random number generator.\n    raise_on_increase : boolean\n        Raise an error if the objective function increase.\n\n    "
DEFAULT = dict(desc='Base class for convolutional dictionary learning algorithms',
  algorithm="\n\n    algorithm : {'batch' | 'greedy' | 'online'}\n        Dictionary learning algorithm.\n    algorithm_params : dict\n        parameter of the global algorithm.")

class ConvolutionalDictionaryLearning(TransformerMixin):
    """ConvolutionalDictionaryLearning"""

    def __init__(self, n_atoms, n_times_atom, n_iter=60, n_jobs=1, loss='l2', loss_params=dict(gamma=0.1, sakoe_chiba_band=10, ordar=10), rank1=True, window=False, uv_constraint='separate', solver_z='l_bfgs', solver_z_kwargs={}, solver_d='alternate_adaptive', solver_d_kwargs={}, reg=0.1, lmbd_max='fixed', eps=1e-10, D_init=None, D_init_params={}, algorithm='batch', algorithm_params={}, alpha=0.8, batch_size=1, batch_selection='random', use_sparse_z=False, unbiased_z_hat=False, verbose=10, callback=None, random_state=None, name='_CDL', raise_on_increase=True, sort_atoms=False):
        self.n_atoms = n_atoms
        self.n_times_atom = n_times_atom
        self.reg = reg
        self.loss = loss
        self.loss_params = loss_params
        self.rank1 = rank1
        self.window = window
        self.uv_constraint = uv_constraint
        self.sort_atoms = sort_atoms
        self.n_iter = n_iter
        self.eps = eps
        self.algorithm = algorithm
        self.algorithm_params = algorithm_params
        self.lmbd_max = lmbd_max
        self.solver_z = solver_z
        self.solver_z_kwargs = solver_z_kwargs
        self.use_sparse_z = use_sparse_z
        self.unbiased_z_hat = unbiased_z_hat
        self.solver_d = solver_d
        self.solver_d_kwargs = solver_d_kwargs
        self.D_init = D_init
        self.D_init_params = D_init_params
        self.n_jobs = n_jobs
        self.verbose = verbose
        self.callback = callback
        self.random_state = random_state
        self.raise_on_increase = raise_on_increase
        self.name = name
        self._D_hat = None

    def fit(self, X, y=None):
        """Learn a convolutional dictionary from the set of signals X.
        """
        res = learn_d_z_multi(X,
          (self.n_atoms), (self.n_times_atom), reg=(self.reg),
          lmbd_max=(self.lmbd_max),
          loss=(self.loss),
          loss_params=(self.loss_params),
          rank1=(self.rank1),
          window=(self.window),
          uv_constraint=(self.uv_constraint),
          algorithm=(self.algorithm),
          algorithm_params=(self.algorithm_params),
          n_iter=(self.n_iter),
          eps=(self.eps),
          solver_z=(self.solver_z),
          solver_z_kwargs=(self.solver_z_kwargs),
          solver_d=(self.solver_d),
          solver_d_kwargs=(self.solver_d_kwargs),
          D_init=(self.D_init),
          D_init_params=(self.D_init_params),
          use_sparse_z=(self.use_sparse_z),
          unbiased_z_hat=False,
          verbose=(self.verbose),
          callback=(self.callback),
          random_state=(self.random_state),
          n_jobs=(self.n_jobs),
          name=(self.name),
          raise_on_increase=(self.raise_on_increase),
          sort_atoms=(self.sort_atoms))
        self._pobj, self._times, self._D_hat, self._z_hat, self.reg_ = res
        self.n_channels_ = X.shape[1]
        return self

    def fit_transform(self, X, y=None):
        """Learn a convolutional dictionary and returns sparse codes.
        """
        self.fit(X)
        z_hat = self._z_hat
        if self.unbiased_z_hat:
            if self.verbose > 0:
                print('Refitting the activation to avoid amplitude bias...', end='',
                  flush=True)
            z_hat, _, _ = update_z_multi(X,
              (self._D_hat), z0=z_hat, n_jobs=(self.n_jobs), reg=0,
              freeze_support=True,
              solver=(self.solver_z),
              solver_kwargs=(self.solver_z_kwargs),
              loss=(self.loss),
              loss_params=(self.loss_params))
            if self.verbose > 0:
                print('done')
        return z_hat

    def transform(self, X):
        """Returns sparse codes associated to the signals X for the dictionary.
        """
        self._check_fitted()
        z_hat, _, _ = update_z_multi(X,
          (self._D_hat), reg=(self.reg_), n_jobs=(self.n_jobs), solver=(self.solver_z),
          solver_kwargs=(self.solver_z_kwargs),
          loss=(self.loss),
          loss_params=(self.loss_params))
        if self.unbiased_z_hat:
            if self.verbose > 0:
                print('Refitting the activation to avoid amplitude bias...', end='',
                  flush=True)
            z_hat, _, _ = update_z_multi(X,
              (self._D_hat), z0=z_hat, n_jobs=(self.n_jobs), reg=0,
              freeze_support=True,
              solver=(self.solver_z),
              solver_kwargs=(self.solver_z_kwargs),
              loss=(self.loss),
              loss_params=(self.loss_params))
            if self.verbose > 0:
                print('done')
        return z_hat

    def transform_inverse(self, z_hat):
        """Reconstruct the signals from the given sparse codes.
        """
        return construct_X_multi(z_hat, self._D_hat, self.n_channels_)

    def _check_fitted(self):
        if self._D_hat is None:
            raise NotFittedError('Fit must be called before accessing the dictionary')

    @property
    def D_hat_(self):
        """array: dictionary in full rank mode.

        shape (n_atoms, n_channels, n_times_atom)
        """
        self._check_fitted()
        if self._D_hat.ndim == 3:
            return self._D_hat
        else:
            return get_D(self._D_hat, self.n_channels_)

    @property
    def uv_hat_(self):
        """array: dictionary in rank 1 mode. If `rank1 = False`, this is an
        approximation of the dictionary obtained through svd.

        shape (n_atoms, n_channels + n_times_atom)
        """
        self._check_fitted()
        if self._D_hat.ndim == 3:
            return get_uv(self._D_hat)
        else:
            return self._D_hat

    @property
    def u_hat_(self):
        """array: spatial map of the dictionary. If `rank1 = False`, this is an
        approximation of the dictionary obtained through svd.

        , shape (n_atoms, n_channels)
        """
        return self.uv_hat_[:, :self.n_channels_]

    @property
    def v_hat_(self):
        """array: temporal patterns of the dictionary. If `rank1 = False`, this
        is an approximation of the dictionary obtained through svd.

        shape (n_atoms, n_times_atom)
        """
        return self.uv_hat_[:, self.n_channels_:]

    @property
    def z_hat_(self):
        """array: Sparse code associated to the signals used to fit the model.

        shape (n_trials, n_atoms, n_times_valid)
        """
        self._check_fitted()
        return self._z_hat

    @property
    def pobj_(self):
        """list: Objective function value at each step of the alternate minimization.
        """
        self._check_fitted()
        return self._pobj

    @property
    def times_(self):
        """list: Cumulative time for each iteration of the coordinate descent.
        """
        self._check_fitted()
        return self._times


class BatchCDL(ConvolutionalDictionaryLearning):
    _default = {}
    _default.update(DEFAULT)
    _default['desc'] = 'Batch algorithm for convolutional dictionary learning'
    _default['algorithm'] = '    Batch algorithm\n'
    __doc__ = (DOC_FMT.format)(**_default)

    def __init__(self, n_atoms, n_times_atom, reg=0.1, n_iter=60, n_jobs=1, solver_z='lgcd', solver_z_kwargs={}, unbiased_z_hat=False, solver_d='alternate_adaptive', solver_d_kwargs={}, rank1=True, window=False, uv_constraint='separate', lmbd_max='scaled', eps=1e-10, D_init=None, D_init_params={}, verbose=10, random_state=None, sort_atoms=False):
        super().__init__(n_atoms,
          n_times_atom, reg=reg, n_iter=n_iter, solver_z=solver_z,
          solver_z_kwargs=solver_z_kwargs,
          rank1=rank1,
          window=window,
          uv_constraint=uv_constraint,
          unbiased_z_hat=unbiased_z_hat,
          sort_atoms=sort_atoms,
          solver_d=solver_d,
          solver_d_kwargs=solver_d_kwargs,
          eps=eps,
          D_init=D_init,
          D_init_params=D_init_params,
          algorithm='batch',
          lmbd_max=lmbd_max,
          raise_on_increase=True,
          loss='l2',
          use_sparse_z=False,
          n_jobs=n_jobs,
          verbose=verbose,
          callback=None,
          random_state=random_state,
          name='BatchCDL')


class GreedyCDL(ConvolutionalDictionaryLearning):
    _default = {}
    _default.update(DEFAULT)
    _default['desc'] = 'Greedy batch algorithm for convolutional dictionary learning'
    _default['algorithm'] = '    Greedy batch algorithm\n'
    __doc__ = (DOC_FMT.format)(**_default)

    def __init__(self, n_atoms, n_times_atom, reg=0.1, n_iter=60, n_jobs=1, solver_z='lgcd', solver_z_kwargs={}, unbiased_z_hat=False, solver_d='alternate_adaptive', solver_d_kwargs={}, rank1=True, window=False, uv_constraint='separate', lmbd_max='scaled', eps=1e-10, D_init=None, D_init_params={}, verbose=10, random_state=None, sort_atoms=False):
        super().__init__(n_atoms,
          n_times_atom, reg=reg, n_iter=n_iter, solver_z=solver_z,
          solver_z_kwargs=solver_z_kwargs,
          rank1=rank1,
          window=window,
          uv_constraint=uv_constraint,
          unbiased_z_hat=unbiased_z_hat,
          sort_atoms=sort_atoms,
          solver_d=solver_d,
          solver_d_kwargs=solver_d_kwargs,
          eps=eps,
          D_init=D_init,
          D_init_params=D_init_params,
          algorithm='greedy',
          lmbd_max=lmbd_max,
          raise_on_increase=True,
          loss='l2',
          use_sparse_z=False,
          n_jobs=n_jobs,
          verbose=verbose,
          callback=None,
          random_state=random_state,
          name='GreedyCDL')