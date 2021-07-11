"""Contains selection methods."""
import numpy as np


def elitism(rng, population, fitness, new_individuals, N):
    """Adds the `N` best individuals of the previous population to the next generation.

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
        concatenation of `new_individuals` with first `N` individuals in `population`.
    """
    if not new_individuals:
        return np.copy(population[:N])
    return np.concatenate((new_individuals, population[:N]), axis=0)


def roulette_wheel(rng, population, fitness, new_individuals, N):
    """Selects `N` individuals according to their fitness and adds them to the new individuals.

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
        concatenation of `new_individuals` with `N` individuals selected from `population`.
    """
    cum_probs = np.cumsum(fitness) / np.sum(fitness)
    coins = rng.random(N)
    to_select = coins <= cum_probs[:, np.newaxis]
    indices = np.argmax(to_select, axis=0)
    selected = population[indices]

    if not new_individuals:
        return selected
    return np.concatenate((new_individuals, selected), axis=0)
