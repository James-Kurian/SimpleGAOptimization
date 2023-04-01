import math
import numpy as np

class MA:
    def __init__(self, function, crossRate, mutationRate, maxIterations, strLength, popSize, maxLocalSearchJump, neighbourSize, localSearchIterations, printGenerations):
        self.function = function
        self.crossRate = crossRate
        self.mutationRate = mutationRate
        self.maxIterations = maxIterations
        self.bestChrom = None
        self.maxFit = -float("inf")
        self.currGen = 0
        self.strLength = strLength
        self.popSize = popSize
        self.pop = self.initPop()
        self.maxLocalSearchJump = maxLocalSearchJump
        self.neighbourSize = neighbourSize
        self.localSearchIterations = localSearchIterations
        self.printGenerations = printGenerations

    def run(self):
        if (self.printGenerations):
            print("Gen 0:")
            print(self.pop)

        while(self.currGen < self.maxIterations):
            weights = self.fitness()
            self.crossover(weights)
            self.mutate()
            self.localSearch()
            self.currGen+=1
            if (self.printGenerations):
                print("Gen " + str(self.currGen) + ":")
                print(self.pop)

    def initPop(self):
        return np.array(["".join(np.random.randint(0,2,self.strLength).astype(str).tolist()) for x in range(self.popSize)])
    
    def fitness(self):
        fitness = np.array([])
        minFit = float("inf")
        for chrom in self.pop:
            x = int(chrom,2)
            chromFit = self.function(x)
            if (chromFit < minFit):
                minFit = chromFit
            if(chromFit >= self.maxFit):
                self.bestChrom = chrom
                self.maxFit = chromFit
            fitness = np.append(fitness, chromFit)
        fitness = fitness+abs(minFit)
        sum = np.sum(fitness)
        if (sum==0):
            return fitness.fill(1/len(self.pop))
        return (fitness)/sum
    
    def crossover(self, weights):
        newPop = []
        for doCross in np.random.rand(math.floor(len(self.pop)/2)) <= self.crossRate:
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
        self.pop = np.array(newPop)
    
    def mutate(self):
        newPop = []
        for chrom in self.pop:
            if (mutationRate > np.random.rand()):
                index = math.floor(np.random.rand()*strLength)
                if (chrom[index]=="0"):
                    newPop.append(chrom[:index] + "1" + chrom[index+1:])
                else:
                    newPop.append(chrom[:index] + "0" + chrom[index+1:])
            else:
                newPop.append(chrom)
        self.pop=np.array(newPop)

    def localSearch(self):
        for i in range(len(self.pop)):
            val = int(self.pop[i], 2)
            iterations = 0
            while(iterations < self.localSearchIterations):
                neighbours = self.getNeighbours(val)
                val = self.findBest(neighbours, val)
                iterations+=1
            self.pop[i]=bin(val).replace("0b","").zfill(self.strLength)
    
    def getNeighbours(self, val):
        arr = []
        for i in range(self.neighbourSize):
            add = np.random.randint(0,2)
            #this code looks stupid
            if (add == 1):
                arr.append(val + math.ceil(np.random.rand()*self.maxLocalSearchJump))
            else:
                arr.append(val - math.ceil(np.random.rand()*self.maxLocalSearchJump))
        return arr
    
    def findBest(self, arr, base):
        bestVal = base
        bestFit = self.function(base)
        for val in arr:
            fit=self.function(val)
            if (fit>bestFit):
                bestVal=val
                bestFit=fit
        return bestVal

    def getPop(self):
        return self.pop
    
    def getBestChrom(self):
        return self.bestChrom

if __name__ == "__main__":
    crossRate = 0.5
    maxIterations = 60
    popSize = 4
    strLength = 5
    mutationRate = 0.3
    maxLocalSearchJump = 2
    neighbourSize = 2
    localSearchIterations = 10
    seed = math.floor(np.random.rand()*1000)
    print("Seed: " + str(seed)) 
    printGenerations = True
    np.random.seed(seed)
    simpleGeneticAlgorithm = MA(lambda x : (-x**2 + 8*x + 15), crossRate, mutationRate, maxIterations, strLength, popSize, maxLocalSearchJump, neighbourSize, localSearchIterations, printGenerations)
    startPop = simpleGeneticAlgorithm.getPop()
    simpleGeneticAlgorithm.run()

    print("")
    print ("Initial Pop: " + np.array_str(startPop))
    print ("Final Pop:   " + np.array_str(simpleGeneticAlgorithm.getPop()))
    print("Best Chrom: " + simpleGeneticAlgorithm.getBestChrom())
    print("Seed: " + str(seed)) 