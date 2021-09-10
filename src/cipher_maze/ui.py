from builtins import input
from typing import Set, Optional

from .maze import Maze, Direction, Point


CHARACTER_WIDTH = 2
WALL_CHARACTER = '#'.ljust(CHARACTER_WIDTH)
EMPTY_CHARACTER = ' '.ljust(CHARACTER_WIDTH)


def print_maze(maze: Maze, /, *, player_location: Optional[Point] = None):
    _print_horizontal_wall(maze, 0, Direction.UP)
    for row in range(maze.height):
        print(_get_wall_character(maze.tiles[0][row].walls, Direction.LEFT), end='')
        for col in range(maze.width):
            player_character = '*' if player_location and player_location == Point(x=col, y=row) else None
            tile_character = maze.tiles[col][row].character or EMPTY_CHARACTER
            right_wall = _get_wall_character(maze.tiles[col][row].walls, Direction.RIGHT)
            print(f'{(player_character or tile_character).ljust(CHARACTER_WIDTH)}{right_wall}', end='')
        print()
        _print_horizontal_wall(maze, row, Direction.DOWN)


def _print_horizontal_wall(maze: Maze, row: int, direction: Direction):
    print(WALL_CHARACTER, end='')
    for col in range(maze.width):
        print(f'{_get_wall_character(maze.tiles[col][row].walls, direction)}{WALL_CHARACTER}', end='')
    print()


def _get_wall_character(walls: Set[Direction], direction: Direction):
    return WALL_CHARACTER if direction in walls else EMPTY_CHARACTER


def get_next_move() -> Direction:
    prompt = 'Where do you want to go? (U, D, L, R)'
    user_direction_map = {
        'U': Direction.UP,
        'D': Direction.DOWN,
        'L': Direction.LEFT,
        'R': Direction.RIGHT,
    }
    direction = input(prompt)
    while direction not in user_direction_map:
        print(f'Invalid direction ({direction}).')
        direction = input(prompt)
    return user_direction_map[direction]
