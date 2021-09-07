from string import ascii_lowercase

from cipher_maze.cipher.cipher import Cipher


class CaesarCipher(Cipher):
    right_shift: int
    lowercase_permutation: str = None
    uppercase_permutation: str = None

    def __init__(self, **data):
        super().__init__(**data)
        self.lowercase_permutation = self._caesar_shift(ascii_lowercase, self.right_shift)
        self.uppercase_permutation = self.lowercase_permutation.upper()

    @staticmethod
    def _caesar_shift(text: str, right_shift: int) -> str:
        return text[right_shift:] + text[:right_shift]

