from cipher_maze.cipher import ciphered_input, KeywordCipher, CaesarRepeatingCipher
from cipher_maze.game import play
from cipher_maze.maze import generate_maze, Point

MAZE_WIDTH = 4
MAZE_HEIGHT = 4
maze = generate_maze(
    width=MAZE_WIDTH,
    height=MAZE_HEIGHT,
    start=Point(x=0, y=0),
    end=Point(x=MAZE_WIDTH - 1, y=MAZE_HEIGHT - 1)
)

# with ciphered_input(CaesarRepeatingCipher(right_shift=1)):
with ciphered_input(KeywordCipher(keyword='testkey')):
    play(maze)
