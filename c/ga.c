#include <stdio.h>
#include <stdlib.h>
#include <time.h>

struct Parameter {
    int discrete;
    float min;
    float max;
};

int randint(int min, int max) {
    return (rand() % (max + 1 - min) + min);
}

float randfloat(float min, float max) {
    return (((float) rand()) / ((float) RAND_MAX)) * (max - min) + min;
}

void sort(
    int population_size,
    float *fitnesses,
    float **pop
) { // insertion sort
    int i,j;
    float f;
    float *chromosome;
    for (i = 1; i <= population_size; i++) {
        f = fitnesses[i];
        chromosome = pop[i];
        for(j = i - 1; j >= i && f < fitnesses[j]; j--) {
            fitnesses[j + 1] = fitnesses[j];
            pop[j + 1] = pop[j];
        }
        fitnesses[j + 1] = f;
        pop[j + 1] = chromosome;
    }
}

/* Generates the initial population from the parameters.
 *
 * @param population_size the number of chromosomes to generate
 * @param params the list of parameters (genes)
 * @param n_params total number of parameters (can be inferred from the list but since we have it calculated before just pass it)
 * @param population output matrix, each row is a chromosome with `n_params` genes
 */
void generate_population(
    int population_size,
    struct Parameter * params,
    int n_params,
    float population[population_size][n_params]
) {
    int i, j;
    for (i = 0; i < population_size; i++) {
        for (j = 0; j < n_params; j++) {
            if (params[j].discrete)
                population[i][j] = (float) randint((int) params[j].min, (int) params[j].max);
            else
                population[i][j] = randfloat(params[j].min, params[j].max);
        }
    }
}

/* Selects the next generation accoridng to the roulette wheel method.
 *
 * @param population_size the number of chromosomes to generate
 * @param number_best_candidates the number of chromosomes to select
 * @param population the population used in the previous generation
 * @param fitnesses the fidelity for each chromosome
 * @param selected list of indices corresponding to the candidates selected from the population
 */
void selection(
    int population_size,
    int number_best_candidates,
    int n_params,
    float population[population_size][n_params],
    float fitnesses[population_size],
    float new_population[population_size][n_params]
) {
    sort(population_size, fitnesses, (float **) population);

    float prob[population_size];
    float sum_fit = 0;

    int i, j;
    for (i = 0; i < population_size; i++)
        sum_fit += fitnesses[i];
    for (i = 0; i < population_size; i++)
        prob[i] = fitnesses[i] / sum_fit;

    int selected_candidates = 0;
    float rnd = 0;
    while (selected_candidates < number_best_candidates) {
        rnd = randfloat(0.f, 1.f);
        for (i = 0; i < population_size; i++) {
            if (rnd < prob[i]) {
            	for (j = 0; j < n_params; j++)
            		new_population[selected_candidates][j] = population[i][j];
            	++selected_candidates;
                break;
            }
        }
    }
}

float mutate(float gene, struct Parameter param) {
	if (param.discrete) {
		return (float) randint(param.min, param.max);
	} else {
		return randfloat(param.min, param.max);
	}
}

void crossover(
    float p_cross,
    float p_mut,
    int n_params,
    struct Parameter *params,
    float *parent1,
    float *parent2,
    float *child1,
    float *child2
) {
    int point, i;

    if (randfloat(0, 1) < p_cross) {
    	point = randint(1, n_params - 1);
    } else {
    	point = n_params;
    }

    for (i = 0; i < point; i++) {
		child1[i] = mutate(parent1[i], params[i]);
		child2[i] = mutate(parent2[i], params[i]);
    }
	for (i = point; i < n_params; i++) {
		child1[i] = mutate(parent2[i], params[i]);
		child2[i] = mutate(parent1[i], params[i]);
	}
}

void ga(
	int n_params,
    struct Parameter * params,
    int population_size,
    int number_best_candidates,
    float p_cross,
    float p_mut,
    int generations,
    float (*fitness_func)(float *),
    float output[generations][n_params + 1]
) {
    float population[population_size][n_params];
    generate_population(population_size, params, n_params, population);

    float new_population[population_size][n_params];
    float fitnesses[population_size];
    int *selected;
    int i, j, p1, p2;
    float child1[n_params], child2[n_params];

    for (int generation = 0; generation < generations; generation++) {
    	printf("Generation %d of %d...", generation, generations);
        for (i = 0; i < population_size; i++)
            fitnesses[i] = fitness_func(population[i]);

        selection(population_size, number_best_candidates, n_params, population, fitnesses, new_population);

        printf(" Best fitness: %.5f.\n", fitnesses[0]);
        output[generation][0] = fitnesses[0];
        for (i = 1; i < n_params + 1; i++)
        	output[generation][i] = population[0][i - 1];

        i = number_best_candidates;
        while (i < population_size) {
        	p1 = randint(0, number_best_candidates - 1);
        	p2 = randint(0, number_best_candidates - 2);

        	crossover(p_cross, p_mut, n_params, params, population[p1], population[p2], child1, child2);
        	for (j = 0; j < n_params; j++) {
        		new_population[i][j] = child1[j];
        		new_population[i + 1][j] = child2[j];
        	}

        	i += 2; // can break if n_best is odd an pop_size is even
        }

        for (i = 0; i < population_size; i++)
        	for (j = 0; j < n_params; j++)
        		population[i][j] = new_population[i][j];        
    }
}

float fitness(float *params) {
    return params[0] * params[1];
}

int main(int argc, char *argv[]) {
	time_t t;
	srand((unsigned) time(&t));

	size_t n_params = 2;
    struct Parameter params[] = {
    	{0, 0.f, 1.f},
    	{0, -5.f, 4.f}
    };

    int population_size = 100;
    int number_best_candidates = 70;
    int p_cross = 0.7;
    int p_mut = 0.2;
    int generations = 100;
    float bests[generations][n_params + 1];
    ga(n_params, params, population_size, number_best_candidates, p_cross, p_mut, generations, fitness, bests);

    printf("\n\nResults:\n");
    for (int i = 0; i < generations; i++) {
    	printf("Generation %d: x=%.5f, y=%.5f -> F=%.5f\n", i, bests[i][1], bests[i][2], bests[i][0]);
    }
    
    return 0;
}
