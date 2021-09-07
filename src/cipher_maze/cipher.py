import string
from abc import ABC
from typing import Type
from unittest.mock import patch

from decorator import decorator
from pydantic import BaseModel

from cipher_maze.utils import rotated


class Cipher(ABC, BaseModel):
    lowercase_permutation: str
    uppercase_permutation: str

    def ciphered_input(self, prompt: str = '') -> str:
        input_ = input(prompt).translate(str.maketrans(
            string.ascii_letters,
            self.lowercase_permutation + self.uppercase_permutation
        ))
        self.update_permutations()
        return input_

    def update_permutations(self):
        pass


class Rot1Cipher(Cipher):
    lowercase_permutation = rotated(string.ascii_lowercase, 1)
    uppercase_permutation = rotated(string.ascii_uppercase, 1)

    def update_permutations(self):
        self.lowercase_permutation = rotated(self.lowercase_permutation, 1)
        self.uppercase_permutation = rotated(self.uppercase_permutation, 1)


def ciphered_input(ciphered_keyboard_class: Type[Cipher]):
    ciphered_keyboard = ciphered_keyboard_class()

    @decorator
    def _ciphered_input(func, *args, **kwargs):
        with patch('cipher_maze.ui.input', ciphered_keyboard.ciphered_input):
            return func(*args, **kwargs)

    return _ciphered_input
