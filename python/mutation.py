"""Contains mutation operations."""
import numpy as np


def full(rng, population, fitness, new_individuals, p, params):
    """Mutates all individuals in the new generation by another value in the whole region.

    Parameters
    ----------
    rng : numpy.randon.RandomGenerator
        the random number generator to use
    population : numpy.ndarray
        the previous generation sorted by fitness
    fitness : numpy.ndarray
        the fitness of the individuals in population sorted from highest to lowest.
    new_individuals : numpy.ndarray
        the new individuals that have been added using other functions.
    p : float
        the probability of mutation
    params : list of :class:`Parameter`
        the parameters of the GA.

    Returns
    -------
    numpy.ndarray
        the new individuals mutated
    """
    if not new_individuals:
        return None

    pop_size, _ = new_individuals.shape

    for i, param in enumerate(params):
        to_mutate = rng.random(pop_size) < p
        count = np.count_nonzero(p)
        if count == 0:
            continue
        values = rng.
        if param.data_type == 'discrete':
            data[p, i] = rng.integers(low=int(param.range[0]), high=int(param.range[1]) + 1, size=count)
        else:
            data[p, i] = np.clip(data[p, i] + (rng.random(count) * 2 - 1) * param.scale_factor,
                                 param.range[0], param.range[1])
            # with a probability of p^2 apply a mutation in the full range
            full_p = (rng.random(n_points) < sim_param['proba_mutation']) & p
            count = np.count_nonzero(full_p)
            if count > 0:
                data[full_p, i] = rng.random(count) * (param.range[1] - param.range[0]) + param.range[0]


def scaled_mutation():
    # scale factor like in stopos


def gaussian_mutation():
