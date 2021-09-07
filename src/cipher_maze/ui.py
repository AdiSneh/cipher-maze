from builtins import input
from typing import Set, Optional

from .maze import Maze, Direction, Point

TILE_TEMPLATE_TOP = '#{up}#'
TILE_TEMPLATE_MIDDLE = '{left}{player}{right}'
TILE_TEMPLATE_BOTTOM = '#{down}#'


def print_maze(maze: Maze, /, *, player_location: Optional[Point] = None):
    for row in range(maze.height):
        for col in range(maze.width):
            tile = maze.tiles[col][row]
            print(TILE_TEMPLATE_TOP.format(
                up=_get_wall_character(tile.walls, Direction.UP),
            ), end='')
        print()
        for col in range(maze.width):
            tile = maze.tiles[col][row]
            print(TILE_TEMPLATE_MIDDLE.format(
                left=_get_wall_character(tile.walls, Direction.LEFT),
                right=_get_wall_character(tile.walls, Direction.RIGHT),
                player='*' if player_location and player_location == Point(x=col, y=row) else ' '
            ), end='')
        print()
        for col in range(maze.width):
            tile = maze.tiles[col][row]
            print(TILE_TEMPLATE_BOTTOM.format(
                down=_get_wall_character(tile.walls, Direction.DOWN),
            ), end='')
        print()


def _get_wall_character(walls: Set[Direction], direction: Direction):
    return '#' if direction in walls else ' '


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
