from abc import ABC
from contextlib import contextmanager
from string import ascii_letters
from unittest.mock import patch

from pydantic import BaseModel


class Cipher(ABC, BaseModel):
    lowercase_permutation: str
    uppercase_permutation: str

    def ciphered_input(self, prompt: str = '') -> str:
        return input(prompt).translate(str.maketrans(
            ascii_letters,
            self.lowercase_permutation + self.uppercase_permutation
        ))


@contextmanager
def ciphered_input(cipher):
    with patch('cipher_maze.ui.input', cipher.ciphered_input):
        yield
