from itertools import combinations

import numpy as np
# import yaml
import json


class Parameter:

    def __init__(self, name, bounds, dtype):
        self.name = name
        self.bounds = bounds
        self.dtype = dtype

    def is_discrete(self):
        return self.dtype == 'int'

    def next(self, current=None):
        if self.is_discrete():
            if current - 1 < self.bounds[0] or current + 1 > self.bounds[1]:
                return np.random.randint(self.bounds[0], self.bounds[1] + 1)
            return int(current + (-1)**np.random.randint(2))
        else:
            return np.random.random() * (self.bounds[1] - self.bounds[0]) + self.bounds[0]

    @classmethod
    def from_file(cls, param):
        return cls(param['name'], (param['min'], param['max']), param['type'])


class Parameters:

    def __init__(self, params):
        self.params = params

    def __len__(self):
        return len(self.params)

    def __getitem__(self, i):
        return self.params[i]

    def generate_population(self, size):
        A = np.random.random((size, len(self.params)))

        for i, param in enumerate(self.params):
            A[:, i] = A[:, i] * (param.bounds[0] - param.bounds[1]) + param.bounds[0]
            if param.is_discrete():
                A[:, i] = np.floor(A[:, i])

        return A

    @classmethod
    def from_file(cls, list_of_parameters):
        return cls([Parameter.from_file(param) for param in list_of_parameters])


class GA:

    def __init__(self, parameters, population_size, number_best_candidates, prob_crossover, prob_mutation):
        self.params = parameters
        self.pop_size = population_size
        self.number_best_candidates = number_best_candidates
        self.p_cross = prob_crossover
        self.p_mutation = prob_mutation

        self.rng = np.random.default_rng()

    def run(self, generations, fitness_func):

        population = self.params.generate_population(self.pop_size)

        best_candidates = []

        for generation in range(generations):
            print(f'\tGenetation {generation}/{generations} started. ', end='')

            fitness = fitness_func(population)
            new_fitness, new_pop = self.select(fitness, population)
            new_pop = self.crossover(new_pop)
            new_pop = self.mutate(new_pop)

            best_individual = population[np.argmax(fitness)]
            if len(new_pop) > self.pop_size:
                population[0, :] = best_individual[:]
                population[1:, :] = self.rng.choice(new_pop, size=self.pop_size - 1)
            else:
                population[0, :] = best_individual[:]
                population[1:len(new_pop), :] = new_pop
                population[len(new_pop):, :] = self.rng.choice(population, size=self.pop_size - len(new_pop) - 1)
            best_candidates.append((np.max(fitness), best_individual))
            print('OK')

        return best_candidates

    def select(self, fitness, population):
        """
        order = fitness.argsort()

        fitness_ord = np.take_along_axis(fitness, order, axis=0)
        cum_prob_ord = fitness_ord.cumsum() / fitness_ord.sum()

        coins = np.random.random(self.number_best_candidates)

        to_select = coins <= cum_prob_ord[:, np.newaxis]
        incides = (to_select == True).argmax(axis=0)

        new_pop = population[order][incides]
        """
        minf, maxf = np.min(fitness), np.max(fitness)
        scaled = fitness - minf
        prob = scaled / np.sum(scaled)

        pop_with_f = np.concatenate((np.reshape(fitness, (self.pop_size, 1)), population), axis=1)

        pop_with_f = self.rng.choice(pop_with_f, axis=0, size=self.number_best_candidates, p=prob)
        return pop_with_f[:, 0], pop_with_f[:, 1:]

    def crossover(self, population):
        pop_size, params = population.shape
        new_individuals = []
        for j, k in combinations(range(pop_size), 2):
            if np.random.random() < self.p_cross:
                cut_point = np.random.randint(1, params)
                a = self.cross(population[j].copy(), population[k].copy(), cut_point)
                new_individuals.append(a)

        return np.concatenate((population, new_individuals))

    def cross(self, a, b, point):
        a[point:] = b[point:]
        return a

    def mutate(self, population):
        pop_size, params = population.shape
        coins = np.random.random((pop_size, params))

        to_mutate_x, to_mutate_y = np.nonzero(coins < self.p_mutation)
        for c, g in zip(to_mutate_x, to_mutate_y):
            population[c, g] = self.params[g].next(population[c, g])

        return population

    @classmethod
    def from_file(cls, params_file):
        extension = params_file.rsplit('.', 1)[-1].lower()
        if extension == 'json':
            return cls.from_json_file(params_file)
        elif extension in ['yaml', 'yml']:
            return cls.from_yaml_file(params_file)
        else:
            raise ValueError('Unrecognized file format {}'.format(params_file))

    def from_json_file(cls, params_file):
        with open(params_file) as f:
            props = json.loads(f.read())

        return cls(
            Parameters.from_file(props['parameters']),
            props['population_size'],
            props['number_best_candidates'],
            props['prob_crossover'],
            props['prob_mutation']
        )

    def from_yaml_file(cls, params_file):
        with open(params_file) as f:
            props = yaml.load(f.read())

        return cls(
            Parameters.from_file(props['parameters']),
            props['population_size'],
            props['number_best_candidates'],
            props['prob_crossover'],
            props['prob_mutation']
        )


if __name__ == '__main__':
    params = [
        Parameter('x', (-10, 10), 'float'),
        Parameter('y', (1, 5), 'int'),
        Parameter('z', (0, 2 * np.pi), 'float')
    ]

    def func(X):
        return np.power(X[:, 0], X[:, 1]) * np.sin(X[:, 2])

    ga = GA(Parameters(params), 100, 70, 0.7, 0.1)
    bests = ga.run(100, func)
    for f, best in bests:
        print(f'x={best[0]}, y={best[1]}, z={best[2]} -> f={f}')
