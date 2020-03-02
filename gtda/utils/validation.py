"""Utilities for input validation."""
# License: GNU AGPLv3

import numbers
import numpy as np
import types

from sklearn.utils.validation import check_array

available_metrics = {
    'bottleneck': [('delta', numbers.Number, (0., 1.))],
    'wasserstein': [('p', int, (1, np.inf)),
                    ('delta', numbers.Number, (1e-16, 1.))],
    'betti': [('p', numbers.Number, (1, np.inf)),
              ('n_bins', int, (1, np.inf))],
    'landscape': [('p', numbers.Number, (1, np.inf)),
                  ('n_bins', int, (1, np.inf)),
                  ('n_layers', int, (1, np.inf))],
    'heat': [('p', numbers.Number, (1, np.inf)),
             ('n_bins', int, (1, np.inf)),
             ('sigma', numbers.Number, (0., np.inf))],
    'persistence_image': [('p', numbers.Number, (1, np.inf)),
                          ('n_bins', int, (1, np.inf)),
                          ('sigma', numbers.Number, (0., np.inf)),
                          ('weight_function', types.FunctionType,
                           None)],
    'silhouette': [('order', numbers.Number, (0, np.inf)),
                   ('n_bins', int, (1, np.inf))]}

available_metric_params = {metric: [p[0] for p in param_lst]
                           for metric, param_lst in available_metrics.items()}


def check_diagram(X, copy=False):
    """Input validation on a persistence diagram.

    """
    if len(X.shape) != 3:
        raise ValueError(f"X should be a 3d np.array: X.shape = {X.shape}.")
    if X.shape[2] != 3:
        raise ValueError(
            f"X should be a 3d np.array with a 3rd dimension of 3 components: "
            f"X.shape[2] = {X.shape[2]}.")

    homology_dimensions = sorted(list(set(X[0, :, 2])))
    for dim in homology_dimensions:
        if dim == np.inf:
            if len(homology_dimensions) != 1:
                raise ValueError(
                    f"np.inf is a valid homology dimension for a stacked "
                    f"diagram but it should be the only one: "
                    f"homology_dimensions = {homology_dimensions}.")
        else:
            if dim != int(dim):
                raise ValueError(
                    f"All homology dimensions should be integer valued: "
                    f"{dim} can't be cast to an int of the same value.")
            if dim != np.abs(dim):
                raise ValueError(
                    f"All homology dimensions should be integer valued: "
                    f"{dim} can't be cast to an int of the same value.")

    n_points_above_diag = np.sum(X[:, :, 1] >= X[:, :, 0])
    n_points_global = X.shape[0] * X.shape[1]
    if n_points_above_diag != n_points_global:
        raise ValueError(
            f"All points of all persistence diagrams should be above the "
            f"diagonal, X[:,:,1] >= X[:,:,0]. "
            f"{n_points_global - n_points_above_diag} points are under the "
            f"diagonal.")
    if copy:
        return np.copy(X)
    else:
        return X


def check_graph(X):
    return X


# Check the type and range of numerical parameters
def validate_params(parameters, references):
    """Function to automate the validation of hyperparameters.

    Parameters
    ----------
    parameters : dict, required
        Dictionary in which the keys are hyperparameter names and the
        corresponding values are hyperparameter values.

    references : dict, required
        Dictionary in which the keys are hyperparameter names and the
        corresponding values are lists. The first element of that list is a
        type. If that type is not an iterable, the second element can be one
        of:

        - ``None``, when only the type should be checked.
        - A tuple of two numbers, when the type is numerical. In this case,
          the first (resp. second) entry in the tuple defines a lower
          (resp. upper) bound constraining the value of the corresponding
          hyperparameter.
        - A list containing all possible allowed values for the
          corresponding hyperparameter.

        If that type is an iterable, the second element is a list that provides
        information to validate each element of that iterable. The first
        element of that list is the type of the elements of the iterable and
        the second element of that list can be one of:

        - ``None``, when only the type of the iterable elements should be
          checked.
        - A tuple of two numbers, when the type is numerical. In this case,
          the first (resp. second) entry in the tuple defines a lower
          (resp. upper) bound constraining the value of the corresponding
          iterable element.
        - A list containing all possible allowed values for the
          corresponding iterable element.

    """
    for key in references.keys():
        # Check type
        if not isinstance(parameters[key], references[key][0]):
            raise TypeError(
                f"Parameter {key} is of type {type(parameters[key])} while it "
                f"should be of type {references[key][0]}.")

        # If the key is a list, tuple, or numpy array, check element by element
        if references[key][0] == list or references[key][0] == tuple or \
           references[key][0] == np.ndarray:
            for parameter in parameters[key]:
                # If an element has to be an int, it can be passed as a float
                # that has no decimals, else we check the type of the element
                if references[key][1][0] == int:
                    if not isinstance(parameter, numbers.Number):
                        raise TypeError(
                            f"Parameter {key} is a {type(parameters[key])} of "
                            f"{references[key][1][0]} but contains an "
                            f"element of type {type(parameter)}.")
                    if not float(parameter).is_integer():
                        raise TypeError(
                            f"Parameter {key} is a {type(parameters[key])} of "
                            f"int but contains an element of type "
                            f"{type(parameter)} that is not an integer.")
                else:
                    # Otherwise just check for the type
                    if not isinstance(parameter, references[key][1][0]):
                        raise TypeError(
                            f"Parameter {key} is a {type(parameters[key])} of "
                            f"{references[key][1][0]}  but contains an "
                            f"element of type {type(parameter)}.")

                # If there is no parameter range to check, continue
                if references[key][1][1] is None:
                    continue
                # Check element range indicated by a tuple of 2 values
                if isinstance(references[key][1][1], tuple):
                    if (parameter < references[key][1][1][0] or
                            parameter > references[key][1][1][1]):
                        raise ValueError(
                            f"Parameter {key} is a {type(parameters[key])} "
                            f"containing {parameter} which should be in the "
                            f"range [{references[key][1][1][0]}, "
                            f"{references[key][1][1][1]}].")
                # Check if element is in a list
                elif isinstance(references[key][1][1], list):
                    if parameter not in references[key][1][1]:
                        raise ValueError(
                            f"Parameter {key} is a {type(parameters[key])} "
                            f"containing {parameter}, while it should only "
                            f"contain one of the following: "
                            f"{references[key][1][1]}.")
        else:
            # If only the type should be checked, continue
            if references[key][1] is None:
                continue

            # Check parameter range indicated by a tuple of 2 values
            if isinstance(references[key][1], tuple):
                if (parameters[key] < references[key][1][0] or
                        parameters[key] > references[key][1][1]):
                    raise ValueError(
                        f"Parameter {key} is {parameters[key]}, while it  "
                        f"should be in the range [{references[key][1][0]}, "
                        f"{references[key][1][1]}].")
            # Check if parameter is in a list
            elif isinstance(references[key][1], list):
                if parameters[key] not in references[key][1]:
                    raise ValueError(
                        f"Parameter {key} is {parameters[key]}, while it "
                        f"should be one of the following: "
                        f"{references[key][1]}.")


def validate_metric_params(metric, metric_params):
    if metric not in available_metrics.keys():
        raise ValueError(
            f"No metric called {metric}. Available metrics are "
            f"{list(available_metrics.keys())}.")

    for (param, param_type, param_values) in available_metrics[metric]:
        if param in metric_params.keys():
            input_param = metric_params[param]
            if not isinstance(input_param, param_type):
                raise TypeError(
                    f"{param} in params_metric is of type {type(input_param)} "
                    f" but must be an {param_type}.")
            if param_values is not None:
                if input_param < param_values[0]\
                        or input_param > param_values[1]:
                    raise ValueError(
                        f"{param} in param_metric should be between "
                        f"{param_values[0]} and {param_values[1]} but has "
                        f"been set to {input_param}.")

    for param in metric_params.keys():
        if param not in available_metric_params[metric]:
            raise ValueError(
                f"{param} in metric_param is not an available parameter. "
                f"Available metric_params are: "
                f"{available_metric_params[metric]}.")


def check_list_of_images(X, **kwargs):
    """Check a list of arrays representing images, by integrating
    through the input one by one. To pass a test when `kwargs` is ``None``,
    all images ``x``, ``y`` in `X` must satisfy:
        - ``x.ndim >= 2``,
        - ``all(np.isfinite(x))``,
        - ``x.shape == y.shape``.

    Parameters
    ----------
    X : list of ndarray
        Each entry of `X` corresponds to an image.

    kwargs : dict or None, optional, default: ``None``
        Parameters accepted by
        :func:`~gtda.utils.validation.check_list_of_arrays`.

    Returns
    -------
    X : list of ndarray
        as modified by :func:`~sklearn.utils.validation.check_array`

    """
    if hasattr(X, 'shape'):
        return check_array(X, **kwargs)
    else:
        kwargs_default = {'force_all_finite': True,
                          'ensure_2d': False, 'allow_nd': True,
                          'check_shapes': [('embedding_dimension',
                                            lambda x: x.shape,
                                            'The images should have exactly'
                                            'the same shape')]}
        kwargs_default.update(kwargs)
        return check_list_of_arrays(X, **kwargs_default)


def check_list_of_point_clouds(X, **kwargs):
    """Check a list of arrays representing point clouds, by integrating
    through the input one by one. To pass a test when `kwargs` is ``None``,
    all point clouds ``x``, ``y`` in X must satisfy:
        - ``x.ndim == 2``,
        - ``len(y.shape[1:]) == len(y.shape[1:])``.

    Parameters
    ----------
    X : list of ndarray, such that ``X[i].ndim==2`` (n_points, n_dimensions),
        or an array `X.dim==3`

    kwargs : dict or None, optional, default: ``None``
        Parameters accepted by
        :func:`~`gtda.utils.validation.check_list_of_arrays``.

    Returns
    -------
    X : list of input arrays
        as modified by :func:`~sklearn.utils.validation.check_array`

    """
    if hasattr(X, 'shape'):
        return check_array(X, **kwargs)
    else:
        kwargs_default = {'ensure_2d': False, 'force_all_finite': False,
                          'check_shapes': [('embedding_dimension',
                                            lambda x: x.shape[1:],
                                            'Not all point clouds have the same'
                                            'embedding dimension')]}
        kwargs_default.update(kwargs)
        return check_list_of_arrays(X, **kwargs_default)


def check_dimensions(X, get_property):
    """Check the dimensions of X are consistent, where the check is defined
    by get_property 'sample-wise'.
    Parameters
    ----------
    X: list of ndarray,
        Usually represents point clouds or images- see
        :func:`~`gtda.utils.validation.check_list_of_arrays``.

    get_property: function: ndarray -> _,
        Defines a property to be conserved, across all arrays (samples)
        in X.

    """
    from functools import reduce
    from operator import and_
    reference = get_property(X[0])
    return reduce(and_, map(lambda x: get_property(x) == reference, X[1:]),
                  True)


def check_list_of_arrays(X, check_shapes=list(), **kwargs):
    """Input validation on a list of lists, arrays, sparse matrices, or similar.

    The constraints are to be specified in `kwargs`. On top of
    parameters from :func:`~sklearn.utils.validation.check_array`,
    the optional parameters are listed below.

    Parameters
    ----------
    X : list
        Input list of objects to check / convert.

    check_shapes: list of tuples t, where t = (str, function to pass to
        check_dimensions, error message if test fails).
        The checks are applied in the order they are provided, only until
        the first failure.

    kwargs : dict or None, optional, default: ``None``
        Parameters accepted by :func:`~sklearn.utils.validation.check_array`.

    Returns
    -------
    X : list
        Output list of objects, each checked / converted by
        :func:`~sklearn.utils.validation.check_array`

    """

    # if restrictions on the dimensions of the input are imposed
    for (test_name, get_property, err_message) in check_shapes:
        if check_dimensions(X, get_property):
            continue
        else:
            raise ValueError(err_message)

    is_check_failed = False
    messages = []
    for i, x in enumerate(X):
        try:
            # TODO: verifythe behavior depending on copy.
            X[i] = check_array(x.reshape(1, *x.shape),
                               **kwargs).reshape(*x.shape)
            messages = ['']
        except ValueError as e:
            is_check_failed = True
            messages.append(str(e))
    if is_check_failed:
        raise ValueError("The following errors were raised" +
                         "by the inputs: \n" + "\n".join(messages))
    else:
        return X
