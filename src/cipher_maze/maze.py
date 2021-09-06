from enum import Enum
from random import shuffle
from typing import List, Set

from pydantic import BaseModel, PrivateAttr

from cipher_maze.exceptions import NotAnEdgeTileException


class Direction(str, Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    def __repr__(self):
        return self.value


class Tile(BaseModel):
    walls: Set[Direction] = set(Direction)
    is_visited: bool = False


class Point(BaseModel):
    x: int
    y: int

    def get_relative_direction_of(self, other: 'Point', /) -> Direction:
        x_diff = self.x - other.x
        y_diff = self.y - other.y
        if y_diff == 1:
            return Direction.UP
        if y_diff == -1:
            return Direction.DOWN
        if x_diff == 1:
            return Direction.LEFT
        if x_diff == -1:
            return Direction.RIGHT


class Maze(BaseModel):
    width: int
    height: int
    start: Point
    end: Point
    tiles: List[List[Tile]] = None

    def __init__(self, **data):
        super().__init__(**data)
        self.tiles = [[Tile() for _ in range(self.height)] for _ in range(self.width)]
        self._remove_one_edge_wall(self.start)
        self._remove_one_edge_wall(self.end)

    def _remove_one_edge_wall(self, point: Point):
        tile = self[point]
        if point.y == 0:
            tile.walls.remove(Direction.UP)
        elif point.y == self.height - 1:
            tile.walls.remove(Direction.DOWN)
        elif point.x == 0:
            tile.walls.remove(Direction.LEFT)
        elif point.x == self.width - 1:
            tile.walls.remove(Direction.RIGHT)
        else:
            raise NotAnEdgeTileException()

    def __getitem__(self, item):
        if isinstance(item, Point):
            return self.tiles[item.x][item.y]


def generate_maze(width: int, height: int, start: Point, end: Point):
    maze = Maze(width=width, height=height, start=start, end=end)
    _generate_maze(maze, maze.start)
    return maze


def _generate_maze(maze: Maze, point: Point):
    maze[point].is_visited = True
    neighbors = _get_neighbors(point)
    shuffle(neighbors)
    for neighbor_point in neighbors:
        if not _is_valid(neighbor_point, width=maze.width, height=maze.height) or maze[neighbor_point].is_visited:
            continue

        maze[point].walls.remove(point.get_relative_direction_of(neighbor_point))
        maze[neighbor_point].walls.remove(neighbor_point.get_relative_direction_of(point))

        _generate_maze(maze, neighbor_point)


def _get_neighbors(point: Point) -> List[Point]:
    return [
        Point(x=point.x, y=point.y + 1),
        Point(x=point.x, y=point.y - 1),
        Point(x=point.x - 1, y=point.y),
        Point(x=point.x + 1, y=point.y),
    ]


def _is_valid(point: Point, /, *, width: int, height: int) -> bool:
    return all(
        0 <= coordinate < max_
        for coordinate, max_ in ((point.x, width), (point.y, height))
    )


# TODO: Func to print the maze (choose a GUI first I guess)
maze = generate_maze(width=4, height=4, start=Point(x=0, y=0), end=Point(x=3, y=3))
print([tile.walls for col in maze.tiles for tile in col])
