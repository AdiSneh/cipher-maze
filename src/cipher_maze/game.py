from .maze import Maze
from .ui import get_next_move, print_maze


def play(maze: Maze):
    current_location = maze.start
    print_maze(maze, player_location=current_location)
    while current_location != maze.end:
        while (
                not (new_location := current_location + get_next_move()).is_valid(max_x=maze.width, max_y=maze.height)
                or current_location.get_relative_direction_of(new_location) in maze[current_location].walls
        ):
            print(f'The point {new_location} is out of bounds or unreachable from {current_location}.')
        current_location = new_location
        print_maze(maze, player_location=current_location)
    print('You win!')
