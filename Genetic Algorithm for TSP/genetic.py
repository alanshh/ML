import random
import csv
import os
import numpy as np
import sys
import time

def getLength(tour):
    """
    Get length of given tour

    Parameters:
        tour(numpy.ndarray): Array of indices (of cities according to csv file) representing the tour order
    
    Returns:
        length(numpy.float64): Length of the tour
    """
    length = 0
    for i in range(nCities-1):
        length += distances[tour[i], tour[i+1]]
    length += distances[tour[nCities-1], tour[0]]
    return length

def selection(pop):
    """
    Run selection on given population using fitness proportionate selection (FPS) and elitism

    Parameters:
        pop(numpy.ndarray): population to select surviving tours from. Contains arrays of the tours (array of city indices)

    Returns:
        newPop(numpy.ndarray): Selected tours (through FPS)
        eliteTours(numpy.ndarray): The top half tours
    """
    tours = []
    fitnessVals = []
    
    #Get fitness values of tours
    for tour in pop:
        tourLength = 0
        for i in range(nCities-1):
            tourLength += distances[tour[i], tour[i+1]]
        tourLength += distances[tour[nCities-1], tour[0]]
        tours.append(tour)
        fitnessVal = 10000/tourLength
        fitnessVals.append(fitnessVal)

    toursNp = np.array(tours)
    fitnessValsNp = np.array(fitnessVals)
    
    #Get best tours directly and unaltered to next generation in elitism-fashion   
    best_indices = np.argsort(fitnessValsNp)[::-1]
    eliteTours = toursNp[best_indices][:int(popSize/2)]

    
    def roulette():
        """
        Fitness proportionate selection (A.K.A. roulette wheel) as selection operator.
        Select a tour from current list of tours, with a higher chance of selecting a shorter tour.

        Returns:
            selected(numpy.ndarray): Selected tour: an array of indices (of cities according to csv file) representing the tour order
        """
        totalProb = sum(fitnessVals)
        r = random.uniform(0, totalProb)
        currentTour = 0
        for i in range(len(tours)):
            assert len(tours) == len(fitnessVals)
            currentTour += fitnessVals[i]
            if currentTour > r:
                fitnessVals.pop(i)
                selected = tours.pop(i)
                return selected
                
    newPop = []
    #Get surviving tours using roulette wheel selection
    for i in range(int(popSize/2)):
        newTour = np.asarray(roulette())
        newPop.append(newTour)
    newPop = np.array(newPop)

    return newPop, eliteTours


def crossover(parents):
    """
    Partially mapped crossover (PMX) as crossover operator.

    Parameters:
        parents(numpy.ndarray): Array of parent tours, which are arrays with indices (of the cities according to the csv file) representing the tour order. 
    
    Returns:
        offspring(numpy.ndarray): The resulting tour, a new array of city indices.
    """
    #Choose two parents randomly
    parentIndices = random.sample(range(0, len(parents)), 2)
    p1, p2 = parents[parentIndices[0]], parents[parentIndices[1]]
    #Get crossover points
    crossoverIndices = random.sample(range(0, len(parents)), 2)
    c1, c2 = min(crossoverIndices), max(crossoverIndices)
    #Copy over segment from parent 1
    seg1 = p1[c1:c2]
    seg2 = p2[c1:c2]
    offspring = [-1] * nCities
    offspring[c1:c2] = seg1
    pDiff = np.setdiff1d(seg2, seg1)
    
    #Recursively find new position for parent 2 segment element
    def findPos(pos, elem):
        if(offspring[pos] != -1):
            newPos = np.where(p2 == offspring[pos])[0][0]
            findPos(newPos, elem)
        else:
            offspring[pos] = elem
            return
    #Insert all elements from parent2's segment according to Partially Mapped Crossover
    for seg2Elem in pDiff:
        ind = np.where(p2 == seg2Elem)[0][0]
        findPos(ind, seg2Elem)
    offspring = np.array(offspring)
    #Insert remaining parent 2 alleles into offspring
    for i in range(len(offspring)):
        if(offspring[i] == -1):
            offspring[i] = p2[i]
    return offspring
          
    

def mutation(tour):
    """
    Simple mutation operator: switch two cities in given tour for a 60% chance   
    
    Parameters:

        tour(numpy.ndarray): Array of indices (of cities according to csv file) representing the tour order
    Returns:
        tour(numpy.ndarray): The mutated tour 
    """
    if(random.random() <= 0.6):
        switchIndices = random.sample(range(0, len(tour)), 2)
        t1 = tour[switchIndices[0]]
        t2 = tour[switchIndices[1]]
        tour[switchIndices[1]] = t1
        tour[switchIndices[0]] = t2
    return tour


if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    #get city and distance data
    with open("european_cities.csv", 'r') as newfile:
        data_iter = csv.reader(newfile,delimiter = ";",quotechar = '"')
        data = [data for data in data_iter]
    cities = np.asarray(data)
    cityIndex = dict(zip(cities[0], range(cities[0].size)))
    distances = cities[1:].astype('float64')
    #Parameters
    popSize = 100
    nGen = 50
    nCities = 10
    assert nCities < cities.shape[1]
    #Create initial population
    cityNumbers = np.arange(0, nCities)
    initPop = np.array([cityNumbers] * popSize)
    for i in range(len(initPop)):
        initPop[i] = np.random.permutation(initPop[i])
    currPop = initPop
    #Run nGen number of generations
    for i in range(nGen):
        s = selection(currPop)
        currPop = s[0]
        elitePop = s[1]
        offspring = []
        #Ensure number of offspring is half of population
        while(len(offspring) < popSize/2):
            offspring.append(crossover(currPop))
        for i in range(len(offspring)):
            offspring[i] = mutation(offspring[i])
        currPop = []
        #Add elite tours from current generation
        currPop.extend(elitePop)
        #Add offspring from current generation
        currPop.extend(offspring)
        
        #Continue to next gen
    print("Last gen: final tours")
    #reverse city index dictionary to print each tour and length
    inv_cityIndex ={v:k for k, v in cityIndex.items()}
    for tour in currPop:
        cities = [inv_cityIndex[i] for i in tour]
        print(cities, getLength(tour))
