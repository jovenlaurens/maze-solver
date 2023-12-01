from Direction import Direction
import traceback
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


# Class that holds all the maze data. This means the pheromones, the open and blocked tiles in the system as
# well as the starting and end coordinates.
class Maze:

    # Constructor of a maze
    # @param walls int array of tiles accessible (1) and non-accessible (0)
    # @param width width of Maze (horizontal)
    # @param length length of Maze (vertical)
    def __init__(self, walls, width, length):
        self.walls = walls
        self.pheromones = walls
        self.length = length
        self.width = width
        self.start = None
        self.end = None
        self.initialize_pheromones()

    # Initialize pheromones to a start value.
    def initialize_pheromones(self):
        self.pheromones = self.walls

    # Reset the maze for a new shortest path problem.
    def reset(self):
        self.initialize_pheromones()

    # Traverse the route of the ant from its starting position,
    # adding pheromones_per_cell to update the pheromone trail
    # @param r The route of the ants
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_route(self, route, q):

        coordinates = []
        pos = route.start
        for step in route.route:
            pos = pos.add_direction(step)
            if pos not in coordinates:
                coordinates.append(pos)

        pheromones_per_cell = q / route.size()
        for coord in coordinates:
            self.pheromones[coord.x][coord.y] += pheromones_per_cell
        # pos = route.start
        # for step in route.route:
        #     pos = pos.add_direction(step)
        #     self.pheromones[pos.x][pos.y] += pheromones_per_cell

    # Update pheromones for a list of routes
    # @param routes A list of routes
    # @param Q Normalization factor for amount of dropped pheromone
    def add_pheromone_routes(self, routes, q):
        for r in routes:
            self.add_pheromone_route(r, q)

    # Evaporate pheromone
    # @param rho evaporation factor
    def evaporate(self, rho):

        # after evaporation method, a pheromone holding cell equals: cell_value * (1 - rho)
        for i, col in enumerate(self.pheromones):
            for j, cell in enumerate(col):
                new_cell = cell * (1 - rho)
                self.pheromones[i][j] = 0.1 if 0 < new_cell < 0.1 else new_cell

    # Width getter
    # @return width of the maze
    def get_width(self):
        return self.width

    # Length getter
    # @return length of the maze
    def get_length(self):
        return self.length

    # Returns the amount of pheromones on the neighbouring positions (N/S/E/W).
    # @param pos The position to check the neighbours of.
    # @return the pheromones of the neighbouring positions.
    def get_surrounding_pheromone(self, pos):

        # If out of bounds, return 0
        if not self.in_bounds(pos):
            return 0

        # Returns pheromones of E/N/W/S
        return [self.get_pheromone(pos.add_direction(Direction.east)),
                self.get_pheromone(pos.add_direction(Direction.north)),
                self.get_pheromone(pos.add_direction(Direction.west)),
                self.get_pheromone(pos.add_direction(Direction.south))]

    # Pheromone getter for a specific position. If the position is not in bounds returns 0
    # @param pos Position coordinate
    # @return pheromone at point
    def get_pheromone(self, pos):

        # If out of bounds, return 0
        if not self.in_bounds(pos):
            return 0

        # Return pheromones found
        return self.pheromones[pos.x][pos.y]

    # Check whether a coordinate lies in the current maze.
    # @param position The position to be checked
    # @return Whether the position is in the current maze
    def in_bounds(self, position):
        return position.x_between(0, self.width) and position.y_between(0, self.length)

    # Representation of Maze as defined by the input file format.
    # @return String representation
    def __str__(self):
        string = ""
        string += str(self.width)
        string += " "
        string += str(self.length)
        string += " \n"
        for y in range(self.length):
            for x in range(self.width):
                string += str(self.walls[x][y])
                string += " "
            string += "\n"
        return string

    # Method that builds a mze from a file
    # @param filePath Path to the file
    # @return A maze object with pheromones initialized to 0's inaccessible and 1's accessible.
    @staticmethod
    def create_maze(file_path):
        try:
            f = open(file_path, "r")
            lines = f.read().splitlines()
            dimensions = lines[0].split(" ")
            width = int(dimensions[0])
            length = int(dimensions[1])

            # make the maze_layout
            maze_layout = []
            for x in range(width):
                maze_layout.append([])

            for y in range(length):
                line = lines[y+1].split(" ")
                for x in range(width):
                    if line[x] != "":
                        state = int(line[x])
                        maze_layout[x].append(state)
            print("Ready reading maze file " + file_path)
            return Maze(maze_layout, width, length)
        except FileNotFoundError:
            print("Error reading maze file " + file_path)
            traceback.print_exc()
            sys.exit()
