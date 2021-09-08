from builtins import input
from typing import Set, Optional

from .maze import Maze, Direction, Point

HORIZONTAL_WALL_TEMPLATE = '{wall}# '
MIDDLE_TILE_TEMPLATE = '{player}{right}'


def print_maze(maze: Maze, /, *, player_location: Optional[Point] = None):
    _print_horizontal_wall(maze, 0, Direction.UP)
    for row in range(maze.height):
        print(_get_wall_character(maze.tiles[0][row].walls, Direction.LEFT), end='')
        for col in range(maze.width):
            print(MIDDLE_TILE_TEMPLATE.format(
                player='* ' if player_location and player_location == Point(x=col, y=row) else '  ',
                right=_get_wall_character(maze.tiles[col][row].walls, Direction.RIGHT),
            ), end='')
        print()
        _print_horizontal_wall(maze, row, Direction.DOWN)


def _print_horizontal_wall(maze: Maze, row: int, direction: Direction):
    print('# ', end='')
    for col in range(maze.width):
        print(HORIZONTAL_WALL_TEMPLATE.format(
            wall=_get_wall_character(maze.tiles[col][row].walls, direction),
        ), end='')
    print()


def _get_wall_character(walls: Set[Direction], direction: Direction):
    return '# ' if direction in walls else '  '


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
