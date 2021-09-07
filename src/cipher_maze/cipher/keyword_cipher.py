from string import ascii_lowercase

from pydantic import validator

from cipher_maze.cipher.cipher import Cipher


class KeywordCipher(Cipher):
    keyword: str
    lowercase_permutation: str = None
    uppercase_permutation: str = None

    @validator('keyword')
    def validate_keyword(cls, v):
        return ''.join(dict.fromkeys(v.lower()))

    def __init__(self, **data):
        super().__init__(**data)
        self.lowercase_permutation = self.keyword.lower() + ''.join(
            letter for letter in ascii_lowercase if letter not in self.keyword.lower()
        )
        self.uppercase_permutation = self.lowercase_permutation.upper()
