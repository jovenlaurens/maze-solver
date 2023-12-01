import time
import matplotlib.pyplot as plt
import os
import sys


from AntColonyOptimization import AntColonyOptimization
from Maze import Maze
from PathSpecification import PathSpecification
from Config import config

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["easy", "medium", "hard", "insane"]:
        print("[USAGE] python Visualizer.py easy|medium|hard|insane")
        exit(1)

    # Construct the optimization objects
    difficulty = sys.argv[1]
    maze = Maze.create_maze("./data/" + difficulty + " maze.txt")
    spec = PathSpecification.read_coordinates(
        "./data/" + difficulty + " coordinates.txt")
    aco = AntColonyOptimization(maze, config)

    # Save starting time
    start_time = int(round(time.time() * 1000))

    # Run optimization
    iter, shortest_route = aco.find_shortest_route(spec)
    plt.show()
    # Print time taken
    print("Time taken: " + str((int(round(time.time() * 1000)) -
          start_time) / 1000.0) + " seconds")

    # Save solution
    shortest_route.write_to_file("./data/" + difficulty + " routes.txt")

    # Print route size
    print("Route size: " + str(shortest_route.size()))
    print("Found in iteration", iter)
