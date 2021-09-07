from cipher_maze.game import play
from cipher_maze.maze import generate_maze, Point
from cipher_maze.ui import print_maze

MAZE_WIDTH = 5
MAZE_HEIGHT = 5
maze = generate_maze(
    width=MAZE_WIDTH,
    height=MAZE_HEIGHT,
    start=Point(x=0, y=0),
    end=Point(x=MAZE_WIDTH - 1, y=MAZE_HEIGHT - 1)
)
# print_maze(maze)

play(maze)
