
## traveling saleman

import numpy as np

class Ant:
    def __init__(self, startCity):
        self.startCity = startCity
        self.tabooList = [startCity,]
        self.currentCity = startCity

## Paths to files with matrix: distance and cost
number = 12
mainDir = "data/cities-47-"
distanceDir = mainDir + "distance.txt"
costDir = mainDir + "cost.txt"
pointsDir = f"results/points{number}.txt"
paretoDir = f"results/paretoFront{number}.txt"
delim = " "
matricesNumber = 2

## Parameters of algorithm
maxCycle = 250

antsInCity = 100

alpha = pheromoneWeight = 1
beta = cityVisibility = 2
q = exploitationOrExploration = 0.6
vaporizeFactor = 0.05
pheromoneZero = 0.1

## Read data from files
distance = np.genfromtxt(distanceDir, delimiter=delim)

#cost = np.genfromtxt(costDir, delimiter=delim)
cost = np.genfromtxt(costDir, delimiter=delim).T

print("Distance matrix:")
print(distance)
print("\nCost matrix:")
print(cost)

## Init variables  
distanceCopy = distance
distanceMax = np.max(distance)
distance = distance/np.max(distance)

costCopy = cost
costMax = np.max(cost)
cost = cost/np.max(cost)

matrices = [distance, cost]

cities = cost.shape[0]

maxes = [distanceMax, costMax]
paretoFront = []
paretoPath = []
points = []

## Build pheromone matrix with initial value
pheromone = np.ones((cities, cities)) * pheromoneZero

ants = []

print(f"Biggest distance beetwen two cities: {distanceMax}")

## Algorithm
for k in range(maxCycle):

    ## save points
    if k%10 == 9:
        print(f"Iter: {k+1}")
        pointsCopy = np.copy(points)
        for i in range(len(pointsCopy)):
            for j in range(matricesNumber):
                pointsCopy[i][j] *= maxes[j]
        saveToFile = np.reshape(pointsCopy, (len(pointsCopy),matricesNumber))
        np.savetxt(pointsDir, saveToFile, delimiter='\t')
        paretoFrontCopy = np.copy(paretoFront)
        
        for i in range(len(paretoFrontCopy)):
            for j in range(matricesNumber):
                paretoFrontCopy[i][j] *= maxes[j]
        saveToFile = np.reshape(paretoFrontCopy, (len(paretoFrontCopy),matricesNumber))
        np.savetxt(paretoDir, saveToFile, delimiter='\t')
        
    localPheromone = np.copy(pheromone)    
    ## create ants
    for i in range(cities):
        for j in range(antsInCity):
            ants.append(Ant(i))

    ## travel through the cities
    for i in range(cities-1):
        newLocalPheromone = np.copy(localPheromone)*(1-vaporizeFactor)
        for ant in ants:
            avalaibleCities = [x for x in np.arange(cities) if x not in ant.tabooList]

            ## calculate probability to choose the city
            sumHeuristic = 0
            for j in range(matricesNumber):
                sumHeuristic += matrices[j][ant.currentCity][avalaibleCities] ** beta
            sumTotal = np.sum( localPheromone[ant.currentCity][avalaibleCities] ** alpha / sumHeuristic )
            probabilityVector = localPheromone[ant.currentCity][avalaibleCities] ** alpha / sumHeuristic / sumTotal

            ## if exploration pick with probability, else pick the best
            if np.random.sample() < q:
                destinationCity = int(np.random.choice(avalaibleCities, 1, p=probabilityVector))
            else:
                destinationCity = avalaibleCities[list(probabilityVector).index(np.max(probabilityVector))]
            ant.currentCity = destinationCity
            ant.tabooList.append(destinationCity)
            newLocalPheromone[ant.tabooList[-2]][ant.tabooList[-1]] = localPheromone[ant.tabooList[-2]][ant.tabooList[-1]] + vaporizeFactor*pheromoneZero
        localPheromone = np.copy(newLocalPheromone)
            
    ## check that all roads are the same and add pheromone
    for ant in ants:
        path = np.zeros((matricesNumber,1))

        ## calculate travel parametr e.g. distance, cost
        for i in range(cities):
            index = i-1
            for j in range(matricesNumber):
                path[j] += matrices[j][ant.tabooList[index]][ant.tabooList[i]]

        ## Add solution
        points.append(path)
        
        ## update pareto solutions
        indexes = []
        flagAdd = 1
        for i in range(len(paretoFront)):
            validArray = np.linspace(0,0,matricesNumber)
            for j in range(matricesNumber):
                if path[j] < paretoFront[i][j]:
                    validArray[j] = 1
                elif path[j] > paretoFront[i][j]:
                    validArray[j] = -1
            if 1 in validArray and not -1 in validArray:
                indexes.append(i)
            if -1 in validArray and not 1 in validArray:
                flagAdd = 0
            if not 1 in validArray and not -1 in validArray:
                flagAdd = 0
        paretoFront = [i for j,i in enumerate(paretoFront) if j not in indexes]
        paretoPath = [i for j,i in enumerate(paretoPath) if j not in indexes]
        if flagAdd == 1:
            paretoFront.append(path)
            paretoPath.append(ant.tabooList)

    ## update pheromones for pareto path
    pheromone *= (1-vaporizeFactor)
    for elem, value in zip(paretoPath,paretoFront):
        for i in range(cities):
            index = i-1
            pheromoneAmount = 0
            for d in value:
                pheromoneAmount += d
            pheromone[elem[index]][elem[i]] += vaporizeFactor/pheromoneAmount*matricesNumber
    
    ants.clear()

pointsCopy = np.copy(points)
for i in range(len(pointsCopy)):
    for j in range(matricesNumber):
        pointsCopy[i][j] *= maxes[j]
saveToFile = np.reshape(pointsCopy, (len(pointsCopy),matricesNumber))
np.savetxt(pointsDir, saveToFile, delimiter='\t')

paretoFrontCopy = np.copy(paretoFront)
for i in range(len(paretoFrontCopy)):
    for j in range(matricesNumber):
        paretoFrontCopy[i][j] *= maxes[j]
saveToFile = np.reshape(paretoFrontCopy, (len(paretoFrontCopy),matricesNumber))
np.savetxt(paretoDir, saveToFile, delimiter='\t')
