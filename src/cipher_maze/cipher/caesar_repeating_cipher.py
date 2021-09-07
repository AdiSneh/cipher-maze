import string

from cipher_maze.cipher.cipher import RepeatingCipher


class CaesarRepeatingCipher(RepeatingCipher):
    right_shift: int
    lowercase_permutation: str = None
    uppercase_permutation: str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.lowercase_permutation = self._caesar_shift(string.ascii_lowercase, self.right_shift)
        self.uppercase_permutation = self._caesar_shift(string.ascii_uppercase, self.right_shift)

    def update_permutations(self):
        self.lowercase_permutation = self._caesar_shift(self.lowercase_permutation, 1)
        self.uppercase_permutation = self._caesar_shift(self.uppercase_permutation, 1)

    @staticmethod
    def _caesar_shift(text: str, right_shift: int) -> str:
        return text[right_shift:] + text[:right_shift]

