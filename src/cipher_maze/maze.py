from enum import Enum
from random import shuffle
from typing import List, Set, Optional, Union, Callable

from bidict import bidict
from pydantic import BaseModel


class Direction(str, Enum):
    UP = 'up'
    DOWN = 'down'
    LEFT = 'left'
    RIGHT = 'right'


class Point(BaseModel):
    x: int
    y: int

    class Config:
        frozen = True

    def __add__(self, other: Union[Direction, 'Point']):
        if isinstance(other, Point):
            return Point(x=self.x + other.x, y=self.y + other.y)
        elif isinstance(other, Direction):
            return self + POINT_DIFF_DIRECTIONS[other]
        else:
            raise NotImplementedError()

    def __eq__(self, other: 'Point'):
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def get_neighbors(self) -> List['Point']:
        return [
            self + Direction.UP,
            self + Direction.DOWN,
            self + Direction.LEFT,
            self + Direction.RIGHT,
        ]

    def get_relative_direction_of(self, other: 'Point', /) -> Direction:
        diff = Point(x=other.x - self.x, y=other.y - self.y)
        return POINT_DIFF_DIRECTIONS.inverse[diff]

    def is_valid(self, *, min_x: int = 0, max_x: int, min_y: int = 0, max_y: int) -> bool:
        return all(
            min_ <= coordinate < max_
            for min_, coordinate, max_ in ((min_x, self.x, max_x), (min_y, self.y, max_y))
        )


POINT_DIFF_DIRECTIONS = bidict({
    Direction.UP: Point(x=0, y=-1),
    Direction.DOWN: Point(x=0, y=1),
    Direction.LEFT: Point(x=-1, y=0),
    Direction.RIGHT: Point(x=1, y=0),
})


class Tile(BaseModel):
    walls: Set[Direction] = set(Direction)
    is_visited: bool = False
    character: Optional[str]
    callback: Optional[Callable]


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

    def __getitem__(self, item: Point) -> Tile:
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
            raise KeyError(f'The point {point} is not an edge.')


def generate_maze(width: int, height: int, start: Point, end: Point) -> Maze:
    maze = Maze(width=width, height=height, start=start, end=end)
    _generate_maze(maze)
    return maze


def _generate_maze(maze: Maze, point: Optional[Point] = None):
    if not point:
        point = Point(x=0, y=0)
    maze[point].is_visited = True
    neighbors = point.get_neighbors()
    shuffle(neighbors)
    for neighbor_point in neighbors:
        if not neighbor_point.is_valid(max_x=maze.width, max_y=maze.height) or maze[neighbor_point].is_visited:
            continue

        maze[point].walls.remove(point.get_relative_direction_of(neighbor_point))
        maze[neighbor_point].walls.remove(neighbor_point.get_relative_direction_of(point))

        _generate_maze(maze, neighbor_point)
