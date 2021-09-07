import string
from abc import ABC
from typing import Type
from unittest.mock import patch

from decorator import decorator
from pydantic import BaseModel

from cipher_maze.utils import rotated


class CipheredKeyboard(ABC, BaseModel):
    lowercase_translation_strip: str
    uppercase_translation_strip: str

    def translated_input(self, prompt: str = '') -> str:
        input_ = input(prompt).translate(str.maketrans(
            string.ascii_letters,
            self.lowercase_translation_strip + self.uppercase_translation_strip
        ))
        self.update_translation_strips()
        return input_

    def update_translation_strips(self):
        pass


class Rot1Keyboard(CipheredKeyboard):
    lowercase_translation_strip = rotated(string.ascii_lowercase, 1)
    uppercase_translation_strip = rotated(string.ascii_uppercase, 1)

    def update_translation_strips(self):
        self.lowercase_translation_strip = rotated(self.lowercase_translation_strip, 1)
        self.uppercase_translation_strip = rotated(self.uppercase_translation_strip, 1)


def ciphered_input(ciphered_keyboard_class: Type[CipheredKeyboard]):
    ciphered_keyboard = ciphered_keyboard_class()

    @decorator
    def _ciphered_input(func, *args, **kwargs):
        with patch('cipher_maze.ui.input', ciphered_keyboard.translated_input):
            return func(*args, **kwargs)

    return _ciphered_input
