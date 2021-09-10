import itertools
import random
from typing import Callable

from .maze import Maze, Point
from .ui import get_next_move, print_maze


def randomly_place_tile_callbacks(maze: Maze, num_callbacks: int, callback: Callable):
    points = [
        Point(x=x_, y=y_)
        for x_, y_ in list(itertools.product(range(maze.width), range(maze.height)))
        if (point := Point(x=x_, y=y_)) != maze.start and point != maze.end
    ]
    for point in random.sample(points, k=num_callbacks):
        maze[point].character = '?'
        maze[point].callback = callback


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
        if callback := maze[current_location].callback:
            callback()
        print_maze(maze, player_location=current_location)
    print('You win!')
