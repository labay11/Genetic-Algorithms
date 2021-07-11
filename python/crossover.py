"""Contains crossover operations."""
import numpy as np


def single_point(rng, population, fitness, new_individuals, N):
    """Add `N` individuals based on the crossovering two randomly selected individuals by a middle point.

    If there are no new individuals, then they crossovering occurs between the individuals in the previous generation.

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
    N : int
        the number of elitist individuals to append to the new individuals

    Returns
    -------
    numpy.ndarray
        concatenation of `new_individuals` with `N` crossover individuals.
    """
    if new_individuals is not None and new_individuals.shape[0] > 1:
        pop = new_individuals
        has_new_individuals = True
    else:
        pop = population
        has_new_individuals = False

    pop_size, n_params = population.shape
    crossover_points = np.zeros((N, n_params), dtype=population.dtype)

    for i in range(N):
        i1, i2 = rng.integers(pop_size, size=2)
        crossover_location = rng.integers(1, n_params)
        if rng.random() < 0.5:
            i1, i2 = i2, i1
        crossover_points[i, :crossover_location] = pop[i1, :crossover_location]
        crossover_points[i, crossover_location:] = pop[i2, crossover_location:]

    if not has_new_individuals:
        return crossover_points
    return np.concatenate((new_individuals, crossover_points), axis=0)


def two_point(rng, population, fitness, new_individuals, N):
    """Add `N` individuals based on the crossovering two randomly selected individuals by a middle point.

    If there are no new individuals, then they crossovering occurs between the individuals in the previous generation.

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
    N : int
        the number of elitist individuals to append to the new individuals

    Returns
    -------
    numpy.ndarray
        concatenation of `new_individuals` with `N` crossover individuals.
    """
    if new_individuals is not None and new_individuals.shape[0] > 1:
        pop = new_individuals
        has_new_individuals = True
    else:
        pop = population
        has_new_individuals = False

    pop_size, n_params = population.shape
    crossover_points = np.zeros((N, n_params), dtype=population.dtype)

    for i in range(N):
        i1, i2 = rng.integers(pop_size, size=2)
        c1, c2 = rng.integers(2, n_params)
        while c1 == c2:
            c2 = rng.integers(1, n_params)
        if c1 > c2:
            c1, c2 = c2, c1
        if rng.random() < 0.5:
            i1, i2 = i2, i1

        crossover_points[i, :c1] = pop[i1, :c1]
        crossover_points[i, c1:c2] = pop[i2, c1:c2]
        crossover_points[i, c2:] = pop[i1, c2:]

    if not has_new_individuals:
        return crossover_points
    return np.concatenate((new_individuals, crossover_points), axis=0)
