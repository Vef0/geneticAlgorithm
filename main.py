import random
from collections.abc import Callable
from typing_extensions import TypeAlias

if __name__ == '__main__':
    def genetic_algorithm():

        # Population

        Individual: TypeAlias = list[int]
        Population: TypeAlias = list[Individual]

        def generate_individual(length: int) -> Individual:
            random.shuffle(individual := list(range(1, length + 1)))
            return individual

        def generate_population(pop_size: int, individual_length: int) -> Population:
            return [generate_individual(individual_length) for _ in range(pop_size)]

        # Fitness

        FitnessFunc: TypeAlias = Callable[[Individual], int]

        # -- Number of clashes (the lower the better)

        def fitness(individual: Individual) -> int:
            clashes = 0
            for i in range(len(individual) - 1):
                for j in range(i + 1, len(individual)):
                    if abs(individual[j] - individual[i]) == j - i:
                        clashes += 1
            return clashes

            # Selection

        IndividualPair: TypeAlias = tuple[Individual, Individual]
        SelectionFunc: TypeAlias = Callable[[Population, FitnessFunc], IndividualPair]

        # -- Roulette wheel selection

        def roulette_selection(population: Population, fitness: FitnessFunc) -> IndividualPair:
            parents = random.choices(
                population=population,
                weights = [fitness(individual) for individual in population],
                k=2,
            )
            return parents[0], parents[1]

        # Crossover

        CrossoverFunc: TypeAlias = Callable[[IndividualPair], IndividualPair]

        # -- Ordered crossover

        def ordered_crossover(parents: IndividualPair) -> IndividualPair:
            parent_a, parent_b = parents
            split_idx = random.randint(1, len(parent_a) - 1)
            offspring_x = parent_a[:split_idx] + list(
                filter(lambda pos: pos not in parent_a[:split_idx], parent_b)
            )
            offspring_y = parent_a[:split_idx] + list(
                filter(lambda pos: pos not in parent_b[:split_idx], parent_a)
            )
            return offspring_x, offspring_y

        # Mutation

        MutationFunc: TypeAlias = Callable[[Individual, float], Individual]

        def swap_mutation(individual: Individual, mutation_rate: float) -> Individual:
            if random.random() < mutation_rate:
                pos1 = random.randint(0, len(individual) - 1)
                pos2 = random.randint(0, len(individual) - 1)
                individual[pos1], individual[pos2] = individual[pos2], individual[pos1]
            return individual

        def run_evolution(pop_size: int, individual_length: int, fitness_limit: int = 0, mutation_prob: float = 0.3, n_iter: int = 100) -> Individual:
            population = generate_population(pop_size, individual_length)
            for i in range(n_iter):
                population = sorted(population, key=fitness)
                if fitness(population[0]) <= fitness_limit:
                    break
                population = compute_next_generation(population, mutation_prob, n_elites)
            return sorted(population, key=fitness)[0]
        # https://www.youtube.com/watch?v=c-B5mIq04bg