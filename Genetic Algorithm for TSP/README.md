# Genetic Algorithm for Traveling Salesman Problem
Traveling Salesman Problem: Find the shortest possible tour that visits each city once and returns to the original city. We will be solving this optimization problem through a genetic algorithm, an approach that mimics the natural selection process to carry generation, i.e. survival of the fittest .

#### Chosen operators:
	Selection: Fitness proportionate selection (FPS)
	Crossover: Partially mapped crossover (PMX)
	Mutation: Switch two tours for a 60% chance


# Prerequisites

### Run with python 3.8.3 (anaconda)
	https://www.anaconda.com/products/individual
#### With ordinary python, install numpy:
	pip install numpy
	
# How to run
	[py/PATH_TO_python.exe] genetic.py

## Data representation of European cities and their relative distances 
### First 6 cities from european_cities.csv
|  &nbsp;   | Barcelona | Belgrade |  Berlin | Brussels | Bucharest | Budapest |
|:---------:|:---------:|:--------:|:-------:|:--------:|:---------:|:--------:|
| **Barcelona** |     0     |  1528.13 | 1497.61 |  1062.89 |  1968.42  |  1498.79 |
|  **Belgrade** |  1528.13  |     0    |  999.25 |  1372.59 |   447.34  |  316.41  |
|   **Berlin**  |  1497.61  |  999.25  |    0    |  651.62  |  1293.40  |  1293.40 |
|  **Brussels** |  1062.89  |  1372.59 |  651.62 |     0    |  1769.69  |  1131.52 |
| **Bucharest** |  1968.42  |  447.34  | 1293.40 |  1769.69 |     0     |  639.77  |
|  **Budapest** |  1498.79  |  316.41  | 1293.40 |  1131.52 |   639.77  |     0    |
	
