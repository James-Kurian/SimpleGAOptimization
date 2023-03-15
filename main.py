import math
import numpy as np

class GA:
    def __init__(self, function, crossRate, maxIterations, strLength, popSize, printGenerations):
        self.function = function
        self.crossRate = crossRate
        self.maxIterations = maxIterations
        self.bestChrom = None
        self.maxFit = -float("inf")
        self.currGen = 0
        self.converged = False
        self.strLength = strLength
        self.popSize = popSize
        self.pop = self.initPop()
        self.printGenerations = printGenerations

    def run(self):
        if (self.printGenerations):
            print("Gen 0:")
            print(self.pop)

        while(self.currGen < self.maxIterations and not self.converged):
            weights = self.fitness(self.pop)
            self.pop = self.crossover(weights)
            if ((self.pop==self.pop[0]).all()):
                self.converged = True
            self.currGen+=1
            if (self.printGenerations):
                print("Gen " + str(self.currGen) + ":")
                print(self.pop)

    def initPop(self):
        return np.array(["".join(np.random.randint(0,2,self.strLength).astype(str).tolist()) for x in range(self.popSize)])
    
    def fitness(self, pop):
        fitness = np.array([])
        minFit = float("inf")
        for chrom in pop:
            x = int(chrom,2)
            chromFit = self.function(x)
            if (chromFit < minFit):
                minFit = chromFit
            if(chromFit >= self.maxFit):
                self.bestChrom = chrom
                self.maxFit = chromFit
            fitness = np.append(fitness, chromFit)
        fitness = fitness+abs(minFit)
        self.pop = pop
        return (fitness)/np.sum(fitness)
    
    def crossover(self, weights):
        newPop = []
        for doCross in np.random.rand(math.floor(len(self.pop)/2)) <= crossRate:
            #np.random.choice takes two arguments. First, an array of elems to choose. Second, an array with weights with respect to the first array. Effectivley this selection acts like a roulette wheel
            childOne = np.random.choice(self.pop, p=weights)
            childTwo = np.random.choice(self.pop, p=weights)
            if (doCross and childOne != childTwo):
                #idk what cross over function to use... so i used the one in the document.  
                splitIndex = math.floor(1+np.random.rand()*4)
                newPop.extend([childOne[:splitIndex] + childTwo[splitIndex:], childTwo[:splitIndex] + childOne[splitIndex:]])
            else:
                newPop.extend([childOne,childTwo])
        if (len(self.pop)%2==1):
            childOne = np.random.choice(self.pop, p=weights)
            if (np.random.rand() <= crossRate):
                childTwo = np.random.choice(self.pop, p=weights)
                splitIndex = math.floor(1+np.random.rand()*4)
                newPop.extend(np.random.choice([childOne[:splitIndex] + childTwo[splitIndex:], childTwo[:splitIndex] + childOne[splitIndex:]]))
            else:
                newPop.extend(childOne)
        return np.array(newPop)
    
    def getPop(self):
        return self.pop
    
    def getBestChrom(self):
        return self.bestChrom
    
    def isConverged(self):
        return self.converged

if __name__ == "__main__":
    crossRate = 0.5
    maxIterations = 60
    popSize = 4
    strLength = 5
    seed = math.floor(np.random.rand()*1000)
    printGenerations = True
    np.random.seed(seed)
    simpleGeneticAlgorithm = GA(lambda x : (-x**2 + 8*x + 15), crossRate, maxIterations, strLength, popSize, printGenerations)
    startPop = simpleGeneticAlgorithm.getPop()
    simpleGeneticAlgorithm.run()

    print("")
    print ("Initial Pop: " + np.array_str(startPop))
    print ("Final Pop:   " + np.array_str(simpleGeneticAlgorithm.getPop()))
    print("Best Chrom: " + simpleGeneticAlgorithm.getBestChrom())
    print("Converged: " + str(simpleGeneticAlgorithm.isConverged()))
    print("Seed: " + str(seed))