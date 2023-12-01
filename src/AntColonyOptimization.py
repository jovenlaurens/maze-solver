"""

Ant                         Implement logics
AntColonyOptimization       Implement maze creation, allowing ants to explore
Coordinate
Direction
Maze                        Implement initialisation, adding and resetting pheromones, # surroundingPheromone
                                for a given coordinate
PathSpecification           Starting point and end point in the maze
Route
SurroundingPheromone

"""


import matplotlib.pyplot as plt

from Ant import Ant
from concurrent.futures import ThreadPoolExecutor


# Class representing the first assignment. Finds the shortest path between two points in a maze according to a specific
# path specification.
class AntColonyOptimization:

    # Constructs a new optimization object using ants.
    # @param maze the maze .
    # @param antsPerGen the amount of ants per generation.
    # @param generations the amount of generations.
    # @param Q normalization factor for the amount of dropped pheromone
    # @param evaporation the evaporation factor.
    def __init__(self, maze, config):
        self.maze = maze
        self.ants_per_gen = config['ants_per_gen']
        self.generations = config['generations']
        self.q = config['q']
        self.evaporation = config['evaporation']
        self.num_ants = config['num_ants']

    # Runs one generation of ants

    def run_generation(self, path, it):
        # Create ants
        ants = [Ant(self.maze, path) for _ in range(self.ants_per_gen)]

        # Use ThreadPoolExecutor for parallelizing ant search
        with ThreadPoolExecutor() as executor:
            routes = list(executor.map(lambda ant: ant.find_route(), ants))

        # Filter out None routes (unsuccessful ants)
        routes = [route for route in routes if route is not None]

        # Add pheromones and return best ant
        self.maze.evaporate(self.evaporation)
        self.maze.add_pheromone_routes(routes, self.q)

        # Calculate statistics for plotting
        lengths = [route.size() for route in routes]
        avg_length = sum(lengths) / len(lengths)
        shortest_route = min(routes, key=lambda route: route.size())

        # Plot average and best route length over time
        plt.plot(it, avg_length, marker="o", color="#55F")  # Plot average
        plt.plot(it, shortest_route.size(),
                 marker="o", color="#5A5")  # Plot best

        return avg_length, shortest_route

    # Loop that starts the shortest path process
    # @param spec Specification of the route we wish to optimize
    # @return ACO optimized route
    def find_shortest_route(self, path_specification):

        # Reset the maze
        self.maze.reset()

        # Run the generations as many times as the network requires
        avg, shortest = self.run_generation(path_specification, 1)
        itr = 0
        print("ITER: {}, AVERAGE ROUTE SIZE: {}".format(itr, avg))

        for i in range(1, self.generations):
            avg, route = self.run_generation(path_specification, i + 1)
            if route.shorter_than(shortest):
                shortest = route
                itr = i + 1
            print("ITER: {}, AVERAGE ROUTE SIZE: {}".format(i, avg))

        plt.xlabel("Generation")
        plt.ylabel("Route length")
        plt.legend(["Average", "Best"])
        plt.title("Average and best route length over time")
        plt.show()  # Show the plot

        return itr, shortest
