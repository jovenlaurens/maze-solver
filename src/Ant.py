from Direction import Direction
from Coordinate import Coordinate
from Route import Route
import random
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class that represents ant functionality.
class Ant:

    # Constructor for ant taking a Maze and PathSpecification.
    # @param maze Maze the ant will be running in.
    # @param spec The path specification consisting of a start coordinate and an end coordinate.
    def __init__(self, maze, path_specification):
        self.maze = maze
        self.start = path_specification.get_start()
        self.end = path_specification.get_end()
        self.current_position = self.start
        self.rand = random.random()

    # Method that performs a single run through the maze by the ant.
    # @return The route the ant found through the maze.
    def find_route(self):

        # Initialise position and route
        route = Route(self.start)
        pos = self.start
        direction = None

        # As long as we're searching for the end
        it = 0
        while not pos == self.end:

            # Get pheromones, put cell we came from at 0
            # Increase chance of keeping direction
            chances = self.maze.get_surrounding_pheromone(pos)
            if direction is not None:
                dir = Direction.dir_to_int(direction)
                chances[(dir + 2) % 4] = 0
                chances[dir] *= 2 + \
                    (2 if len(list(filter(lambda x: x == 0, chances))) == 0 else 0)

            # Go back if we're in a dead end
            if sum(chances) == 0:
                while len(list(filter(lambda x: x > 0, chances))) <= 2:
                    direction = route.remove_last()
                    pos = pos.subtract_direction(direction)
                    chances = self.maze.get_surrounding_pheromone(pos)

            # Calculate chances
            total_pheromones = sum(chances)
            chances = [x / total_pheromones for x in chances]

            # Make it a line by adding cumulatively
            cumulatives = [chances[0]]
            for i in range(1, len(chances)):
                cumulatives.append(cumulatives[i - 1] + chances[i])

            # Select one of the directions
            choice = random.random()
            lower = 0
            dir = -1
            for i, c in enumerate(chances):
                if lower <= choice < lower + c:
                    dir = i
                    break
                lower += c  # Move lower boundary

            # Get next cell
            direction = Direction(dir)
            pos = pos.add_direction(direction)
            route.add(direction)
            it += 1

        return route

    def __str__(self):
        return "Ant{" + str(self.rand) + "}"
