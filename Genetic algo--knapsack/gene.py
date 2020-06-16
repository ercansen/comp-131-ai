# COMP 131: Artificial Intelligence
# Homework 4: Genetic Algorithms -- Knapsack Problem
# 
# Brandon Bell and Ercan Sen
# Date: 11-24-2019

import random

# Executes the crossover operation; generates two new genomes from two parents
def crossover(parent1, parent2):
    # Randomly picks a length for the segment before the crossover point
    ## It has a length 1-6 since a length 0 or 7 would indicate no crossover 
    ## between parents
    length_seg = random.randint(1,6)
    child1 = []
    child2 = []

    # Populates the children for the portion before the crossover point 
    for k in range(length_seg):
        child1.append(parent1[k])
        child2.append(parent2[k])

    # Populates the children for the portion after the crossover point 
    for l in range(7 - length_seg):
        child1.append(parent2[l+length_seg])
        child2.append(parent1[l+length_seg])

    return child1, child2

# Generates a random genome (a binary list)
## A value of 0 at index i represents item (i+1) is not in the knapsack
## A value of 1 at index i represents item (i+1) is in in the knapsack
def generator():
    genome = []
    for i in range(7):
        genome.append(random.randint(0,1))
    return genome

# Sorts a list of tuples by index 0 of each tuple in descending order
def sort_list(tup_list):
    return sorted(tup_list, key = lambda x: x[0], reverse = True)

# Class that holds the attributes and functions to solve the knapsack problem
class Knapsack():
    def __init__(self):
    	# Dimension; number of possible items we are trying to fit in knapsack
        self.dimen = 7
        # Max weight that the knapsack can carry
        self.maxweight = 120
        # Holds the population of genomes; initially empty
        self.population = []
        # Holds the fitness values for the population; initally empty
        self.fit = []
        # Weights of all the possible items
        self.weight = [20, 30, 60, 90, 50, 70, 30]
        # Importance values of all the possible items
        self.importance = [6, 5, 8, 7, 6, 9, 4]

    # Determines the fitness score for the given genome
    def fitness(self, genome):
        sum_weight = 0
        sum_importance = 0

        for i in range(self.dimen):
        	# Calculates the total weight of knapsack for the given genome
            sum_weight += genome[i]*self.weight[i]
            # Calculates the total importance of knapsack for the given genome
            sum_importance += genome[i]*self.importance[i]

        if sum_weight > self.maxweight:
        	# Exceeding max weight incurs a penalty of 200
            return (sum_importance - 200)
        else:
            return sum_importance

    # The main functionality for the genetic algorithm
    ## Populates the population list. Sorts the genomes by fitness.
    ## Culls the bottom 50%. Generates a new generation from the top 50%.
    ## Performs a mutation on the newly-generated genomes with 10% chance.
    def pool(self):
        if(len(self.population) == 0):
            # When population is empty, generates 100 random genomes
            for i in range(100):
                self.population.append(generator())
                # Calculates fitness scores for the random genomes
                self.fit.append(self.fitness(self.population[i]))
        else:
            for i in range(100):
            	# Calculates fitness scores for population from prev.iteration
                self.fit.append(self.fitness(self.population[i]))

        # Zips the genomes with fitness scores into a list of tuples
        fittest = list(zip(self.fit,self.population))
        # Sorts by fitness scores
        fittest = sort_list(fittest)

        # Places the fittest 50 genomes to the first 50 positions in population
        for i in range(50):
            self.population[i] = fittest[i][1]

        # Writes over (culls) the least fit 50 genomes in population
        # From 50 fittest parents, generates 50 children, using crossover
        for k in range(0, 49, 2):
            tuple = crossover(fittest[k][1], fittest[k+1][1])
            # Places the children into population
            self.population[50+k] = tuple[0]
            self.population[50+k+1] = tuple[1]

        # Applies mutation on newly-generated children
        for l in range(50,100):
            self.population[l] = self.mutation(self.population[l])

        # Replaces culled population's fitness scores with new population's
        self.fit = []
        for i in range(100):
            self.fit.append(self.fitness(self.population[i]))
        # Sorts population again to return fittest genome at final iteration
        fittest = list(zip(self.fit,self.population))
        fittest = sort_list(fittest)

        #Cleans the fitness values for the next iteration
        self.fit = []

    # Performs mutation operation; mutation is only valid if fitness increases
    ## Otherwise disregards the result of mutation and returns original genome
    def mutation(self, genome):
        mutated = genome

        # Mutation only occurs with 10% probability
        if(random.randint(1,100) <= 10):
            # Picks a random index of the genome
            i = random.randint(0,6)

            # Switches 0 to 1, or 1 to 0
            if (genome[i] == 0):
                mutated[i] = 1
            else:
                mutated[i] = 0

        # Returns the fittest of the original or the mutated genome
        if (self.fitness(genome) > self.fitness(mutated)):
            return genome
        else:
            return mutated


### MAIN
# Creates a Knapsack object
bag = Knapsack()
# Runs the genetic algorithm for 20 iterations by performing fringe operations
for i in range(20):
    bag.pool()

# Calculates sum_weight again for final print statement
sum_weight = 0

# Prints out what is in the knapsack in the optimal solution
print('The solution is: ', end=' ')
for i in range(bag.dimen):
	sum_weight += bag.population[0][i] * bag.weight[i]
	if (bag.population[0][i] == 1) and (sum(bag.population[0][i:]) > 1):
		print('Item ', i+1, ',', end=' ', sep='')
	elif (bag.population[0][i] == 1) and (sum(bag.population[0][i:]) == 1):
		print('Item ', i+1, '.', sep='')
		break

# Prints genome solution
print(bag.population[0])
# Prints out total weight and importance values for the items in knapsack 
print('Total weight is ', sum_weight, ', and total importance value is ', 
	  bag.fitness(bag.population[0]), sep='')
