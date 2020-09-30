"""Feature extraction from curves."""
# License: GNU AGPLv3

from copy import deepcopy
from types import FunctionType

from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted, check_array

from ._functions import _AVAILABLE_FUNCTIONS, _implemented_function_recipes, \
    _parallel_featurization
from ..utils._docs import adapt_fit_transform_docs
from ..utils.validation import validate_params


@adapt_fit_transform_docs
class StandardFeatures(BaseEstimator, TransformerMixin):
    """Standard features from multi-channel curves.

    Applies functions to extract features from each channel in each
    multi-channel curve in a collection.

    Parameters
    ----------
    function : string or callable, optional, default: ``max``
        Function to transform a single-channel curve into scalar features per
        channel. Implemented functions are [``"identity"``, ``"argmin"``,
        `"argmax"``, ``"min"``, ``"max"``, ``"mean"``, ``"std"``, ``"median"``,
        ``"average"``].

    function_params : dict, optional, default: ``None``
        Additional keyword arguments for `function`. Passing ``None`` is
        equivalent to passing no arguments. Additionally:

        - If ``function == "average"``, the only argument is `weights`
          (np.ndarray or None, default: ``None``).
        - Otherwise, there are no arguments.

    n_jobs : int or None, optional, default: ``None``
        The number of jobs to use for the computation. ``None`` means 1 unless
        in a :obj:`joblib.parallel_backend` context. ``-1`` means using all
        processors.

    Attributes
    ----------
    n_channels_ : int

    effective_function_params_ : dict
        Dictionary containing all information present in `function_params` as
        well as on any relevant quantities computed in :meth:`fit`.

    """
    _hyperparameters = {
        "function": {"type": (str, FunctionType, list, tuple),
                     "in": tuple(_AVAILABLE_FUNCTIONS.keys()),
                     "of": {"type": (str, FunctionType, type(None)),
                            "in": tuple(_AVAILABLE_FUNCTIONS.keys())}},
        "function_params": {"type": (dict, type(None), list, tuple)},
        }

    def __init__(self, function="max", function_params=None, n_jobs=None):
        self.function = function
        self.function_params = function_params
        self.n_jobs = n_jobs

    def _validate_params(self):
        params = self.get_params().copy()
        _hyperparameters = deepcopy(self._hyperparameters)
        if not isinstance(self.function, str):
            _hyperparameters["function"].pop("in")
        try:
            validate_params(params, _hyperparameters, exclude=["n_jobs"])
        # Another go if we fail because function is a list/tuple containing
        # instances of FunctionType and the "in" key checks fail
        except ValueError as ve:
            end_string = f"which is not in " \
                         f"{tuple(_AVAILABLE_FUNCTIONS.keys())}."
            function = params["function"]
            if ve.args[0].endswith(end_string) \
                    and isinstance(function, (list, tuple)):
                params["function"] = [f for f in function
                                      if isinstance(f, str)]
                validate_params(params, _hyperparameters, exclude=["n_jobs"])
            else:
                raise ve

        if isinstance(self.function, (list, tuple)) \
                and isinstance(self.function_params, dict):
            raise TypeError("If `function` is a list/tuple then "
                            "`function_params` must be a list/tuple of dict, "
                            "or None.")
        elif isinstance(self.function, (str, FunctionType)) \
                and isinstance(self.function_params, (list, tuple)):
            raise TypeError("If `function` is a string or a callable "
                            "function then `function_params` must be a dict "
                            "or None.")

    def fit(self, X, y=None):
        """Compute :attr:`function_` and :attr:`effective_function_params_`.
        Then, return the estimator.

        This function is here to implement the usual scikit-learn API and hence
        work in pipelines.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_channels, n_bins)
            Input data. Collection of multi-channel curves.

        y : None
            There is no need for a target in a transformer, yet the pipeline
            API requires this parameter.

        Returns
        -------
        self : object

        """
        check_array(X, ensure_2d=False, allow_nd=True)
        if X.ndim != 3:
            raise ValueError("Input must be 3-dimensional.")
        self._validate_params()

        self.n_channels_ = X.shape[-2]

        if isinstance(self.function, str):
            self._function = _implemented_function_recipes[self.function]

            if self.function_params is None:
                self.effective_function_params_ = {}
            else:
                validate_params(self.function_params,
                                _AVAILABLE_FUNCTIONS[self.function])
                self.effective_function_params_ = self.function_params.copy()

        else:
            if isinstance(self.function, FunctionType):
                self._function = tuple([self.function] * self.n_channels_)
                if self.function_params is None:
                    self.effective_function_params_ = \
                        tuple([{}] * self.n_channels_)
                else:
                    self.effective_function_params_ = \
                        tuple(self.function_params.copy()
                              for _ in range(self.n_channels_))
            else:
                n_functions = len(self.function)
                if len(self.function) != self.n_channels_:
                    raise ValueError(
                        f"`function` has length {n_functions} while curves in "
                        f"`X` have {self.n_channels_} channels."
                        )

                if self.function_params is None:
                    self._effective_function_params = [{}] * self.n_channels_
                else:
                    self._effective_function_params = self.function_params

                n_function_params = len(self._effective_function_params)
                if n_function_params != self.n_channels_:
                    raise ValueError(
                        f"`function_params` has length {n_function_params} "
                        f"while curves in `X` have {self.n_channels_} "
                        f"channels."
                        )

                self._function = []
                self.effective_function_params_ = []
                for f, p in zip(self.function,
                                self._effective_function_params):
                    if isinstance(f, str):
                        validate_params(p, _AVAILABLE_FUNCTIONS[f])
                        self._function.append(_implemented_function_recipes[f])
                    else:
                        self._function.append(f)
                    self.effective_function_params_.append({} if p is None
                                                           else p.copy())
                self._function = tuple(self._function)
                self.effective_function_params_ = \
                    tuple(self.effective_function_params_)

        return self

    def transform(self, X, y=None):
        """Compute features of multi-channel curves.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_channels, n_bins)
            Input collection of multi-channel curves.

        y : None
            There is no need for a target in a transformer, yet the pipeline
            API requires this parameter.

        Returns
        -------
        Xt : ndarray of shape (n_samples, n_channels * n_features)
            Output collection of curves features. ``n_features`` denotes the
            number of features output byt :attr:`function_` for each channel of
            the multi-channel curve.

        """
        check_is_fitted(self)
        Xt = check_array(X, ensure_2d=False, allow_nd=True)
        if Xt.ndim != 3:
            raise ValueError("Input must be 3-dimensional.")
        if Xt.shape[-2] != self.n_channels_:
            raise ValueError(f"Number of channels must be the same as in "
                             f"`fit`. Passed {Xt.shape[-2]}, expected "
                             f"{self.n_channels_}.")

        Xt = _parallel_featurization(Xt, self._function,
                                     self.effective_function_params_,
                                     self.n_jobs)

        return Xt
