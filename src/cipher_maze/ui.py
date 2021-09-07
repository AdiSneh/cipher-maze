from typing import Set

from cipher_maze.maze import Maze, Direction

TILE_TEMPLATE_TOP = '#{up}#'
TILE_TEMPLATE_MIDDLE = '{left} {right}'
TILE_TEMPLATE_BOTTOM = '#{down}#'


def print_maze(maze: Maze):
    for row in range(maze.height):
        for col in range(maze.width):
            tile = maze.tiles[col][row]
            print(TILE_TEMPLATE_TOP.format(
                up=_get_character_for_direction(tile.walls, Direction.UP),
            ), end='')
        print()
        for col in range(maze.width):
            tile = maze.tiles[col][row]
            print(TILE_TEMPLATE_MIDDLE.format(
                left=_get_character_for_direction(tile.walls, Direction.LEFT),
                right=_get_character_for_direction(tile.walls, Direction.RIGHT),
            ), end='')
        print()
        for col in range(maze.width):
            tile = maze.tiles[col][row]
            print(TILE_TEMPLATE_BOTTOM.format(
                down=_get_character_for_direction(tile.walls, Direction.DOWN),
            ), end='')
        print()


def _get_character_for_direction(walls: Set[Direction], direction: Direction):
    return '#' if direction in walls else ' '
