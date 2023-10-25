import random
import math

# random.seed(42)

tsp_data = [
    [0, 2451, 713, 1018, 1631, 1374, 2408, 213, 2571, 875, 1420, 2145, 1972],
    [2451, 0, 1745, 1524, 831, 1240, 959, 2596, 403, 1589, 1374, 357, 579],
    [713, 1745, 0, 355, 920, 803, 1737, 851, 1858, 262, 940, 1453, 1260],
    [1018, 1524, 355, 0, 700, 862, 1395, 1123, 1584, 466, 1056, 1280, 987],
    [1631, 831, 920, 700, 0, 663, 1021, 1769, 949, 796, 879, 586, 371],
    [1374, 1240, 803, 862, 663, 0, 1681, 1551, 1765, 547, 225, 887, 999],
    [2408, 959, 1737, 1395, 1021, 1681, 0, 2493, 678, 1724, 1891, 1114, 701],
    [213, 2596, 851, 1123, 1769, 1551, 2493, 0, 2699, 1038, 1605, 2300, 2099],
    [2571, 403, 1858, 1584, 949, 1765, 678, 2699, 0, 1744, 1645, 653, 600],
    [875, 1589, 262, 466, 796, 547, 1724, 1038, 1744, 0, 679, 1272, 1162],
    [1420, 1374, 940, 1056, 879, 225, 1891, 1605, 1645, 679, 0, 1017, 1200],
    [2145, 357, 1453, 1280, 586, 887, 1114, 2300, 653, 1272, 1017, 0, 504],
    [1972, 579, 1260, 987, 371, 999, 701, 2099, 600, 1162, 1200, 504, 0],
]

# Correct answer = 6465
# 1 -> 8 -> 3 -> 4 -> 10 -> 11 -> 6 -> 5 -> 13 -> 12 -> 2 -> 9 -> 7 -> 1

class Individual:
    def __init__(self, sequence):
        self.sequence = sequence
        self.sequenceLen = len(sequence)

    def getFitness(self):
        val = 0
        for i in range(len(self.sequence)-1):
            val+= tsp_data[self.sequence[i]-1][self.sequence[i+1]-1]
        val += tsp_data[self.sequence[-1]-1][0]
        return val
    
    
class World:
    def __init__(self):
        self.population = 300
        self.mutationChance = 0.5
        self.maxIterations = 200
        self.repetitions = 0
        self.maxRepetitions = 20
        self.hasConverged = False

    def spawn(self):
        self.individuals = [self.generateIndividual() for i in range(self.population)]
        # self.displayIndis(self.individuals)
        # print('\n')
    
    def getBestIndividual(self):
        sortedIndis = self.individuals
        sortedIndis.sort(key = lambda x : x.getFitness(),reverse=False)
        # self.displayIndis(C)
        # print(sortedIndis[0] , sortedIndis[0].getFitness())

    def generateIndividual(self):
        sequence = list(range(2,len(tsp_data) + 1))
        random.shuffle(sequence)
        sequence  = [1] + sequence
        return Individual(sequence)
    
    def displayIndis(self, indis):
        for i in indis:
            print(i.sequence , i.getFitness())

    def newGeneration(self):
        offsprings = []
        for i in range(self.population):
            mother = self.getParent()
            father = self.getParent()

            while(mother == father):
                father = self.getParent()
            offspring1, offspring2 = self.getCrossover(mother,father)
            offsprings.append(offspring1)
            offsprings.append(offspring2)
        offsprings += self.individuals
        offsprings.sort(key = lambda x : x.getFitness(),reverse=False)
        if self.individuals[0].getFitness() == offsprings[0].getFitness():
            self.repetitions += 1
            if self.repetitions >= self.maxRepetitions:
                self.hasConverged = True
        else:
            self.repetitions = 0
        self.individuals = offsprings[0:self.population]
    
    def getParent(self):
        if random.random() > 0.5:
            # Tournament Selection
            return self.tournamentSelection()
        else : 
            # Biased Random Selection
            return self.biasedRandomSelection()
    
    def tournamentSelection(self):
        candidate1 = self.individuals[random.randint(0,self.population-1)]
        candidate2 = self.individuals[random.randint(0,self.population-1)]

        while(candidate1 == candidate2):
            candidate2 = self.individuals[random.randint(0,self.population-1)]
        
        if candidate1.getFitness() < candidate2.getFitness():
            return candidate1
        else:
            return candidate2
    
    def biasedRandomSelection(self):
        fitnessSum = 0
        for i in self.individuals:
            fitnessSum += i.getFitness()
        proportions = [fitnessSum/i.getFitness() for i in self.individuals]
        proportionsSum = sum(proportions)
        normalizedProportions = [p/proportionsSum for p in proportions]

        cumulativeProportions = []
        cumulativeTotal = 0
        for np in normalizedProportions:
            cumulativeTotal += np
            cumulativeProportions.append(cumulativeTotal)

        selectedValue = random.random()

        for i in range(self.population):
            if selectedValue <= cumulativeProportions[i]:
                return self.individuals[i]
        return self.individuals[random.randint(0,self.population - 1)] # Redundant

    def getCrossover(self,mother,father):
        headLength = -(-(mother.sequenceLen)//2)
        headSequence1 = mother.sequence[0:headLength]
        tailSequence1 = list(set(father.sequence) - set(headSequence1))

        headSequence2 = father.sequence[0:headLength]
        tailSequence2 = list(set(mother.sequence) - set(headSequence2))

        offSpring1 = Individual(headSequence1 + tailSequence1)
        offSpring2 = Individual(headSequence2 + tailSequence2)

        offSpring1 = self.mutate(offSpring1)
        offSpring2 = self.mutate(offSpring2)
        return offSpring1,offSpring2
    
    def mutate(self,offspring):
        if random.random() < self.mutationChance:
            if random.random() < 0.1:
                newOffspring = self.swapMutate(offspring)
            else:
                newOffspring = self.rotateMutate(offspring)
            return newOffspring
    
        return offspring
    
    def swapMutate(self,offspring):
        sequence = offspring.sequence
        index1 = random.randint(1,offspring.sequenceLen-1)
        index2 = random.randint(1,offspring.sequenceLen-1)
        while index1 == index2:
            index2 = random.randint(1,offspring.sequenceLen-1)
        sequence[index1],sequence[index2] = sequence[index2],sequence[index1]

        return Individual(sequence)

    def rotateMutate(self,offspring):
        sequence = offspring.sequence
        index1 = random.randint(1,offspring.sequenceLen-1)
        index2 = random.randint(1,offspring.sequenceLen-1)
        while index1 == index2 and index1<index2:
            index1 = random.randint(1,offspring.sequenceLen-1)
            index2 = random.randint(1,offspring.sequenceLen-1)
        sequence[index1:index2+1] = sequence[index1:index2+1][::-1]
        return Individual(sequence)
            



if __name__ == "__main__":
    w = World()
    w.spawn()
    i=0
    while i < w.maxIterations and w.hasConverged == False:
        print("Generation : " , i , w.individuals[0].sequence, w.individuals[0].getFitness())
        w.newGeneration()
        i+=1
    