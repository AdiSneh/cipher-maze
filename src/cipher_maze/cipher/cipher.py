from abc import ABC, abstractmethod
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


class RepeatingCipher(Cipher):
    def ciphered_input(self, prompt: str = '') -> str:
        input_ = super().ciphered_input(prompt)
        self.update_permutations()
        return input_

    # TODO: It's way too hard when the cipher changes after every guess.
    #  Maybe only update after stepping on some sort of trigger, maybe only after moving.
    @abstractmethod
    def update_permutations(self):
        pass


@contextmanager
def ciphered_input(cipher):
    with patch('cipher_maze.ui.input', cipher.ciphered_input):
        yield
