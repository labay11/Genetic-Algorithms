import numpy as np


class Parameter:
    """Represents a single parameter.

    dtype : np.dtype
        https://numpy.org/doc/stable/reference/arrays.dtypes.html#specifying-and-constructing-data-types
    """

    def __init__(self, name, range, dtype):
        self.name = name
        self.range = range

        if not isinstance(dtype, np.dtype):
            raise ValueError('Passed parameter type is not an instance of numpy.dtype')
        self.dtype = dtype

    @classmethod
    def from_config(cls, data):
        return cls(data['name'], (data['min'], data['max']), np.dtype(data['type']))


class GA:
    """Genetic algorithm"""

    def __init__(self, generations, population, parameters, gen_functions, fitness_func):
        self.generations = generations
        self.parameters = parameters
        self.funcs = gen_functions
        self.fitness_func = fitness_func

        self.dtype_genome = np.dtype([p.dtype for p in self.parameters])

    @classmethod
    def from_config(cls, data, fitness_func):
        params = [Parameter.from_config(p) for p in data['parameters']]
        gen_functions = [(func['name'], paramtopasstothefunction) for func in data['functions']]
        return cls(data['generations'], data['population'], params, gen_functions, fitness_func)
