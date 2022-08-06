import random
import string
import time

"""Genetic algorithm that, given an initial string, generates individuals and optimizes the solutions 
    until it arrives at an individual that resembles the initial problem."""

#Constants
PROBLEM = "when mr bilbo baggins of bag end announced that he would shortly be celebrating his eleventy first birthday"
PROBLEMSIZE = len(PROBLEM)
MAX_SIZE = 20

ALPHABET = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 
    'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', ' ']

class Individual:
    """Represents an individual of the genetic algorithm"""
    def __init__(self, value):
        """Initializes an Individual object
        Args:
            value (str) : string "genome" of the Individual
        """
        self.value = value
        self.fitness = self.calcFitness()

    def calcFitness(self):    
        """Calculates the similarity of the individual with the problem to be solved """
        counter = 0
        #Count whether the individual's character is present in the problem.
        for i in range(len(self.value)):
            if self.value[i] == PROBLEM[i]:
                counter += 1
        return counter 

    def mutate(self):
        """Randomly changes a gene of the individual in question"""
        n = len(self.value)
        randomGen = random.randint(0, n - 1)
        #Change the individual's gen with a random char
        self.value = self.value[:randomGen] + random.choice(ALPHABET) + self.value[randomGen+1:]
        self.value = self.value.lower()         
        self.fitness = self.calcFitness() 

#Main module

def generateInitialPopulation(size):
    """Initializes an initial population for the algorithm"""
    population = []
    for i in range(0, size):
        individual = Individual(getRandomString().lower())
        population.append(individual)
    return population

def getRandomString():
    """Creates a randomly generated string"""
    return "".join(random.choice(ALPHABET) for _ in range(PROBLEMSIZE))

 
def createIndividualFromParents(offspring, parent1, parent2):
    """Creates a new individual from two parents, the new individual has genes from both parents
    Args:
        offspring (int) : boolean value defining which child is being created
        parent1 (str) : string value of the parent 1
        parent2 (str) : string value of the parent 2
    """
    chromosome = ""
    for i in range(len(parent1)):
        flag = random.randint(0,1)
        # From both parents we get two childrens
        if (offspring == 0):
            if (flag == 0):
                chromosome += parent1[i]
            else:
                chromosome += parent2[i]
        else:
            if (flag == 1):
                chromosome += parent1[i]
            else:
                chromosome += parent2[i]      
    return chromosome        


def sortPopulation(population):
    """Sort the population according to their similarity to the problem to be solved
    Args:
        population (list) : list of all the individuals
    """
    n = len(population)

    swapped = False

    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if population[j].fitness < population[j + 1].fitness:
                swapped = True
                population[j], population[j + 1] = population[j + 1], population[j]
        if not swapped:
            return

def crossover(population):
    """Crosses between individuals in the population, priority is given to the best ones
    Args:
        population (list) : list of all the individuals
    """
    newPopulation = []

    crossOversAmount = int(MAX_SIZE / 2)
    for i in range(crossOversAmount):
        parentOne = population[i]
        parentTwo = population[i + 1]

        #Both parents can have two childrens
        randomValue1 = createIndividualFromParents(0, parentOne.value, parentTwo.value)
        randomValue2 = createIndividualFromParents(1, parentOne.value, parentTwo.value)

        offspring1 = Individual(randomValue1)
        offspring2 = Individual(randomValue2)

        newPopulation.append(offspring1)
        newPopulation.append(offspring2)
        
    return newPopulation        

def writeReport(report):
    f = open("reports.txt", "a")
    f.write(report + "\n")
    f.close()

def main():
    
    population = generateInitialPopulation(MAX_SIZE)

    sortPopulation(population)

    generation = 0
    ##Get the best individual, given that the population is sorted descedendly
    terminationCriterion = population[0].fitness

    ##Start counting time 
    start_time = time.time()

    #Until convergence repeat
    while terminationCriterion < PROBLEMSIZE:
        population = crossover(population)
        for i in range(len(population)):
            population[i].mutate()
        sortPopulation(population)    
        generation += 1
        ## Given that the population is ordered from best to worst
        terminationCriterion = population[0].fitness
        
        print("Mejor individuo: %s | Semejanza %d" % (population[0].value, population[0].fitness))
    ##End time countdown
    end_time = time.time() - start_time

    print("\nMejor individuo encontrado después de %d generaciones: %s | Semejanza: %d" %(generation, population[0].value, population[0].fitness))        
    print("Tiempo transcurrido: %.6f segundos"%end_time)

    report = population[0].value + " | " + "Semejanza: " + str(population[0].fitness) + " | " + "Tiempo Transcurrido: " + str(end_time) + " | " + "Generación: " + str(generation)
    writeReport(report)
    print("Reporte generado!")


if __name__ == "__main__":
    main()    