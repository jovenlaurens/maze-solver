import numpy as np
import matplotlib.pyplot as plt
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def apply_ant_movement(maze_array, start_point, ant_movement):
    current_position = start_point

    for instruction in ant_movement:
        current_position = move_ant(current_position, instruction)
        maze_array[current_position] = 1  # Mark the path as the ant moves

    return maze_array


def move_ant(position, direction):
    # Function to move the ant to an adjacent cell in the specified direction
    x, y = position
    if direction == 0:  # east
        return (x, y + 1)
    elif direction == 1:  # north
        return (x - 1, y)
    elif direction == 2:  # west
        return (x, y - 1)
    elif direction == 3:  # south
        return (x + 1, y)


def read_maze_file(file_path):
    with open(file_path, 'r') as file:
        # Read the first line to get maze dimensions
        dimensions = file.readline().split()
        num_rows, num_columns = int(dimensions[1]), int(dimensions[0])

        # Read the rest of the lines to get maze data
        maze_data = [file.readline().replace(" ", "").strip()
                     for _ in range(num_rows)]

    return maze_data, num_rows, num_columns


def read_coordinates_file(file_path):
    start_point, end_point = None, None

    with open(file_path, 'r') as file:
        for line in file:
            # Remove commas and semicolons, split, and extract coordinates
            coordinates = line.replace(",", "").replace(";", "").split()
            coordinates = (int(coordinates[1]), int(coordinates[0]))

            if start_point is None:
                start_point = coordinates
            else:
                end_point = coordinates

    return start_point, end_point


def read_routes_file(file_path):
    start_point, end_point = None, None

    with open(file_path, 'r') as file:
        for line in file:
            # Remove commas and semicolons, split, and extract coordinates
            coordinates = line.replace(",", "").replace(";", "").split()
            coordinates = (int(coordinates[1]), int(coordinates[0]))

            if start_point is None:
                start_point = coordinates
            else:
                end_point = coordinates

    return start_point, end_point


def read_ant_route(file_path):
    ant_route = []
    with open(file_path, 'r') as file:
        # Read the first line to get the total number of instructions
        total_instructions = int(file.readline().strip().split(';')[0])
        file.readline()

        # Read the rest of the lines and extract ant movement instructions
        for _ in range(total_instructions):
            line = file.readline().replace(";", "")
            ant_route.append(int(line))

    return ant_route


def visualize_ant_movement(maze_data, ncol, nrow, start_point, end_point, ant_movement):
    maze_array = np.array([[int(cell) for cell in row] for row in maze_data])
    print(maze_array)
    start = end = routes = np.zeros((nrow, ncol))

    start[start_point] = 1  # Represent the starting point with value 2
    end[end_point] = 1    # Represent the endpoint with value 3

    routes = apply_ant_movement(routes, start_point, ant_movement)

    # Plotting the maze
    plt.imshow(maze_array, cmap='binary_r', interpolation='nearest', alpha=0.5)

    # Highlighting the start and end points
    plt.scatter(*start_point[::-1], color='green',
                marker='o', label='Start Point')
    plt.scatter(*end_point[::-1], color='red', marker='x', label='End Point')

    # Plotting the route as a line
    rows, cols = np.where(routes == 1)
    plt.scatter(cols, rows, color='blue', marker='.',
                s=30, label='Route', alpha=0.8)

    # Adding legend
    plt.legend(loc=3)

    # Show the plot
    plt.title('Maze with Start Point, End Point, and Route')
    plt.show()


if __name__ == "__main__":
    if len(sys.argv) < 2 or sys.argv[1] not in ["easy", "medium", "hard", "insane"]:
        print("[USAGE] python Visualizer.py easy|medium|hard|insane")
        exit(1)

    difficulty = sys.argv[1]
    maze_data, nrow, ncol = read_maze_file("data/" + difficulty + " maze.txt")
    start_point, end_point = read_coordinates_file(
        "data/" + difficulty + " coordinates.txt")
    ant_movement = read_ant_route("data/" + difficulty + " routes.txt")
    visualize_ant_movement(maze_data, ncol, nrow,
                           start_point, end_point, ant_movement)
