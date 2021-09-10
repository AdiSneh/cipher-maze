from cipher_maze.cipher import ciphered_input, CaesarCipher
from cipher_maze.game import play, randomly_place_tile_callbacks
from cipher_maze.maze import generate_maze, Point

MAZE_WIDTH = 4
MAZE_HEIGHT = 4


def main():
    maze = generate_maze(
        width=MAZE_WIDTH,
        height=MAZE_HEIGHT,
        start=Point(x=0, y=0),
        end=Point(x=MAZE_WIDTH - 1, y=MAZE_HEIGHT - 1)
    )
    cipher = CaesarCipher(right_shift=1)
    randomly_place_tile_callbacks(maze=maze, num_callbacks=3, callback=cipher.update_permutations)
    with ciphered_input(cipher):  # with ciphered_input(KeywordCipher(keyword='testkey')):
        play(maze)


if __name__ == '__main__':
    main()
