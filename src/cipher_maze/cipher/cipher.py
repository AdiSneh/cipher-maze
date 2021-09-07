import string
from abc import ABC, abstractmethod
from unittest.mock import patch

from decorator import decorator
from pydantic import BaseModel


class Cipher(ABC, BaseModel):
    lowercase_permutation: str
    uppercase_permutation: str

    def ciphered_input(self, prompt: str = '') -> str:
        return input(prompt).translate(str.maketrans(
            string.ascii_letters,
            self.lowercase_permutation + self.uppercase_permutation
        ))


class RepeatingCipher(Cipher):
    def ciphered_input(self, prompt: str = '') -> str:
        input_ = super().ciphered_input(prompt)
        self.update_permutations()
        return input_

    @abstractmethod
    def update_permutations(self):
        pass


def ciphered_input(cipher):
    @decorator
    def _ciphered_input(func, *args, **kwargs):
        with patch('cipher_maze.ui.input', cipher.ciphered_input):
            return func(*args, **kwargs)

    return _ciphered_input
