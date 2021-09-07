from enum import Enum
from random import shuffle
from typing import List, Set

from pydantic import BaseModel

from cipher_maze.exceptions import NotAnEdgeTileException


class Direction(str, Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'

    def __repr__(self):
        return self.value


class Point(BaseModel):
    x: int
    y: int

    def __add__(self, other: Direction):
        if isinstance(other, Direction):
            if other == Direction.UP:
                return Point(x=self.x, y=self.y - 1)
            elif other == Direction.DOWN:
                return Point(x=self.x, y=self.y + 1)
            elif other == Direction.LEFT:
                return Point(x=self.x - 1, y=self.y)
            elif other == Direction.RIGHT:
                return Point(x=self.x + 1, y=self.y)
        else:
            raise NotImplementedError()

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

    def is_valid(self, max_x: int, max_y: int, min_x: int = 0, min_y: int = 0) -> bool:
        return all(
            min_ <= coordinate < max_
            for min_, coordinate, max_ in ((min_x, self.x, max_x), (min_y, self.y, max_y))
        )


class Tile(BaseModel):
    walls: Set[Direction] = set(Direction)
    is_visited: bool = False


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

    def __getitem__(self, item: Point):
        if isinstance(item, Point):
            return self.tiles[item.x][item.y]
        else:
            raise KeyError(f'Expected a key of type Point but got {item} instead')

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


def generate_maze(width: int, height: int, start: Point, end: Point):
    maze = Maze(width=width, height=height, start=start, end=end)
    _generate_maze(maze, maze.start)
    return maze


def _generate_maze(maze: Maze, point: Point):
    maze[point].is_visited = True
    neighbors = _get_neighbors(point)
    shuffle(neighbors)
    for neighbor_point in neighbors:
        if not neighbor_point.is_valid(max_x=maze.width, max_y=maze.height) or maze[neighbor_point].is_visited:
            continue

        maze[point].walls.remove(point.get_relative_direction_of(neighbor_point))
        maze[neighbor_point].walls.remove(neighbor_point.get_relative_direction_of(point))

        _generate_maze(maze, neighbor_point)


def _get_neighbors(point: Point) -> List[Point]:
    return [
        point + Direction.UP,
        point + Direction.DOWN,
        point + Direction.LEFT,
        point + Direction.RIGHT,
    ]
