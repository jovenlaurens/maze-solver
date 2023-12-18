from collections import deque
import os
import sys
import numpy as np
import matplotlib.pyplot as plt

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def is_valid_move(grid, visited, row, col):
    rows, cols = len(grid), len(grid[0])
    return 0 <= row < rows and 0 <= col < cols and grid[row][col] == 1 and not visited[row][col]


def bfs(grid, start, end):
    rows, cols = len(grid), len(grid[0])
    visited = [[False] * cols for _ in range(rows)]

    queue = deque([(start[0], start[1], 0, [])])
    iterations = 0

    while queue:
        row, col, distance, path = queue.popleft()
        visited[row][col] = True
        iterations += 1

        if (row, col) == end:
            print("Number of iterations:", iterations)
            return path + [(row, col)]

        # Check and enqueue valid neighbors
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_row, new_col = row + dr, col + dc
            if is_valid_move(grid, visited, new_row, new_col):
                queue.append(
                    (new_row, new_col, distance + 1, path + [(row, col)]))
                visited[new_row][new_col] = True

    print("Number of iterations:", iterations)
    return None  # No path found


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


def visualize(maze_data, ncol, nrow, start_point, end_point, path):
    start = end = routes = np.zeros((nrow, ncol))

    start[start_point] = 1  # Represent the starting point with value 2
    end[end_point] = 1    # Represent the endpoint with value 3

    # Plotting the maze
    plt.imshow(maze_data, cmap='binary_r', interpolation='nearest', alpha=0.5)

    routes = update_maze_with_path(routes, path)
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


def update_maze_with_path(maze, path):
    for row, col in path:
        maze[row][col] = 1
    return maze


if __name__ == "__main__":

    if len(sys.argv) < 2 or sys.argv[1] not in ["easy", "medium", "hard", "insane"]:
        print("[USAGE] python Visualizer.py easy|medium|hard|insane")
        exit(1)

    difficulty = sys.argv[1]
    maze_data, nrow, ncol = read_maze_file("data/" + difficulty + " maze.txt")
    start_point, end_point = read_coordinates_file(
        "data/" + difficulty + " coordinates.txt")
    maze = np.array([[int(cell) for cell in row] for row in maze_data])

    shortest_path = bfs(maze, start_point, end_point)
    if shortest_path:
        print("Size of the Route:", len(shortest_path))
    else:
        print("No path found.")

    visualize(maze, ncol, nrow, start_point, end_point, shortest_path)
