from cipher_maze.cipher.caesar_cipher import CaesarCipher
from cipher_maze.cipher.cipher import RepeatingCipher


class CaesarRepeatingCipher(CaesarCipher, RepeatingCipher):
    def update_permutations(self):
        self.lowercase_permutation = self._caesar_shift(self.lowercase_permutation, 1)
        self.uppercase_permutation = self.lowercase_permutation.upper()
